#!/usr/bin/env bash
# Script de build da implantacao no Render.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# O db.sqlite3 e ignorado pelo git (exigencia do enunciado), entao o banco
# da implantacao nasce vazio a cada build. Este comando e idempotente e
# repoe o conteudo do blog.
python manage.py popular_banco
