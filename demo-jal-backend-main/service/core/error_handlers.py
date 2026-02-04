import time
import traceback
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from service.core.exceptions import ServiceException

# 获取日志记录器
logger = logging.getLogger("error_handler")

async def service_exception_handler(request: Request, exc: ServiceException):
    """处理自定义服务异常"""
    error_id = int(time.time())
    
    # 记录错误日志
    logger.error(
        f"Error ID: {error_id} - {exc.__class__.__name__}: {exc.message}",
        extra={
            "error_id": error_id,
            "error_code": exc.code,
            "error_details": exc.details,
            "request_path": request.url.path,
            "request_method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": {
                "id": error_id,
                "code": exc.code,
                "type": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证异常"""
    error_id = int(time.time())
    
    # 提取验证错误详情
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    
    # 记录错误日志
    logger.error(
        f"Error ID: {error_id} - ValidationError",
        extra={
            "error_id": error_id,
            "error_details": error_details,
            "request_path": request.url.path,
            "request_method": request.method,
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "id": error_id,
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "type": "ValidationError",
                "message": "请求参数验证失败",
                "details": error_details
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """处理所有其他未捕获的异常"""
    error_id = int(time.time())
    
    # 记录错误日志，包含堆栈跟踪
    logger.error(
        f"Error ID: {error_id} - Unhandled Exception: {str(exc)}",
        extra={
            "error_id": error_id,
            "request_path": request.url.path,
            "request_method": request.method,
            "traceback": traceback.format_exc()
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "id": error_id,
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "type": exc.__class__.__name__,
                "message": "服务器内部错误",
                "details": {"info": "请联系管理员并提供错误ID"}
            }
        }
    )
