#!/bin/bash

celery -A workers.tasks worker --loglevel=INFO --concurrency=1
