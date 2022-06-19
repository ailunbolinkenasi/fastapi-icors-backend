import os
# from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings
from typing import List


class Config(BaseSettings):
    # 加载环境变量
    # load_dotenv(find_dotenv(), override=True)
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "icors设备管理系统接口文档"
    DESCRIPTION: str = '服务的API接口文档'
    # 静态资源目录
    # STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    # TEMPLATE_DIR: str = os.path.join(STATIC_DIR, "templates")
    # 跨域请求
    CORS_ORIGINS: List = ["http://localhost:3003"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]
    # Session
    SECRET_KEY = "session"
    SESSION_COOKIE = "session_id"
    SESSION_MAX_AGE = 14 * 24 * 60 * 60
    # Jwt秘钥
    JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
    SWAGGER_UI_OAUTH2_REDIRECT_URL = "/v1/oath2"

    # 阿里云短信配置
    ALIYUN_ACCESSKEY_ID = ''
    ALIYUN_ACCESSKEY_SECRET = ''
    ALIYUN_SIGN_NAME = ''


settings = Config()
