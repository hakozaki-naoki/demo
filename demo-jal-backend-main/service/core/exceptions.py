class ServiceException(Exception):
    """基础服务异常类"""
    def __init__(self, message="服务异常", code=500, details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

# 数据库相关异常
class DatabaseException(ServiceException):
    """数据库操作异常"""
    def __init__(self, message="数据库操作异常", details=None):
        super().__init__(message=message, code=500, details=details)

class QueryException(DatabaseException):
    """查询异常"""
    pass

class ConnectionException(DatabaseException):
    """连接异常"""
    pass

# LLM相关异常
class LLMException(ServiceException):
    """LLM服务异常"""
    def __init__(self, message="LLM服务异常", provider=None, details=None):
        details = details or {}
        if provider:
            details["provider"] = provider
        super().__init__(message=message, code=502, details=details)

class ProviderNotFoundException(LLMException):
    """LLM提供商不存在"""
    def __init__(self, provider, details=None):
        super().__init__(message=f"LLM提供商不存在: {provider}", provider=provider, details=details)

class ProviderTimeoutException(LLMException):
    """LLM提供商超时"""
    def __init__(self, provider, timeout, details=None):
        details = details or {}
        details["timeout"] = timeout
        super().__init__(message=f"LLM提供商响应超时: {provider}", provider=provider, details=details)

# 数据处理相关异常
class DataProcessingException(ServiceException):
    """数据处理异常"""
    def __init__(self, message="数据处理异常", details=None):
        super().__init__(message=message, code=500, details=details)

class FileReadException(DataProcessingException):
    """文件读取异常"""
    def __init__(self, file_path, details=None):
        details = details or {}
        details["file_path"] = file_path
        super().__init__(message=f"文件读取异常: {file_path}", details=details)

# API相关异常
class APIException(ServiceException):
    """API异常"""
    def __init__(self, message="API异常", code=400, details=None):
        super().__init__(message=message, code=code, details=details)

class ValidationException(APIException):
    """请求验证异常"""
    def __init__(self, message="请求参数验证失败", details=None):
        super().__init__(message=message, code=422, details=details)

class ResourceNotFoundException(APIException):
    """资源不存在异常"""
    def __init__(self, resource_type, resource_id, details=None):
        details = details or {}
        details["resource_type"] = resource_type
        details["resource_id"] = resource_id
        super().__init__(
            message=f"资源不存在: {resource_type} (ID: {resource_id})", 
            code=404, 
            details=details
        )
