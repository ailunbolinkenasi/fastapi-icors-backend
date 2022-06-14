from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# 地址管理入参模型


# 基础的基础
class BaseBody(BaseModel):
    class Config:
        anystr_strip_whitespace = True


# 添加主机
class AddHost(BaseModel):
    physical_addr: str = Field(..., description="服务器硬件地址", max_length=32)
    ipaddr: str = Field(..., description="IP地址", max_length=32)
    cpu: str = Field(..., description="CPU核心数量", max_length=8)
    memory: str = Field(..., description="内存容量", max_length=8)
    hard_disk: str = Field(..., description="硬盘容量", max_length=8)
    username: str = Field(..., description="服务器用户名", max_length=12)
    password: str = Field(..., description="服务器密码", max_length=32)
    manager: str = Field(..., description="管理者", max_length=12)


# 更新主机
# class UpdateHost(BaseModel):
#     physical_addr: str = Field(..., description="服务器硬件地址", max_length=32)
#     ipaddr: str = Field(..., description="IP地址", max_length=32)
#     cpu: str = Field(..., description="CPU核心数量", max_length=8)
#     memory: str = Field(..., description="内存容量", max_length=8)
#     hard_disk: str = Field(..., description="硬盘容量", max_length=8)
#     username: Optional[str] = Field(..., description="服务器用户名", max_length=12)
#     password: Optional[str] = Field(..., description="服务器密码", max_length=32)
#     manager: Optional[str] = Field(..., description="管理者", max_length=12)
