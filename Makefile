.PHONY: build

CONFIG = ~/.config/hu-announcement-bot/config.py

build: .venv $(CONFIG)
	cp $(CONFIG) src

.venv: requirements.txt
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
