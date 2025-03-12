import time
import datetime
import psutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tinydb import TinyDB, Query

# Створюємо або відкриваємо базу даних
db = TinyDB('system_metrics.json')

def collect_metrics():
    """Збирає метрики продуктивності та зберігає їх у TinyDB."""
    timestamp = time.time()  # Час у секундах (Unix timestamp)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    db.insert({'timestamp': timestamp, 'cpu': cpu, 'ram': ram, 'disk': disk})

def get_last_minute_data():
    """Отримує дані за останню хвилину."""
    one_minute_ago = time.time() - 60
    return db.search(Query().timestamp >= one_minute_ago)

def plot_metrics():
    """Будує графік продуктивності системи за останню хвилину."""
    data = get_last_minute_data()
    if not data:
        print("Немає даних для відображення.")
        return

    # Конвертуємо час у зрозумілий формат
    timestamps = [datetime.datetime.fromtimestamp(entry['timestamp']) for entry in data]
    cpu_values = [entry['cpu'] for entry in data]
    ram_values = [entry['ram'] for entry in data]
    disk_values = [entry['disk'] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_values, label='CPU (%)', marker='o', linestyle='-')
    plt.plot(timestamps, ram_values, label='RAM (%)', marker='s', linestyle='-')
    plt.plot(timestamps, disk_values, label='Disk (%)', marker='^', linestyle='-')

    plt.xlabel('Час')
    plt.ylabel('Завантаження (%)')
    plt.legend()
    plt.title('Продуктивність системи за останню хвилину')
    plt.grid()

    # Форматуємо вісь часу для правильного відображення
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gcf().autofmt_xdate()  # Автоматичне обертання підписів часу

    plt.show()

# Головний цикл збору даних
try:
    print("Збираю дані... (натисни Ctrl+C для побудови графіка)")
    while True:
        collect_metrics()
        time.sleep(5)  # Збираємо дані кожні 5 секунд
except KeyboardInterrupt:
    print("\nЗупинка збору даних. Будую графік...")
    plot_metrics()
