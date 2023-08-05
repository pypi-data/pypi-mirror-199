import numpy as np
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import check_scoring
import lightgbm as lgbm


def lgbm_opt_classifier(
    X,
    y,
    n_iter=10,
    metric="accuracy",
    n_estimators=(10, 50, 100),
    max_depth=(3, 6, 9),
    num_leaves=(20, 50, 100, 500),
    learning_rate=(0.01, 0.1, 0.3, 0.5),
    boosting_type=("gbdt",),
    min_child_weight=(1, 5, 15, 100),
    subsample=(1.0,),
    subsample_for_bin=(200000,),
    colsample_bytree=(1.0,),
    reg_alpha=(0,),
    reg_lambda=(0.1, 1.0, 5.0),
    n_jobs=None,
    random_state=None,
):
    """
    Get LightGBM model with the best hyperparameters configuration.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.

    y : array-like of shape (n_samples,)
        The class labels.

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of the base classifier (LightGBM)
        in Hyperopt.

    metric: string, default="accuracy"
        The score of the base classifier (LightGBM) optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    n_estimators : tuple, default=(10, 50, 100)
        The number of LightGBM estimators. The number of estimators of
        LightGBM corresponds to the number of boosting rounds. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).

    max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for LightGBM base learners. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).
        
    num_leaves : tuple, default=(20, 50, 100, 500)
        Maximum tree leaves. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of LightGBM. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).
        
    boosting_type : ("dart", "gbdt", "rf"), default=("gbdt",)
        The type of boosting type to use: "dart" dropouts meet Multiple Additive 
        Regression Trees; "gbdt" traditional Gradient Boosting Decision Tree; "rf" Random Forest. 
        The tuple provided is the search space used for the hyperparameter optimization (Hyperopt).

    min_child_weight : tuple, default=(1, 5, 15, 100)
        `min_child_weight` of LightGBM. `min_child_weight` defines the
        minimum sum of instance weight (hessian) needed in a child. If the tree
        partition step results in a leaf node with the sum of instance weight
        less than `min_child_weight`, then the building process will give up further
        partitioning. The larger `min_child_weight` is, the more conservative LightGBM
        algorithm will be. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    subsample : tuple, default=(1.0,)
        LightGBM subsample ratio of the training instances. Setting it to 0.5 means
        that LightGBM would randomly sample half of the training data prior to
        growing trees, and this will prevent overfitting. Subsampling will occur
        once in every boosting iteration. The tuple provided is the search space used for
        the hyperparameter optimization (Hyperopt).
        
    subsample_for_bin : tuple, default=(200000,)
        Number of samples for constructing bins. The tuple provided is the
        search space used for the hyperparameter optimization (Hyperopt).

    colsample_bytree : tuple, default=(1.0,)
        LightGBM subsample ratio of columns when constructing each tree.
        Subsampling occurs once for every tree constructed. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    reg_alpha : tuple, default=(0,)
        `reg_alpha` of LightGBM. `reg_alpha` corresponds to the L1 regularization
        term on the weights. Increasing this value will make LightGBM model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` of LightGBM. `reg_lambda` corresponds to the L2 regularization
        term on the weights. Increasing this value will make LightGBM model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the base learner LightGBM and
        the Hyperopt algorithm.

    Returns
    -------
    model: object
        LightGBM model with the best configuration and fitted on the input data.
    """
    # Parameters
    classes, y = np.unique(y, return_inverse=True)
    n_classes = classes.size
        
    if n_classes == 2:
        objective = "binary"
        num_class = 1
    else: 
        objective = "multiclass"
        num_class = n_classes

    space = {
        "n_estimators": hp.choice("n_estimators", n_estimators),
        "max_depth": hp.choice("max_depth", max_depth),
        "num_leaves": hp.choice("num_leaves", num_leaves),
        "learning_rate": hp.choice("learning_rate", learning_rate),
        "boosting_type": hp.choice("boosting_type", boosting_type),
        "min_child_weight": hp.choice("min_child_weight", min_child_weight),
        "subsample": hp.choice("subsample", subsample),
        "subsample_for_bin": hp.choice("subsample_for_bin", subsample_for_bin),
        "colsample_bytree": hp.choice("colsample_bytree", colsample_bytree),
        "reg_alpha": hp.choice("reg_alpha", reg_alpha),
        "reg_lambda": hp.choice("reg_lambda", reg_lambda),
        "objective": objective,
        "num_class": num_class,
        "n_jobs": n_jobs,
        "random_state": random_state,
    }

    # Get best configuration
    def p_model(params):
        clf = lgbm.LGBMClassifier(**params, verbose=-1)
        clf.fit(X, y)
        scorer = check_scoring(clf, scoring=metric)
        return scorer(clf, X, y)

    global best
    best = -np.inf

    def f(params):
        global best
        perf = p_model(params)
        if perf > best:
            best = perf
        return {"loss": -best, "status": STATUS_OK}

    rstate = np.random.default_rng(random_state)
    best_config = fmin(
        fn=f,
        space=space,
        algo=tpe.suggest,
        max_evals=n_iter,
        trials=Trials(),
        rstate=rstate,
        verbose=0,
    )

    # Fit best model
    final_params = {
        "n_estimators": n_estimators[best_config["n_estimators"]],
        "max_depth": max_depth[best_config["max_depth"]],
        "num_leaves": num_leaves[best_config["num_leaves"]],
        "learning_rate": learning_rate[best_config["learning_rate"]],
        "boosting_type": boosting_type[best_config["boosting_type"]],
        "min_child_weight": min_child_weight[best_config["min_child_weight"]],
        "subsample": subsample[best_config["subsample"]],
        "subsample_for_bin": subsample_for_bin[best_config["subsample_for_bin"]],
        "colsample_bytree": colsample_bytree[best_config["colsample_bytree"]],
        "reg_alpha": reg_alpha[best_config["reg_alpha"]],
        "reg_lambda": reg_lambda[best_config["reg_lambda"]],
        "objective": objective,
        "num_class": num_class,
        "n_jobs": n_jobs,
        "random_state": random_state,
    }
    clf = lgbm.LGBMClassifier(**final_params, verbose=-1)
    return clf.fit(X, y)


