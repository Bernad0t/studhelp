# Используем Python в качестве базового образа
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Указываем рабочий порт
EXPOSE 8000

# Запускаем сервер
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000
