all:
	pandoc -t latex -o bachelor-jonathan-werner.pdf --filter pandoc-citeproc bachelor.md
