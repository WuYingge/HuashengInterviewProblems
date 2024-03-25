"""
错误码和错误信息
"""

class ErrorCode:
    
    SUCCESS = 0
    MODEL_NOT_READY = 1
    MODEL_ERROR = 2
    DATA_ERROR = 3
    BUSY = 4
    UNKNOWN = 999
    
class ErrorMessage:
    
    SUCCESS = "Success"
    MODEL_NOT_READY = "Model is not ready"
    MODEL_ERROR = "Model error"
    DATA_ERROR = "Data error {}"
    BUSY = "Server is busy"
    UNKNOWN = "Unknown error"