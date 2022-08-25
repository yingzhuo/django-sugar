usage:
	@echo "======================================================================"
	@echo "usage (default)  : display this menu"
	@echo "github           : push source code to github.com"
	@echo "install-requires : install requirements"
	@echo "======================================================================"

github:
	@pip3 freeze > $(CURDIR)/requirements.txt
	@git status
	@git add .
	@git commit -m 'update'
	@git push

install-requires:
	@pip3 install -r $(CURDIR)/requirements.txt
