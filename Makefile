
# Development
dev:
	docker-compose up --build

# Production
prod:
	docker-compose -f docker-compose.prod.yml up --build -d

# Stop all
stop:
	docker-compose down
	docker-compose -f docker-compose.prod.yml down

# Run migrations
migrate:
	docker-compose exec api alembic upgrade head