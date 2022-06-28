from dataclasses import dataclass
from pydantic import Field, BaseModel
from typing import Optional, List



# 开启自定义数据类型转换
class Config:
    arbitrary_types_allowed = True


# 短信登录模型
@dataclass
class Message:
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
