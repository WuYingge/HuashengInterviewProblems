import time
import requests
from requests.exceptions import HTTPError
from fastapi import FastAPI, BackgroundTasks, HTTPException  
from fastapi.responses import JSONResponse  
import xgboost as xgb  
import asyncio  
import numpy as np
from validator import validate_predict_data, ValidationError
from model import Model, ModelException
from concurrent.futures import ThreadPoolExecutor
from common.error_code import ErrorCode, ErrorMessage
from logger import LOGGER
  
app = FastAPI()
executor = ThreadPoolExecutor(max_workers=10)


# 加载预训练的模型
def init_model():
    trained_model = None
    try:
        trained_model = Model(config_path='config.yaml')
        trained_model.init()
    except ModelException as e:
        LOGGER.error(f"Failed to load model: {e}", exc_info=True)
    return trained_model


model = init_model()


def check_model_ready(model):
    if model is None or not model.is_model_ready():
        raise ModelException("Model is not ready")
    
    
# 预处理函数（耗时较长）  
def preprocess_data(data):  
    # 耗时的预处理逻辑
    time.sleep(3)
    return data
  
# 异步发送回调的函数  
async def send_callback_async(url, result):
    print(result)
    loop = asyncio.get_running_loop()
    def post_result(url, result):
        def post_func(func):
            return func(url, json=result)
        return post_func
    response = await loop.run_in_executor(executor, post_result(url, result), requests.post)
    return response


async def do_predict(data):
    task_id = data.get("taskId", "")
    callback_url = data.get("callbackUrl", "")
    predict_data = data.get("data", [])
    loop = asyncio.get_running_loop()
    try:
        # 调用预处理函数
        processed_data = await loop.run_in_executor(executor, preprocess_data, predict_data)
        target = await loop.run_in_executor(executor, model.predict, processed_data)
        error_message = ErrorMessage.SUCCESS
        error_code = ErrorCode.SUCCESS
    except Exception as err:
        target = ""
        error_message = ErrorMessage.MODEL_ERROR
        error_code = ErrorCode.MODEL_ERROR
        LOGGER.error(f"process data error {err}: {data}", exc_info=True)
    try:
        response = await send_callback_async(
                callback_url, 
                {"taskId": task_id, "target": target, "error_message": error_message, "error_code": error_code}
                )
        response.raise_for_status()
        LOGGER.info(f"Callback success for task {task_id}, target as {target}")
    except HTTPError as err:
        LOGGER.error(f"Callback error for task {task_id}: {err}")
  
@app.post("/predict")  
async def predict_endpoint(data: dict, background_tasks: BackgroundTasks):
    try:
        check_model_ready(model)
        # 验证数据格式（这里仅作为示例）  
        validate_predict_data(data)
        # 将任务添加到后台任务队列  
        background_tasks.add_task(do_predict, data)  
        
        # 立即返回一个确认响应给客户端  
        return JSONResponse({"error_message": ErrorMessage.SUCCESS, "error_code": ErrorCode.SUCCESS}, status_code=202)
    except ModelException as e:
        LOGGER.error(f"model error: {e}")
        return JSONResponse({"error_message": ErrorMessage.MODEL_ERROR, "error_code": ErrorCode.MODEL_ERROR}, status_code=500)
    except ValidationError as e:
        LOGGER.error(f"invalid requests data: {e}")
        return JSONResponse({"error_message": ErrorMessage.DATA_ERROR, "error_code": ErrorCode.DATA_ERROR}, status_code=400)
    except asyncio.QueueFull as err:
        LOGGER.error(f"task queue is full: {err}, rejected {data}")
        return JSONResponse({"error_message": ErrorMessage.BUSY, "error_code": ErrorCode.BUSY}, status_code=503)
    except Exception as e:
        LOGGER.error(f"unknown error: {e}", exc_info=True)
        return JSONResponse({"error_message": ErrorMessage.UNKNOWN, "error_code": ErrorCode.UNKNOWN}, status_code=500)
  
# 运行FastAPI应用  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)