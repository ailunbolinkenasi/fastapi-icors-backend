import psutil
from fastapi import HTTPException
from applications.monitor.bodys import MonitorList


async def get_monitor_data():
    # 获取CPU占比
    cpu_percent = psutil.cpu_percent(percpu=True)
    # 获取CPU总核心数
    logical_cpus = psutil.cpu_count()

    # 获取内存
    use_memory = psutil.virtual_memory()
    THRESHOLD = 100 * 1024 * 1024  # 100MB
    # 如果请求接口的时候发现内存小于等于100m直接抛异常
    if use_memory.available <= THRESHOLD:
        raise HTTPException(status_code=400, detail="服务器内存即将用满,请及时清理内存.")
    data = {
        "cpu_percent": cpu_percent,
        "cpu_number": logical_cpus,
        "memory_total": round(use_memory.total / 1024000000, 2),
        "used_memory": round(use_memory.used / 1024000000, 2)
    }
    return data
