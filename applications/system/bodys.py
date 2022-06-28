from typing import Optional
from ipaddress import IPv4Address
from pydantic import Field, BaseModel

# 地址管理入参模型


# 添加主机
class AddHost(BaseModel):
    # physical_addr: IPv4Address = Field(..., description="服务器硬件地址")
    # ipaddr: str = Field(..., description="IP地址", max_length=32)
    physical_addr: IPv4Address = Field(..., description="物理机地址")
    ipaddr: IPv4Address = Field(..., description="虚拟机IP地址")
    cpu: str = Field(..., description="CPU核心数量", max_length=8)
    memory: str = Field(..., description="内存容量", max_length=8)
    hard_disk: str = Field(..., description="硬盘容量", max_length=8)
    username: str = Field(..., description="服务器用户名", max_length=12)
    password: str = Field(..., description="服务器密码", max_length=32)
    manager: str = Field(..., description="管理者", max_length=12)


# 更新主机
class UpdateHost(BaseModel):
    physical_addr: IPv4Address = Field(..., description="物理机地址")
    ipaddr: IPv4Address = Field(..., description="虚拟机IP地址")
    cpu: str = Field(..., description="CPU核心数量", max_length=8)
    memory: str = Field(..., description="内存容量", max_length=8)
    area: str = Field(..., description="服务器所在地区", max_length=255)
    brand: str = Field(..., description="服务器型号", max_length=255)
    hard_disk: str = Field(..., description="硬盘容量", max_length=8)
    username: Optional[str] = Field(..., description="服务器用户名", max_length=12)
    password: Optional[str] = Field(..., description="服务器密码", max_length=32)
    manager: Optional[str] = Field(..., description="管理者", max_length=12)
