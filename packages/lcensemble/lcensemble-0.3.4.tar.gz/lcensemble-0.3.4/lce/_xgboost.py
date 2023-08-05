import numpy as np
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import check_scoring
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb


def xgb_opt_classifier(
    X,
    y,
    n_iter=10,
    metric="accuracy",
    n_estimators=(10, 50, 100),
    max_depth=(3, 6, 9),
    learning_rate=(0.01, 0.1, 0.3, 0.5),
    booster=("gbtree",),
    gamma=(0, 1, 10),
    min_child_weight=(1, 5, 15, 100),
    subsample=(1.0,),
    colsample_bytree=(1.0,),
    colsample_bylevel=(1.0,),
    colsample_bynode=(1.0,),
    reg_alpha=(0,),
    reg_lambda=(0.1, 1.0, 5.0),
    n_jobs=None,
    random_state=None,
):
    """
    Get XGBoost model with the best hyperparameters configuration.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.

    y : array-like of shape (n_samples,)
        The class labels.

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of the base classifier (XGBoost)
        in Hyperopt.

    metric: string, default="accuracy"
        The score of the base classifier (XGBoost) optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    n_estimators : tuple, default=(10, 50, 100)
        The number of XGBoost estimators. The number of estimators of
        XGBoost corresponds to the number of boosting rounds. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).

    max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for XGBoost base learners. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of XGBoost. The learning rate corresponds to the
        step size shrinkage used in update to prevent overfitting. After each
        boosting step, the learning rate shrinks the feature weights to make the boosting
        process more conservative. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).

    booster : ("dart", "gblinear", "gbtree"), default=("gbtree",)
        The type of booster to use. "gbtree" and "dart" use tree based models
        while "gblinear" uses linear functions. The tuple provided is the search space used
        for the hyperparameter optimization (Hyperopt).

    gamma : tuple, default=(0, 1, 10)
        `gamma` of XGBoost. `gamma` corresponds to the minimum loss reduction
        required to make a further partition on a leaf node of the tree.
        The larger `gamma` is, the more conservative XGBoost algorithm will be.
        The tuple provided is the search space used for the hyperparameter optimization
        (Hyperopt).

    min_child_weight : tuple, default=(1, 5, 15, 100)
        `min_child_weight` of XGBoost. `min_child_weight` defines the
        minimum sum of instance weight (hessian) needed in a child. If the tree
        partition step results in a leaf node with the sum of instance weight
        less than `min_child_weight`, then the building process will give up further
        partitioning. The larger `min_child_weight` is, the more conservative XGBoost
        algorithm will be. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    subsample : tuple, default=(1.0,)
        XGBoost subsample ratio of the training instances. Setting it to 0.5 means
        that XGBoost would randomly sample half of the training data prior to
        growing trees, and this will prevent overfitting. Subsampling will occur
        once in every boosting iteration. The tuple provided is the search space used for
        the hyperparameter optimization (Hyperopt).

    colsample_bytree : tuple, default=(1.0,)
        XGBoost subsample ratio of columns when constructing each tree.
        Subsampling occurs once for every tree constructed. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    colsample_bylevel : tuple, default=(1.0,)
        XGBoost subsample ratio of columns for each level. Subsampling occurs
        once for every new depth level reached in a tree. Columns are subsampled
        from the set of columns chosen for the current tree. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    colsample_bynode : tuple, default=(1.0,)
        XGBoost subsample ratio of columns for each node (split). Subsampling
        occurs once every time a new split is evaluated. Columns are subsampled
        from the set of columns chosen for the current level. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    reg_alpha : tuple, default=(0,)
        `reg_alpha` of XGBoost. `reg_alpha` corresponds to the L1 regularization
        term on the weights. Increasing this value will make XGBoost model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` of XGBoost. `reg_lambda` corresponds to the L2 regularization
        term on the weights. Increasing this value will make XGBoost model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the base learner XGBoost and
        the Hyperopt algorithm.

    Returns
    -------
    model: object
        XGBoost model with the best configuration and fitted on the input data.
    """
    # Parameters
    classes, y = np.unique(y, return_inverse=True)
    n_classes = classes.size

    space = {
        "n_estimators": hp.choice("n_estimators", n_estimators),
        "max_depth": hp.choice("max_depth", max_depth),
        "learning_rate": hp.choice("learning_rate", learning_rate),
        "booster": hp.choice("booster", booster),
        "gamma": hp.choice("gamma", gamma),
        "min_child_weight": hp.choice("min_child_weight", min_child_weight),
        "subsample": hp.choice("subsample", subsample),
        "colsample_bytree": hp.choice("colsample_bytree", colsample_bytree),
        "colsample_bylevel": hp.choice("colsample_bylevel", colsample_bylevel),
        "colsample_bynode": hp.choice("colsample_bynode", colsample_bynode),
        "reg_alpha": hp.choice("reg_alpha", reg_alpha),
        "reg_lambda": hp.choice("reg_lambda", reg_lambda),
        "objective": "multi:softprob",
        "num_class": n_classes,
        "n_jobs": n_jobs,
        "random_state": random_state,
    }

    # Get best configuration
    def p_model(params):
        clf = xgb.XGBClassifier(**params, use_label_encoder=False, verbosity=0)
        clf.fit(X, y)
        if n_classes == 2:
            onehot_encoder = OneHotEncoder(sparse=False)
            y_score = onehot_encoder.fit_transform(y.reshape(len(y), 1))
        else:
            y_score = y
        scorer = check_scoring(clf, scoring=metric)
        return scorer(clf, X, y_score)

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
        "learning_rate": learning_rate[best_config["learning_rate"]],
        "booster": booster[best_config["booster"]],
        "gamma": gamma[best_config["gamma"]],
        "min_child_weight": min_child_weight[best_config["min_child_weight"]],
        "subsample": subsample[best_config["subsample"]],
        "colsample_bytree": colsample_bytree[best_config["colsample_bytree"]],
        "colsample_bylevel": colsample_bylevel[best_config["colsample_bylevel"]],
        "colsample_bynode": colsample_bynode[best_config["colsample_bynode"]],
        "reg_alpha": reg_alpha[best_config["reg_alpha"]],
        "reg_lambda": reg_lambda[best_config["reg_lambda"]],
        "objective": "multi:softprob",
        "num_class": n_classes,
        "n_jobs": n_jobs,
        "random_state": random_state,
    }
    clf = xgb.XGBClassifier(**final_params, use_label_encoder=False, verbosity=0)
    return clf.fit(X, y)


