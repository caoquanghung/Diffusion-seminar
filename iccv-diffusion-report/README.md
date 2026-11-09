# CS420 Diffusion Report — ICCV 2025 two-column edition

## Import into Overleaf

1. Upload the delivered ZIP with **New Project → Upload Project**.
2. Set **Main document: main.tex** and **Compiler: pdfLaTeX**.
3. Recompile. All style files, bibliography style, figures, and data are included.
4. Replace the three full-name/student-ID placeholders in the author block in **main.tex**.

## Format and contents

The requested template is https://www.overleaf.com/latex/templates/iccv2025-author-kit/nwnvrwcqwcsh.
This edition uses the official ICCV 2025 style and bibliography files, 10-point text, two columns, and US Letter paper. The new template request supersedes the previous HCMUS cover and A4 layout. The manuscript is a CS420 seminar report, not a claim of ICCV acceptance or a conference submission. Author names remain visible; page numbers are enabled.

The main report occupies **9 pages**, followed by **1 page of references** and **9 pages of appendices** (19 pages total). Wide figures/tables span the two-column grid for readability. Long equations are split across lines rather than reduced to tiny text. The appendix requirement and notation tables are full-width, with accompanying prose in two columns.

Edit scientific content in **content/report.tex**, appendices in **content/appendices.tex**, and references in **references.bib**. The report retains all six written task requirements and reviews DDPM and LDM around the guiding question: how can learning to remove noise enable a model to generate new images? The learning objective also explicitly covers why latent diffusion reduces computational demands. Standalone slides/oral presentation requirements remain outside this package.

## Evidence and reproducibility

Subsection 3.6 explains both fixed reverse-variance choices from DDPM 2020
before its sampling update, contrasting them with the learned covariance
in subsection 3.2. It distinguishes the final noise-free sampling update
from the likelihood decoder and the original 2015 endpoint.

Appendix F contains numbered, side-by-side pseudocode for forward Gaussian
diffusion and the original 2015 backward sampler, referenced at the end of
subsection 3.2. It explicitly handles the 2015 stationary-kernel endpoint and
explains the changes needed for DDPM sampling. These algorithms are expository
pseudocode, not evidence of a trained-model experiment.

Subsection 3.3 introduces the minimized 2015 loss (-K) and then the full
three-part variational loss (prior, intermediate reverse KLs, final decoder)
using DDPM Eq. 5 notation. Subsections 3.4-3.5 transform the intermediate
KLs into weighted noise MSE and then the simplified surrogate. The two
papers' endpoint conventions remain distinct.

Results distinguish original numerical/noising illustrations from published DDPM objective-ablation results and LDM inpainting measurements. No pretrained-generation, GPU-time, peak-memory, or prompt-control benchmark was run. Section 3.1-3.3 explains the 2015 Gaussian diffusion framework: forward process and beta schedule, learned reverse mean/covariance and sampling, and the original variational objective. Section 3.4-3.6 then distinguishes DDPM's fixed-variance/noise-prediction parameterization, simplified loss, sampling choices and brief score interpretation; score/Langevin background is optional material in Appendix C. The LDM section emphasizes latent space and VAE encoder/decoder roles. Cross-attention and guidance receive brief treatment. DSM, the original 2015 objective and covariance KL, DDPM variational-bound and reverse-mean derivations are in Appendix C; detailed VAE/attention/guidance material is in Appendix D. The user-supplied qualitative-comparison illustration is included at full text width in Appendix E and referenced from subsection 2.2. The original figure data and reproducibility code are retained.

Compile locally with:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

Regenerate the included noise illustration only if desired:

    python -m pip install -r code/requirements.txt
    python code/make_figures.py

Python is not needed by Overleaf. SOURCE-NOTES.md records technical evidence; TEMPLATE-NOTICE.md records template provenance. AI assistance remains disclosed in Appendix B.3.

Figure 1 is an editable TikZ architecture diagram with two lanes: forward
Gaussian corruption and backward neural parameter prediction plus sampling.
It shows schedule/noise inputs, timestep conditioning, mean/covariance outputs,
and the prior-to-image direction. Its source is at the end of subsection 3.2.
The displayed network outputs follow the 2015 formulation; DDPM's later
noise-prediction parameterization is explained in subsection 3.4. The earlier
RGB scene tiles and `code/make_overview.py` are retained as historical assets
and are no longer used by Figure 1. The separate five-level grayscale worked
illustration and its original data remain in Figure 2.
