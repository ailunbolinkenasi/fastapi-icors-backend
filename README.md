# 一个简单的项目管理系统
> 后续打算使用`TDesignStarter`作为项目的前端了 [官网](https://tdesign.tencent.com/react/overview)
- [x] 登录、注册功能
- [x] 短信接口功能
- [ ] 设备管理地址功能
- [ ] 添加、删除、更新、查询用户功能

后续打算一点一点的更新了,因为初学`FastAPI`也不太会前端,所以会相当的慢！

当然了,本项目也可以作为初学者新入门FastAPI的教程文本

## 配置部分
配置文件存放`core/Config.py`配置文件中,项目目录后续在更新吧.
```python
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
    VERSION: str = "0.0.1" # 填写你的项目版本
    PROJECT_NAME: str = " FastAPI-Demo" # 填写你的项目名称
    DESCRIPTION: str = '服务的API接口文档' # 项目描述
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
    JWT_SECRET_KEY = "" # 填写你的JWK_KEY
    JWT_ALGORITHM = "HS256" 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
    SWAGGER_UI_OAUTH2_REDIRECT_URL = "/v1/oath2"

    # 阿里云短信配置
    ALIYUN_ACCESSKEY_ID = "" # 填写阿里云API的ACCESS_KEY_ID
    ALIYUN_ACCESSKEY_SECRET = "" # 填写阿里云API的ACCESS_KEY_SECRET
    ALIYUN_SIGN_NAME = '' # 填写阿里云短信签名


settings = Config()
```