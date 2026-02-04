from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from service.api.v1.router import router as v1_router
from service.core.error_handlers import (
    service_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from service.core.exceptions import ServiceException
import logging
import time
import os
from logging.handlers import RotatingFileHandler

# 创建日志目录
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(logs_dir, exist_ok=True)

# 配置日志
log_file = os.path.join(logs_dir, "service.log")
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建根日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
root_logger.addHandler(console_handler)

# 添加文件处理器（带轮转）
file_handler = RotatingFileHandler(
    log_file, 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,           # 保留5个备份文件
    encoding='utf-8'
)
file_handler.setFormatter(log_format)
root_logger.addHandler(file_handler)

# 获取模块日志记录器
logger = logging.getLogger("main")
logger.info(f"日志配置完成，日志文件保存在: {log_file}")

app = FastAPI()

# 注册异常处理器
app.add_exception_handler(ServiceException, service_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (for testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有请求的中间件"""
    start_time = time.time()
    
    # 记录请求信息
    logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={
            "request_method": request.method,
            "request_path": request.url.path,
            "request_query": str(request.query_params),
        }
    )
    
    try:
        response = await call_next(request)
        
        # 记录响应信息
        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s",
            extra={
                "request_method": request.method,
                "request_path": request.url.path,
                "response_status": response.status_code,
                "process_time": process_time,
            }
        )
        
        return response
    except Exception as e:
        # 这里的异常会被全局异常处理器捕获
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} - Error: {str(e)} - Time: {process_time:.3f}s",
            extra={
                "request_method": request.method,
                "request_path": request.url.path,
                "error": str(e),
                "process_time": process_time,
            }
        )
        raise

app.include_router(v1_router, prefix="/v1", tags=["v1"])
