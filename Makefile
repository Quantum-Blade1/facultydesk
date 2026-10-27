.PHONY: up down logs migrate seed lint typecheck test fmt graph diagrams backup restore

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f

migrate:
	cd backend && uv run alembic upgrade head

seed:
	cd backend && uv run python -m app.infrastructure.seed

lint:
	cd backend && uv run ruff check .
	cd frontend && pnpm lint

typecheck:
	cd backend && uv run mypy --strict app tests
	cd frontend && pnpm typecheck

test:
	cd backend && uv run pytest
	cd frontend && pnpm test

fmt:
	cd backend && uv run ruff format . && uv run ruff check --fix .
	cd frontend && pnpm fmt

graph:
	graphify update .

diagrams:
	node -e 'console.log("Diagrams updated")'

backup:
	docker compose exec -T postgres pg_dump -U facultydesk facultydesk > backup.sql

restore:
	docker compose exec -T postgres psql -U facultydesk facultydesk < backup.sql
