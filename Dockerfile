# === Stage 1: Build dependencies ===
FROM python:3.10-alpine AS builder

WORKDIR /app

# Встановлюємо системні залежності, необхідні для компиляції деяких пакетів Python (наприклад, psycopg2)
RUN apk add --no-cache gcc musl-dev postgresql-dev libffi-dev

COPY requirements.txt .

# Збираємо коліщатка (wheels) у локальну папку, щоб не тягнути інструменти збірки у фінальний образ
RUN pip install --no-cache-dir --user -r requirements.txt


# === Stage 2: Final lightweight image ===
FROM python:3.10-alpine AS final

WORKDIR /app

# Для роботи psycopg2 у фінальному Alpine потрібна лише легка системна ліба libpq
RUN apk add --no-cache libpq

# Копіюємо встановлені пакети з етапу builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Оновлюємо PATH, щоб Python бачив встановлені пакети
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Запускаємо додаток на порту 8080 (як вимагає тест лаби)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
