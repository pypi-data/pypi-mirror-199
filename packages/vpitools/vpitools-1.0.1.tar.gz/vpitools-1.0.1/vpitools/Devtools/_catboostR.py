import numpy as np
import pandas as pd
import optuna
import os
import catboost as cat
from catboost import Pool
from .score_cal import RScore
import fasttreeshap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

seed=42
def Train_CATR(features:any=None,
               target:any=None,
               iterations:int=50,
               scoring:str=None,
               validation_size:float=0.2,
               test_size:float=0.1,
               validation_set:tuple=None,
               test_set:tuple=None,
               task:str="MAE",
               objectives:any="valid_score", #{0: "valid_score", 1: "train_test_drop"}
               base_score:float=None,
               show_shap:bool=False,
               saved_dir:any=None,
               refit=False,
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
        task : str,
            internal method for catboost to optimize gradient. Available tasks of CatBoost regression are:
            MAE, MAPE, Poisson, Quantile, RMSE, Tweedie, R2, MSLE, MedianAbsoluteError, Huber.
        objectives : any, {int or str}
            the way to perform optimization.
            "valid_score" or 0: mean to optimize valid score
            "train_test_drop" or 1: mean to optimize different between train and test score.
        base_score: float
            control underfitting when apply objective is train_test_drop / 1
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
        
        train_x, test_x, train_target, test_target = train_test_split(features, 
                                                                      target, 
                                                                      test_size=test_size, 
                                                                      random_state=seed)
        
    # if validation_set:
    #     train_x, train_target = features, target
    #     valid_x, valid_target = validation_set
    # else:
    #     train_x, valid_x, train_target, valid_target = train_test_split(features, target, test_size=validation_size, random_state=seed)
    dtrain = Pool(data=train_x, label=train_target, feature_names=features.columns.to_list())
    dvalid = Pool(data=valid_x, label=valid_target, feature_names=features.columns.to_list())
    dtest  = Pool(data=test_x, label=test_target, feature_names=features.columns.to_list())

    def objective(trial):
        param = {
            "objective": task,
            "eval_metric": task,
            "bootstrap_type": trial.suggest_categorical("bootstrap_type", 
                                                        ["MVS", 
                                                         "Bernoulli", 
                                                         "Bayesian"]),
            "l2_leaf_reg": trial.suggest_loguniform("l2_leaf_reg", 1e-2, 5),
            "learning_rate": trial.suggest_loguniform("learning_rate", 0.001, 0.1),
            "mvs_reg": trial.suggest_float("mvs_reg", 0, 10),
            "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 10, 1000),
            "grow_policy": trial.suggest_categorical("grow_policy", 
                                                     ["SymmetricTree", 
                                                      "Lossguide", 
                                                      "Depthwise"]),
            "nan_mode": trial.suggest_categorical("nan_mode", ["Min", "Max"]),
        }

        if param["bootstrap_type"] != "Bayesian":
            param["subsample"] = trial.suggest_loguniform("subsample", 0.4, .9)
        if param["grow_policy"] == "Lossguide":
            param["max_leaves"] = trial.suggest_int("max_leaves", 11, 63)
        if param["grow_policy"] == "SymmetricTree":
            param["boosting_type"] = trial.suggest_categorical("boosting_type", 
                                                               ["Ordered", 
                                                                "Plain"])

        model = cat.train(
            pool=dtrain, 
            params=param,
            iterations=150,
            # eval_set=dvalid,
            # early_stopping_rounds=5,
            verbose=0,
            )
        #model.fit(train_x, train_labels)#, valid_sets=dvalid, num_boost_round=100)
        preds = model.predict(dvalid)
        pred_trains = model.predict(dtrain)
        valid_score = RScore(valid_target, preds, scoring=scoring)
        train_score = RScore(train_target, pred_trains, scoring=scoring)
        diff = train_score-valid_score
        #scores = ["R2", "ExV", "Poisson", "D2T", "D2Pi", "D2A"]
        if objectives==0 or objectives=='valid_score':
            print(f"train-test differs: {diff}")
            return valid_score
        else:
            if valid_score >= base_score:
                print(valid_score)
                return np.abs(diff)
            else:
                return np.exp(np.abs(diff)) * 10

    guides = ["R2", "ExV", "Poisson", "D2T", "D2Pi", "D2A"]

    if scoring in guides:
        if objectives==0 or objectives=='valid_score':
            direction="maximize"
        else: direction='minimize'
    else:
        direction="minimize"

    study = optuna.create_study(direction=direction, study_name="find best model")
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
            "eval_metric": task,
        }
    best_params.update(study.best_params)
    
    if refit:
        x_ = pd.concat([train_x, valid_x])
        target_ = pd.concat([train_target, valid_target])
        model = cat.train(
            pool=Pool(x_, label=target_), 
            params=best_params, 
            eval_set=dvalid, 
            verbose=0, 
            early_stopping_rounds=5,
            )
            
    else:
        model = cat.train(
            pool=dtrain, 
            params=best_params, 
            eval_set=dvalid, 
            verbose=0, 
            early_stopping_rounds=5,
            )

    preds = model.predict(dvalid)
    pred_trains = model.predict(dtrain)
    pred_tests = model.predict(dtest)
    
    valid_score = RScore(valid_target, 
                         preds, 
                         scoring=scoring)
    
    train_score = RScore(train_target, 
                         pred_trains, 
                         scoring=scoring)
    
    test_score  = RScore(test_target, 
                         pred_tests, 
                         scoring=scoring)
    
    print(f"Train score: {train_score}")
    if not refit:
        print(f"Valid score: {valid_score}")
    print(f"Test score: {test_score}")
        
    shap_values = model.get_feature_importance(Pool(features, label=target), 
                                               type='ShapValues')
    #expected_value = shap_values[0, -1]
    shap_values = shap_values[:, :-1]
    if saved_dir is None:
        list_dirs = os.scandir(os.getcwd())
        gate_ = [i for i in list_dirs if i.name=="catboost_shap"]
        if len(gate_) == 1:
            saved_dir = os.path.join(os.getcwd(), "catboost_shap")
        else:
            os.mkdir(os.path.join(os.getcwd(), "catboost_shap"))
            saved_dir = os.path.join(os.getcwd(), "catboost_shap")

    if show_shap:
        fasttreeshap.summary_plot(shap_values, features)
        for feature in features.columns:
            fasttreeshap.dependence_plot(feature, shap_values, features)
    else:
        fasttreeshap.summary_plot(shap_values, features, show=False)
        f = plt.gcf()
        plt.title(f"Feature importances of Catboost model")
        plt.savefig(f"{saved_dir}/Catboost_summary_plot.png", bbox_inches='tight')
        plt.close()
        # visualize the first prediction's explanation
        for feature in features.columns:
            fasttreeshap.dependence_plot(feature, 
                                         shap_values, 
                                         features, 
                                         show=False)
            f = plt.gcf()
            plt.title(f"Catboost_{feature}_features dependency plot")
            plt.savefig(f"{saved_dir}/Catboost_{feature}_features dependency plot.png",
                        bbox_inches='tight')
            plt.close()
    return model
