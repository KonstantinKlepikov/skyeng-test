# target: dev - run docker-compose
serve:
	sh ./scripts/dev.sh

# target: down - stop and down docker stack
down:
	docker compose -f docker-stack.yml down
