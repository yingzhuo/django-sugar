usage:
	@echo "======================================================================"
	@echo "usage (default) : display this menu"
	@echo "github          : push source code to github.com"
	@echo "======================================================================"

github:
	@git status
	@git add .
	@git commit -m 'update'
	@git push
