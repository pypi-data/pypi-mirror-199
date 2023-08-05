import numpy as np
import pandas as pd
import optuna
import lightgbm as lgb
from .score_cal import RScore
from sklearn.model_selection import train_test_split
import os
seed = 42


def Train_LGBMR(features: any = None,
                target: any = None,
                iterations: int = 50,
                scoring: str = None,
                validation_size: float = 0.2,
                test_size: float = 0.1,
                validation_set: tuple = None,
                test_set: tuple = None,
                task: str = "regression",
                # {0: "valid_score", 1: "train_valid_drop"}
                objectives: any = "valid_score",
                base_score:float=None,
                start: any = 1,  # 1 or True
                show_shap: bool = True,
                saved_dir:any=None,
                refit: bool = True,
                ):
    """Construct a function to train a booster.

        Parameters
        ----------
        features : any, {dataframe, array} of predictors
            features use to build model.
        target : any, {array, Series} of target
            continuous target to be predicted.
        iterations : int,
            number of optimization rounds.
        scoring : str,
            scoring method for optimization.
            Available scoring method is sklearn regression metrics: R2 (r2), MAE, MSE, RMSE, MAPE, Poisson, Tweedie, MeAE,
                ExVS, MSLE, ME, Gama, D2T, D2Pi, D2A.
        validation_size: float,
            size of validation set use to evaluate model.
        test_size: float,
            size of test set.
        validation_set: tuple,
            tuple of (X_valid, y_valid)
        test_set: tuple,
            tuple of (X_test, y_test)
        task : str,
            internal method for LightGBM to optimize gradient. Available tasks of LightGBM regression are:
            regression (rmse), mae, huber, fair, poisson, quantile, mape, gamma, tweedie, lambdarank, rank_xendcg,
                rank_xendcg.
        objectives : any, {int or str}
            the way to perform optimization.
            "valid_score" or 0: mean to optimize valid score
            "train_test_drop" or 1: mean to optimize different between train and valid score.
        base_score: float
            control under fitting when apply objective is train_test_drop / 1
        start : any,
            default=1
            is internal param for starting optimize.
        show_shap : bool,
            default=False, show shap chart after tuning if True other while save charts as pictures.

        Returns
        -------
        estimator : object
            The trained model.
    """
    if validation_set and test_set:
        train_x, train_target = features, target
        valid_x, valid_target = validation_set
        test_x, test_target = test_set

    elif validation_set and test_size:
        valid_x, valid_target = validation_set
        train_x, test_x, train_target, test_target = train_test_split(features,
                                                                      target,
                                                                      test_size=test_size,
                                                                      random_state=seed)

    elif test_set and validation_size:
        train_x, valid_x, train_target, valid_target = train_test_split(features,
                                                                        target,
                                                                        test_size=validation_size,
                                                                        random_state=seed)
        test_x, test_target = test_set

    else:
        train_x, valid_x, train_target, valid_target = train_test_split(features,
                                                                        target,
                                                                        test_size=validation_size,
                                                                        random_state=seed)

        train_x, test_x, train_target, test_target = train_test_split(train_x,
                                                                      train_target,
                                                                      test_size=test_size,
                                                                      random_state=seed)

    dtrain = lgb.Dataset(train_x, label=train_target, free_raw_data=False)
    dvalid = lgb.Dataset(valid_x, label=valid_target, free_raw_data=False)

    def objective(trial):
        params = {
            "objective": task,
            "verbosity": -1,
            "feature_pre_filter": False,
            "learning_rate": trial.suggest_loguniform("learning_rate", 1e-2, 0.1),
            "lambda_l1": trial.suggest_loguniform("lambda_l1", 1e-8, 10.0),
            "lambda_l2": trial.suggest_loguniform("lambda_l2", 1e-8, 10.0),
            "num_leaves": trial.suggest_("num_leaves", [21, 31, 41, 51, 61, 63]),
            "feature_fraction": trial.suggest_loguniform("feature_fraction", 0.4, 1.0),
            "bagging_fraction": trial.suggest_loguniform("bagging_fraction", 0.4, 1.0),
            "bagging_freq": trial.suggest_int("bagging_freq", 1, 15),
            "min_data_in_leaf": trial.suggest_categorical("min_data_in_leaf", [21, 31, 41, 51, 61]),
            "tree_learner": trial.suggest_categorical("tree_learner", ["serial", "feature", "data", "voting"])
        }
        if params["objective"] == "tweedie":
            params["tweedie_variance_power"] = trial.suggest_float(
                "tweedie_variance_power", 1., 1.99)

        model = lgb.train(
            params,
            dtrain,
            # valid_sets=[dvalid],
            # valid_names=["valid"],
            # num_boost_round=500,
            # early_stopping_rounds=5,
            verbose_eval=False,
        )

        preds = model.predict(valid_x)
        pred_trains = model.predict(train_x)
        valid_score = RScore(valid_target, preds, scoring=scoring)
        train_score = RScore(train_target, pred_trains, scoring=scoring)
        diff = train_score-valid_score
        if objectives == 0 or objectives == 'valid_score':
            print(f"train-test differs: {diff}")
            return valid_score
        else:
            if valid_score >= base_score:
                print(valid_score)
                return np.abs(diff)
            else:
                return np.exp(np.abs(diff)) * 10

    guides = ["R2", "ExV", "D2T", "D2Pi", "D2A"]

    if scoring in guides:
        if objectives == 0 or objectives == 'valid_score':
            direction = "maximize"
        else:
            direction = "minimize"
    else:
        direction = "minimize"

    if start == 1 or start == True:
        study = optuna.create_study(
            direction=direction, study_name="find best model")
        study.optimize(objective, n_trials=iterations)

        print("Number of finished trials: {}".format(len(study.trials)))

        print("Best trial:")
        trial = study.best_trial

        print("  Value: {}".format(trial.value))

        print("  Params: ")
        for key, value in trial.params.items():
            print("    {}: {}".format(key, value))

    best_params = {
        "objective": task,
        "metric": task,
        "verbosity": -1,
        "boosting_type": "gbdt",
        "seed": 42,
        "num_boost_round": 500,
        "early_stopping_rounds": 5,
    }
    best_params.update(study.best_params)
    if refit:
        x_ = pd.concat([train_x, valid_x])
        target_ = pd.concat([train_target, valid_target])
        model = lgb.train(
            params=best_params,
            train_set=lgb.Dataset(x_, label=target_, free_raw_data=False),
            valid_sets=[dtrain, dvalid],
            valid_names=["train", "valid"],
            verbose_eval=False
        )
    else:
        model = lgb.train(
            params=best_params,
            train_set=dtrain,
            valid_sets=[dtrain, dvalid],
            valid_names=["train", "valid"],
            verbose_eval=False
        )

    preds = model.predict(valid_x)
    pred_trains = model.predict(train_x)
    pred_tests = model.predict(test_x)

    valid_score = RScore(valid_target,
                         preds,
                         scoring=scoring)

    train_score = RScore(train_target,
                         pred_trains,
                         scoring=scoring)

    test_score = RScore(test_target,
                        pred_tests,
                        scoring=scoring)

    print(f"Train score: {train_score}")
    if not refit:
        print(f"Valid score: {valid_score}")
    print(f"Test score: {test_score}")

    feature_names = features.columns
    if saved_dir is None:
        list_dirs = os.scandir(os.getcwd())
        gate_ = [i for i in list_dirs if i.name=="lightgbm_shaps"]
        if len(gate_) == 1:
            saved_dir = os.path.join(os.getcwd(), "lightgbm_shaps")
        else:
            os.mkdir(os.path.join(os.getcwd(), "lightgbm_shaps"))
            saved_dir = os.path.join(os.getcwd(), "lightgbm_shaps")

    if show_shap:
        import sys
        sys.path.append('../Shapley')
        from .ShapleyC import shapley_importances_C
        shapley_importances_C(model=model, X=features,
                            feature_names=feature_names,
                            shap_sample_size=1, show_plot=show_shap, saved_dir=saved_dir)

    else:
        import sys
        sys.path.append('../Shapley')
        from .ShapleyC import shapley_importances_C
        shapley_importances_C(model=model, X=features,
                            feature_names=feature_names,
                            shap_sample_size=1, show_plot=False, saved_dir=saved_dir)

    return model
