develop:  ## install dependencies
	python3 -m pip install .'[develop]'
build:  ## build the python library
	python3 setup.py build build_ext --inplace 
install: ## install library
	python3 -m pip install .
run: ## run main.py
	python3 splotify/main.py
test: ## run tests with coverage stats
	python3 -m pytest --cov=splotify/ splotify/tests/
format: # autoformat with black
	python3 -m black splotify/
lint:  ## run static analysis with flake8
	python3 -m flake8 splotify/
## VERSION
patch:
	bump2version patch
minor:
	bump2version minor
major:
	bump2version major