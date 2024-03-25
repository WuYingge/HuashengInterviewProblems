import json  
from logger import LOGGER
from jsonschema import Draft7Validator, ValidationError  
  
# 定义JSON模式  
schema = {  
    "type": "object",  
    "properties": {  
        "callbackUrl": {"type": "string"},  
        "taskId": {"type": "string"},  
        "data": {  
            "type": "array",  
            "items": {"type": "integer"},
            "minItems": 4,
            "maxItems": 4
        }  
    },  
    "required": ["callbackUrl", "taskId", "data"]  
}  


predict_validator = Draft7Validator(schema)


def validate_predict_data(data):
    errors = []
    for error in predict_validator.iter_errors(data):
        errors.append(error.message)
    if errors:
        raise ValidationError(','.join(errors))
    

if __name__ == "__main__":
    res = validate_predict_data({"url": "", "data": [1,2,3]}, predict_validator)
    print(res)
    