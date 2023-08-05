import math
import numbers
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.ensemble import BaggingClassifier, BaggingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from ._lcetree import LCETreeClassifier, LCETreeRegressor


class LCEClassifier(ClassifierMixin, BaseEstimator):
    """
    A **Local Cascade Ensemble (LCE) classifier**. LCEClassifier is **compatible with scikit-learn**;
    it passes the `check_estimator <https://scikit-learn.org/stable/modules/generated/sklearn.utils.estimator_checks.check_estimator.html#sklearn.utils.estimator_checks.check_estimator>`_.
    Therefore, it can interact with scikit-learn pipelines and model selection tools.


    Parameters
    ----------
    n_estimators : int, default=10
        The number of trees in the ensemble.

    bootstrap : bool, default=True
        Whether bootstrap samples are used when building trees. If False, the
        whole dataset is used to build each tree.

    criterion : {"gini", "entropy"}, default="gini"
        The function to measure the quality of a split. Supported criteria are
        "gini" for the Gini impurity and "entropy" for the information gain.

    splitter : {"best", "random"}, default="best"
        The strategy used to choose the split at each node. Supported strategies
        are "best" to choose the best split and "random" to choose the best random
        split.

    max_depth : int, default=2
        The maximum depth of a tree.

    max_features : int, float or {"auto", "sqrt", "log"}, default=None
        The number of features to consider when looking for the best split:

        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a fraction and
          `round(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=sqrt(n_features)`.
        - If "sqrt", then `max_features=sqrt(n_features)` (same as "auto").
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.

        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    max_samples : int or float, default=1.0
        The number of samples to draw from X to train each base estimator
        (with replacement by default, see ``bootstrap`` for more details).

        - If int, then draw `max_samples` samples.
        - If float, then draw `max_samples * X.shape[0]` samples. Thus, `max_samples` should be in the interval `(0.0, 1.0]`.

    min_samples_leaf : int or float, default=1
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.

        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a fraction and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of each node base
        classifier in Hyperopt.

    metric: string, default="accuracy"
        The score of the base classifier optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    base_learner : {"catboost", "lightgbm", "xgboost"}, default="xgboost"
        The base classifier trained in each node of a tree.

    base_n_estimators : tuple, default=(10, 50, 100)
        The number of estimators of the base learner. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).

    base_max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for base learners. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).
        
    base_num_leaves : tuple, default=(20, 50, 100, 500)
        Maximum tree leaves (applicable to LightGBM only). The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of the base learner. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).

    base_booster : ("dart", "gblinear", "gbtree"), default=("gbtree",)
        The type of booster to use (applicable to XGBoost only). "gbtree" and "dart" use tree based models
        while "gblinear" uses linear functions. The tuple provided is the search space used
        for the hyperparameter optimization (Hyperopt).
        
    base_boosting_type : ("dart", "gbdt", "rf"), default=("gbdt",)
        The type of boosting type to use (applicable to LightGBM only): "dart" dropouts meet Multiple Additive 
        Regression Trees; "gbdt" traditional Gradient Boosting Decision Tree; "rf" Random Forest. 
        The tuple provided is the search space used for the hyperparameter optimization (Hyperopt).

    base_gamma : tuple, default=(0, 1, 10)
        `gamma` of XGBoost. `gamma` corresponds to the minimum loss reduction
        required to make a further partition on a leaf node of the tree.
        The larger `gamma` is, the more conservative XGBoost algorithm will be.
        The tuple provided is the search space used for the hyperparameter optimization
        (Hyperopt).

    base_min_child_weight : tuple, default=(1, 5, 15, 100)
        `min_child_weight` of base learner (applicable to LightGBM and XGBoost only). `min_child_weight` defines the
        minimum sum of instance weight (hessian) needed in a child. If the tree
        partition step results in a leaf node with the sum of instance weight
        less than `min_child_weight`, then the building process will give up further
        partitioning. The larger `min_child_weight` is, the more conservative the base learner
        algorithm will be. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    base_subsample : tuple, default=(1.0,)
        Base learner subsample ratio of the training instances (applicable to LightGBM and XGBoost only). 
        Setting it to 0.5 means that the base learner would randomly sample half of the training data prior to
        growing trees, and this will prevent overfitting. Subsampling will occur
        once in every boosting iteration. The tuple provided is the search space used for
        the hyperparameter optimization (Hyperopt).
        
    base_subsample_for_bin : tuple, default=(200000,)
        Number of samples for constructing bins (applicable to LightGBM only). The tuple provided is the
        search space used for the hyperparameter optimization (Hyperopt).

    base_colsample_bytree : tuple, default=(1.0,)
        Base learner subsample ratio of columns when constructing each tree (applicable to LightGBM and XGBoost only).
        Subsampling occurs once for every tree constructed. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_colsample_bylevel : tuple, default=(1.0,)
        Subsample ratio of columns for each level (applicable to CatBoost and XGBoost only). Subsampling occurs
        once for every new depth level reached in a tree. Columns are subsampled
        from the set of columns chosen for the current tree. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_colsample_bynode : tuple, default=(1.0,)
        Subsample ratio of columns for each node split (applicable to XGBoost only). Subsampling
        occurs once every time a new split is evaluated. Columns are subsampled
        from the set of columns chosen for the current level. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_reg_alpha : tuple, default=(0,)
        `reg_alpha` of the base learner (applicable to LightGBM and XGBoost only). 
        `reg_alpha` corresponds to the L1 regularization term on the weights. 
        Increasing this value will make the base learner more conservative. 
        The tuple provided is the search space used for the hyperparameter optimization (Hyperopt).

    base_reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` of the base learner. `reg_lambda` corresponds to the L2 regularization term 
        on the weights. Increasing this value will make the base learner more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the bootstrapping of the samples used
        when building trees (if ``bootstrap=True``), the sampling of the
        features to consider when looking for the best split at each node
        (if ``max_features < n_features``), the base classifier and
        the Hyperopt algorithm.

    verbose : int, default=0
        Controls the verbosity when fitting.

    Attributes
    ----------
    base_estimator_ : LCETreeClassifier
        The child estimator template used to create the collection of fitted
        sub-estimators.

    estimators_ : list of LCETreeClassifier
        The collection of fitted sub-estimators.

    classes_ : ndarray of shape (n_classes,) or a list of such arrays
        The classes labels.

    n_classes_ : int
        The number of classes.

    n_features_in_ : int
        The number of features when ``fit`` is performed.

    encoder_ : LabelEncoder
        The encoder to have target labels with value between 0 and n_classes-1.

    Notes
    -----
    The default values for the parameters controlling the size of the trees
    (e.g. ``max_depth``, ``min_samples_leaf``, etc.) lead to fully grown and
    unpruned trees which can potentially be very large on some data sets. To
    reduce memory consumption, the complexity and size of the trees should be
    controlled by setting those parameter values.

    The features are always randomly permuted at each split. Therefore,
    the best found split may vary, even with the same training data,
    ``max_features=n_features`` and ``bootstrap=False``, if the improvement
    of the criterion is identical for several splits enumerated during the
    search of the best split. To obtain a deterministic behaviour during
    fitting, ``random_state`` has to be fixed.

    References
    ----------
    .. [1] Fauvel, K., E. Fromont, V. Masson, P. Faverdin and A. Termier. "XEM: An Explainable-by-Design Ensemble Method for Multivariate Time Series Classification", Data Mining and Knowledge Discovery, 36(3):917-957, 2022. https://hal.inria.fr/hal-03599214/document
    """

    def __init__(
        self,
        n_estimators=10,
        bootstrap=True,
        criterion="gini",
        splitter="best",
        max_depth=2,
        max_features=None,
        max_samples=1.0,
        min_samples_leaf=1,
        n_iter=10,
        metric="accuracy",
        base_learner="xgboost",
        base_n_estimators=(10, 50, 100),
        base_max_depth=(3, 6, 9),
        base_num_leaves=(20, 50, 100, 500),
        base_learning_rate=(0.01, 0.1, 0.3, 0.5),
        base_booster=("gbtree",),
        base_boosting_type=("gbdt",),
        base_gamma=(0, 1, 10),
        base_min_child_weight=(1, 5, 15, 100),
        base_subsample=(1.0,),
        base_subsample_for_bin=(200000,),
        base_colsample_bytree=(1.0,),
        base_colsample_bylevel=(1.0,),
        base_colsample_bynode=(1.0,),
        base_reg_alpha=(0,),
        base_reg_lambda=(0.1, 1.0, 5.0),
        n_jobs=None,
        random_state=None,
        verbose=0,
    ):
        self.n_estimators = n_estimators
        self.bootstrap = bootstrap
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.max_features = max_features
        self.max_samples = max_samples
        self.min_samples_leaf = min_samples_leaf
        self.n_iter = n_iter
        self.metric = metric
        self.base_learner = base_learner
        self.base_n_estimators = base_n_estimators
        self.base_max_depth = base_max_depth
        self.base_num_leaves = base_num_leaves
        self.base_learning_rate = base_learning_rate
        self.base_booster = base_booster
        self.base_boosting_type = base_boosting_type
        self.base_gamma = base_gamma
        self.base_min_child_weight = base_min_child_weight
        self.base_subsample = base_subsample
        self.base_subsample_for_bin = base_subsample_for_bin
        self.base_colsample_bytree = base_colsample_bytree
        self.base_colsample_bylevel = base_colsample_bylevel
        self.base_colsample_bynode = base_colsample_bynode
        self.base_reg_alpha = base_reg_alpha
        self.base_reg_lambda = base_reg_lambda
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose

    def _generate_estimator(self):
        """Generate an estimator."""
        est = LCETreeClassifier()
        est.n_classes_in = self.n_classes_
        est.criterion = self.criterion
        est.splitter = self.splitter
        est.max_depth = self.max_depth
        est.max_features = self.max_features
        est.min_samples_leaf = self.min_samples_leaf
        est.n_iter = self.n_iter
        est.metric = self.metric
        est.base_learner = self.base_learner
        est.base_n_estimators = self.base_n_estimators
        est.base_max_depth = self.base_max_depth
        est.base_num_leaves = self.base_num_leaves
        est.base_learning_rate = self.base_learning_rate
        est.base_booster = self.base_booster
        est.base_boosting_type = self.base_boosting_type
        est.base_gamma = self.base_gamma
        est.base_min_child_weight = self.base_min_child_weight
        est.base_subsample = self.base_subsample
        est.base_subsample_for_bin = self.base_subsample_for_bin        
        est.base_colsample_bytree = self.base_colsample_bytree        
        est.base_colsample_bylevel = self.base_colsample_bylevel
        est.base_colsample_bynode = self.base_colsample_bynode
        est.base_reg_alpha = self.base_reg_alpha
        est.base_reg_alpha = self.base_reg_lambda
        est.n_jobs = self.n_jobs
        est.random_state = self.random_state
        est.verbose = self.verbose
        return est

    def _more_tags(self):
        """Update scikit-learn estimator tags."""
        return {"allow_nan": True, "requires_y": True}

    def _validate_extra_parameters(self, X):
        """Validate parameters not already validated by methods employed."""
        # Validate max_depth
        if isinstance(self.max_depth, numbers.Integral):
            if not (0 <= self.max_depth):
                raise ValueError(
                    "max_depth must be greater than or equal to 0, "
                    "got {0}.".format(self.max_depth)
                )
        else:
            raise ValueError("max_depth must be int")

        # Validate min_samples_leaf
        if isinstance(self.min_samples_leaf, numbers.Integral):
            if not 1 <= self.min_samples_leaf:
                raise ValueError(
                    "min_samples_leaf must be at least 1 "
                    "or in (0, 0.5], got %s" % self.min_samples_leaf
                )
        elif isinstance(self.min_samples_leaf, float):
            if not 0.0 < self.min_samples_leaf <= 0.5:
                raise ValueError(
                    "min_samples_leaf must be at least 1 "
                    "or in (0, 0.5], got %s" % self.min_samples_leaf
                )
            self.min_samples_leaf = int(math.ceil(self.min_samples_leaf * X.shape[0]))
        else:
            raise ValueError("min_samples_leaf must be int or float")

        # Validate n_iter
        if isinstance(self.n_iter, numbers.Integral):
            if self.n_iter <= 0:
                raise ValueError(
                    "n_iter must be greater than 0, " "got {0}.".format(self.n_iter)
                )
        else:
            raise ValueError("n_iter must be int")

        # Validate verbose
        if isinstance(self.verbose, numbers.Integral):
            if self.verbose < 0:
                raise ValueError(
                    "verbose must be greater than or equal to 0, "
                    "got {0}.".format(self.verbose)
                )
        else:
            raise ValueError("verbose must be int")

    def fit(self, X, y):
        """
        Build a forest of LCE trees from the training set (X, y).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        y : array-like of shape (n_samples,)
            The class labels.

        Returns
        -------
        self : object
        """
        X, y = check_X_y(X, y, force_all_finite="allow-nan")
        check_classification_targets(y)
        self._validate_extra_parameters(X)
        self.n_features_in_ = X.shape[1]
        self.X_ = True
        self.y_ = True
        self.classes_, y = np.unique(y, return_inverse=True)
        self.n_classes_ = self.classes_.size
        self.encoder_ = LabelEncoder()
        self.encoder_.fit(self.classes_)
        self.base_estimator_ = self._generate_estimator()
        self.estimators_ = BaggingClassifier(
            base_estimator=self.base_estimator_,
            n_estimators=self.n_estimators,
            bootstrap=self.bootstrap,
            max_samples=self.max_samples,
            n_jobs=self.n_jobs,
            random_state=self.random_state,
        )
        self.estimators_.fit(X, y)
        return self

    def predict(self, X):
        """
        Predict class for X.
        The predicted class of an input sample is computed as the class with
        the highest mean predicted probability.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted classes.
        """
        check_is_fitted(self, ["X_", "y_"])
        X = check_array(X, force_all_finite="allow-nan")
        predictions = self.estimators_.predict(X)
        return self.encoder_.inverse_transform(predictions)

    def predict_proba(self, X):
        """
        Predict class probabilities for X.
        The predicted class probabilities of an input sample are computed as
        the mean predicted class probabilities of the base estimators in the
        ensemble.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute ``classes_``.
        """
        check_is_fitted(self, ["X_", "y_"])
        X = check_array(X, force_all_finite="allow-nan")
        return self.estimators_.predict_proba(X)

    def set_params(self, **params):
        """
        Set the parameters of the estimator.

        Parameters
        ----------
        **params : dict
            Estimator parameters.

        Returns
        -------
        self : object
        """
        if not params:
            return self

        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self


