PYTHON ?= python3

.PHONY: validate test mirror-check check dmg

validate:
	$(PYTHON) scripts/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

mirror-check:
	scripts/check-skills-mirror.sh

check: validate test mirror-check

dmg:
	scripts/build-dmg.sh
