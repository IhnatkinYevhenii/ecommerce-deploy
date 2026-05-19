import asyncio
import logging
import sys
import time
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from sqlalchemy import text

from config import settings
from database import SessionLocal, run_migrations

# ----------------- 2. Налаштування JSON логування (Вбудований Python) -----------------
class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_object, ensure_ascii=False)

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(CustomJsonFormatter())

logger = logging.getLogger("ecommerce_app")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# Вимикаємо стандартний uvicorn текстовий вивід
logging.getLogger("uvicorn.access").disabled = True


# ----------------- 3. Плавне завершення (Graceful Shutdown) -----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    try:
        run_migrations()
    except Exception as e:
        logger.error(f"Migration failed during startup: {str(e)}")
    
    yield
    
    logger.info("SIGTERM received. Starting graceful shutdown...")
    logger.info("Closing all database connections...")
    await asyncio.sleep(1) 
    logger.info("Graceful shutdown complete. Exiting with code 0.")
    sys.exit(0)


app = FastAPI(lifespan=lifespan)


# ----------------- 1. Глибока перевірка стану (Health Check) -----------------
@app.get("/health")
def health_check(response: Response):
    db_alive = False
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db_alive = True
    except Exception as e:
        logger.error(f"Health check failed: Database connection error: {str(e)}")
    finally:
        db.close()

    if db_alive:
        return {"status": "UP", "database": "CONNECTED"}
    
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "DOWN", "database": "DISCONNECTED"}
