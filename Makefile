PY_VERSION := 3
VENV_PATH  := venv

venv :
	@virtualenv -p python$(PY_VERSION) $@

.PHONY : dev
dev : venv
	@$(VENV_PATH)/bin/pip install -r requirements.txt

.PHONY : notebook
notebook : venv
	@$(VENV_PATH)/bin/pip install jupyter
	@$(VENV_PATH)/bin/jupyter-notebook
