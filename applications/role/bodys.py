from pydantic import Field
from typing import Optional, List
from dataclasses import dataclass


# 角色分配模型
@dataclass
class SetRole:
    id: int
    roles: Optional[List[int]] = Field(default=[], description="角色")
