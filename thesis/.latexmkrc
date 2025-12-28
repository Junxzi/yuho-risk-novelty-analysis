# Overleaf用: upLaTeX + dvipdfmx
# OverleafのMenu > Settings > Compiler は「LaTeX」を選ぶ（latexmkがこの設定を読む）

$latex = 'uplatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$dvipdf = 'dvipdfmx %O -o %D %S';
$pdf_mode = 3; # 0:dvi, 1:ps, 2:pdf (pdflatex), 3:pdf (dvipdf/dvipdfmx)

# bibtexを使う場合（今はthebibliographyなので未使用）
$bibtex = 'upbibtex %O %B';


