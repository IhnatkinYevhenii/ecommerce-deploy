# ecommerce-deploy
# E-Commerce Application — Lab 0 (Readiness & Standardization)

### 1. Налаштування змінних оточення (Environment Variables)
Для запуску застосунку необхідно експортувати такі змінні:
```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="ecommerce"
export DB_USER="postgres"
export DB_PASSWORD="your_secure_password"

2. Підтвердження Health Check (Deep Health Check)
БД підключена (200 OK):
[СЮДИ ВСТАВ СКРИНШОТ: Результат команди curl -i localhost:8000/health]
Очікувана відповідь: HTTP/1.1 200 OK, {"status": "UP", "database": "CONNECTED"}

БД вимкнена (503 Service Unavailable):
[СЮДИ ВСТАВ СКРИНШОТ: Зупини докер з БД docker stop <db_container> і знову зроби curl -i localhost:8000/health]
Очікувана відповідь: HTTP/1.1 503 Service Unavailable, {"status": "DOWN", "database": "DISCONNECTED"}

3. Приклад структурованих логів у форматі JSON
Рядки з логів під час старту застосунку:

JSON
{"asctime": "2026-05-19 15:15:00,000", "levelname": "INFO", "message": "Application starting up..."}
{"asctime": "2026-05-19 15:15:01,123", "levelname": "INFO", "message": "Running automatic DB migrations..."}
4. Підтвердження Плавного завершення роботи (Graceful Shutdown)
[СЮДИ ВСТАВ СКРИНШОТ: Логи в терміналі після того, як ти відправив у іншому вікні kill -15 <PID>]

Логи під час завершення:

JSON
{"asctime": "2026-05-19 15:16:42,456", "levelname": "INFO", "message": "SIGTERM received. Starting graceful shutdown..."}
{"asctime": "2026-05-19 15:16:42,457", "levelname": "INFO", "message": "Closing all database connections..."}
{"asctime": "2026-05-19 15:16:43,458", "levelname": "INFO", "message": "Graceful shutdown complete. Exiting with code 0."}

---

### Як це швидко протестувати для скриншотів:
1. Запусти застосунок: `uvicorn main:app --port 8000`
2. Зроби запит для першого скриншоту: `curl -i http://localhost:8000/health`
3. Зупини свою локальну базу даних і зроби запит ще раз для другого скриншоту.
4. Дізнайся PID процесу увікорна (`ps aux | grep uvicorn`) та вбий його через `kill -15 <PID>`. Скопіюй вивід з консолі у файл README.

<FollowUp label="Тобі допомогти написати простий unit-тест для перевірки endpoint /health?" query="Напиши pytest тест для перевірки ендпоінту /health у FastAPI, який симулює успішне підключення до БД та помилку підключення."/></PID>
