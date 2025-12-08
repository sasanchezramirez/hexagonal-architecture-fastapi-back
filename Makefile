.PHONY: install run test docker-build docker-run clean

install:
	poetry install

run:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest

docker-build:
	docker build -t hex-app .

docker-run:
	docker run -p 8000:8000 hex-app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
