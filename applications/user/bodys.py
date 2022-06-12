from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# 入参模型

# 基础的基础
class BaseBody(BaseModel):
    class Config:
        anystr_strip_whitespace = True


# 短信登录模型
class SmsBody(BaseModel):
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    sms_code: str = Field(..., description="短信验证码", min_length=6, max_length=6)


# 用户基础模
class UserBodyBase(BaseBody):
    username: str = Field(..., description="用户名", min_length=5, max_length=15)
    password: str = Field(..., description="用户密码", min_length=8)


# 注册模型
class RegisterBody(UserBodyBase):
    email: EmailStr = Field(..., description="用户邮箱")
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    login_host: Optional[str] = "127.0.0.1"


# 登录校验模型
class UserAuth(UserBodyBase):
    pass


# 返回用户信息模型
class UserInfo(BaseModel):
    id: int
    username: str
    mobile_phone: str
    email: str
    is_active: str = Field(..., description="用户是否激活")
