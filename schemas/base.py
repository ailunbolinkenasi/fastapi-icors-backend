from pydantic import BaseModel, Field


class BaseResp(BaseModel):
    code: int = Field(description="状态码")
    message: str = Field(description="信息")