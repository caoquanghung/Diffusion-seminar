# CS420 Diffusion Report — ICCV 2025 two-column edition

## Import into Overleaf

1. Upload the delivered ZIP with **New Project → Upload Project**.
2. Set **Main document: main.tex** and **Compiler: pdfLaTeX**.
3. Recompile. All style files, bibliography style, figures, and data are included.
4. Replace the three full-name/student-ID placeholders in the author block in **main.tex**.

## Format and contents

The requested template is https://www.overleaf.com/latex/templates/iccv2025-author-kit/nwnvrwcqwcsh.
This edition uses the official ICCV 2025 style and bibliography files, 10-point text, two columns, and US Letter paper. The new template request supersedes the previous HCMUS cover and A4 layout. The manuscript is a CS420 seminar report, not a claim of ICCV acceptance or a conference submission. Author names remain visible; page numbers are enabled.

The main report occupies **10 pages**, followed by **1 page of references** and **11 pages of appendices** (22 pages total). Wide figures/tables span the two-column grid for readability. Long equations are split across lines rather than reduced to tiny text. The appendix requirement and notation tables are full-width, with accompanying prose in two columns.

Edit scientific content in **content/report.tex**, appendices in **content/appendices.tex**, and references in **references.bib**. The report retains all six written task requirements and reviews DDPM and LDM around the guiding question: how can learning to remove noise enable a model to generate new images? The learning objective also explicitly covers why latent diffusion reduces computational demands. Standalone slides/oral presentation requirements remain outside this package.

## Evidence and reproducibility

Subsection 3.3 introduces the minimized 2015 loss (-K) and then the full
three-part variational loss (prior, intermediate reverse KLs, final decoder)
using DDPM Eq. 5 notation. Subsections 3.4-3.5 transform the intermediate
KLs into weighted noise MSE and then the simplified surrogate. The two
papers' endpoint conventions remain distinct.

Section 5 tabulates both Colab configurations and compares sampling latency, peak tensor allocation, and visual quality on LSUN Churches. It also reports qualitative ImageNet results for five classes, and published DDPM and LDM comparisons. Appendix F shows the full forward and reverse traces. The notebook and run records are in `code/colab/`. The ImageNet experiment uses class labels. Text-prompt control is discussed using published work. Section 3.1-3.3 explains the 2015 Gaussian diffusion framework: forward process and beta schedule, learned reverse mean/covariance and sampling, and the original variational objective. Section 3.4-3.6 then distinguishes DDPM's fixed-variance/noise-prediction parameterization, simplified loss, sampling choices and brief score interpretation; score/Langevin background is optional material in Appendix C. The LDM section emphasizes latent space and VAE encoder/decoder roles. Cross-attention and guidance receive brief treatment. DSM, the original 2015 objective and covariance KL, DDPM variational-bound and reverse-mean derivations are in Appendix C; detailed VAE/attention/guidance material is in Appendix D. The user-supplied qualitative-comparison illustration is included at full text width in Appendix E and referenced from subsection 2.2. The original figure data and reproducibility code are retained.

Compile locally with:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

Regenerate the included noise illustration only if desired:

    python -m pip install -r code/requirements.txt
    python code/make_figures.py

Python is not needed by Overleaf. SOURCE-NOTES.md records technical evidence; TEMPLATE-NOTICE.md records template provenance. AI assistance remains disclosed in Appendix B.

Figure 1 combines editable TikZ arrows/labels with four original RGB scene tiles.
Regenerate those tiles with `python code/make_overview.py` (standard library only).
They visualize Gaussian forward corruption; the reverse arrows are a conceptual
model schematic, not outputs from a trained denoiser. The separate five-level
grayscale worked illustration and its original data remain in Figure 2.
