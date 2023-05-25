init:
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

tests:
	PYTHONPATH=. pytest test

check_types:
	mypy src