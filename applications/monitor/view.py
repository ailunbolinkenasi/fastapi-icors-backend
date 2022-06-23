import psutil

from applications.monitor.bodys import MonitorList


async def get_cpu():
    # 获取CPU占比
    cpu_percent = psutil.cpu_percent(percpu=True)
    # 获取CPU总核心数
    logical_cpus = psutil.cpu_count()

    data = MonitorList(
        cpu_params=cpu_percent,
        logical_cpus=logical_cpus
    )
    return data