def xgb_opt_regressor(
    X,
    y,
    n_iter=10,
    metric="neg_mean_squared_error",
    n_estimators=(10, 50, 100),
    max_depth=(3, 6, 9),
    learning_rate=(0.01, 0.1, 0.3, 0.5),
    booster=("gbtree",),
    gamma=(0, 1, 10),
    min_child_weight=(1, 5, 15, 100),
    subsample=(1.0,),
    colsample_bytree=(1.0,),
    colsample_bylevel=(1.0,),
    colsample_bynode=(1.0,),
    reg_alpha=(0,),
    reg_lambda=(0.1, 1.0, 5.0),
    n_jobs=None,
    random_state=None,
):
    """
    Get XGBoost model with the best hyperparameters configuration.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.

    y : array-like of shape (n_samples,)
        The target values (real numbers).

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of the base regressor (XGBoost)
        in Hyperopt.

    metric: string, default="neg_mean_squared_error"
        The score of the base regressor (XGBoost) optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    n_estimators : tuple, default=(10, 50, 100)
        The number of XGBoost estimators. The number of estimators of
        XGBoost corresponds to the number of boosting rounds. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).

    max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for XGBoost base learners. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of XGBoost. The learning rate corresponds to the
        step size shrinkage used in update to prevent overfitting. After each
        boosting step, the learning rate shrinks the feature weights to make the boosting
        process more conservative. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).

    booster : ("dart", "gblinear", "gbtree"), default=("gbtree",)
        The type of booster to use. "gbtree" and "dart" use tree based models
        while "gblinear" uses linear functions. The tuple provided is the search space used
        for the hyperparameter optimization (Hyperopt).

    gamma : tuple, default=(0, 1, 10)
        `gamma` of XGBoost. `gamma` corresponds to the minimum loss reduction
        required to make a further partition on a leaf node of the tree.
        The larger `gamma` is, the more conservative XGBoost algorithm will be.
        The tuple provided is the search space used for the hyperparameter optimization
        (Hyperopt).

    min_child_weight : tuple, default=(1, 5, 15, 100)
        `min_child_weight` of XGBoost. `min_child_weight` defines the
        minimum sum of instance weight (hessian) needed in a child. If the tree
        partition step results in a leaf node with the sum of instance weight
        less than `min_child_weight`, then the building process will give up further
        partitioning. The larger `min_child_weight` is, the more conservative XGBoost
        algorithm will be. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    subsample : tuple, default=(1.0,)
        XGBoost subsample ratio of the training instances. Setting it to 0.5 means
        that XGBoost would randomly sample half of the training data prior to
        growing trees, and this will prevent overfitting. Subsampling will occur
        once in every boosting iteration. The tuple provided is the search space used for
        the hyperparameter optimization (Hyperopt).

    colsample_bytree : tuple, default=(1.0,)
        XGBoost subsample ratio of columns when constructing each tree.
        Subsampling occurs once for every tree constructed. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    colsample_bylevel : tuple, default=(1.0,)
        XGBoost subsample ratio of columns for each level. Subsampling occurs
        once for every new depth level reached in a tree. Columns are subsampled
        from the set of columns chosen for the current tree. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    colsample_bynode : tuple, default=(1.0,)
        XGBoost subsample ratio of columns for each node (split). Subsampling
        occurs once every time a new split is evaluated. Columns are subsampled
        from the set of columns chosen for the current level. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    reg_alpha : tuple, default=(0,)
        `reg_alpha` of XGBoost. `reg_alpha` corresponds to the L1 regularization
        term on the weights. Increasing this value will make XGBoost model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` of XGBoost. `reg_lambda` corresponds to the L2 regularization
        term on the weights. Increasing this value will make XGBoost model more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the base learner XGBoost and
        the Hyperopt algorithm.

    Returns
    -------
    model: object
        XGBoost model with the best configuration and fitted on the input data.
    """
    space = {
        "n_estimators": hp.choice("n_estimators", n_estimators),
        "max_depth": hp.choice("max_depth", max_depth),
        "learning_rate": hp.choice("learning_rate", learning_rate),
        "booster": hp.choice("booster", booster),
        "gamma": hp.choice("gamma", gamma),
        "min_child_weight": hp.choice("min_child_weight", min_child_weight),
        "subsample": hp.choice("subsample", subsample),
        "colsample_bytree": hp.choice("colsample_bytree", colsample_bytree),
        "colsample_bylevel": hp.choice("colsample_bylevel", colsample_bylevel),
        "colsample_bynode": hp.choice("colsample_bynode", colsample_bynode),
        "reg_alpha": hp.choice("reg_alpha", reg_alpha),
        "reg_lambda": hp.choice("reg_lambda", reg_lambda),
        "objective": "reg:squarederror",
        "n_jobs": n_jobs,
        "random_state": random_state,
    }

    # Get best configuration
    def p_model(params):
        reg = xgb.XGBRegressor(**params, verbosity=0)
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
        "learning_rate": learning_rate[best_config["learning_rate"]],
        "booster": booster[best_config["booster"]],
        "gamma": gamma[best_config["gamma"]],
        "min_child_weight": min_child_weight[best_config["min_child_weight"]],
        "subsample": subsample[best_config["subsample"]],
        "colsample_bytree": colsample_bytree[best_config["colsample_bytree"]],
        "colsample_bylevel": colsample_bylevel[best_config["colsample_bylevel"]],
        "colsample_bynode": colsample_bynode[best_config["colsample_bynode"]],
        "reg_alpha": reg_alpha[best_config["reg_alpha"]],
        "reg_lambda": reg_lambda[best_config["reg_lambda"]],
        "objective": "reg:squarederror",
        "n_jobs": n_jobs,
        "random_state": random_state,
    }
    reg = xgb.XGBRegressor(**final_params, verbosity=0)
    return reg.fit(X, y)
