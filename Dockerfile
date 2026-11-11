FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools==78.1.1 wheel && \
    pip install -r requirements.txt && \
    pip cache purge

COPY . .

EXPOSE 80

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]
