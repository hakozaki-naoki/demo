from fastapi import APIRouter
from service.schemas.schemas import (
    AnswerRequest,
    AnswerResponse,
    RegenerateRequest,
    RegenerateResponse,
)
from service.tools.extract_query import ExtractQuery
from service.core.exceptions import (
    ServiceException,
    ValidationException,
    ResourceNotFoundException,
    DataProcessingException,
)
import json
from service.core.config import settings
import logging

import time
import os
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

# 配置日志
logger = logging.getLogger("routes")

router = APIRouter()


@router.post("/generate_answer")
async def generate_answer(answer_request: AnswerRequest) -> AnswerResponse:
    """生成回答的API端点"""
    start_time = time.time()
    extract_query = ExtractQuery()

    try:
        # 验证请求
        if not answer_request.query or answer_request.query.strip() == "":
            raise ValidationException(
                message="转译内容不能为空", details={"field": "query"}
            )

        logger.info(f"处理转译请求: {answer_request.query[:50]}...")

        # 提取客户问题
        try:
            client_queries = extract_query.extract_informations(
                answer_request.query, "openai"
            )["questions"]
            logger.info(f"提取到 {len(client_queries)} 个信息")
            # 展示所有提取的问题
            for i, query in enumerate(client_queries):
                logger.info(f"信息 {i + 1}: {query}")
        except Exception as e:
            logger.error(f"提取关键信息失败: {str(e)}")
            raise DataProcessingException(
                message="提取关键信息失败", details={"original_error": str(e)}
            )
        
        client_queries = ['要約結果']+client_queries
        response_data = {
            "extract_query": client_queries,
        }

        execution_time = time.time() - start_time
        logger.info(f"请求处理完成, 耗时: {execution_time:.2f}秒")

        return AnswerResponse(data=response_data)
    except ServiceException:
        # 已经是服务异常，直接抛出
        raise
    except Exception as e:
        # 其他未知异常
        logger.error(f"处理请求时发生未知错误: {str(e)}")
        raise ServiceException(
            message="处理请求时发生未知错误", details={"original_error": str(e)}
        )
