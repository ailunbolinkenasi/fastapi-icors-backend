from dataclasses import dataclass
from pydantic import Field, BaseModel
from typing import Optional, List, Dict


# 开启自定义数据类型转换
class Config:
    arbitrary_types_allowed = True


class MonitorList(BaseModel):
    cpu_percent: str = Field(..., description="CPU百分比使用率")
    cpu_count: str = Field(..., description="CPU核心数")
