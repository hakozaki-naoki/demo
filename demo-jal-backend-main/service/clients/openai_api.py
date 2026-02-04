import openai
import os
import json
import logging
from service.tools.retry import retry_with_backoff
from service.core.exceptions import LLMException, ProviderTimeoutException

# 配置日志
logger = logging.getLogger("openai_client")

class OpenAIClient:
    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=os.environ['OPENAI_API_KEY'],
            azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
            api_version=os.environ['OPENAI_API_VERSION']
        )
        logger.info("OpenAI客户端初始化完成")

    def generate(
        self,
        system_prompt,
        user_prompt,
        response_format,
        temperature,
        model,
    ):
        """生成回复"""
        logger.info(f"调用OpenAI API，模型: {model}")
        
        try:
            if response_format:
                logger.debug("使用格式化响应")
                return self.format_generate(
                    system_prompt, user_prompt, model, temperature, response_format
                )
            else:
                logger.debug("使用标准响应")
                if model == os.environ["DEPLOYMENT_o1"]:
                    logger.debug("调用思考模型")
                    return self.o1_generate(system_prompt + user_prompt)
                else:
                    logger.debug("调用基础聊天模型")
                    return self.not_o1_generate(
                        system_prompt, user_prompt, temperature, model
                    )

        except openai.APITimeoutError as e:
            logger.error(f"OpenAI API超时: {str(e)}")
            raise ProviderTimeoutException(
                provider="openai",
                timeout=60,  # 假设超时时间为60秒
                details={"model": model}
            )
        except openai.APIError as e:
            logger.error(f"OpenAI API错误: {str(e)}")
            raise LLMException(
                message=f"OpenAI API错误: {str(e)}",
                provider="openai",
                details={"model": model}
            )
        except Exception as e:
            logger.error(f"调用OpenAI API时发生错误: {str(e)}")
            logger.error(f"提示词: {system_prompt + user_prompt}")
            raise LLMException(
                message=f"调用OpenAI API时发生错误: {str(e)}",
                provider="openai",
                details={"model": model}
            )

    @retry_with_backoff(max_retries=3, base_delay=2, max_delay=30)
    def o1_generate(self, prompt):
        """使用o1模型生成回复，带重试机制"""
        try:
            response = self.client.chat.completions.create(
                model=os.environ["DEPLOYMENT_o1"],
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"o1模型生成失败，将重试: {str(e)}")
            raise

    @retry_with_backoff(max_retries=3, base_delay=2, max_delay=30)
    def not_o1_generate(self, system_prompt, user_prompt, temperature, model_deploy):
        """使用非o1模型生成回复，带重试机制"""
        try:
            completion = self.client.chat.completions.create(
                model=model_deploy,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.warning(f"模型 {model_deploy} 生成失败，将重试: {str(e)}")
            raise

    @retry_with_backoff(max_retries=3, base_delay=2, max_delay=30)
    def format_generate(self, system_prompt, user_prompt, model_deploy, temperature, response_format):
        """使用格式化响应生成回复，带重试机制"""
        try:
            completion = self.client.beta.chat.completions.parse(
                model=model_deploy,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                response_format=response_format,
            )
            json_output = json.loads(completion.choices[0].message.content)
            return json_output
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON响应失败: {str(e)}")
            raise LLMException(
                message="解析模型响应为JSON格式失败",
                provider="openai",
                details={"model": model_deploy}
            )
        except Exception as e:
            logger.warning(f"格式化生成失败，将重试: {str(e)}")
            raise


if __name__ == "__main__":
    # 配置测试日志
    test_logger = logging.getLogger("openai_test")
    openai_client = OpenAIClient()
    response = openai_client.generate(
        "System: Hello, how are you today?",
        "User: I'm doing well, how about you?",
        response_format=None,
        temperature=0.5,
        model=os.environ["DEPLOYMENT_4O"],
    )
    test_logger.info(f"测试响应: {response}")
