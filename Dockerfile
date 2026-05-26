FROM python:3.12-slim

# evita arquivos pyc
ENV PYTHONDONTWRITEBYTECODE=1

# logs em tempo real
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# instala requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copia projeto
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
