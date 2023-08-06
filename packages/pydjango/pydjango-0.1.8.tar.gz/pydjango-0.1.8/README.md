Cheatsheet
===

Update requirements: `poetry export -f requirements.txt --output requirements.txt`

Activate .venv: `poetry shell`

Update deps: `poetry update`

Release: `poetry version patch && poetry publish --build`