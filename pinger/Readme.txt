Простая утилита для проверки интернета, создана для графической среды под линукс

Результат мониторинга выводиться в виде зеленой или красной иконке в трее.

Для установки нужен сам скрипт на питоне pinger.py и systemd юнит который управляет его работой. 

В скрипте для проверки интернета указан хост ya.ru в строке  ip = "ya.ru" можешь заминить на свой

В pinger.service измени путь к файлу pinger.py и  имя пользователя в примере указан /home/username/

Для работы нужно установить 
pip install psutil pystray pillow

Нужно создать systemd юнит /etc/systemd/system/pinger.service
После создания юнита  выполни 
systemctl daemon-reload
systemctl start pinger.service


Для дебага состояния
systemctl status  pinger.service
journalctl -u pinger.service
