from dataclasses import dataclass
from pydantic import Field, BaseModel
from typing import Optional, List


# 开启自定义数据类型转换
class Config:
    arbitrary_types_allowed = True


class MonitorList(BaseModel):
    cpu_params: Optional[List] = Field(...)