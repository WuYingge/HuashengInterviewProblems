import logging  
import logging.handlers  
import os  
  
# 日志文件目录  
LOG_DIR = 'logs'  
  
# 确保日志文件目录存在  
if not os.path.exists(LOG_DIR):  
    os.makedirs(LOG_DIR)  
  
# 日志文件名  
LOG_FILE = os.path.join(LOG_DIR, 'app.log')  

def create_logger():
    # 创建一个logger  
    logger = logging.getLogger('myapp')  
    logger.setLevel(logging.DEBUG)  
    
    # 创建一个handler，用于写入日志文件，并设置日志级别、日志格式等  
    handler = logging.handlers.RotatingFileHandler(  
        LOG_FILE, maxBytes=1024*1024, backupCount=5  # 日志文件最大1MB，保留5个备份  
    )
    
    # 定义日志格式  
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    handler.setFormatter(formatter)  
    watch_handler = logging.handlers.WatchedFileHandler(LOG_FILE)  
    
    # 给logger添加handler  
    logger.addHandler(handler)
    logger.addHandler(watch_handler)
    return logger

LOGGER = create_logger()
