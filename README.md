# Asimov_Agno_AI_Customer_Service

## Comandos para rodar o projeto

```bash
# Para rodar o docker
docker compose up

# Rodar a API
fastapi dev main.py
# ou
fastapi dev --host 127.0.0.1 --port=8000

# Rodar workers
celery -A workers.tasks worker --loglevel=INFO --concurrency=1
```
