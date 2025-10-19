#!/bin/bash

# Em produção
# celery -A workers.tasks worker --loglevel=INFO --concurrency=1

# Isso roda o worker sem processos paralelos, evitando fork.
# Ideal para desenvolvimento local.
celery -A workers.tasks worker --pool=solo --loglevel=INFO --concurrency=1


