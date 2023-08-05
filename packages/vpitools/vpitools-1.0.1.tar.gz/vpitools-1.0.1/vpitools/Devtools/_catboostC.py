import numpy as np
import pandas as pd
import optuna
import catboost as cat
from catboost import Pool
from .score_cal import Score
from sklearn.model_selection import train_test_split
import os

seed=42
def Train_CATC(features:any=None,
               labels:any=None,
               iterations:int=50,
               scoring:str=None,
               validation_size:float=0.1,
               test_size:float=0.1,
               validation_set:tuple=None,
               test_set:tuple=None,
               task:str="Logloss",
               objectives:any="valid_score", #{0: "valid_score", 1: "train_test_drop"}
               base_score:float=None,
               favor_class:any=1, #{0: "min false negative", 1: "min false positive", 2: "balanced"}
               start:any=1, # 1 or True
               show_shap:bool=False,
               saved_dir:any=None,
               refit:bool=False,
               ):
    """Construct a function to train a booster.

    Parameters
    ----------
    features : any, {dataframe, array} of predictors
        features use to build model.
    labels : any, {array, Series} of labels
        labels to be predicted.
    iterations : int,
        default = 50, number of optimization rounds.
    scoring : str,
        scoring method for optimization.
        Available scoring method is sklearn regression metrics: balanced_accuracy, f1_weighted, precision, recall,
                roc_auc, accuracy.
    validation_size: float,
        size of validation set use to evaluate model.
    task : str,
        internal method for CatBoost to optimize gradient. Available tasks of CatBoost classification are:
        Logloss, Accuracy, AUC, BalancedAccuracy, F, F1, Precision, Recall, CrossEntropy.
    objectives : any, {int or str}
        the way to perform optimization.
        "valid_score" or 0: mean to optimize valid score
        "train_test_drop" or 1: mean to optimize different between train and test score.
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
    # if validation_set:
    #     train_x, train_labels = features, labels
    #     valid_x, valid_labels = validation_set
    # else:
    #     train_x, valid_x, train_labels, valid_labels = train_test_split(features, labels, test_size=validation_size, random_state=seed)
    dtrain = Pool(data=train_x, label=train_labels, feature_names=features.columns.to_list())
    dvalid = Pool(data=valid_x, label=valid_labels, feature_names=features.columns.to_list())
    dtest = Pool(data=test_x, label=test_labels, feature_names=features.columns.to_list())

    def objective(trial):
        param = {
            "objective": trial.suggest_categorical("objective", ["Logloss"]),
            #"eval_metric": "Accuracy",
            #"grow_policy": "Lossguide",
            #"bootstrap_type": "Bayesian",
            "bootstrap_type": trial.suggest_categorical("bootstrap_type", ["MVS", "Bernoulli", "Bayesian"]),
            "l2_leaf_reg": trial.suggest_loguniform("l2_leaf_reg", 1e-2, 5),
            "learning_rate": trial.suggest_loguniform("learning_rate", 0.001, 0.3),
            "mvs_reg": trial.suggest_float("mvs_reg", 0, 10),
            "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 10, 1000),
            "grow_policy": trial.suggest_categorical("grow_policy", ["SymmetricTree", "Lossguide", "Depthwise"]),
            # "nan_mode": trial.suggest_categorical("nan_mode", ["Min", "Max"]),
            # "subsample": trial.suggest_loguniform("subsample", 0.01, 1.),
            # "scale_pos_weight": trial.suggest_loguniform("scale_pos_weight", 1, 20.),
            # "sampling_frequency": trial.suggest_categorical("sampling_frequency", ["PerTree", "PerTreeLevel"]),
            #"auto_class_weights": trial.suggest_categorical("auto_class_weights", ["Balanced", "SqrtBalanced"]),
            #"langevin": trial.suggest_categorical("langevin", [True, False]),
            #"max_ctr_complexity": trial.suggest_int("max_ctr_complexity", 0, 8),
            # "colsample_bylevel": trial.suggest_loguniform("colsample_bylevel", 0.01, 1),
            #"depth": trial.suggest_int("depth", 3, 16)
        }

        if param["objective"] == "Logloss":
            param["auto_class_weights"] = trial.suggest_categorical("auto_class_weights", ["Balanced"])
        # if param["objective"] == "CrossEntropy":
        #     param["scale_pos_weight"] = trial.suggest_loguniform("scale_pos_weight", 1, 20.)
        if param["bootstrap_type"] != "Bayesian":
            param["subsample"] = trial.suggest_loguniform("subsample", 0.4, .9)
        if param["grow_policy"] == "Lossguide":
            param["max_leaves"] = trial.suggest_int("max_leaves", 11, 63)
        if param["grow_policy"] == "SymmetricTree":
            param["boosting_type"] = trial.suggest_categorical("boosting_type", ["Ordered", "Plain"])

        model = cat.train(
            pool=dtrain, 
            params=param, 
            iterations=150,
            # eval_set=dvalid,
            # early_stopping_rounds=5,
            verbose=0,
            )

        preds = model.predict(dvalid, prediction_type="Probability")[:,1]
        pred_labels = preds>0.5
        pred_trains = model.predict(dtrain, prediction_type="Probability")[:,1]
        pred_trains = pred_trains>0.5
        valid_score = Score(valid_labels.astype(int), pred_labels.astype(int), scoring=scoring, favor_class=favor_class)
        train_score = Score(train_labels.astype(int), pred_trains.astype(int), scoring=scoring, favor_class=favor_class)
        diff = train_score-valid_score

        if objectives==0 or objectives=='valid_score':
            print(f"train-test differs: {diff}")
            return valid_score
        else:
            if valid_score >= base_score:
                print(valid_score)
                return np.abs(diff)
            else:
                return np.exp(np.abs(diff)) * 10

    guides = ["balanced_accuracy", "recall", "f1_weighted", "precision", "roc_auc", "R2", "ExV", "Poisson", "D2T", "D2Pi", "D2A"]

    if objectives==0 or objectives=='valid_score':
        direction="maximize"
    else:
        direction="minimize"

    if start==1 or start==True:
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
            #"objective": "Logloss",
            "eval_metric": "Logloss",
        }

    best_params.update(study.best_params)
    
    if refit:
        x_ = pd.concat([train_x, valid_x])
        label_ = pd.concat([train_labels, valid_labels])
        model = cat.train(
            pool=Pool(x_, label=label_), 
            params=best_params, 
            eval_set=dvalid, 
            early_stopping_rounds=5, 
            verbose=0)
    else:
        model = cat.train(
            pool=dtrain, 
            params=best_params, 
            eval_set=dvalid, 
            early_stopping_rounds=5, 
            verbose=0)
        
    preds = model.predict(dvalid, prediction_type="Probability")[:,1]
    pred_labels = preds >0.5
    
    pred_trains = model.predict(dtrain, prediction_type="Probability")[:,1]
    pred_trains = pred_trains >0.5
    
    pred_tests = model.predict(dtest, prediction_type="Probability")[:,1]
    pred_tests = pred_tests >0.5
    
    valid_score = Score(valid_labels.astype(int), 
                        pred_labels.astype(int), 
                        scoring=scoring, 
                        favor_class=favor_class)
    train_score = Score(train_labels.astype(int), 
                        pred_trains.astype(int), 
                        scoring=scoring, 
                        favor_class=favor_class)
    
    test_score = Score(test_labels.astype(int), 
                        pred_tests.astype(int), 
                        scoring=scoring, 
                        favor_class=favor_class)
    
    print(f"Train score: {train_score}")
    if not refit:
        print(f"Valid score: {valid_score}")
        
    print(f"Test score: {test_score}")
    # train_pool_slice = Pool(features, label=labels).slice([i for i in range(len(features.columns))])
    # prediction_diff = model.get_feature_importance(train_pool_slice,
    #                                                type='PredictionDiff',
    #                                                prettified=True)
    #
    # model.plot_predictions(data=train_pool_slice,
    #                        features_to_change=prediction_diff["Feature Id"][:2],
    #                        plot=True,
    #                        plot_file="plot_predictions_file.html")
    if saved_dir is None:
        list_dirs = os.scandir(os.getcwd())
        gate_ = [i for i in list_dirs if i.name=="catboost_shap"]
        if len(gate_) == 1:
            saved_dir = os.path.join(os.getcwd(), "catboost_shap")
        else:
            os.mkdir(os.path.join(os.getcwd(), "catboost_shap"))
            saved_dir = os.path.join(os.getcwd(), "catboost_shap")

    if show_shap:
        import sys
        sys.path.append('../Shapley')
        from .ShapleyC import shapley_importances_C
        shapley_importances_C(model=model, X=features, feature_names=features.columns,
                            shap_sample_size=1, show_plot=show_shap, saved_dir=saved_dir)
    else:
        import sys
        sys.path.append('../Shapley')
        from .ShapleyC import shapley_importances_C
        shapley_importances_C(model=model, X=features, feature_names=features.columns, shap_sample_size=1,
                            show_plot=False, saved_dir=saved_dir)
    return model
