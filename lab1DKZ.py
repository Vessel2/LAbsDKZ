import os
import platform
import psutil
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def get_system_info():
    table = Table(title="Системна інформація")
    table.add_column("Параметр", style="cyan", no_wrap=True)
    table.add_column("Значення", style="magenta")
    
    table.add_row("Дата та час", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    table.add_row("ОС", platform.system() + " " + platform.release())
    table.add_row("Процесор", platform.processor())
    table.add_row("Кількість ядер", str(psutil.cpu_count(logical=False)))
    table.add_row("Кількість потоків", str(psutil.cpu_count(logical=True)))
    
    ram = psutil.virtual_memory()
    table.add_row("Оперативна пам'ять", f"{ram.total / (1024 ** 3):.2f} GB")
    
    cpu_load = psutil.cpu_percent(interval=1)
    table.add_row("Завантаження CPU", f"{cpu_load} %")
    
    disk_info = "".join([f"{d.device} {d.mountpoint} ({d.fstype}) - {psutil.disk_usage(d.mountpoint).percent}%\n" for d in psutil.disk_partitions()])
    table.add_row("Диски", disk_info.strip())
    
    return table

if __name__ == "__main__":
    try:
        while True:
            console.clear()
            console.print(get_system_info())
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("[bold red]Моніторинг завершено.[/bold red]")
