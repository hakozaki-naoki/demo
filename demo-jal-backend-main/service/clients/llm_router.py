from service.clients.openai_api import OpenAIClient
from service.core.exceptions import LLMException, ProviderNotFoundException
import logging
import os

# 配置日志
logger = logging.getLogger("llm_router")


class LLMRouter:
    def __init__(self):
        self.openai_client = OpenAIClient()
        logger.info("LLM路由器初始化完成")

    def generate(
        self,
        system_prompt,
        user_prompt,
        response_format=None,
        temperature=1.0,
        provider="openai",
        mode="chat",
    ):
        """LLM请求 - 只使用OpenAI"""
        logger.info(f"LLM请求路由到OpenAI, 模式: {mode}")

        try:
            if provider != "openai":
                logger.warning(f"请求的提供商 {provider} 已被忽略，将使用OpenAI")
                
            if mode == "chat":
                logger.debug("使用OpenAI聊天模式")
                return self.openai_client.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    response_format=response_format,
                    temperature=temperature,
                    model=os.getenv("DEPLOYMENT_4O", "gpt-4o"),
                )
            elif mode == "reasoning":
                logger.debug("使用OpenAI思考模式")
                return self.openai_client.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    response_format=response_format,
                    temperature=temperature,
                    model=os.getenv("DEPLOYMENT_o1", "o1"),
                )
            else:
                raise ValueError(f"未知模式: {mode}")
        except LLMException:
            # 已经是LLM异常，直接抛出
            raise
        except Exception as e:
            # 其他未知异常
            logger.error(f"LLM生成时发生错误: {str(e)}")
            raise LLMException(
                message=f"LLM生成时发生错误: {str(e)}",
                provider="openai",
                details={"mode": mode},
            )
