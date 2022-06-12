import hashlib
import uuid
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional, Union, List
from core.config import settings
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models

# 推荐的算法是 Bcrypt
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# 生成随机字符串函数
def random_str():
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)


# 加密密码函数
def hash_password(password: str) -> str:
    """
    :param password:  需要加密的密码
    :return:
    """
    return pwd_context.hash(password)


# 校验密码函数
def verify_password(plain_password: str, hash_password: str) -> bool:
    """
    :param plain_password: 明文密码
    :param hash_password:  hash密码
    :return:
    """
    return pwd_context.verify(plain_password, hash_password)


# 创建阿里云短信client
def create_client(
        access_key_id: str = settings.ALIYUN_ACCESSKEY_ID,
        access_key_secret: str = settings.ALIYUN_ACCESSKEY_SECRET,
) -> Dysmsapi20170525Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    print(access_key_id)
    config = open_api_models.Config(
        # 您的AccessKey ID,
        access_key_id=access_key_id,
        # 您的AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'dysmsapi.aliyuncs.com'
    return Dysmsapi20170525Client(config)
