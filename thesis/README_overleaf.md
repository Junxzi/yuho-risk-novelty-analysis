# Overleafでの使い方（このフォルダをそのままアップロード）

## 手順
1. この`thesis/`フォルダ一式をzip化（Overleafにアップロードするため）
2. Overleafで **New Project → Upload Project** からzipをアップロード
3. Overleafの **Menu → Settings → Compiler** を **LaTeX** に変更（このプロジェクトは `.latexmkrc` で upLaTeX を指定します）
4. `main.tex` を開いてコンパイル

## PDFをそのまま「完全一致」で出力したい場合
- `main_embedpdf.tex` をコンパイルしてください（`source.pdf` をそのまま埋め込みます）
- これにより、見出し/本文/改行/ページ割りまで100%同一になります

## よくあるエラー：Unicode character... / compile timed out
- 本テンプレは **upLaTeX + dvipdfmx** で軽量にコンパイルします（LuaLaTeXのフォント初期化で無料枠タイムアウトしがちなため）
- 必ず Compiler を **LaTeX** にしてコンパイルしてください（`.latexmkrc` が有効になります）

## 画像（図）の置き場所
- `thesis/figures/` にPNG/PDFを置き、`main.tex`や各`sections/*.tex`で `\includegraphics{figures/xxx.png}` のように参照

## 参考文献
- まずはOverleaf無料枠でのコンパイル安定性を優先し、`main.tex`内の `thebibliography` を使います
- 本文では `\cite{Vaswani2017}` のように `\bibitem{...}` のキーを引用してください
- 文献が増えて管理を自動化したくなったら、`biblatex/biber` に切り替え可能です（その時点で対応します）

## 章（セクション）編集
- 第1章: `sections/01_introduction.tex`
- 第2章: `sections/02_method.tex`

（第3章以降も同様に `sections/03_results.tex` 等を追加して `main.tex` から `\input{}` してください）

## 改行・スペースの基本方針（本文）
- 本文では、原則として **手動の改行（`\\`）や手動スペース（`~` など）の多用は避け**、LaTeXの自動整形に任せます。
- `\hspace` / `\vspace` は **本文では極力使わない** 想定です（表紙など、レイアウト目的の例外を除く）。
- 参考: 森畑研のメモ「改行・スペースについて」 `https://www.graco.c.u-tokyo.ac.jp/labs/morihata/thesis_memo.htm#latex-space`

## 本文の固定（重要）
- 既に書いた本文（章立て・文章）は **一語一句変更しない** 方針のため、現時点の本文を `sections/frozen/` にバックアップしています。
- 誤って上書きしてしまった場合は、`sections/frozen/` の内容で復元できます。


