import numpy as np
from sklearn.datasets import (
    load_breast_cancer,
    load_diabetes,
    load_iris,
    make_regression,
)
from sklearn.utils.estimator_checks import check_estimator
import unittest
import warnings

from .._lce import LCEClassifier, LCERegressor


class Test(unittest.TestCase):
    """Tests of LCE"""

    def test_classifier_params(self):
        # Load Iris dataset
        data = load_iris()

        # max_depth
        with self.assertRaises(ValueError):
            LCEClassifier(max_depth=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(max_depth=1.1).fit(data.data, data.target)

        # min_samples_leaf
        with self.assertRaises(ValueError):
            LCEClassifier(min_samples_leaf=0).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(min_samples_leaf=1.1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(min_samples_leaf="a").fit(data.data, data.target)
        with warnings.catch_warnings():
            LCEClassifier(min_samples_leaf=0.3).fit(data.data, data.target)

        # n_iter
        with self.assertRaises(ValueError):
            LCEClassifier(n_iter=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(n_iter=1.1).fit(data.data, data.target)

        # verbose
        with self.assertRaises(ValueError):
            LCEClassifier(verbose=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCEClassifier(verbose=1.1).fit(data.data, data.target)
        with warnings.catch_warnings():
            LCEClassifier(verbose=1).fit(data.data, data.target)

    def test_classifier(self):
        # Load Breast Cancer dataset
        data = load_breast_cancer()
        
        # Fit and predict (base learner: CatBoost)
        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="catboost",
                random_state=0,
                verbose=1,
            ).fit(data.data, data.target)
            clf.predict(data.data)
            
        # Fit and predict (base learner: LightGBM)
        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="lightgbm",
                random_state=0,
                verbose=1,
            ).fit(data.data, data.target)
            clf.predict(data.data)

        # Fit and predict (base learner: XGBoost)
        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="xgboost",
                random_state=0,
                verbose=1,
            ).fit(data.data, data.target)
            clf.predict(data.data)
    

    def test_classifier_missing(self):
        # Load Iris dataset
        data = load_iris()
        
        # Input 2% of missing values per variable (base learner: CatBoost)
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="catboost",
                random_state=0,
                verbose=1,
            ).fit(temp, data.target)
            clf.predict(temp)
            
        # Input 2% of missing values per variable (base learner: LightGBM)
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="lightgbm",
                random_state=0,
                verbose=1,
            ).fit(temp, data.target)
            clf.predict(temp)

        # Input 2% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="xgboost",
                random_state=0,
                verbose=1,
            ).fit(temp, data.target)
            clf.predict(temp)

        # Input 20% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 0.2
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3, max_depth=50, min_samples_leaf=1, base_learner="xgboost", random_state=0
            ).fit(temp, data.target)
            clf.predict(temp)

        # Input 60% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 0.6
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3, max_depth=50, min_samples_leaf=1, base_learner="xgboost", random_state=0
            ).fit(temp, data.target)
            clf.predict(temp)

        # Input 100% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 1.0
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            clf = LCEClassifier(
                n_estimators=3, max_depth=50, min_samples_leaf=1, base_learner="xgboost", random_state=0
            ).fit(temp, data.target)
            clf.predict(temp)

    def test_classifier_sklearn_estimator(self):
        # scikit-learn check estimator
        assert check_estimator(LCEClassifier()) == None

    def test_regressor_params(self):
        # Load Diabetes dataset
        data = load_diabetes()

        # max_depth
        with self.assertRaises(ValueError):
            LCERegressor(max_depth=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(max_depth=1.1).fit(data.data, data.target)

        # min_samples_leaf
        with self.assertRaises(ValueError):
            LCERegressor(min_samples_leaf=0).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(min_samples_leaf=1.1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(min_samples_leaf="a").fit(data.data, data.target)
        with warnings.catch_warnings():
            LCERegressor(min_samples_leaf=0.3).fit(data.data, data.target)

        # n_iter
        with self.assertRaises(ValueError):
            LCERegressor(n_iter=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(n_iter=1.1).fit(data.data, data.target)

        # verbose
        with self.assertRaises(ValueError):
            LCERegressor(verbose=-1).fit(data.data, data.target)
        with self.assertRaises(ValueError):
            LCERegressor(verbose=1.1).fit(data.data, data.target)
        with warnings.catch_warnings():
            LCERegressor(verbose=1).fit(data.data, data.target)

    def test_regressor(self):
        # Load dataset
        n_samples, n_features = 100, 20
        rng = np.random.RandomState(0)
        X, y = make_regression(n_samples, n_features, random_state=rng)

        # Fit and predict (base learner: CatBoost)
        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="catboost",
                random_state=0,
                verbose=1,
            ).fit(X, y)
            reg.predict(X)
            
        # Fit and predict (base learner: LightGBM)
        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="lightgbm",
                random_state=0,
                verbose=1,
            ).fit(X, y)
            reg.predict(X)
            
        # Fit and predict (base learner: XGBoost)
        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="xgboost",
                random_state=0,
                verbose=1,
            ).fit(X, y)
            reg.predict(X)

    def test_regressor_missing(self):
        # Load Diabetes dataset
        data = load_diabetes()
        
        # Input 2% of missing values per variable (base learner: CatBoost)
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="catboost",
                random_state=0,
                verbose=1,
            ).fit(temp, data.target)
            reg.predict(temp)
            
        # Input 2% of missing values per variable (base learner: LightGBM)
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="lightgbm",
                random_state=0,
                verbose=1,
            ).fit(temp, data.target)
            reg.predict(temp)

        # Input 2% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 0.02
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3,
                max_depth=50,
                min_samples_leaf=1,
                base_learner="xgboost",
                random_state=0,
                verbose=1,
            ).fit(temp, data.target)
            reg.predict(temp)

        # Input 20% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 0.2
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3, max_depth=50, min_samples_leaf=1, base_learner="xgboost", random_state=0
            ).fit(temp, data.target)
            reg.predict(temp)

        # Input 60% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 0.6
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3, max_depth=50, min_samples_leaf=1, base_learner="xgboost", random_state=0
            ).fit(temp, data.target)
            reg.predict(temp)

        # Input 100% of missing values per variable (base learner: XGBoost)
        np.random.seed(0)
        m = 1.0
        for j in range(0, data.data.shape[1]):
            sub = np.random.choice(data.data.shape[0], int(data.data.shape[0] * m))
            temp = data.data
            temp[sub, j] = np.nan

        with warnings.catch_warnings():
            reg = LCERegressor(
                n_estimators=3, max_depth=50, min_samples_leaf=1, base_learner="xgboost", random_state=0
            ).fit(temp, data.target)
            reg.predict(temp)

    def test_regressor_sklearn_estimator(self):
        # scikit-learn check estimator
        assert check_estimator(LCERegressor()) == None
