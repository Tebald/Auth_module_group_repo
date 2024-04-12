.PHONY: prod-up prod-down tests-up tests-down


prod-up:
	@docker compose up -d --build

prod-down:
	@docker compose down

tests-up:
	@docker compose -f docker-compose.tests.yml up -d --build

tests-down:
	@docker compose -f docker-compose.tests.yml down
