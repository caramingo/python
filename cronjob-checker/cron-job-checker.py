
# Импорт необходимых библиотек
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading

# Инициализация FastAPI-приложения
app = FastAPI()

# Указание папки с шаблонами HTML (для отображения статистики)
templates = Jinja2Templates(directory="templates")

# Словарь для хранения количества запросов по каждому job_id
request_counts = {}

# Блокировка для потокобезопасного доступа к request_counts
request_lock = threading.Lock()

# 🔧 Индивидуальные пороговые значения для каждого job_id
THRESHOLDS = {
    "job-id1": 2,
    "job-id2": 4,
    "job-id3": 1,
}

# Обработка входящих запросов вида /job-idX
@app.get("/{job_id}")
def count_job_id(job_id: str):
    # Игнорируем запрос к favicon.ico, который браузер может отправлять автоматически
    if job_id == "favicon.ico":
        return {"message": "Ignored"}

    # Увеличиваем счётчик запросов по данному job_id (в потокобезопасном режиме)
    with request_lock:
        request_counts[job_id] = request_counts.get(job_id, 0) + 1

    # Возвращаем текущее значение счётчика
    return {"message": f"Counted job ID: {job_id}", "total": request_counts[job_id]}

# Главная страница, отображающая HTML-таблицу со статистикой
@app.get("/", response_class=HTMLResponse)
def stats_page(request: Request):
    with request_lock:
        data = {}
        for job_id, count in request_counts.items():
            threshold = THRESHOLDS.get(job_id)

            # Определяем статус:
            # "OK" — если count == threshold
            # "WARN" — если count < threshold или count > threshold
            # "UNKNOWN" — если threshold не задан
            if threshold is None:
                status = "UNKNOWN"
            elif count == threshold:
                status = "OK"
            else:
                status = "WARN"

            # Сохраняем данные для отображения в таблице
            data[job_id] = {
                "count": count,
                "threshold": threshold,
                "status": status
            }

    # Возвращаем HTML-шаблон со статистикой
    return templates.TemplateResponse("stats.html", {
        "request": request,
        "stats": data,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Функция сброса статистики (обнуляет все счётчики)
def reset_counts():
    with request_lock:
        request_counts.clear()
    print(f"[{datetime.now()}] Статистика сброшена.")

# Создание планировщика задач и добавление ежедневного сброса в 23:59
scheduler = BackgroundScheduler()
scheduler.add_job(reset_counts, trigger='cron', hour=23, minute=59)
scheduler.start()

# Остановка планировщика при завершении работы приложения
import atexit
atexit.register(lambda: scheduler.shutdown())
