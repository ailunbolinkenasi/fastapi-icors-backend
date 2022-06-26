from tortoise import fields
from tortoise.models import Model


class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True


# 角色表
class Role(TimestampMixin):
    role_name = fields.CharField(max_length=15, description="角色名称")
    user: fields.ManyToManyRelation["User"] = fields.ManyToManyField("base.User", related_name="role",
                                                                     on_delete=fields.CASCADE)
    access: fields.ManyToManyRelation["Access"] = fields.ManyToManyField("base.Access", related_name="role",
                                                                         on_delete=fields.CASCADE)
    role_status = fields.BooleanField(default=False, description="True:启用 False:禁用")
    role_desc = fields.CharField(null=True, max_length=255, description='角色描述')

    class Meta:
        table_description = "角色表"
        table = "role"


# 用户表
class User(TimestampMixin):
    role: fields.ManyToManyRelation[Role]
    username = fields.CharField(unique=True, null=False, min_length=5, max_length=32, description="用户名")
    password = fields.CharField(null=False, min_length=8, max_length=255)
    mobile_phone = fields.CharField(unique=True, null=False, description="手机号", max_length=11)
    email = fields.CharField(unique=True, null=False, description='邮箱', max_length=32)
    full_name = fields.CharField(null=True, description='姓名', max_length=15)
    is_activate = fields.BooleanField(default=0, description='0未激活 1正常 2禁用')
    is_staff = fields.BooleanField(default=False, description="用户类型 True:超级管理员 False:普通管理员")
    header_img = fields.CharField(null=True, max_length=255, description='用户头像')
    sex = fields.IntField(default=0, null=True, description='0未知 1男 2女')
    login_host = fields.CharField(null=True, max_length=15, description="访问IP")

    # 返回用户名默认
    def __str__(self):
        return self.username

    class Meta:
        table_description = "用户表"
        table = "user"


# 权限表
class Access(TimestampMixin):
    role: fields.ManyToManyRelation[Role]
    access_name = fields.CharField(max_length=15, description="权限名称")
    parent_id = fields.IntField(default=0, description='父id')
    scopes = fields.CharField(unique=True, max_length=255, description='权限范围标识')
    access_desc = fields.CharField(null=True, max_length=255, description='权限描述')
    menu_icon = fields.CharField(null=True, max_length=255, description='菜单图标')
    is_check = fields.BooleanField(default=False, description='是否验证权限 True为验证 False不验证')
    is_menu = fields.BooleanField(default=False, description='是否为菜单 True菜单 False不是菜单')

    def __str__(self):
        return self

    class Meta:
        table_description = "权限表"
        table = "access"


# 访问日志
class AccessLog(TimestampMixin):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("base.User", related_name="events")
    target_url = fields.CharField(null=True, description="访问的url", max_length=255)
    user_agent = fields.CharField(null=True, description="访问UA", max_length=255)
    request_params = fields.JSONField(null=True, description="请求参数get|post")
    ip = fields.CharField(null=True, max_length=32, description="访问IP")
    note = fields.CharField(null=True, max_length=255, description="备注")

    class Meta:
        table_description = "用户操作记录表"
        table = "access_log"
