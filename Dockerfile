# Imagem base slim (menor, mais portável)
FROM python:3.11.8-slim-bullseye

# Evita input interativo e mensagens pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instala dependências do sistema mínimas
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta do Gunicorn
EXPOSE 5001

# Comando de inicialização com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app.interface:create_app()"]
