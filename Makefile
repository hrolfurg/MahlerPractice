COMPOSE_FILE      = docker-compose.yml
COMPOSE_PROD_FILE = docker-compose.prod.yml

.PHONY: up down restart build logs shell prod-up prod-down prod-restart prod-logs

# ── Development (port 8080 exposed locally) ──────────────────────────────────
up:
	docker compose -f $(COMPOSE_FILE) up -d --build

down:
	docker compose -f $(COMPOSE_FILE) down

restart:
	docker compose -f $(COMPOSE_FILE) restart

build:
	docker compose -f $(COMPOSE_FILE) build

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

shell:
	docker compose -f $(COMPOSE_FILE) exec mahler sh

# ── Production (Cloudflare tunnel, no exposed ports) ─────────────────────────
prod-up:
	docker compose -f $(COMPOSE_PROD_FILE) up -d --build

prod-down:
	docker compose -f $(COMPOSE_PROD_FILE) down

prod-restart:
	docker compose -f $(COMPOSE_PROD_FILE) restart

prod-logs:
	docker compose -f $(COMPOSE_PROD_FILE) logs -f
