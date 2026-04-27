PYTHON ?= python3

.PHONY: validate test check

validate:
	$(PYTHON) scripts/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

check: validate test