class LCERegressor(RegressorMixin, BaseEstimator):
    """
    A **Local Cascade Ensemble (LCE) regressor**. LCERegressor is **compatible with scikit-learn**;
    it passes the `check_estimator <https://scikit-learn.org/stable/modules/generated/sklearn.utils.estimator_checks.check_estimator.html#sklearn.utils.estimator_checks.check_estimator>`_.
    Therefore, it can interact with scikit-learn pipelines and model selection tools.


    Parameters
    ----------
    n_estimators : int, default=10
        The number of trees in the ensemble.

    bootstrap : bool, default=True
        Whether bootstrap samples are used when building trees. If False, the
        whole dataset is used to build each tree.

    criterion : {"squared_error", "friedman_mse", "absolute_error", "poisson"}, default="squared_error"
        The function to measure the quality of a split. Supported criteria are "squared_error" for
        the mean squared error, which is equal to variance reduction as feature selection
        criterion and minimizes the L2 loss using the mean of each terminal node,
        "friedman_mse", which uses mean squared error with Friedman's improvement score
        for potential splits, "absolute_error" for the mean absolute error, which
        minimizes the L1 loss using the median of each terminal node, and "poisson"
        which uses reduction in Poisson deviance to find splits.

    splitter : {"best", "random"}, default="best"
        The strategy used to choose the split at each node. Supported strategies
        are "best" to choose the best split and "random" to choose the best random
        split.

    max_depth : int, default=2
        The maximum depth of a tree.

    max_features : int, float or {"auto", "sqrt", "log"}, default=None
        The number of features to consider when looking for the best split:

        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a fraction and
          `round(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=sqrt(n_features)`.
        - If "sqrt", then `max_features=sqrt(n_features)` (same as "auto").
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.

        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    max_samples : int or float, default=1.0
        The number of samples to draw from X to train each base estimator
        (with replacement by default, see ``bootstrap`` for more details).

        - If int, then draw `max_samples` samples.
        - If float, then draw `max_samples * X.shape[0]` samples. Thus, `max_samples` should be in the interval `(0.0, 1.0]`.

    min_samples_leaf : int or float, default=1
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.

        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a fraction and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.

    n_iter: int, default=10
        Number of iterations to set the hyperparameters of each node base
        regressor in Hyperopt.

    metric: string, default="neg_mean_squared_error"
        The score of the base regressor optimized by Hyperopt. Supported metrics
        are the ones from `scikit-learn <https://scikit-learn.org/stable/modules/model_evaluation.html>`_.

    base_learner : {"catboost", "lightgbm", "xgboost"}, default="xgboost"
        The base classifier trained in each node of a tree.

    base_n_estimators : tuple, default=(10, 50, 100)
        The number of estimators of the base learner. The tuple provided is
        the search space used for the hyperparameter optimization (Hyperopt).

    base_max_depth : tuple, default=(3, 6, 9)
        Maximum tree depth for base learners. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).
        
    base_num_leaves : tuple, default=(20, 50, 100, 500)
        Maximum tree leaves (applicable to LightGBM only). The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_learning_rate : tuple, default=(0.01, 0.1, 0.3, 0.5)
        `learning_rate` of the base learner. The tuple provided is the search space used for the
        hyperparameter optimization (Hyperopt).

    base_booster : ("dart", "gblinear", "gbtree"), default=("gbtree",)
        The type of booster to use (applicable to XGBoost only). "gbtree" and "dart" use tree based models
        while "gblinear" uses linear functions. The tuple provided is the search space used
        for the hyperparameter optimization (Hyperopt).
        
    base_boosting_type : ("dart", "gbdt", "rf"), default=("gbdt",)
        The type of boosting type to use (applicable to LightGBM only): "dart" dropouts meet Multiple Additive 
        Regression Trees; "gbdt" traditional Gradient Boosting Decision Tree; "rf" Random Forest. 
        The tuple provided is the search space used for the hyperparameter optimization (Hyperopt).

    base_gamma : tuple, default=(0, 1, 10)
        `gamma` of XGBoost. `gamma` corresponds to the minimum loss reduction
        required to make a further partition on a leaf node of the tree.
        The larger `gamma` is, the more conservative XGBoost algorithm will be.
        The tuple provided is the search space used for the hyperparameter optimization
        (Hyperopt).

    base_min_child_weight : tuple, default=(1, 5, 15, 100)
        `min_child_weight` of base learner (applicable to LightGBM and XGBoost only). `min_child_weight` defines the
        minimum sum of instance weight (hessian) needed in a child. If the tree
        partition step results in a leaf node with the sum of instance weight
        less than `min_child_weight`, then the building process will give up further
        partitioning. The larger `min_child_weight` is, the more conservative the base learner
        algorithm will be. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    base_subsample : tuple, default=(1.0,)
        Base learner subsample ratio of the training instances (applicable to LightGBM and XGBoost only). 
        Setting it to 0.5 means that the base learner would randomly sample half of the training data prior to
        growing trees, and this will prevent overfitting. Subsampling will occur
        once in every boosting iteration. The tuple provided is the search space used for
        the hyperparameter optimization (Hyperopt).
        
    base_subsample_for_bin : tuple, default=(200000,)
        Number of samples for constructing bins (applicable to LightGBM only). The tuple provided is the
        search space used for the hyperparameter optimization (Hyperopt).

    base_colsample_bytree : tuple, default=(1.0,)
        Base learner subsample ratio of columns when constructing each tree (applicable to LightGBM and XGBoost only).
        Subsampling occurs once for every tree constructed. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_colsample_bylevel : tuple, default=(1.0,)
        Subsample ratio of columns for each level (applicable to CatBoost and XGBoost only). Subsampling occurs
        once for every new depth level reached in a tree. Columns are subsampled
        from the set of columns chosen for the current tree. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_colsample_bynode : tuple, default=(1.0,)
        Subsample ratio of columns for each node split (applicable to XGBoost only). Subsampling
        occurs once every time a new split is evaluated. Columns are subsampled
        from the set of columns chosen for the current level. The tuple provided is the search
        space used for the hyperparameter optimization (Hyperopt).

    base_reg_alpha : tuple, default=(0,)
        `reg_alpha` of the base learner (applicable to LightGBM and XGBoost only). 
        `reg_alpha` corresponds to the L1 regularization term on the weights. 
        Increasing this value will make the base learner more conservative. 
        The tuple provided is the search space used for the hyperparameter optimization (Hyperopt).

    base_reg_lambda : tuple, default=(0.1, 1.0, 5.0)
        `reg_lambda` of the base learner. `reg_lambda` corresponds to the L2 regularization term 
        on the weights. Increasing this value will make the base learner more
        conservative. The tuple provided is the search space used for the hyperparameter
        optimization (Hyperopt).

    n_jobs : int, default=None
        The number of jobs to run in parallel.
        ``n_jobs=None`` means 1. ``n_jobs=-1`` means using all processors.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the bootstrapping of the samples used
        when building trees (if ``bootstrap=True``), the sampling of the
        features to consider when looking for the best split at each node
        (if ``max_features < n_features``), the base classifier (XGBoost) and
        the Hyperopt algorithm.

    verbose : int, default=0
        Controls the verbosity when fitting.

    Attributes
    ----------
    base_estimator_ : LCETreeRegressor
        The child estimator template used to create the collection of fitted
        sub-estimators.

    estimators_ : list of LCETreeRegressor
        The collection of fitted sub-estimators.

    n_features_in_ : int
        The number of features when ``fit`` is performed.

    Notes
    -----
    The default values for the parameters controlling the size of the trees
    (e.g. ``max_depth``, ``min_samples_leaf``, etc.) lead to fully grown and
    unpruned trees which can potentially be very large on some data sets. To
    reduce memory consumption, the complexity and size of the trees should be
    controlled by setting those parameter values.

    The features are always randomly permuted at each split. Therefore,
    the best found split may vary, even with the same training data,
    ``max_features=n_features`` and ``bootstrap=False``, if the improvement
    of the criterion is identical for several splits enumerated during the
    search of the best split. To obtain a deterministic behaviour during
    fitting, ``random_state`` has to be fixed.
    """

    def __init__(
        self,
        n_estimators=10,
        bootstrap=True,
        criterion="squared_error",
        splitter="best",
        max_depth=2,
        max_features=None,
        max_samples=1.0,
        min_samples_leaf=1,
        metric="neg_mean_squared_error",
        n_iter=10,
        base_learner="xgboost",
        base_n_estimators=(10, 50, 100),
        base_max_depth=(3, 6, 9),
        base_num_leaves=(20, 50, 100, 500),
        base_learning_rate=(0.01, 0.1, 0.3, 0.5),
        base_booster=("gbtree",),
        base_boosting_type=("gbdt",),
        base_gamma=(0, 1, 10),
        base_min_child_weight=(1, 5, 15, 100),
        base_subsample=(1.0,),
        base_subsample_for_bin=(200000,),
        base_colsample_bytree=(1.0,),
        base_colsample_bylevel=(1.0,),
        base_colsample_bynode=(1.0,),
        base_reg_alpha=(0,),
        base_reg_lambda=(0.1, 1.0, 5.0),
        n_jobs=None,
        random_state=None,
        verbose=0,
    ):
        self.n_estimators = n_estimators
        self.bootstrap = bootstrap
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.max_features = max_features
        self.max_samples = max_samples
        self.min_samples_leaf = min_samples_leaf
        self.n_iter = n_iter
        self.metric = metric
        self.base_learner = base_learner
        self.base_n_estimators = base_n_estimators
        self.base_max_depth = base_max_depth
        self.base_num_leaves = base_num_leaves
        self.base_learning_rate = base_learning_rate
        self.base_booster = base_booster
        self.base_boosting_type = base_boosting_type
        self.base_gamma = base_gamma
        self.base_min_child_weight = base_min_child_weight
        self.base_subsample = base_subsample
        self.base_subsample_for_bin = base_subsample_for_bin
        self.base_colsample_bytree = base_colsample_bytree
        self.base_colsample_bylevel = base_colsample_bylevel
        self.base_colsample_bynode = base_colsample_bynode
        self.base_reg_alpha = base_reg_alpha
        self.base_reg_lambda = base_reg_lambda
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose

    def _generate_estimator(self):
        """Generate an estimator."""
        est = LCETreeRegressor()
        est.criterion = self.criterion
        est.splitter = self.splitter
        est.max_depth = self.max_depth
        est.max_features = self.max_features
        est.min_samples_leaf = self.min_samples_leaf
        est.n_iter = self.n_iter
        est.metric = self.metric
        est.base_learner = self.base_learner
        est.base_n_estimators = self.base_n_estimators
        est.base_max_depth = self.base_max_depth
        est.base_num_leaves = self.base_num_leaves
        est.base_learning_rate = self.base_learning_rate
        est.base_booster = self.base_booster
        est.base_boosting_type = self.base_boosting_type
        est.base_gamma = self.base_gamma
        est.base_min_child_weight = self.base_min_child_weight
        est.base_subsample = self.base_subsample
        est.base_subsample_for_bin = self.base_subsample_for_bin        
        est.base_colsample_bytree = self.base_colsample_bytree        
        est.base_colsample_bylevel = self.base_colsample_bylevel
        est.base_colsample_bynode = self.base_colsample_bynode
        est.base_reg_alpha = self.base_reg_alpha
        est.base_reg_alpha = self.base_reg_lambda
        est.n_jobs = self.n_jobs
        est.random_state = self.random_state
        est.verbose = self.verbose
        return est

    def _more_tags(self):
        """Update scikit-learn estimator tags."""
        return {"allow_nan": True, "requires_y": True}

    def _validate_extra_parameters(self, X):
        """Validate parameters not already validated by methods employed."""
        # Validate max_depth
        if isinstance(self.max_depth, numbers.Integral):
            if not (0 <= self.max_depth):
                raise ValueError(
                    "max_depth must be greater than or equal to 0, "
                    "got {0}.".format(self.max_depth)
                )
        else:
            raise ValueError("max_depth must be int")

        # Validate min_samples_leaf
        if isinstance(self.min_samples_leaf, numbers.Integral):
            if not 1 <= self.min_samples_leaf:
                raise ValueError(
                    "min_samples_leaf must be at least 1 "
                    "or in (0, 0.5], got %s" % self.min_samples_leaf
                )
        elif isinstance(self.min_samples_leaf, float):
            if not 0.0 < self.min_samples_leaf <= 0.5:
                raise ValueError(
                    "min_samples_leaf must be at least 1 "
                    "or in (0, 0.5], got %s" % self.min_samples_leaf
                )
            self.min_samples_leaf = int(math.ceil(self.min_samples_leaf * X.shape[0]))
        else:
            raise ValueError("min_samples_leaf must be int or float")

        # Validate n_iter
        if isinstance(self.n_iter, numbers.Integral):
            if self.n_iter <= 0:
                raise ValueError(
                    "n_iter must be greater than 0, " "got {0}.".format(self.n_iter)
                )
        else:
            raise ValueError("n_iter must be int")

        # Validate verbose
        if isinstance(self.verbose, numbers.Integral):
            if self.verbose < 0:
                raise ValueError(
                    "verbose must be greater than or equal to 0, "
                    "got {0}.".format(self.verbose)
                )
        else:
            raise ValueError("verbose must be int")

    def fit(self, X, y):
        """
        Build a forest of LCE trees from the training set (X, y).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        y : array-like of shape (n_samples,)
            The target values (real numbers).

        Returns
        -------
        self : object
        """
        X, y = check_X_y(X, y, y_numeric=True, force_all_finite="allow-nan")
        self._validate_extra_parameters(X)
        self.n_features_in_ = X.shape[1]
        self.X_ = True
        self.y_ = True
        self.base_estimator_ = self._generate_estimator()
        self.estimators_ = BaggingRegressor(
            base_estimator=self.base_estimator_,
            n_estimators=self.n_estimators,
            bootstrap=self.bootstrap,
            max_samples=self.max_samples,
            n_jobs=self.n_jobs,
            random_state=self.random_state,
        )
        self.estimators_.fit(X, y)
        return self

    def predict(self, X):
        """
        Predict regression target for X.
        The predicted regression target of an input sample is computed as the
        mean predicted regression targets of the trees in the forest.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted values.
        """
        check_is_fitted(self, ["X_", "y_"])
        X = check_array(X, force_all_finite="allow-nan")
        return self.estimators_.predict(X)

    def set_params(self, **params):
        """
        Set the parameters of the estimator.

        Parameters
        ----------
        **params : dict
            Estimator parameters.

        Returns
        -------
        self : object
        """
        if not params:
            return self

        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self
