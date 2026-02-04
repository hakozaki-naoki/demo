import time
import random
import logging
from functools import wraps
from service.core.exceptions import ServiceException

logger = logging.getLogger("retry")

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=10, backoff_factor=2, jitter=0.1):
    """
    重试装饰器，带指数退避策略
    
    参数:
        max_retries (int): 最大重试次数
        base_delay (float): 初始延迟时间（秒）
        max_delay (float): 最大延迟时间（秒）
        backoff_factor (float): 退避因子
        jitter (float): 抖动因子，增加随机性以避免同时重试
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"重试失败，已达到最大重试次数 {max_retries}: {str(e)}")
                        if isinstance(e, ServiceException):
                            raise
                        else:
                            # 将普通异常转换为服务异常
                            raise ServiceException(
                                message=f"操作失败，已重试 {max_retries} 次",
                                details={"original_error": str(e)}
                            )
                    
                    # 计算延迟时间
                    delay = min(base_delay * (backoff_factor ** (retries - 1)), max_delay)
                    # 添加随机抖动
                    delay = delay * (1 + random.uniform(-jitter, jitter))
                    
                    logger.warning(
                        f"操作失败，将在 {delay:.2f} 秒后重试 (尝试 {retries}/{max_retries}): {str(e)}"
                    )
                    time.sleep(delay)
        return wrapper
    return decorator
