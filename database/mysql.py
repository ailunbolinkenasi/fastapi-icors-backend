from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os

# -----------------------数据库配置-----------------------------------
DB_ORM_CONFIG = {
    "connections": {
        "base": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': os.getenv('BASE_HOST', ''),
                'user': os.getenv('BASE_USER', ''),
                'password': os.getenv('BASE_PASSWORD', ''),
                'port': int(os.getenv('BASE_PORT', )),
                'database': os.getenv('BASE_DB', ''),
            }
        },
        # "db2": {
        #     'engine': 'tortoise.backends.mysql',
        #     "credentials": {
        #         'host': os.getenv('DB2_HOST', '127.0.0.1'),
        #         'user': os.getenv('DB2_USER', 'root'),
        #         'password': os.getenv('DB2_PASSWORD', '123456'),
        #         'port': int(os.getenv('DB2_PORT', 3306)),
        #         'database': os.getenv('DB2_DB', 'db2'),
        #     }
        # },
        # "db3": {
        #     'engine': 'tortoise.backends.mysql',
        #     "credentials": {
        #         'host': os.getenv('DB3_HOST', '127.0.0.1'),
        #         'user': os.getenv('DB3_USER', 'root'),
        #         'password': os.getenv('DB3_PASSWORD', '123456'),
        #         'port': int(os.getenv('DB3_PORT', 3306)),
        #         'database': os.getenv('DB3_DB', 'db3'),
        #     }
        # },

    },
    "apps": {
        "base": {"models": ["models.base","models.device"], "default_connection": "base"},
        # "db2": {"models": ["models.db2"], "default_connection": "db2"},
        # "db3": {"models": ["models.db3"], "default_connection": "db3"}
    },
    'use_tz': True,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    # 注册数据库
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,  # 注册MySQL配置文件
        generate_schemas=False,  # 判断表是否存在,如果不存在就创建
        add_exception_handlers=True,  # 开启异常处理
    )
