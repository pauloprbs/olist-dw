FROM python:3.10-slim

# Dependências do sistema (necessário para o dbt e postgres)
RUN apt-get update && apt-get install -y git libpq-dev gcc

# Define pasta de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto para dentro do container
COPY . .

# Garante que scripts tenham permissão de execução
RUN chmod +x scripts/*.py

# Define o comando padrão: Rodar o pipeline completo
CMD ["bash", "-c", "python scripts/download_data.py && python scripts/load_to_postgres.py && cd transformacao && dbt run --profiles-dir ."]