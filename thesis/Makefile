files=bachelor.md <(echo foo)
all:
	pandoc -t latex -o bachelor-jonathan-werner.pdf --filter pandoc-citeproc ${files}

watch: FORCE
	@while ./watch bachelor.md ; do make ; done

FORCE:
