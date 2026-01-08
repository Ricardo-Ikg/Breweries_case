#!/bin/bash
set -e

echo "Inicializando Airflow (standalone)..."

airflow db migrate

echo "Criando usuário admin padrão (idempotente)..."

airflow users create \
  --username admin \
  --firstname Interview \
  --lastname User \
  --role Admin \
  --email interviewer@case.dev \
  --password admin123 || true

echo "Subindo Airflow standalone..."
exec airflow standalone
