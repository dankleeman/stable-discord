PROJECT=stable_discord
SOURCE_OBJECTS=launch.py stable_discord tests

format.black:
	poetry run black ${SOURCE_OBJECTS}

format.isort:
	poetry run isort --atomic ${SOURCE_OBJECTS}

format.check:
	poetry run black --check ${SOURCE_OBJECTS}
	poetry run isort --check-only ${SOURCE_OBJECTS}

format: format.isort format.black

lint.flake8:
	poetry run flake8 ${SOURCE_OBJECTS}

lint.pylint:
	poetry run pylint --rcfile pyproject.toml ${SOURCE_OBJECTS}

lint: lint.flake8 lint.pylint

test:
	poetry run pytest --cov
