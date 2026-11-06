# CS420 Diffusion Report — ICCV 2025 two-column edition

## Import into Overleaf

1. Upload the delivered ZIP with **New Project → Upload Project**.
2. Set **Main document: main.tex** and **Compiler: pdfLaTeX**.
3. Recompile. All style files, bibliography style, figures, and data are included.
4. Replace the three full-name/student-ID placeholders in the author block in **main.tex**.

## Format and contents

The requested template is https://www.overleaf.com/latex/templates/iccv2025-author-kit/nwnvrwcqwcsh.
This edition uses the official ICCV 2025 style and bibliography files, 10-point text, two columns, and US Letter paper. The new template request supersedes the previous HCMUS cover and A4 layout. The manuscript is a CS420 seminar report, not a claim of ICCV acceptance or a conference submission. Author names remain visible; page numbers are enabled.

The main report occupies **7 pages**, followed by **1 page of references** and **4 pages of appendices** (12 pages total). Wide figures/tables span the two-column grid for readability. Long equations are split across lines rather than reduced to tiny text. The appendix requirement and notation tables are full-width, with accompanying prose in two columns.

Edit scientific content in **content/report.tex**, appendices in **content/appendices.tex**, and references in **references.bib**. The report retains all six written task requirements and the detailed latent-diffusion discussion. Standalone slides/oral presentation requirements remain outside this package.

## Evidence and reproducibility

Results distinguish original numerical/noising illustrations from published LDM inpainting measurements. No pretrained-generation, GPU-time, peak-memory, or prompt-control benchmark was run. The representation and guidance explanations, numerical values, citations, figure data, and reproducibility code are retained from the previous edition.

Compile locally with:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

Regenerate the included noise illustration only if desired:

    python -m pip install -r code/requirements.txt
    python code/make_figures.py

Python is not needed by Overleaf. SOURCE-NOTES.md records technical evidence; TEMPLATE-NOTICE.md records template provenance. AI assistance remains disclosed in Appendix B.3.
