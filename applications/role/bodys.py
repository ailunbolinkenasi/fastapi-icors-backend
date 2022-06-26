from pydantic import Field,BaseModel
from typing import Optional, List


# 角色分配模型
class SetRole(BaseModel):
    id: int
    roles: Optional[List[int]] = Field(default=[], description="角色")
