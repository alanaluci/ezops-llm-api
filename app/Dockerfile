# 🔹 Usar Python 3.12 slim como base
FROM python:3.12-slim

# 🔹 Definir diretório de trabalho
WORKDIR /app

# 🔹 Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 🔹 Atualizar pip e instalar pacotes essenciais
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 🔹 Instalar spaCy e dependências necessárias
RUN pip install --no-cache-dir \
    "blis==0.7.9" \
    "thinc>=8.2.2,<8.3.0" \
    "spacy==3.7.5"

# 🔹 Baixar e instalar o modelo do spaCy manualmente
RUN python -m spacy download pt_core_news_sm

# 🔹 Copiar os arquivos do projeto para dentro do container
COPY . /app

# 🔹 Instalar dependências do projeto (FastAPI, Uvicorn, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Expor a porta 8000 para o servidor FastAPI
EXPOSE 8000

# 🔹 Comando para rodar a API com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
