FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./app .
EXPOSE 5000

CMD ["python", "main.py"]
