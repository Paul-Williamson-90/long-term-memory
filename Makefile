.PHONY: start stop restart logs

create:
	docker-compose up -d
	python setup.py

start:
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose down && docker-compose up -d

logs:
	docker-compose logs -f pgvector-db