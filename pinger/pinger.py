import time
import subprocess
from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading
import os

# Функция для проверки доступности IP-адреса с использованием ping
def check_ip(ip):
    try:
        # Команда ping с тайм-аутом 1 секунда и 1 попыткой
        result = subprocess.run(['ping', '-c', '1', '-W', '2', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка при попытке пинга: {e}")
        return False

# Функция для загрузки иконки из файла
def load_icon(path):
    try:
        return Image.open(path)
    except Exception as e:
        print(f"Ошибка при загрузке иконки '{path}': {e}")
        return None

# Функция для обновления состояния в трее
def update_icon(icon, icons):
    ip = "ya.ru"
    while True:
        if check_ip(ip):
            icon.icon = icons['green']
        else:
            icon.icon = icons['red']
        time.sleep(1)

# Функция для закрытия приложения
def on_quit(icon, item):
    icon.stop()

# Основная функция
def main():
    # Загрузка иконок
    red_icon = load_icon('red.ico')
    green_icon = load_icon('green.ico')
    if not red_icon or not green_icon:
        print("Не удалось загрузить иконки. Убедитесь, что файлы 'red.ico' и 'green.ico' находятся в каталоге скрипта.")
        return

    icons = {
        'red': red_icon,
        'green': green_icon
    }

    icon = Icon("IP_Checker", red_icon, menu=Menu(MenuItem('Quit', on_quit)))

    # Запуск обновления иконки в отдельном потоке
    threading.Thread(target=update_icon, args=(icon, icons), daemon=True).start()

    icon.run()

if __name__ == '__main__':
    main()
