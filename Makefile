install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 src/ tests/

all: install lint test
