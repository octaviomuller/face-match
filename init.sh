#!/bin/bash

# Executar o servidor Python em background
echo "Iniciando o servidor back-end em background..."
cd server || { echo "Erro ao entrar na pasta 'server'"; exit 1; }
source venv/bin/activate || { echo "Erro ao ativar o ambiente virtual"; exit 1; }
python3 main.py &

# Voltar para o diretório raiz e entrar na pasta 'web'
cd ../web || { echo "Erro ao entrar na pasta 'web'"; exit 1; }

# Executar 'npm run dev' no 'web' em background
echo "Iniciando o servidor de desenvolvimento do front-end em background..."
npm run dev &