from markitdown import MarkItDown
import pandas as pd
import os
import logging
from service.core.exceptions import FileReadException, DataProcessingException

# 配置日志
logger = logging.getLogger("read_data")

class ReadData:
    def __init__(self):
        self.markitdown = MarkItDown()
        logger.info("文件读取工具初始化完成")
        
    def read(self, file_path):
        """读取文件内容"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                raise FileReadException(
                    file_path=file_path,
                    details={"error": "文件不存在"}
                )
                
            # 获取文件扩展名
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            logger.info(f"读取文件: {file_path}")
            
            try:
                # 使用 MarkItDown 读取文件
                content = self.markitdown.convert(file_path).text_content
                
                if not content.strip():
                    logger.warning(f"文件内容为空: {file_path}")
                
                return content
            except Exception as e:
                logger.error(f"读取文件失败: {str(e)}")
                raise FileReadException(
                    file_path=file_path,
                    details={"error": f"读取文件失败: {str(e)}"}
                )
                
        except FileReadException:
            # 已经是文件读取异常，直接抛出
            raise
        except Exception as e:
            # 其他未知异常
            logger.error(f"读取文件时发生未知错误: {str(e)}")
            raise FileReadException(
                file_path=file_path,
                details={"error": str(e)}
            )
    
    def read_csv(self, file_path):
        """读取CSV文件内容"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"CSV文件不存在: {file_path}")
                raise FileReadException(
                    file_path=file_path,
                    details={"error": "文件不存在"}
                )
                
            # 检查文件扩展名
            _, ext = os.path.splitext(file_path)
            if ext.lower() != '.csv':
                logger.warning(f"文件扩展名不是.csv: {file_path}")
            
            logger.info(f"读取CSV文件: {file_path}")
            
            try:
                # 使用 pandas 读取 CSV 文件
                df = pd.read_csv(file_path)
                
                if df.empty:
                    logger.warning(f"CSV文件内容为空: {file_path}")
                else:
                    logger.info(f"成功读取CSV文件，包含 {len(df)} 行数据")
                
                return df
            except pd.errors.EmptyDataError:
                logger.warning(f"CSV文件为空: {file_path}")
                return pd.DataFrame()
            except Exception as e:
                logger.error(f"读取CSV文件失败: {str(e)}")
                raise FileReadException(
                    file_path=file_path,
                    details={"error": f"读取CSV文件失败: {str(e)}"}
                )
                
        except FileReadException:
            # 已经是文件读取异常，直接抛出
            raise
        except Exception as e:
            # 其他未知异常
            logger.error(f"读取CSV文件时发生未知错误: {str(e)}")
            raise FileReadException(
                file_path=file_path,
                details={"error": str(e)}
            )
