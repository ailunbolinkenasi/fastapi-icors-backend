# 一个简单的项目管理系统
> 目前使用`Arco Work`作为项目的前端 - 附带浏览地址: [点我浏览](http://arco.vueadminwork.com/)
- [x] 短信登录、普通登录、注册功能完成
- [x] 添加、删除、更新、查询用户功能基本完成
- [x] 添加、删除、更新、查询服务器信息基本完成
- [ ] 权限设计
> 当然了,本项目也可以作为初学者新入门FastAPI的项目入门.


## 接口文档地址
[接口文档内容](https://www.apifox.cn/apidoc/shared-349ef5f3-5f31-4e31-84cd-4338af320691/api-25025731)

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