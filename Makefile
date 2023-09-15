.PHONY: build

build: venv
	. venv/bin/activate && pip install -r requirements.txt

venv: requirements.txt
	python3 -m venv venv
