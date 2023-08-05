import numpy as np
import pandas as pd
import optuna
import lightgbm as lgb
from .score_cal import Score
from sklearn.model_selection import train_test_split
import os
seed = 42


def Train_LGBMC(features: any = None,
                labels: any = None,
                iterations: int = 50,
                scoring: str = None,
                base_score: float = 0.8,  # desired scored
                validation_size: float = 0.2,
                test_size: float = 0.1,
                validation_set: tuple = None,
                test_set: tuple = None,
                task: str = "binary",
                # {0: "valid_score", 1: "train_valid_drop"}
                objectives: any = "valid_score",
                # {0: "min false negative", 1: "min false positive", 2: "balanced"}
                favor_class: any = 1,
                start: any = 1,  # 1 or True
                show_shap: bool = True,
                saved_dir: str = None,
                refit: bool = True,
                ):
    """Construct a function to train a booster.

    Parameters
    ----------
    features : any, {dataframe, array} of predictors
        features use to build model.
    labels : any, {array, Series} of labels
        labels to be predicted.
    iterations : int,
        number of optimization rounds.
    scoring : str,
        scoring method for optimization.
        Available scoring method is sklearn regression metrics: balanced_accuracy, f1_weighted, precision, recall,
                roc_auc, accuracy.
    validation_size: float,
        size of validation set use to evaluate model.
    test_size: float,
        size of test set.
    validation_set: tuple,
        tuple of (X_valid, y_valid)
    test_set: tuple,
        tuple of (X_test, y_test)
    task : str,
        internal method for xgboost to optimize gradient. Available tasks of lightgbm classification are:
        binary, cross_entropy, multiclass, multiclassova.
    objectives : any, {int or str}
        the way to perform optimization.
        "valid_score" or 0: mean to optimize valid score
        "train_valid_drop" or 1: mean to optimize different between train and valid score.
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
        train_x, train_labels = features, labels
        valid_x, valid_labels = validation_set
        test_x, test_labels = test_set

    elif validation_set and test_size:
        valid_x, valid_labels = validation_set
        train_x, test_x, train_labels, test_labels = train_test_split(features,
                                                                      labels,
                                                                      test_size=test_size,
                                                                      random_state=seed)
    elif test_set and validation_size:
        train_x, valid_x, train_labels, valid_labels = train_test_split(features,
                                                                        labels,
                                                                        test_size=validation_size,
                                                                        random_state=seed)
        test_x, test_labels = test_set

    else:
        train_x, valid_x, train_labels, valid_labels = train_test_split(features,
                                                                        labels,
                                                                        test_size=validation_size,
                                                                        random_state=seed)

        train_x, test_x, train_labels, test_labels = train_test_split(features,
                                                                      labels,
                                                                      test_size=test_size,
                                                                      random_state=seed)
    # set datamatrix
    dtrain = lgb.Dataset(train_x, label=train_labels, free_raw_data=False)
    dvalid = lgb.Dataset(valid_x, label=valid_labels, free_raw_data=False)
    dtest = lgb.Dataset(test_x, label=test_labels, free_raw_data=False)

    def objective(trial):
        params = {
            "objective": task,
            "verbosity": -1,
            "feature_pre_filter": False,
            "is_unbalance": trial.suggest_categorical("is_unbalance", [True]),
            "boosting_type": trial.suggest_categorical("boosting_type", ["gbdt"]),
            # "n_estimators": trial.suggest_int("n_estimators", 10, 1000),
            "learning_rate": trial.suggest_loguniform("learning_rate", 1e-3, 0.5),
            "lambda_l1": trial.suggest_loguniform("lambda_l1", 1e-2, 5.0),
            "lambda_l2": trial.suggest_loguniform("lambda_l2", 1e-2, 5.0),
            "num_leaves": trial.suggest_("num_leaves", [21, 31, 41, 51, 61, 63]),
            "feature_fraction": trial.suggest_loguniform("feature_fraction", 0.4, 1.0),
            "bagging_fraction": trial.suggest_loguniform("bagging_fraction", 0.4, 1.0),
            # "bagging_freq": trial.suggest_int("bagging_freq", 1, 15),
            "min_data_in_leaf": trial.suggest_categorical("min_data_in_leaf", [21, 31, 41, 51, 61]),
            "min_sum_hessian_in_leaf": trial.suggest_loguniform("min_sum_hessian_in_leaf", 1e-3, 100),
            # "scale_pos_weight": trial.suggest_loguniform("scale_pos_weight", 1., 100),
            "tree_learner": trial.suggest_categorical("tree_learner", ["serial", "feature"]),
            "pos_bagging_fraction": trial.suggest_loguniform("pos_bagging_fraction", 2e-1, .8),
        }

        model = lgb.train(
            params,
            dtrain,
            # valid_sets=[dvalid],
            # valid_names=["valid"],
            # num_boost_round=500,
            # early_stopping_rounds=5,
            verbose_eval=False)

        # model.fit(train_x, train_labels)#, valid_sets=dvalid, num_boost_round=100)
        preds = model.predict(valid_x)
        pred_labels = preds > 0.5
        pred_trains = model.predict(train_x)
        pred_trains = pred_trains > 0.5
        valid_score = Score(valid_labels, pred_labels,
                            scoring=scoring, favor_class=favor_class)
        train_score = Score(train_labels, pred_trains,
                            scoring=scoring, favor_class=favor_class)
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

    guides = ["balanced_accuracy", "recall", "f1_weighted", "precision",
              "roc_auc", "R2", "ExV", "Poisson", "D2T", "D2Pi", "D2A"]

    if objectives == 0 or objectives == 'valid_score':
        direction = "maximize"
    else:
        direction = "minimize"

    if start == 1 or start == True:
        study = optuna.create_study(direction=direction,
                                    study_name="find best model")
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
        "metric": "auc",
        "verbosity": -1,
        # "boosting_type": "gbdt",
        "seed": seed,
        "num_boost_round": 1000,
        "early_stopping_rounds": 5,
    }
    best_params.update(study.best_params)

    if refit:
        x_ = pd.concat([train_x, valid_x])
        label_ = pd.concat([train_labels, valid_labels])
        model = lgb.train(params=best_params,
                          train_set=lgb.Dataset(x_,
                                                label=label_,
                                                free_raw_data=False),
                          valid_sets=[dvalid],
                          valid_names=["valid"],
                          verbose_eval=False)
    else:
        model = lgb.train(params=best_params,
                          train_set=dtrain,
                          valid_sets=[dtrain, dvalid],
                          valid_names=["train", "valid"],
                          verbose_eval=False)

    preds = model.predict(valid_x)
    pred_labels = preds > 0.5
    pred_trains = model.predict(train_x)
    pred_trains = pred_trains > 0.5
    pred_tests = model.predict(test_x)
    pred_tests = pred_tests > 0.5

    valid_score = Score(valid_labels,
                        pred_labels,
                        scoring=scoring,
                        favor_class=favor_class)

    train_score = Score(train_labels,
                        pred_trains,
                        scoring=scoring,
                        favor_class=favor_class)
    test_score = Score(test_labels,
                       pred_tests,
                       scoring=scoring,
                       favor_class=favor_class)

    print(f"Train score: {train_score:.3f}")
    if not refit:
        print(f"Valid score: {valid_score:.3f}")

    print(f"Test score: {test_score:.3f}")

    # shap calculation
    feature_names = features.columns
    if saved_dir is None:
        list_dirs = os.scandir(os.getcwd())
        gate_ = [i for i in list_dirs if i.name=="lightgbm_shap"]
        if len(gate_) == 1:
            saved_dir = os.path.join(os.getcwd(), "lightgbm_shap")
        else:
            os.mkdir(os.path.join(os.getcwd(), "lightgbm_shap"))
            saved_dir = os.path.join(os.getcwd(), "lightgbm_shap")

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
    lgb.plot_importance(model)
    lgb.plot_tree(model)

    return model
