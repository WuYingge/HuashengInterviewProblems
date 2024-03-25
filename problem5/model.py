import os
import xgboost as xgb
import numpy as np
from logger import LOGGER
from yaml import load, Loader, safe_load


class Model:
    
    def __init__(self, config_path=''):
        self.model = xgb.Booster()
        self.config = {}
        self.config_path = config_path
        self.target = []
        self.feature_names = []
        self._init = False
        
        
    def init(self):
        print(os.getcwd())
        # load config
        with open(os.path.realpath(self.config_path), 'r') as f:
            config_data = safe_load(f)
        model_config = config_data.get("Model")
        if not model_config:
            raise ModelException("Model config not found")
        self.target = model_config.get("target", "").split(",")
        model_path = model_config.get("path", "")
        if not model_path:
            raise ModelException("Model path not found")
        try:
            self.model.load_model(model_path)
        except ModelException as e:
            LOGGER.error(f"Failed to load model: {e}", exc_info=True)
            raise
        self._init = True

    def predict(self, data):
        data = np.array(data).reshape(1, -1)
        predictions = self.model.predict(xgb.DMatrix(data))
        predict_class = self.target[np.argmax(predictions)]
        return predict_class
    
    def is_model_ready(self):
        return self._init
    
    def refresh_model(self):
        # todo refresh model
        ...
        
        
class ModelException(Exception):
    
    """
    Model加载预测过程中的异常
    """
    
    def __init__(self, message=None):
        self.message = message
        
    def __repr__(self) -> str:
        return f"ModelException: {self.message}"
