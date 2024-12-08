import os
import psutil
from prometheus_client import start_http_server, Gauge
import time

# Определяем переменные окружения для хоста и порта
EXPORTER_HOST = os.getenv('EXPORTER_HOST', '0.0.0.0')
EXPORTER_PORT = int(os.getenv('EXPORTER_PORT', 8080))

# Создаём метрики
cpu_usage = Gauge('cpu_usage_percent', 'CPU Usage in Percent')
memory_total = Gauge('memory_total', 'Total system memory in bytes')
memory_used = Gauge('memory_used', 'Used system memory in bytes')
disk_total = Gauge('disk_total', 'Total disk space in bytes')
disk_used = Gauge('disk_used', 'Used disk space in bytes')

def collect_metrics():
    # Получаем информацию о процессорах
    cpu_usage.set(psutil.cpu_percent())

    # Получаем информацию о памяти
    memory = psutil.virtual_memory()
    memory_total.set(memory.total)
    memory_used.set(memory.used)

    # Получаем информацию о дисках
    disk = psutil.disk_usage('/')
    disk_total.set(disk.total)
    disk_used.set(disk.used)

if __name__ == '__main__':
    start_http_server(EXPORTER_PORT, addr=EXPORTER_HOST)
    while True:
        collect_metrics()
        time.sleep(10)
