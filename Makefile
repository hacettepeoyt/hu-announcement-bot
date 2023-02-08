.PHONY: run

CONFIG = ../.config-files/hu-announcement-bot/config.py

run: .venv $(CONFIG)
	. .venv/bin/activate && \
	cp $(CONFIG) src && \
	python -m src

.venv: requirements.txt
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
