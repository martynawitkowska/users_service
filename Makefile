ifneq (,$(wildcard envs/api.env))
    include envs/api.env
    export
endif


ruff-format:
	docker compose exec $(SERVICE) ruff format

ruff-lint:
	docker compose exec $(SERVICE) ruff check --fix

ruff-isort:
	docker compose exec $(SERVICE) ruff check --select I --fix

pytest:
	docker compose exec $(SERVICE) pytest

pytest-cov:
	docker compose exec $(SERVICE) pytest --cov-report html:cov_html
