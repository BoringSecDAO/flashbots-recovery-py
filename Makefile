.PHONY: all deps start

all: deps start

deps :; poetry install --no-root

start :; poetry run python3 main.py