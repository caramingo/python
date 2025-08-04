
Что это и зачем? 
Серверное приложение на Python, которое считает и выводит статистику выполнения кронтаб задач на ваших серверах. 

Принцип работы. 
На сервере где нужно контролировать выполнение кронтаб задачи в файле /etc/croontab в строке после самой задачи вы добавляете команду отправки курл запроса на сервер где запущен cronjob-checker. Пример как это может быть
0 23 * * * /opt/script/backup.sh  && curl http://your-server.com:8000/job-id1
где backup.sh ваш задание которое нужно контролировать 
curl http://your-server.com:8000/job-id1  сам курл запрос на сервер cronjob-checker который считает запросы.
для других задачь нужно указать любой свободный id, вот пример
0 */1 * * * /opt/script/somejob-every-hours.sh  && curl http://your-server.com:8000/job-id2

В итоге за сутки на сервер должен придти 1 курл запрос c id1 и 24 запроса с id2
В коде cron-job-checker.py можно указать нужное количество запросов по каждой джобе
Если берем пример выше то получаеться 
THRESHOLDS = {
    "job-id1": 1,
    "job-id2": 24,


Как установить?
apt install python3-pip 
pip install fastapi uvicorn jinja2 apscheduler 
С pip пакетами будте осторожны, они могу "сломать" вашу систему, возможно понадобиться ключ --break-system-packages для установки

Создайте каталог
mkdir /opt/cron-job-checker  и скопируйте в него  cron-job-checker.py

Cоздайте каталог
mkdir /opt/cron-job-checker/templates/  и скопируйте в него  stats.html 

Cозадйте systemd юнит /etc/systemd/system/cron-job-checker.service
После создания юнита выполните 
systemctl daemon-reexec && systemctl daemon-reload
systemctl enable cron-job-checker.service &&  systemctl start cron-job-checker.service

Проверьте статус systemctl status cron-job-checker.service


Как отправить тестовый запрос ? 
curl http://your-server.com:8000/job-id1

Где смотреть статистику ?
http://your-server.com:8000/
Страница без какой либо авторизации, учитывайте это. 
