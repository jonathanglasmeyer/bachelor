all:
	pandoc -t latex -o bachelor-jonathan-werner.pdf --filter pandoc-citeproc bachelor.md

watch: FORCE
	@while ./watch bachelor.md ; do make ; done

FORCE:
