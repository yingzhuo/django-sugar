timestamp := $(shell /bin/date "+%F %T")

usage:
	@echo "======================================================================"
	@echo "usage (default)  : display this menu"
	@echo "install-requires : install requirements"
	@echo "github           : push source code to github.com"
	@echo "======================================================================"

install-requires:
	@pip3 install -r $(CURDIR)/requirements.txt

github:
	@pip3 freeze > $(CURDIR)/requirements.txt
	@git status
	@git add .
	@git commit -m "$(timestamp)"
	@git push
