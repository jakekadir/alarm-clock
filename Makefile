venv:
	python3 -m venv .venv

initial-setup: venv
	.venv/bin/pip install --editable .[dev]
	.venv/bin/pre-commit install

i: initial-setup

clean:
	rm -rf .venv

b-run:
	uvicorn alarm_clock.main:app --reload

f-run:
	cd alarm_clock_frontend && npm run start