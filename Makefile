venv:
	python3 -m venv .venv

initial-setup: venv
	.venv/bin/pip install --editable .[dev]
	.venv/bin/pre-commit install

i: initial-setup

clean:
	rm -rf .venv