#!/bin/sh

# Copiando arquivos de variáveis de ambiente para arquivos ignorados pelo git (usados somente na sua máquina)
cp .env-sample .env
cp .env-sample-db .env.db

# Rodando o projeto
docker-compose up -d --build

# Aguardando finalizar o script do entrypoint
sleep 10

# Rodando os testes unitários
docker-compose exec app python manage.py test
