ifneq (,$(wildcard envs/api.env))
    include envs/api.env
    export
endif


ruff-format:
	docker compose exec $(SERVICE) ruff format

ruff-lint:
	docker compose exec $(SERVICE) ruff check

ruff-isort:
	docker compose exec $(SERVICE) ruff check --select I --fix
