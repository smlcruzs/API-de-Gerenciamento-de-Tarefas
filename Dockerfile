FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY task_manager ./task_manager

CMD ["uvicorn", "task_manager.main:app", "--host", "0.0.0.0", "--port", "8000"]
