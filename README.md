# 🛒 E-Commerce Service: Readiness & Standardization
> **Lab 0** — Інфраструктурна підготовка застосунку за стандартами MLOps / DevOps. Застосунок розроблено як "Black Box", що повністю відповідає методології **12-Factor App**.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)
![Status](https://img.shields.io/badge/Status-Commerce--Ready-success.svg)

---

## 🛠 1. Налаштування та запуск (Phase 1)

### 🔑 Змінні оточення (Environment Variables)
Конфігурація застосунку повністю ізольована від коду. Для запуску сервісу необхідно експортувати такі змінні (або створити файл `.env` у корені проєкту):

```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="ecommerce"
export DB_USER="postgres"
export DB_PASSWORD="your_secure_password"
🚀 Запуск однією командою (One-Command Build)
Встановлення залежностей та запуск юніт-тестів виконується стандартними командами:

Bash
# 1. Встановлення залежностей
pip install -r requirements.txt

# 2. Запуск тестів однією командою
pytest
Примітка щодо міграцій БД: Застосунок підтримує автоматичне керування схемою даних за допомогою Alembic. Під час кожного старту сервіс самостійно перевіряє та застосовує нові міграції перед підняттям HTTP-сервера.

🚀 2. Перевірка Production-Grade фіч (Phase 2)
🏥 Глибока перевірка стану (Dependency-Aware Health Check)
Сервіс повертає статус 200 OK тільки за умови успішного ping-запиту до бази даних. Якщо БД недоступна — повертається статус 503 Service Unavailable.

Варіант А: База даних підключена (200 OK)
Bash
curl -i http://localhost:8000/health
<img width="390" height="191" alt="image" src="https://github.com/user-attachments/assets/f75f22eb-2863-4c3b-afcb-14aab8e6bb4c" />


Варіант Б: База даних вимкнена (503 Service Unavailable)
Bash
curl -i http://localhost:8000/health
<img width="1321" height="309" alt="image" src="https://github.com/user-attachments/assets/c0f901e8-06dc-4751-a1e5-9b623f4e1864" />


📝 Структуроване логування в JSON
Усі логи застосунку стандартизовано під формат JSON для подальшого збору системами моніторингу (ELK / Prometheus / Grafana Loki) та виводяться безпосередньо у STDOUT.

Приклад логів під час запуску (ініціалізація та міграції):

JSON
[ВСТАВ СЮДИ РЕАЛЬНІ РЯДКИ ЛОГІВ З ТЕРМІНАЛА, НАПРИКЛАД:]
{"asctime": "2026-05-19 15:30:12,145", "levelname": "INFO", "message": "Application starting up..."}
{"asctime": "2026-05-19 15:30:13,012", "levelname": "INFO", "message": "Running automatic DB migrations..."}
🛑 Плавне завершення роботи (Graceful Shutdown)
Застосунок коректно обробляє сигнал очікування завершення SIGTERM (або SIGINT), логує процес зупинки, закриває пули з'єднань з базою даних без розриву активних транзакцій та завершує роботу з кодом 0.
<img width="1321" height="309" alt="image" src="https://github.com/user-attachments/assets/e7f7ac13-9b57-49b7-8c2d-b023f6eb5d26" />

Логи завершення роботи:

JSON
{"asctime": "2026-05-19 15:32:00,501", "levelname": "INFO", "message": "SIGTERM received. Starting graceful shutdown..."}
{"asctime": "2026-05-19 15:32:00,502", "levelname": "INFO", "message": "Closing all database connections..."}
{"asctime": "2026-05-19 15:32:01,503", "levelname": "INFO", "message": "Graceful shutdown complete. Exiting with code 0."}
Сервіс повністю готовий до деплою в кластер (Commerce-Ready).
