timestamp := $(shell /bin/date "+%F %T")

usage:
	@echo "======================================================================"
	@echo "usage (default)  : display this menu"
	@echo "install-requires : install requirements"
	@echo "github           : push source code to github.com"
	@echo "clean            : clean up project"
	@echo "deploy-test      : deploy this shit to test.pypi.org"
	@echo "deploy-prod      : deploy this shit to pypi.org"
	@echo "======================================================================"

install-requires:
	@pip3 install -r $(CURDIR)/requirements.txt

github: clean
	@pip3 freeze > $(CURDIR)/requirements.txt
	@git status
	@git add .
	@git commit -m "$(timestamp)"
	@git push

clean:
	@rm -rf $(CURDIR)/dist/
	@rm -rf $(CURDIR)/build/
	@rm -rf $(CURDIR)/*.egg-info/

deploy-test: install-requires clean
	@python3 setup.py sdist bdist_wheel
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy-prod: install-requires clean
	@python3 setup.py sdist bdist_wheel
	@twine upload dist/*
