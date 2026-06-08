.PHONY: check test compile static-check clean

check: clean test compile static-check

test:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests

compile:
	python3 -c "from pathlib import Path; [compile(path.read_text(), str(path), 'exec') for path in [Path('app.py'), Path('stuff/tomtom.py'), *Path('tests').glob('*.py')]]"

static-check:
	python3 scripts/check-baseline.py

clean:
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
