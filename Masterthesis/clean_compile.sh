#!/usr/bin/bash

rm -r pythontex-files-main
rm *.aux
rm *.bbl
rm *.blg
rm *.out
rm *.pytxcode
lualatex --shell-escape main.tex
pythontex main.tex
lualatex --shell-escape  main.tex
bibtex main
lualatex --shell-escape  main.tex
lualatex --shell-escape  main.tex
