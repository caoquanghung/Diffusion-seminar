# CS420 Diffusion Report — ICCV 2025 two-column edition

## Import into Overleaf

1. Upload the delivered ZIP with **New Project → Upload Project**.
2. Set **Main document: main.tex** and **Compiler: pdfLaTeX**.
3. Recompile. All style files, bibliography style, figures, and data are included.
4. Replace the three full-name/student-ID placeholders in the author block in **main.tex**.

## Format and contents

The requested template is https://www.overleaf.com/latex/templates/iccv2025-author-kit/nwnvrwcqwcsh.
This edition uses the official ICCV 2025 style and bibliography files, 10-point text, two columns, and US Letter paper. The new template request supersedes the previous HCMUS cover and A4 layout. The manuscript is a CS420 seminar report, not a claim of ICCV acceptance or a conference submission. Author names remain visible; page numbers are enabled.

The main report occupies **9 pages**, followed by **1 page of references** and **11 pages of appendices** (21 pages total). Wide figures/tables span the two-column grid for readability. Long equations are split across lines rather than reduced to tiny text. The appendix requirement and notation tables are full-width, with accompanying prose in two columns.

Edit scientific content in **content/report.tex**, appendices in **content/appendices.tex**, and references in **references.bib**. The report retains all six written task requirements and reviews DDPM and LDM around the guiding question: how can learning to remove noise enable a model to generate new images? The learning objective also explicitly covers why latent diffusion reduces computational demands. Standalone slides/oral presentation requirements remain outside this package.

## Evidence and reproducibility

Subsection 3.3 explains both fixed reverse-variance choices from DDPM 2020
before its sampling update, contrasting them with the learned covariance
in subsection 3.2. It distinguishes the final noise-free sampling update
from the likelihood decoder and the original 2015 endpoint.

Appendix F contains numbered, side-by-side pseudocode for forward Gaussian
diffusion and the original 2015 backward sampler, referenced at the end of
subsection 3.2. It explicitly handles the 2015 stationary-kernel endpoint and
explains the changes needed for DDPM sampling. These algorithms are expository
pseudocode, not evidence of a trained-model experiment.

The original 2015 bound and minimized loss (-K) are in Appendix C.5.
Subsection 3.3 begins with DDPM's full three-part variational loss (prior,
intermediate reverse KLs, final decoder), explains the posterior targets,
then connects mean/noise prediction to score estimation and derives weighted
noise MSE. The same subsection continues to the simplified surrogate,
reweighting, empirical benefit, and reverse sampling. It links to supporting
Appendices C.2-C.7 and F at the corresponding steps. The two papers'
endpoint conventions remain distinct.

The redundant appendix section deriving weighted noise MSE from the
variational bound has been removed. Subsection 3.3 now contains that
explanation; later appendix subsections have been renumbered automatically.

Section 5 tabulates both Colab configurations and compares sampling latency, peak tensor allocation, and visual quality on LSUN Churches. It also reports qualitative ImageNet results for five classes, and published DDPM and LDM comparisons. Appendix G shows the full forward and reverse traces. The notebook and run records are in `code/colab/`. The ImageNet experiment uses class labels. Text-prompt control is discussed using published work.

Subsections 3.1-3.2 introduce the forward/reverse Gaussian framework with historical attribution to 2015. Subsection 3.3 covers DDPM's objective, noise/score parameterization, simplified loss and sampling; worked examples follow in 3.4-3.5. Score/Langevin background is optional material in Appendix C. The LDM section emphasizes latent space and VAE encoder/decoder roles. Cross-attention and guidance receive brief treatment. DSM, the original 2015 objective and covariance KL, and the score-to-reverse-mean derivation are in Appendix C; detailed VAE/attention/guidance material is in Appendix D. The user-supplied qualitative-comparison illustration is included at full text width in Appendix E and referenced from subsection 2.2. The original figure data and reproducibility code are retained.

Compile locally with:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

Regenerate the included noise illustration only if desired:

    python -m pip install -r code/requirements.txt
    python code/make_figures.py

Python is not needed by Overleaf. SOURCE-NOTES.md records technical evidence; TEMPLATE-NOTICE.md records template provenance. AI assistance remains disclosed in Appendix B.

Figure 1 is an editable TikZ architecture diagram with two lanes: forward
Gaussian corruption and backward neural parameter prediction plus sampling.
It shows schedule/noise inputs, timestep conditioning, mean/covariance outputs,
and the prior-to-image direction. Its source is at the end of subsection 3.2.
The displayed network outputs follow the 2015 formulation; DDPM's later
noise-prediction parameterization is explained in subsection 3.3. The earlier
RGB scene tiles and `code/make_overview.py` are retained as historical assets
and are no longer used by Figure 1. The separate five-level grayscale worked
illustration and its original data remain in Figure 2.
