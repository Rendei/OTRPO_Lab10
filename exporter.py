import os
import psutil
from prometheus_client import start_http_server, Gauge
import time

# Определяем переменные окружения для хоста и порта
EXPORTER_HOST = os.getenv('EXPORTER_HOST', '0.0.0.0')
EXPORTER_PORT = int(os.getenv('EXPORTER_PORT', 8080))

# Создаём метрики
cpu_usage_per_core = Gauge('cpu_usage_percent_per_core', 'CPU Usage in Percent per Core', ['core'])
cpu_usage_total = Gauge('cpu_usage_percent', 'CPU Usage in Percent')

memory_used = Gauge('memory_used', 'Used system memory in bytes')

disk_total = Gauge('disk_total', 'Total disk space in bytes', ['disk'])
disk_used = Gauge('disk_used', 'Used disk space in bytes', ['disk'])

def collect_metrics():
    # Получаем информацию о процессорах
    for i, percent in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_usage_per_core.labels(core=f'core_{i}').set(percent)

    cpu_usage_total.set(psutil.cpu_percent())

    # Получаем информацию о памяти
    memory = psutil.virtual_memory()    
    memory_used.set(memory.used)

    # Получаем информацию о дисках
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            print(partition.device)
            disk = psutil.disk_usage(partition.mountpoint)
            disk_total.labels(disk=partition.device).set(disk.total)
            disk_used.labels(disk=partition.device).set(disk.used)
        except PermissionError:
            # Игнорируем разделы, к которым нет доступа
            continue

if __name__ == '__main__':
    start_http_server(EXPORTER_PORT, addr=EXPORTER_HOST)
    while True:
        collect_metrics()
        time.sleep(10)
