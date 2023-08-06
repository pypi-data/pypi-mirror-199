from xgboost import XGBRegressor, XGBClassifier


class XGBRegressorWrapper(XGBRegressor):
    # A wrapper for XGBRegressor that automatically uses the best number of trees for inference when early stopping is
    # used in learning
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def predict(self, *args, **kwargs):
        return super().predict(*args, **kwargs, iteration_range=(0, self.best_iteration))


class XGBClassifierWrapper(XGBClassifier):
    # A wrapper for XGBClassifier that automatically uses the best number of trees for inference when early stopping is
    # used in learning
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def predict(self, *args, **kwargs):
        return super().predict(*args, **kwargs, iteration_range=(0, self.best_iteration))

    def predict_proba(self, *args, **kwargs):
        return super().predict_proba(*args, **kwargs, iteration_range=(0, self.best_iteration))
