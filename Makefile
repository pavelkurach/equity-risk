run_tests:
	PYTHONPATH=. pytest test

check_types:
	mypy src