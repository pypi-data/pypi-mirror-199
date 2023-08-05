import numpy as np
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import check_scoring
from catboost import CatBoostClassifier, CatBoostRegressor


def catboost_opt_classifier(
    X,
    y,
    n_iter=10,
    metric="accuracy",
    n_estimators=(10, 50, 100),
    max_depth=(3, 6, 9),
    learning_rate=(0.01, 0.1, 0.3, 0.5),
    colsample_bylevel=(1.0,),
    reg_lambda=(0.1, 1.0, 5.0),
    n_jobs=None,
    random_state=None,
):
    """
    Get CatBoost model with the best hyperparameters configuration.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.

    y : array-like of shape (n_samples,)
        The class labels.

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of the base classifier (CatBoost)
        in Hyperopt.

    metric: string, default="accuracy"
        The score of the base classifier (CatBoost) optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    n_estimators : tuple, default=(10, 50, 100)
        The number of estimators for the base learner. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).
        
    max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for the base learner. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).
        
    learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of the base learner. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).
        
    colsample_bylevel : tuple, default=(1.0,)
        Subsample ratio of columns for each level. Subsampling occurs
        once for every new depth level reached in a tree. Columns are subsampled
        from the set of columns chosen for the current tree. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` / `l2_leaf_reg` of CatBoost. The tuple provided is the search 
        space used for the hyperparameter optimization (Hyperopt).
        
    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the base learner CatBoost and
        the Hyperopt algorithm.

    Returns
    -------
    model: object
        CatBoost model with the best configuration and fitted on the input data.
    """
    # Parameters
    classes, y = np.unique(y, return_inverse=True)
    
    space = {
        "n_estimators": hp.choice("n_estimators", n_estimators),
        "depth": hp.choice("max_depth", max_depth),
        "learning_rate": hp.choice("learning_rate", learning_rate),
        "colsample_bylevel": hp.choice("colsample_bylevel", colsample_bylevel),
        "reg_lambda": hp.choice("reg_lambda", reg_lambda),
        "thread_count": n_jobs,
        "random_state": random_state,
    }

    # Get best configuration
    def p_model(params):
        clf = CatBoostClassifier(**params, verbose=False)
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
        "depth": max_depth[best_config["max_depth"]],
        "learning_rate": learning_rate[best_config["learning_rate"]],
        "colsample_bylevel": colsample_bylevel[best_config["colsample_bylevel"]],
        "reg_lambda": reg_lambda[best_config["reg_lambda"]],   
        "thread_count": n_jobs,
        "random_state": random_state,
    }
    clf = CatBoostClassifier(**final_params, verbose=False)
    return clf.fit(X, y)


def catboost_opt_regressor(
    X,
    y,
    n_iter=10,
    metric="neg_mean_squared_error",
    n_estimators=(10, 50, 100),
    max_depth=(3, 6, 9),
    learning_rate=(0.01, 0.1, 0.3, 0.5),
    colsample_bylevel=(1.0,),
    reg_lambda=(0.1, 1.0, 5.0),
    n_jobs=None,
    random_state=None,
):
    """
    Get CatBoost model with the best hyperparameters configuration.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.

    y : array-like of shape (n_samples,)
        The target values (real numbers).

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of the base regressor (CatBoost)
        in Hyperopt.

    metric: string, default="neg_mean_squared_error"
        The score of the base regressor (CatBoost) optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    n_estimators : tuple, default=(10, 50, 100)
        The number of estimators for the base learner. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).
        
    max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for the base learner. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).
        
    learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of the base learner. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).
        
    colsample_bylevel : tuple, default=(1.0,)
        Subsample ratio of columns for each level. Subsampling occurs
        once for every new depth level reached in a tree. Columns are subsampled
        from the set of columns chosen for the current tree. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` / `l2_leaf_reg` of CatBoost. The tuple provided is the search 
        space used for the hyperparameter optimization (Hyperopt).
        
    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the base learner CatBoost and
        the Hyperopt algorithm.

    Returns
    -------
    model: object
        CatBoost model with the best configuration and fitted on the input data.
    """
    space = {
        "n_estimators": hp.choice("n_estimators", n_estimators),
        "depth": hp.choice("max_depth", max_depth),
        "learning_rate": hp.choice("learning_rate", learning_rate),
        "colsample_bylevel": hp.choice("colsample_bylevel", colsample_bylevel),
        "reg_lambda": hp.choice("reg_lambda", reg_lambda),
        "thread_count": n_jobs,
        "random_state": random_state,
    }

    # Get best configuration
    def p_model(params):
        reg = CatBoostRegressor(**params, verbose=False)
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
        "depth": max_depth[best_config["max_depth"]],
        "learning_rate": learning_rate[best_config["learning_rate"]],
        "colsample_bylevel": colsample_bylevel[best_config["colsample_bylevel"]],
        "reg_lambda": reg_lambda[best_config["reg_lambda"]],
        "thread_count": n_jobs,
        "random_state": random_state,
    }
    reg = CatBoostRegressor(**final_params, verbose=False)
    return reg.fit(X, y)
