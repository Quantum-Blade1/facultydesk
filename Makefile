.PHONY: up down logs migrate seed lint typecheck test fmt graph diagrams backup restore vapid-keys

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f

migrate:
	cd backend && uv run alembic upgrade head

seed:
	cd backend && uv run python -m app.infrastructure.seed.seed_data

lint:
	cd backend && uv run ruff check .
	cd frontend && pnpm lint

typecheck:
	cd backend && uv run python -c "from app.main import app; import json; open('../openapi.json', 'w').write(json.dumps(app.openapi(), indent=2))"
	cd backend && uv run mypy --strict app tests
	cd frontend && pnpm gen:api && pnpm typecheck

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

vapid-keys:
	@cd backend && uv run python -c 'from pywebpush import Vapid; import base64; from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat; v = Vapid(); v.generate_keys(); raw_pub = v.public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint); b64_pub = base64.urlsafe_b64encode(raw_pub).decode().rstrip("="); b64_priv = base64.urlsafe_b64encode(v.private_key.private_numbers().private_value.to_bytes(32, "big")).decode().rstrip("="); print(f"VAPID_PUBLIC_KEY={b64_pub}\nVAPID_PRIVATE_KEY={b64_priv}")'

