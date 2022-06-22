from dataclasses import dataclass
from pydantic import Field


# 短信登录模型
@dataclass
class Message:
    mobile_phone: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
