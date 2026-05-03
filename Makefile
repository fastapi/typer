# For tests, a large terminal width
TERMINAL_WIDTH ?= 3000
# Force disable terminal for tests inside of pytest, takes precedence over GITHUB_ACTIONS env var
_TYPER_FORCE_DISABLE_TERMINAL ?= 1
# Run autocompletion install tests in the CI
_TYPER_RUN_INSTALL_COMPLETION_TESTS ?= 1

PYTEST_TARGET ?=
PYTEST_ARGS_BASE = -o console_output_style=progress --numprocesses=auto --show-locals
PYTEST_ARGS_COV ?= --cov --cov-report=term-missing --cov-report=html
PYTEST_ARGS_USER ?=

RUN ?= uv run
LINT_DIRS := typer

###################
##@ General
help: ## Print this message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

clean: ## Removes all bulid/test artifacts
	rm -rf .pdm-build/
	rm -rf .mypy_cache/ .ruff_cache/
	rm -rf .pytest_cache/ coverage/ htmlcov/

###################
##@ Tests
test: ## Run tests
	$(RUN) pytest $(PYTEST_ARGS_BASE) $(PYTEST_ARGS_USER) $(PYTEST_TARGET)

cov: ## Runs tests and produces HTML coverage report
	$(RUN) pytest $(PYTEST_ARGS_BASE) $(PYTEST_ARGS_USER) $(PYTEST_ARGS_COV) $(PYTEST_TARGET)
	@echo "Run 'open htmlcov/index.html' to see results"

###################
##@ Docs
docs-build: ## Build docs
	$(RUN) scripts/docs.py build

docs-status: ## Check docs status
	$(RUN) scripts/deploy_docs_status.py

###################
##@ Lint
lint-check: ruff-check ty-check mypy-check ## Perform all linting (ruff, ty, and mypy)

lint-fix: ruff-fix ## Attempt to fix linting issues

mypy-check: ## Perform mypy checking
	$(RUN) mypy $(LINT_DIRS)

ty-check: ## Perform ty checks
	$(RUN) ty check $(LINT_DIRS)

ruff-check: ## Perform ruff formatting checks
	$(RUN) ruff check

ruff-format: ## Formats files
	$(RUN) ruff format
