.PHONY: prod-up prod-down tests-up tests-down local-up local-down


prod-up:
	@docker compose up -d --build

prod-down:
	@docker compose down

tests-up:
	@docker compose -f docker-compose.tests.yml up -d --build

tests-down:
	@docker compose -f docker-compose.tests.yml down

local-up:
	@docker compose -f docker-compose.local.yml up -d

local-down:
	@docker compose -f docker-compose.local.yml down
