.PHONY: install
install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf .venv

run: .venv
	. .venv/bin/activate && python3 run.py
