FROM python:3.13-slim

WORKDIR /app

# Отключаем создание pyc файлов и буферизацию вывода (важно для логов в Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]