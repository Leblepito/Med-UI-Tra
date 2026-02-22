.PHONY: dev dev-frontend dev-backend install build test typecheck lint clean docker-up docker-down

# Start both frontend and backend in parallel
dev:
	@echo "Starting ThaiTurk dev servers..."
	@make dev-backend & make dev-frontend

dev-frontend:
	cd 01_frontend && npm run dev

dev-backend:
	cd 02_backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Install all dependencies
install:
	cd 01_frontend && npm install
	cd 02_backend && pip install -r requirements.txt

# Build frontend
build:
	cd 01_frontend && npm run build

# TypeScript check
typecheck:
	cd 01_frontend && npx tsc --noEmit

# Lint
lint:
	cd 01_frontend && npm run lint

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

# Health check
health:
	@curl -s http://localhost:8000/health | python -m json.tool
	@curl -s -o /dev/null -w "Frontend: HTTP %{http_code}\n" http://localhost:3000/

# Clean
clean:
	rm -rf 01_frontend/.next 01_frontend/node_modules/.cache
