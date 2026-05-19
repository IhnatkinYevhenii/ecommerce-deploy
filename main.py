import asyncio
import logging
import sys
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from python_json_logger import jsonlogger
from sqlalchemy import text

from config import settings
from database import SessionLocal, run_migrations

# ----------------- 2. Налаштування JSON логування -----------------
log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(message)s",
    json_ensure_ascii=False
)
log_handler.setFormatter(formatter)

logger = logging.getLogger("ecommerce_app")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# Вимикаємо стандартні текстові логи uvicorn, щоб вони не смітили в STDOUT
logging.getLogger("uvicorn.access").disabled = True


# ----------------- 3. Плавне завершення (Graceful Shutdown) -----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код виконується ПРИ ЗАПУСКУ
    logger.info("Application starting up...")
    try:
        run_migrations()
    except Exception as e:
        logger.error(f"Migration failed during startup: {str(e)}")
    
    yield
    
    # Код виконується ПРИ ОТРИМАННІ SIGTERM / SIGINT
    logger.info("SIGTERM received. Starting graceful shutdown...")
    logger.info("Closing all database connections...")
    # SQLAlchemy engine закриває пул автоматично при виході, 
    # але тут можна додати логіку завершення фонових задач, якщо вони є.
    await asyncio.sleep(1) # Симулюємо дообробку поточних запитів
    logger.info("Graceful shutdown complete. Exiting with code 0.")
    sys.exit(0)


app = FastAPI(lifespan=lifespan)


# ----------------- 1. Глибока перевірка стану (Health Check) -----------------
@app.get("/health")
def health_check(response: Response):
    db_alive = False
    try:
        db = SessionLocal()
        # Швидкий ping-запит до бази даних
        db.execute(text("SELECT 1"))
        db_alive = True
    except Exception as e:
        logger.error(f"Health check failed: Database connection error: {str(e)}")
    finally:
        db.close()

    if db_alive:
        return {"status": "UP", "database": "CONNECTED"}
    
    # Якщо БД лежить — повертаємо 503
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "DOWN", "database": "DISCONNECTED"}