def lgbm_opt_regressor(
    X,
    y,
    n_iter=10,
    metric="neg_mean_squared_error",
    n_estimators=(10, 50, 100),
    max_depth=(3, 6, 9),
    num_leaves=(20, 50, 100, 500),
    learning_rate=(0.01, 0.1, 0.3, 0.5),
    boosting_type=("gbdt",),
    min_child_weight=(1, 5, 15, 100),
    subsample=(1.0,),
    subsample_for_bin=(200000,),
    colsample_bytree=(1.0,),
    reg_alpha=(0,),
    reg_lambda=(0.1, 1.0, 5.0),
    n_jobs=None,
    random_state=None,
):
    """
    Get LightGBM model with the best hyperparameters configuration.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.

    y : array-like of shape (n_samples,)
        The target values (real numbers).

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of the base regressor (LightGBM)
        in Hyperopt.

    metric: string, default="neg_mean_squared_error"
        The score of the base regressor (LightGBM) optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    n_estimators : tuple, default=(10, 50, 100)
        The number of LightGBM estimators. The number of estimators of
        LightGBM corresponds to the number of boosting rounds. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).

    max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for LightGBM base learners. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).
        
    num_leaves : tuple, default=(20, 50, 100, 500)
        Maximum tree leaves. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of LightGBM. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).
        
    boosting_type : ("dart", "gbdt", "rf"), default=("gbdt",)
        The type of boosting type to use: "dart" dropouts meet Multiple Additive 
        Regression Trees; "gbdt" traditional Gradient Boosting Decision Tree; "rf" Random Forest. 
        The tuple provided is the search space used for the hyperparameter optimization (Hyperopt).

    min_child_weight : tuple, default=(1, 5, 15, 100)
        `min_child_weight` of LightGBM. `min_child_weight` defines the
        minimum sum of instance weight (hessian) needed in a child. If the tree
        partition step results in a leaf node with the sum of instance weight
        less than `min_child_weight`, then the building process will give up further
        partitioning. The larger `min_child_weight` is, the more conservative LightGBM
        algorithm will be. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    subsample : tuple, default=(1.0,)
        LightGBM subsample ratio of the training instances. Setting it to 0.5 means
        that LightGBM would randomly sample half of the training data prior to
        growing trees, and this will prevent overfitting. Subsampling will occur
        once in every boosting iteration. The tuple provided is the search space used for
        the hyperparameter optimization (Hyperopt).
        
    subsample_for_bin : tuple, default=(200000,)
        Number of samples for constructing bins. The tuple provided is the
        search space used for the hyperparameter optimization (Hyperopt).

    colsample_bytree : tuple, default=(1.0,)
        LightGBM subsample ratio of columns when constructing each tree.
        Subsampling occurs once for every tree constructed. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    reg_alpha : tuple, default=(0,)
        `reg_alpha` of LightGBM. `reg_alpha` corresponds to the L1 regularization
        term on the weights. Increasing this value will make LightGBM model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` of LightGBM. `reg_lambda` corresponds to the L2 regularization
        term on the weights. Increasing this value will make LightGBM model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the base learner LightGBM and
        the Hyperopt algorithm.

    Returns
    -------
    model: object
        LightGBM model with the best configuration and fitted on the input data.
    """
    space = {
        "n_estimators": hp.choice("n_estimators", n_estimators),
        "max_depth": hp.choice("max_depth", max_depth),
        "num_leaves": hp.choice("num_leaves", num_leaves),
        "learning_rate": hp.choice("learning_rate", learning_rate),
        "boosting_type": hp.choice("boosting_type", boosting_type),
        "min_child_weight": hp.choice("min_child_weight", min_child_weight),
        "subsample": hp.choice("subsample", subsample),
        "subsample_for_bin": hp.choice("subsample_for_bin", subsample_for_bin),
        "colsample_bytree": hp.choice("colsample_bytree", colsample_bytree),
        "reg_alpha": hp.choice("reg_alpha", reg_alpha),
        "reg_lambda": hp.choice("reg_lambda", reg_lambda),
        "objective": "regression",
        "n_jobs": n_jobs,
        "random_state": random_state,
    }

    # Get best configuration
    def p_model(params):
        reg = lgbm.LGBMRegressor(**params, verbose=-1)
        reg.fit(X, y)
        scorer = check_scoring(reg, scoring=metric)
        return scorer(reg, X, y)

    global best
    best = -np.inf

    def f(params):
        global best
        perf = p_model(params)
        if perf > best:
            best = perf
        return {"loss": -best, "status": STATUS_OK}

    rstate = np.random.default_rng(random_state)
    best_config = fmin(
        fn=f,
        space=space,
        algo=tpe.suggest,
        max_evals=n_iter,
        trials=Trials(),
        rstate=rstate,
        verbose=0,
    )

    # Fit best model
    final_params = {
        "n_estimators": n_estimators[best_config["n_estimators"]],
        "max_depth": max_depth[best_config["max_depth"]],
        "num_leaves": num_leaves[best_config["num_leaves"]],
        "learning_rate": learning_rate[best_config["learning_rate"]],
        "boosting_type": boosting_type[best_config["boosting_type"]],
        "min_child_weight": min_child_weight[best_config["min_child_weight"]],
        "subsample": subsample[best_config["subsample"]],
        "subsample_for_bin": subsample_for_bin[best_config["subsample_for_bin"]],
        "colsample_bytree": colsample_bytree[best_config["colsample_bytree"]],
        "reg_alpha": reg_alpha[best_config["reg_alpha"]],
        "reg_lambda": reg_lambda[best_config["reg_lambda"]],
        "objective": "regression",
        "n_jobs": n_jobs,
        "random_state": random_state,
    }
    reg = lgbm.LGBMRegressor(**final_params, verbose=-1)
    return reg.fit(X, y)
