from pydantic import Field, BaseModel
from typing import Optional, List
from .base import BaseResp


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=10,description="用户名")
    password: str = Field(min_length=6, max_length=20,description="用户密码")
    user_phone: str = Field(regex="^1[34567890]\\d{9}$",description="手机号")
    user_status: Optional[bool]
    remarks: Optional[str]


class AccountLogin(BaseModel):
    username: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=6, max_length=20)


class UserInfo(BaseModel):
    username: str
    age: Optional[int]
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    user_status: bool
    header_img: Optional[str]
    sex: int


class UserListItem(BaseModel):
    key: int
    username: str
    age: Optional[int]
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    user_status: bool
    header_img: Optional[str]
    sex: int
    remarks: Optional[str]


class CurrentUser(BaseResp):
    data: UserInfo


class AccessToken(BaseModel):
    token: Optional[str]
    expires_in: Optional[int]


class UserLogin(BaseResp):
    data: AccessToken


class ResAntTable(BaseModel):
    success: bool
    data: List
    total: int


class UserListData(ResAntTable):
    data: List[UserListItem]