import time
import asyncio
import json
import requests
from requests.exceptions import HTTPError
import numpy as np  
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from model import ModelException, Model
from logger import LOGGER
from validator import validate_predict_data, ValidationError
from common.error_code import ErrorCode, ErrorMessage
from functools import partial
  
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)
QUEUE = asyncio.Queue(maxsize=1000)

  
# 加载预训练的模型
def init_model():
    trained_model = None
    try:
        trained_model = Model(config_path='config.yaml')
        trained_model.init()
    except ModelException as e:
        LOGGER.error(f"Failed to load model: {e}", exc_info=True)
    return trained_model


def check_model_ready(model):
    if not model.is_model_ready():
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


async def do_predict():
    while True:
        print('sdf')
        data = await QUEUE.get()
        task_id = data.get("taskId", "")
        callback_url = data.get("callbackUrl", "")
        predict_data = data.get("data", [])
        loop = asyncio.get_running_loop()
        try:
            # 调用预处理函数
            processed_data = await loop.run_in_executor(executor, preprocess_data, predict_data)
            target = await loop.run_in_executor(executor, model.predict, await processed_data)
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
        print('ok')
        QUEUE.task_done()
        
  
# API 接口  
@app.route('/predict', methods=['POST'])  
def predict_endpoint():
    try: 
        check_model_ready(model)
        # 获取请求数据  
        data = request.get_json()
        # 检查请求数据是否合法
        validate_predict_data(data)
        
        QUEUE.put_nowait(data)
        # 立即返回调用成功的响应给客户端  
        return jsonify({"": "调用成功", "error_code": 0}), 202
    except ModelException as e:
        LOGGER.error(f"model error: {e}")
        return jsonify({"error_message": ErrorMessage.MODEL_ERROR, "error_code": ErrorCode.MODEL_ERROR}), 500
    except ValidationError as e:
        LOGGER.error(f"invalid requests data: {e}")
        return jsonify({"error_message": ErrorMessage.DATA_ERROR, "error_code": ErrorCode.DATA_ERROR}), 400
    except asyncio.QueueFull as err:
        LOGGER.error(f"task queue is full: {err}, rejected {data}")
        return jsonify({"error_message": ErrorMessage.BUSY, "error_code": ErrorCode.BUSY}), 503
    except Exception as e:
        LOGGER.error(f"unknown error: {e}", exc_info=True)
        return jsonify({"error": "unknown error"}), 500
    

async def start_services():  
    # 创建 Flask 服务的协程任务  
    flask_task = asyncio.create_task(app.run(host='0.0.0.0', port=5000))  
    # 运行我们的自定义协程  
    await do_predict()  
    # 等待 Flask 服务任务完成（通常不会，除非你关闭 Flask 服务）  
    await flask_task  

  
if __name__ == '__main__':
    model = init_model()
    asyncio.run(start_services())
    