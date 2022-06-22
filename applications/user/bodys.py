from typing import Optional, List
from pydantic import EmailStr, Field
from dataclasses import dataclass


@dataclass
class BaseBody:
    class Config:
        anystr_strip_whitespace = True


@dataclass
class SmsBody:
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    sms_code: str = Field(..., description="短信验证码", min_length=6, max_length=6)


# 用户基础模型
@dataclass
class UserBodyBase(BaseBody):
    username: str = Field(..., description="用户名", min_length=4, max_length=32)
    password: str = Field(..., description="用户密码", min_length=8)


# 注册模型
@dataclass
class RegisterBody(UserBodyBase):
    email: EmailStr = Field(..., description="用户邮箱")
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    login_host: Optional[str] = "127.0.0.1"


# 返回用户信息模型
@dataclass
class UserInfo:
    id: int
    username: str
    mobile_phone: str
    email: str
    is_activate: bool = Field(..., description="用户是否激活")


# 创建用户模型
@dataclass
class CreateUser(UserBodyBase):
    email: EmailStr = Field(..., description="用户邮箱")
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    is_activate: bool = Field(..., description="是否激活用户")


# 更新用户模型
@dataclass
class UpdateUser:
    username: Optional[str] = Field(min_length=4, max_length=15)
    password: Optional[str] = Field(min_length=8, max_length=255)
    email: Optional[EmailStr] = Field(..., description="修改后的邮箱")
    mobile_phone: Optional[str] = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    is_activate: Optional[bool] = Field(..., description="是否激活用户")
