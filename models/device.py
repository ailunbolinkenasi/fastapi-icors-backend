from tortoise import fields
from tortoise.models import Model
from models.base import TimestampMixin


# 地址管理表
class Device(TimestampMixin):
    area = fields.CharField(null=True, description="设备存放地址", max_length=255)
    brand = fields.CharField(null=True, description="设备型号", max_length=255)
    physical_addr = fields.CharField(null=False, description="物理机地址", max_length=32)
    ipaddr = fields.CharField(null=False, description="IP地址", max_length=32)
    cpu = fields.CharField(null=False, description="CPU核心数量", max_length=8)
    memory = fields.CharField(null=False, description="内存数量", max_length=8)
    hard_disk = fields.CharField(null=False, description="硬盘容量", max_length=12)
    username = fields.CharField(null=False, default="root", description="服务器用户名", max_length=12)
    password = fields.CharField(null=False, default="123..com", description="服务器密码", max_length=32)
    manager = fields.CharField(null=False, default="王力鑫", description="服务器管理员", max_length=12)
    description = fields.CharField(null=True, description="描述信息", max_length=255)
