# CS420 Diffusion Report — ICCV 2025 two-column edition

## Import into Overleaf

1. Upload the delivered ZIP with **New Project → Upload Project**.
2. Set **Main document: main.tex** and **Compiler: pdfLaTeX**.
3. Recompile. All style files, bibliography style, figures, and data are included.
4. Replace the three full-name/student-ID placeholders in the author block in **main.tex**.

## Format and contents

The requested template is https://www.overleaf.com/latex/templates/iccv2025-author-kit/nwnvrwcqwcsh.
This edition uses the official ICCV 2025 style and bibliography files, 10-point text, two columns, and US Letter paper. The new template request supersedes the previous HCMUS cover and A4 layout. The manuscript is a CS420 seminar report, not a claim of ICCV acceptance or a conference submission. Author names remain visible; page numbers are enabled.

The main report occupies **8 pages**, followed by **1 page of references** and **6 pages of appendices** (15 pages total). Wide figures/tables span the two-column grid for readability. Long equations are split across lines rather than reduced to tiny text. The appendix requirement and notation tables are full-width, with accompanying prose in two columns.

Edit scientific content in **content/report.tex**, appendices in **content/appendices.tex**, and references in **references.bib**. The report retains all six written task requirements and reviews DDPM and LDM around the guiding question: how can learning to remove noise enable a model to generate new images? The learning objective also explicitly covers why latent diffusion reduces computational demands. Standalone slides/oral presentation requirements remain outside this package.

## Evidence and reproducibility

Results distinguish original numerical/noising illustrations from published DDPM objective-ablation results and LDM inpainting measurements. No pretrained-generation, GPU-time, peak-memory, or prompt-control benchmark was run. The main text explains the score-to-noise-prediction connection, DDPM training/sampling and the role of the simplified loss, then emphasizes LDM latent space and VAE encoder/decoder roles. Cross-attention and guidance receive brief treatment. DSM, variational-bound and reverse-mean derivations are in Appendix C; detailed VAE/attention/guidance material is in Appendix D. The original figure data and reproducibility code are retained.

Compile locally with:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

Regenerate the included noise illustration only if desired:

    python -m pip install -r code/requirements.txt
    python code/make_figures.py

Python is not needed by Overleaf. SOURCE-NOTES.md records technical evidence; TEMPLATE-NOTICE.md records template provenance. AI assistance remains disclosed in Appendix B.3.
