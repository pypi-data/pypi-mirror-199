import numpy as np
from joblib import delayed, Parallel
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from ._catboost import catboost_opt_classifier, catboost_opt_regressor
from ._lightgbm import lgbm_opt_classifier, lgbm_opt_regressor
from ._xgboost import xgb_opt_classifier, xgb_opt_regressor



class LCETreeClassifier(ClassifierMixin, BaseEstimator):
    """
    A LCE Tree classifier.


    Parameters
    ----------
    n_classes_in : int, default=None
        The number of classes from the input data.

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
        The score of the base classifier (XGBoost) optimized by Hyperopt. Supported metrics
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
        Controls the randomness of the sampling of the features to consider when
        looking for the best split at each node (if ``max_features < n_features``),
        the base learner and the Hyperopt algorithm.

    verbose : int, default=0
        Controls the verbosity when fitting.

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,) or a list of such arrays
        The classes labels.

    n_features_in_ : int
        The number of features when ``fit`` is performed.
    """

    def __init__(
        self,
        n_classes_in=None,
        criterion="gini",
        splitter="best",
        max_depth=2,
        max_features=None,
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
        self.n_classes_in = n_classes_in
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.max_features = max_features
        self.min_samples_leaf = min_samples_leaf
        self.n_iter = n_iter
        self.metric = metric
        self.base_learner = base_learner
        self.base_n_estimators = base_n_estimators
        self.base_max_depth = base_max_depth
        self.base_num_leaves=base_num_leaves
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

    def fit(self, X, y):
        """
        Build a LCE tree from the training set (X, y).

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
        self.classes_ = np.unique(y)
        self.n_features_in_ = X.shape[1]
        base_dict = {"catboost": catboost_opt_classifier, 
                     "lightgbm": lgbm_opt_classifier, 
                     "xgboost": xgb_opt_classifier}
        
        def _build_tree(X, y):
            """Build a LCE tree."""
            global index_node_global

            def _create_node(X, y, depth, container):
                """Create a node in the tree."""
                y_unique = np.unique(y)
                y_unique_size = y_unique.size
                
                if y_unique_size > 1:                
                    # Add base learner predictions as features to the dataset
                    if self.base_learner=="catboost":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            colsample_bylevel=self.base_colsample_bylevel,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    elif self.base_learner=="lightgbm":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            num_leaves=self.base_num_leaves,
                            learning_rate=self.base_learning_rate,
                            boosting_type=self.base_boosting_type,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            subsample_for_bin=self.base_subsample_for_bin,
                            colsample_bytree=self.base_colsample_bytree,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    else:
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            booster=self.base_booster,
                            gamma=self.base_gamma,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            colsample_bytree=self.base_colsample_bytree,
                            colsample_bylevel=self.base_colsample_bylevel,
                            colsample_bynode=self.base_colsample_bynode,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    pred_proba = np.around(model_node.predict_proba(X), 6)

                c = 0
                X = np.concatenate(
                    [X, np.zeros((X.shape[0], self.n_classes_in))], axis=1
                )
                for i in range(0, self.n_classes_in):
                    if i in y:
                        if y_unique_size == 1:
                            model_node = None
                            X[:, -self.n_classes_in + i] = 1
                        else:
                            X[:, -self.n_classes_in + i] = pred_proba[:, c]
                            c += 1

                # Split
                if y.size > 1:
                    split = DecisionTreeClassifier(
                        criterion=self.criterion,
                        splitter=self.splitter,
                        max_depth=1,
                        max_features=self.max_features,
                        random_state=self.random_state,
                    )
                    split.fit(X, y)
                else:
                    split = None

                # Node information
                node = {
                    "index": container["index_node_global"],
                    "model": model_node,
                    "data": (X, y),
                    "classes_in": y_unique,
                    "num_classes": self.n_classes_in,
                    "split": split,
                    "missing": {"missing": None, "missing_only": None},
                    "missing_side": None,
                    "children": {"left": None, "right": None},
                    "depth": depth,
                }
                container["index_node_global"] += 1
                return node

            def _splitter(node):
                """Perform the split of a node."""
                # Extract data
                X, y = node["data"]
                depth = node["depth"]
                split = node["split"]

                did_split = False
                data = None

                # Perform split if the conditions are met
                stopping_criteria = [
                    depth >= 0,
                    depth < self.max_depth,
                    np.unique(y).size > 1,
                ]

                if all(stopping_criteria):
                    leafs = split.apply(X)
                    leafs_left = leafs == 1
                    leafs_right = np.invert(leafs_left)

                    (X_left, y_left), (X_right, y_right) = (
                        X[leafs_left],
                        y[leafs_left],
                    ), (
                        X[leafs_right],
                        y[leafs_right],
                    )

                    N_left, N_right = y_left.size, y_right.size

                    split_conditions = [
                        N_left >= self.min_samples_leaf,
                        N_right >= self.min_samples_leaf,
                    ]

                    if all(split_conditions):
                        did_split = True
                        data = [(X_left, y_left), (X_right, y_right)]

                result = {"did_split": did_split, "data": data}
                return result

            def _split_traverse_node(node, container):
                """Process splitting results and continue with child nodes."""
                # Perform split and collect result
                result = _splitter(node)

                # Return terminal node if no split
                if not result["did_split"]:
                    if self.verbose > 0 and self.n_jobs == None:
                        depth_spacing_str = " ".join([" "] * node["depth"])
                        print(
                            " {}*leaf {} @ depth {}: Unique_y {},  N_samples {}".format(
                                depth_spacing_str,
                                node["index"],
                                node["depth"],
                                np.unique(node["data"][1]),
                                np.unique(node["data"][1], return_counts=True)[1],
                            )
                        )
                    return
                del node["data"]

                # Extract splitting results
                (X_left, y_left), (X_right, y_right) = result["data"]

                # Report created node to user
                if self.verbose > 0 and self.n_jobs == None:
                    depth_spacing_str = " ".join([" "] * node["depth"])
                    print(
                        " {}node {} @ depth {}: dataset={}, N_left={}, N_right={}".format(
                            depth_spacing_str,
                            node["index"],
                            node["depth"],
                            (X_left.shape[0] + X_right.shape[0], X_left.shape[1]),
                            X_left.shape[0],
                            X_right.shape[0],
                        )
                    )

                # Create child nodes
                node["children"]["left"] = _create_node(
                    X_left, y_left, node["depth"] + 1, container
                )
                node["children"]["right"] = _create_node(
                    X_right, y_right, node["depth"] + 1, container
                )

                # Split nodes
                _split_traverse_node(node["children"]["left"], container)
                _split_traverse_node(node["children"]["right"], container)

            container = {"index_node_global": 0}
            if self.verbose > 0 and self.n_jobs == None:
                print("\nNew Tree")
            root = _create_node(X, y, 0, container)
            Parallel(n_jobs=self.n_jobs, prefer="threads")(
                delayed(_split_traverse_node)(root, container) for _ in range(1)
            )
            return root

        def _build_tree_missing(X, y):
            """Build a LCE tree with missing data."""
            global index_node_global

            def _create_node_missing(X, y, depth, container):
                """Create a node in the tree."""
                y_unique = np.unique(y)
                y_unique_size = y_unique.size
                
                if y_unique_size > 1:                
                    # Add base learner predictions as features to the dataset
                    if self.base_learner=="catboost":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            colsample_bylevel=self.base_colsample_bylevel,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    elif self.base_learner=="lightgbm":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            num_leaves=self.base_num_leaves,
                            learning_rate=self.base_learning_rate,
                            boosting_type=self.base_boosting_type,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            subsample_for_bin=self.base_subsample_for_bin,
                            colsample_bytree=self.base_colsample_bytree,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    else:
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            booster=self.base_booster,
                            gamma=self.base_gamma,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            colsample_bytree=self.base_colsample_bytree,
                            colsample_bylevel=self.base_colsample_bylevel,
                            colsample_bynode=self.base_colsample_bynode,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    pred_proba = np.around(model_node.predict_proba(X), 6)

                c = 0
                X = np.concatenate(
                    [X, np.zeros((X.shape[0], self.n_classes_in))], axis=1
                )
                y_unique = np.unique(y)
                y_unique_size = y_unique.size
                for i in range(0, self.n_classes_in):
                    if i in y:
                        if y_unique_size == 1:
                            model_node = None
                            X[:, -self.n_classes_in + i] = 1
                        else:
                            X[:, -self.n_classes_in + i] = pred_proba[:, c]
                            c += 1

                # Missing data information
                nans = np.isnan(X).any(axis=1)
                num_nans = nans.sum()
                y_size = y.size
                if num_nans > 0:
                    missing = True
                    if num_nans == y_size:
                        missing_only = True
                    else:
                        missing_only = False
                else:
                    missing = False
                    missing_only = False

                # Split
                split_val_conditions = [y_size > 1, missing_only == False]
                if all(split_val_conditions):
                    split = DecisionTreeClassifier(
                        criterion=self.criterion,
                        splitter=self.splitter,
                        max_depth=1,
                        max_features=self.max_features,
                        random_state=self.random_state,
                    )
                    if missing:
                        split.fit(X[~nans], y[~nans])
                    else:
                        split.fit(X, y)
                else:
                    split = None

                # Node information
                node = {
                    "index": container["index_node_global"],
                    "model": model_node,
                    "data": (X, y),
                    "classes_in": y_unique,
                    "num_classes": self.n_classes_in,
                    "split": split,
                    "missing": {"missing": missing, "missing_only": missing_only},
                    "missing_side": None,
                    "children": {"left": None, "right": None},
                    "depth": depth,
                }
                container["index_node_global"] += 1
                return node

            def _splitter_missing(node):
                """Perform the split of a node."""
                # Extract data
                X, y = node["data"]
                depth = node["depth"]
                split = node["split"]
                missing = node["missing"]["missing"]
                missing_only = node["missing"]["missing_only"]

                did_split = False
                data = None

                # Perform split if the conditions are met
                stopping_criteria = [
                    depth >= 0,
                    depth < self.max_depth,
                    np.unique(y).size > 1,
                    missing_only == False,
                ]

                if all(stopping_criteria):
                    if missing:
                        nans = np.isnan(X).any(axis=1)
                        X_withoutnans, y_withoutnans = X[~nans], y[~nans]
                        leafs = split.apply(X_withoutnans)
                        leafs_left = leafs == 1
                        leafs_right = np.invert(leafs_left)
                        (X_left, y_left), (X_right, y_right) = (
                            X_withoutnans[leafs_left, :],
                            y_withoutnans[leafs_left],
                        ), (
                            X_withoutnans[leafs_right, :],
                            y_withoutnans[leafs_right],
                        )
                    else:
                        leafs = split.apply(X)
                        leafs_left = leafs == 1
                        leafs_right = np.invert(leafs_left)

                        (X_left, y_left), (X_right, y_right) = (
                            X[leafs_left, :],
                            y[leafs_left],
                        ), (
                            X[leafs_right, :],
                            y[leafs_right],
                        )

                    N_left, N_right = y_left.size, y_right.size

                    split_conditions = [
                        N_left >= self.min_samples_leaf,
                        N_right >= self.min_samples_leaf,
                    ]

                    if all(split_conditions):
                        did_split = True

                        if N_left == 1:
                            node["missing_side"] = "left"
                            if missing:
                                X_left = np.concatenate([X_left, X[nans]], axis=0)
                                y_left = np.concatenate([y_left, y[nans]], axis=0)

                        if N_right == 1:
                            if N_left > 1:
                                node["missing_side"] = "right"
                                if missing:
                                    X_right = np.concatenate([X_right, X[nans]], axis=0)
                                    y_right = np.concatenate([y_right, y[nans]], axis=0)

                        score_conditions = [N_left > 1, N_right > 1]
                        if all(score_conditions):
                            if split.score(X_left, y_left) > split.score(
                                X_right, y_right
                            ):
                                node["missing_side"] = "left"
                                if missing:
                                    X_left = np.concatenate([X_left, X[nans]], axis=0)
                                    y_left = np.concatenate([y_left, y[nans]], axis=0)
                            else:
                                node["missing_side"] = "right"
                                if missing:
                                    X_right = np.concatenate([X_right, X[nans]], axis=0)
                                    y_right = np.concatenate([y_right, y[nans]], axis=0)

                        data = [(X_left, y_left), (X_right, y_right)]

                result = {"did_split": did_split, "data": data}
                return result

            def _split_traverse_node_missing(node, container):
                """Process splitting results and continue with child nodes."""
                # Perform split and collect result
                result = _splitter_missing(node)

                # Return terminal node if no split
                if not result["did_split"]:
                    if self.verbose > 0 and self.n_jobs == None:
                        depth_spacing_str = " ".join([" "] * node["depth"])
                        print(
                            " {}*leaf {} @ depth {}: Unique_y {},  N_samples {}".format(
                                depth_spacing_str,
                                node["index"],
                                node["depth"],
                                np.unique(node["data"][1]),
                                np.unique(node["data"][1], return_counts=True)[1],
                            )
                        )
                    return
                del node["data"]

                # Extract splitting results
                (X_left, y_left), (X_right, y_right) = result["data"]

                # Report created node to user
                if self.verbose > 0 and self.n_jobs == None:
                    depth_spacing_str = " ".join([" "] * node["depth"])
                    print(
                        " {}node {} @ depth {}: dataset={}, N_left={}, N_right={}".format(
                            depth_spacing_str,
                            node["index"],
                            node["depth"],
                            (X_left.shape[0] + X_right.shape[0], X_left.shape[1]),
                            X_left.shape[0],
                            X_right.shape[0],
                        )
                    )

                # Create child nodes
                node["children"]["left"] = _create_node_missing(
                    X_left, y_left, node["depth"] + 1, container
                )
                node["children"]["right"] = _create_node_missing(
                    X_right, y_right, node["depth"] + 1, container
                )

                # Split nodes
                _split_traverse_node_missing(node["children"]["left"], container)
                _split_traverse_node_missing(node["children"]["right"], container)

            container = {"index_node_global": 0}
            if self.verbose > 0 and self.n_jobs == None:
                print("\nNew Tree")
            root = _create_node_missing(X, y, 0, container)
            Parallel(n_jobs=self.n_jobs, prefer="threads")(
                delayed(_split_traverse_node_missing)(root, container) for _ in range(1)
            )
            return root

        if np.isnan(X).any():
            self.tree = _build_tree_missing(X, y)
        else:
            self.tree = _build_tree(X, y)
        return self

    def predict_proba(self, X):
        """
        Predict class probabilities for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The class probabilities of the input samples.
        """

        def _base_proba(node, X):
            y_unique_size = node["classes_in"].size
            
            if y_unique_size > 1:
                y_pred = np.around(node["model"].predict_proba(X[:, 1:]), 6)
            
            c = 0
            X = np.concatenate([X, np.zeros((X.shape[0], node["num_classes"]))], axis=1)
            for i in range(0, node["num_classes"]):
                if i in node["classes_in"]:
                    if y_unique_size == 1:
                        X[:, -node["num_classes"] + i] = 1
                    else:
                        X[:, -node["num_classes"] + i] = y_pred[:, c]
                        c += 1
            return X

        def _predict_proba(node, X, y_pred_final=None):
            X = _base_proba(node, X)

            no_children = (
                node["children"]["left"] is None and node["children"]["right"] is None
            )
            if no_children:
                y_pred = np.column_stack((X[:, :1], X[:, -node["num_classes"] :]))
                if y_pred_final is not None:
                    y_pred_final = np.concatenate((y_pred_final, y_pred), axis=0)
                else:
                    y_pred_final = y_pred
                return y_pred_final

            else:
                leafs = node["split"].apply(X[:, 1:])
                leafs_left = leafs == 1
                leafs_right = np.invert(leafs_left)

                X_left, X_right = X[leafs_left, :], X[leafs_right, :]

                if len(X_left) > 0:
                    y_pred_final = _predict_proba(
                        node["children"]["left"], X_left, y_pred_final
                    )
                if len(X_right) > 0:
                    y_pred_final = _predict_proba(
                        node["children"]["right"], X_right, y_pred_final
                    )
                return y_pred_final

        def _predict_proba_missing(node, X, y_pred_final=None):
            X = _base_proba(node, X)

            no_children = (
                node["children"]["left"] is None and node["children"]["right"] is None
            )
            if no_children:
                y_pred = np.column_stack((X[:, :1], X[:, -node["num_classes"] :]))
                if y_pred_final is not None:
                    y_pred_final = np.concatenate((y_pred_final, y_pred), axis=0)
                else:
                    y_pred_final = y_pred
                return y_pred_final

            else:
                nans = np.isnan(X).any(axis=1)
                if nans.sum() > 0:
                    leafs = node["split"].apply(X[~nans, 1:])
                    leafs_left = leafs == 1
                    leafs_right = np.invert(leafs_left)

                    X_left, X_right = X[~nans][leafs_left, :], X[~nans][leafs_right, :]

                    if node["missing_side"] == "left":
                        X_left, X_right = (
                            np.concatenate((X_left, X[nans]), axis=0),
                            X_right,
                        )
                    else:
                        X_left, X_right = X_left, np.concatenate(
                            (X_right, X[nans]), axis=0
                        )
                else:
                    leafs = node["split"].apply(X[:, 1:])
                    leafs_left = leafs == 1
                    leafs_right = np.invert(leafs_left)

                    X_left, X_right = X[leafs_left, :], X[leafs_right, :]

                if len(X_left) > 0:
                    y_pred_final = _predict_proba_missing(
                        node["children"]["left"], X_left, y_pred_final
                    )
                if len(X_right) > 0:
                    y_pred_final = _predict_proba_missing(
                        node["children"]["right"], X_right, y_pred_final
                    )
                return y_pred_final

        index = np.arange(0, X.shape[0]).reshape(-1, 1)
        X = np.concatenate((index, X), axis=1)
        if np.isnan(X).any():
            y_pred = _predict_proba_missing(self.tree, X, None)
        else:
            y_pred = _predict_proba(self.tree, X, None)
        y_pred = y_pred[y_pred[:, 0].argsort()]
        y_pred = y_pred[:, 1:]
        return y_pred

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


class LCETreeRegressor(RegressorMixin, BaseEstimator):
    """
    A LCE Tree regressor.


    Parameters
    ----------
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
        Controls the randomness of the sampling of the features to consider when
        looking for the best split at each node (if ``max_features < n_features``),
        the base classifier (XGBoost) and the Hyperopt algorithm.

    verbose : int, default=0
        Controls the verbosity when fitting.

    Attributes
    ----------
    n_features_in_ : int
        The number of features when ``fit`` is performed.
    """

    def __init__(
        self,
        criterion="squared_error",
        splitter="best",
        max_depth=2,
        max_features=None,
        min_samples_leaf=1,
        n_iter=10,
        metric="neg_mean_squared_error",
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
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.max_features = max_features
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

    def fit(self, X, y):
        """
        Build a LCE tree from the training set (X, y).

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
        self.n_features_in_ = X.shape[1]
        base_dict = {"catboost": catboost_opt_regressor, 
                     "lightgbm": lgbm_opt_regressor, 
                     "xgboost": xgb_opt_regressor}

        def _build_tree(X, y):
            """Build a LCE tree."""
            global index_node_global

            def _create_node(X, y, depth, container):
                """Create a node in the tree."""
                y_unique = np.unique(y)
                y_unique_size = y_unique.size
                
                # Add base learner predictions as features to the dataset
                if y_unique_size > 1:
                    if self.base_learner=="catboost":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            colsample_bylevel=self.base_colsample_bylevel,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    elif self.base_learner=="lightgbm":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            num_leaves=self.base_num_leaves,
                            learning_rate=self.base_learning_rate,
                            boosting_type=self.base_boosting_type,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            subsample_for_bin=self.base_subsample_for_bin,
                            colsample_bytree=self.base_colsample_bytree,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    else:
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            booster=self.base_booster,
                            gamma=self.base_gamma,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            colsample_bytree=self.base_colsample_bytree,
                            colsample_bylevel=self.base_colsample_bylevel,
                            colsample_bynode=self.base_colsample_bynode,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    preds = np.around(model_node.predict(X), 6)
                    X = np.column_stack((X, preds))
                    
                    split = DecisionTreeRegressor(
                        criterion=self.criterion,
                        splitter=self.splitter,
                        max_depth=1,
                        max_features=self.max_features,
                        random_state=self.random_state,
                    )
                    split.fit(X, y)
                    
                else:
                    model_node = None
                    X = np.column_stack((X, y))
                    split = None

                # Node information
                node = {
                    "index": container["index_node_global"],
                    "model": model_node,
                    "data": (X, y),
                    "y_unique_size": y_unique_size,
                    "split": split,
                    "missing": {"missing": None, "missing_only": None},
                    "missing_side": None,
                    "children": {"left": None, "right": None},
                    "depth": depth,
                }
                container["index_node_global"] += 1
                return node

            def _splitter(node):
                """Perform the split of a node."""
                # Extract data
                X, y = node["data"]
                depth = node["depth"]
                split = node["split"]

                did_split = False
                data = None

                # Perform split if the conditions are met
                stopping_criteria = [
                    depth >= 0,
                    depth < self.max_depth,
                    np.unique(y).size > 1,
                ]

                if all(stopping_criteria):
                    leafs = split.apply(X)
                    leafs_left = leafs == 1
                    leafs_right = np.invert(leafs_left)
                    (X_left, y_left), (X_right, y_right) = (
                        X[leafs_left, :],
                        y[leafs_left],
                    ), (
                        X[leafs_right, :],
                        y[leafs_right],
                    )

                    N_left, N_right = y_left.size, y_right.size

                    split_conditions = [
                        N_left >= self.min_samples_leaf,
                        N_right >= self.min_samples_leaf,
                    ]

                    if all(split_conditions):
                        did_split = True
                        data = [(X_left, y_left), (X_right, y_right)]

                result = {"did_split": did_split, "data": data}
                return result

            def _split_traverse_node(node, container):
                """Process splitting results and continue with child nodes."""
                # Perform split and collect result
                result = _splitter(node)

                # Return terminal node if no split
                if not result["did_split"]:
                    if self.verbose > 0 and self.n_jobs == None:
                        depth_spacing_str = " ".join([" "] * node["depth"])
                        print(
                            " {}*leaf {} @ depth {}: Unique_y {},  N_samples {}".format(
                                depth_spacing_str,
                                node["index"],
                                node["depth"],
                                np.unique(node["data"][1]),
                                np.unique(node["data"][1], return_counts=True)[1],
                            )
                        )
                    return
                del node["data"]

                # Extract splitting results
                (X_left, y_left), (X_right, y_right) = result["data"]

                # Report created node to user
                if self.verbose > 0 and self.n_jobs == None:
                    depth_spacing_str = " ".join([" "] * node["depth"])
                    print(
                        " {}node {} @ depth {}: dataset={}, N_left={}, N_right={}".format(
                            depth_spacing_str,
                            node["index"],
                            node["depth"],
                            (X_left.shape[0] + X_right.shape[0], X_left.shape[1]),
                            X_left.shape[0],
                            X_right.shape[0],
                        )
                    )

                # Create child nodes
                node["children"]["left"] = _create_node(
                    X_left, y_left, node["depth"] + 1, container
                )
                node["children"]["right"] = _create_node(
                    X_right, y_right, node["depth"] + 1, container
                )

                # Split nodes
                _split_traverse_node(node["children"]["left"], container)
                _split_traverse_node(node["children"]["right"], container)

            container = {"index_node_global": 0}
            if self.verbose > 0 and self.n_jobs == None:
                print("\nNew Tree")
            root = _create_node(X, y, 0, container)
            Parallel(n_jobs=self.n_jobs, prefer="threads")(
                delayed(_split_traverse_node)(root, container) for _ in range(1)
            )
            return root

        def _build_tree_missing(X, y):
            """Build a LCE tree with missing data."""
            global index_node_global

            def _create_node_missing(X, y, depth, container):
                """Create a node in the tree."""
                y_size = y.size
                y_unique = np.unique(y)
                y_unique_size = y_unique.size
                
                # Add base learner predictions as features to the dataset
                if y_unique_size > 1:
                    if self.base_learner=="catboost":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            colsample_bylevel=self.base_colsample_bylevel,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    elif self.base_learner=="lightgbm":
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            num_leaves=self.base_num_leaves,
                            learning_rate=self.base_learning_rate,
                            boosting_type=self.base_boosting_type,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            subsample_for_bin=self.base_subsample_for_bin,
                            colsample_bytree=self.base_colsample_bytree,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    else:
                        model_node = base_dict[self.base_learner](
                            X,
                            y,
                            n_iter=self.n_iter,
                            metric=self.metric,
                            n_estimators=self.base_n_estimators,
                            max_depth=self.base_max_depth,
                            learning_rate=self.base_learning_rate,
                            booster=self.base_booster,
                            gamma=self.base_gamma,
                            min_child_weight=self.base_min_child_weight,
                            subsample=self.base_subsample,
                            colsample_bytree=self.base_colsample_bytree,
                            colsample_bylevel=self.base_colsample_bylevel,
                            colsample_bynode=self.base_colsample_bynode,
                            reg_alpha=self.base_reg_alpha,
                            reg_lambda=self.base_reg_lambda,
                            n_jobs=self.n_jobs,
                            random_state=self.random_state,
                        )
                    preds = np.around(model_node.predict(X), 6)
                    X = np.column_stack((X, preds))
                else:
                    model_node = None
                    X = np.column_stack((X, y))

                # Missing data information
                nans = np.isnan(X).any(axis=1)
                num_nans = nans.sum()
                if num_nans > 0:
                    missing = True
                    if num_nans == y_size:
                        missing_only = True
                    else:
                        missing_only = False
                else:
                    missing = False
                    missing_only = False

                # Split
                split_val_conditions = [y_size > 1, missing_only == False]
                if all(split_val_conditions):
                    split = DecisionTreeRegressor(
                        criterion=self.criterion,
                        splitter=self.splitter,
                        max_depth=1,
                        max_features=self.max_features,
                        random_state=self.random_state,
                    )
                    if missing:
                        split.fit(X[~nans], y[~nans])
                    else:
                        split.fit(X, y)
                else:
                    split = None

                # Node information
                node = {
                    "index": container["index_node_global"],
                    "model": model_node,
                    "data": (X, y),
                    "y_unique_size": y_unique_size,
                    "split": split,
                    "missing": {"missing": missing, "missing_only": missing_only},
                    "missing_side": None,
                    "children": {"left": None, "right": None},
                    "depth": depth,
                }
                container["index_node_global"] += 1
                return node

            def _splitter_missing(node):
                """Perform the split of a node."""
                # Extract data
                X, y = node["data"]
                depth = node["depth"]
                split = node["split"]
                missing = node["missing"]["missing"]
                missing_only = node["missing"]["missing_only"]

                did_split = False
                data = None

                # Perform split if the conditions are met
                stopping_criteria = [
                    depth >= 0,
                    depth < self.max_depth,
                    np.unique(y).size > 1,
                    missing_only == False,
                ]

                if all(stopping_criteria):
                    if missing:
                        nans = np.isnan(X).any(axis=1)
                        X_withoutnans, y_withoutnans = X[~nans], y[~nans]
                        leafs = split.apply(X_withoutnans)
                        leafs_left = leafs == 1
                        leafs_right = np.invert(leafs_left)
                        (X_left, y_left), (X_right, y_right) = (
                            X_withoutnans[leafs_left, :],
                            y_withoutnans[leafs_left],
                        ), (
                            X_withoutnans[leafs_right, :],
                            y_withoutnans[leafs_right],
                        )
                    else:
                        leafs = split.apply(X)
                        leafs_left = leafs == 1
                        leafs_right = np.invert(leafs_left)
                        (X_left, y_left), (X_right, y_right) = (
                            X[leafs_left, :],
                            y[leafs_left],
                        ), (
                            X[leafs_right, :],
                            y[leafs_right],
                        )

                    N_left, N_right = y_left.size, y_right.size

                    split_conditions = [
                        N_left >= self.min_samples_leaf,
                        N_right >= self.min_samples_leaf,
                    ]

                    if all(split_conditions):
                        did_split = True

                        if N_left == 1:
                            node["missing_side"] = "left"
                            if missing:
                                X_left = np.concatenate([X_left, X[nans]], axis=0)
                                y_left = np.concatenate([y_left, y[nans]], axis=0)

                        if N_right == 1:
                            if N_left > 1:
                                node["missing_side"] = "right"
                                if missing:
                                    X_right = np.concatenate([X_right, X[nans]], axis=0)
                                    y_right = np.concatenate([y_right, y[nans]], axis=0)

                        score_conditions = [N_left > 1, N_right > 1]
                        if all(score_conditions):
                            if split.score(X_left, y_left) > split.score(
                                X_right, y_right
                            ):
                                node["missing_side"] = "left"
                                if missing:
                                    X_left = np.concatenate([X_left, X[nans]], axis=0)
                                    y_left = np.concatenate([y_left, y[nans]], axis=0)
                            else:
                                node["missing_side"] = "right"
                                if missing:
                                    X_right = np.concatenate([X_right, X[nans]], axis=0)
                                    y_right = np.concatenate([y_right, y[nans]], axis=0)

                        data = [(X_left, y_left), (X_right, y_right)]

                result = {"did_split": did_split, "data": data}
                return result

            def _split_traverse_node_missing(node, container):
                """Process splitting results and continue with child nodes."""
                # Perform split and collect result
                result = _splitter_missing(node)

                # Return terminal node if no split
                if not result["did_split"]:
                    if self.verbose > 0 and self.n_jobs == None:
                        depth_spacing_str = " ".join([" "] * node["depth"])
                        print(
                            " {}*leaf {} @ depth {}: Unique_y {},  N_samples {}".format(
                                depth_spacing_str,
                                node["index"],
                                node["depth"],
                                np.unique(node["data"][1]),
                                np.unique(node["data"][1], return_counts=True)[1],
                            )
                        )
                    return
                del node["data"]

                # Extract splitting results
                (X_left, y_left), (X_right, y_right) = result["data"]

                # Report created node to user
                if self.verbose > 0 and self.n_jobs == None:
                    depth_spacing_str = " ".join([" "] * node["depth"])
                    print(
                        " {}node {} @ depth {}: dataset={}, N_left={}, N_right={}".format(
                            depth_spacing_str,
                            node["index"],
                            node["depth"],
                            (X_left.shape[0] + X_right.shape[0], X_left.shape[1]),
                            X_left.shape[0],
                            X_right.shape[0],
                        )
                    )

                # Create child nodes
                node["children"]["left"] = _create_node_missing(
                    X_left, y_left, node["depth"] + 1, container
                )
                node["children"]["right"] = _create_node_missing(
                    X_right, y_right, node["depth"] + 1, container
                )

                # Split nodes
                _split_traverse_node_missing(node["children"]["left"], container)
                _split_traverse_node_missing(node["children"]["right"], container)

            container = {"index_node_global": 0}
            if self.verbose > 0 and self.n_jobs == None:
                print("\nNew Tree")
            root = _create_node_missing(X, y, 0, container)
            Parallel(n_jobs=self.n_jobs, prefer="threads")(
                delayed(_split_traverse_node_missing)(root, container) for _ in range(1)
            )
            return root

        if np.isnan(X).any():
            self.tree = _build_tree_missing(X, y)
        else:
            self.tree = _build_tree(X, y)
        return self

    def predict(self, X):
        """
        Predict regression target for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted values.
        """

        def _base(node, X):
            if node["y_unique_size"] > 1:
                y_pred = np.around(node["model"].predict(X[:, 1:]), 6)
                X = np.column_stack((X, y_pred))
            else:
                X = np.column_stack((X, X[:, -1]))
            return X

        def _predict(node, X, y_pred_final=None):
            X = _base(node, X)

            no_children = (
                node["children"]["left"] is None and node["children"]["right"] is None
            )
            if no_children:
                y_pred = np.column_stack((X[:, :1], X[:, -1:]))
                if y_pred_final is not None:
                    y_pred_final = np.concatenate((y_pred_final, y_pred), axis=0)
                else:
                    y_pred_final = y_pred
                return y_pred_final

            else:
                leafs = node["split"].apply(X[:, 1:])
                leafs_left = leafs == 1
                leafs_right = np.invert(leafs_left)
                X_left, X_right = X[leafs_left, :], X[leafs_right, :]

                if len(X_left) > 0:
                    y_pred_final = _predict(
                        node["children"]["left"], X_left, y_pred_final
                    )
                if len(X_right) > 0:
                    y_pred_final = _predict(
                        node["children"]["right"], X_right, y_pred_final
                    )
                return y_pred_final

        def _predict_missing(node, X, y_pred_final=None):
            X = _base(node, X)

            no_children = (
                node["children"]["left"] is None and node["children"]["right"] is None
            )
            if no_children:
                y_pred = np.column_stack((X[:, :1], X[:, -1:]))
                if y_pred_final is not None:
                    y_pred_final = np.concatenate((y_pred_final, y_pred), axis=0)
                else:
                    y_pred_final = y_pred
                return y_pred_final

            else:
                nans = np.isnan(X).any(axis=1)
                if nans.sum() > 0:
                    leafs = node["split"].apply(X[~nans, 1:])
                    leafs_left = leafs == 1
                    leafs_right = np.invert(leafs_left)
                    X_left, X_right = X[~nans][leafs_left, :], X[~nans][leafs_right, :]
                    if node["missing_side"] == "left":
                        X_left, X_right = (
                            np.concatenate((X_left, X[nans]), axis=0),
                            X_right,
                        )
                    else:
                        X_left, X_right = X_left, np.concatenate(
                            (X_right, X[nans]), axis=0
                        )
                else:
                    leafs = node["split"].apply(X[:, 1:])
                    leafs_left = leafs == 1
                    leafs_right = np.invert(leafs_left)
                    X_left, X_right = X[leafs_left, :], X[leafs_right, :]

                if len(X_left) > 0:
                    y_pred_final = _predict_missing(
                        node["children"]["left"], X_left, y_pred_final
                    )
                if len(X_right) > 0:
                    y_pred_final = _predict_missing(
                        node["children"]["right"], X_right, y_pred_final
                    )
                return y_pred_final

        index = np.arange(0, X.shape[0]).reshape(-1, 1)
        X = np.concatenate((index, X), axis=1)
        if np.isnan(X).any():
            y_pred = _predict_missing(self.tree, X, None)
        else:
            y_pred = _predict(self.tree, X, None)
        y_pred = y_pred[y_pred[:, 0].argsort()]
        y_pred = y_pred[:, 1]
        return y_pred

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
