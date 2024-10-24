#!/bin/bash

# Entrar na pasta 'web' e executar 'npm install'
echo "Instalando dependências do front-end..."
cd web || { echo "Erro ao entrar na pasta 'web'"; exit 1; }
npm install || { echo "Erro ao executar 'npm install' na pasta 'web'"; exit 1; }

# Voltar para o diretório raiz e entrar na pasta 'server'
cd ../server || { echo "Erro ao entrar na pasta 'server'"; exit 1; }

# Criar o ambiente virtual e instalar as dependências
echo "Instalando dependências do back-end..."
python3 -m venv venv || { echo "Erro ao criar o ambiente virtual"; exit 1; }
source venv/bin/activate || { echo "Erro ao ativar o ambiente virtual"; exit 1; }
pip install -r requirements.txt || { echo "Erro ao instalar dependências do 'requirements.txt'"; exit 1; }