# 一个简单的项目管理系统
> 后续打算使用`TDesignStarter`作为项目的前端了 [官网](https://tdesign.tencent.com/react/overview)
- [x] 登录、注册功能
- [x] 短信接口功能
- [ ] 设备管理地址功能
- [ ] 添加、删除、更新、查询用户功能

后续打算一点一点的更新了,因为初学`FastAPI`也不太会前端,所以会相当的慢！

当然了,本项目也可以作为初学者新入门FastAPI的教程文本

## 项目配置部分
配置文件存放`core/Config.py`配置文件中.
```python
# 阿里云短信配置
ALIYUN_ACCESSKEY_ID = "" # 填写阿里云API的ACCESS_KEY_ID
ALIYUN_ACCESSKEY_SECRET = "" # 填写阿里云API的ACCESS_KEY_SECRET
ALIYUN_SIGN_NAME = '' # 填写阿里云短信签名

# 填写你生成带的JTW_KEY
JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60 # 过期时间
SWAGGER_UI_OAUTH2_REDIRECT_URL = "/v1/oath2"  # 请求oath2的地址
```