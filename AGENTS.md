# Repository memory and agent handoff

Last updated: 2026-11-06 (Asia/Ho_Chi_Minh).

## Purpose and current state

This repository contains an English CS420 seminar report about **Diffusion Models: From Adding Noise to Generating Images**, with particular emphasis on latent diffusion. The report and its Overleaf package have been completed. Continue from the **ICCV edition** when the user requests changes; do not restart from the older HCMUS layout.

The user communicates in Vietnamese. Explain progress/results in Vietnamese, but keep the report in English. This file is persistent context, not a new request to revise or rerun the report. Follow the user's latest instructions if they supersede these recorded decisions.

## Canonical files: use these for future edits

Active source directory: `iccv-diffusion-report/`.

| File | Role |
| --- | --- |
| `main.tex` | Entry point, packages, author placeholders, ICCV layout |
| `content/report.tex` | Complete scientific report, including abstract and conclusion |
| `content/appendices.tex` | Requirement map, reproducibility, future protocol, notation, derivations |
| `references.bib` | Scientific references, template credit, AI-assistance citation |
| `iccv.sty` / `ieeenat_fullname.bst` | Unmodified official ICCV kit files |
| `figures/noise_sequence.pdf` | Original five-level noise illustration |
| `figures/noise_arrays.npz` | Unclipped frames, timesteps, beta schedule, alpha-bar values |
| `figures/noise_levels.csv` / `figures/analysis.json` | Numerical coefficients, derived arithmetic, versions |
| `code/make_figures.py` / `code/requirements.txt` | Reproducible CPU-only illustration generation |
| `README.md` | Import/build instructions and edition overview |
| `SOURCE-NOTES.md` | Technical source locations and claim checks |
| `TEMPLATE-NOTICE.md` | ICCV provenance and adaptations |

Current deliverables:
- `CS420_Diffusion_Report_ICCV2025_Overleaf.zip`
- `pdf/CS420_Diffusion_Report_ICCV2025.pdf`


## Assignment and template sources
Written requirements:

1. Generative vs. discriminative models; qualitative GAN/autoregressive/diffusion comparison.
2. Forward process, beta schedule, Gaussian noise, reverse process, noise predictor, sampling, and a two-direction diagram.
3. A complete manual 1D forward step and interpretation of stochastic expectation.
4. A small image at five noise levels. A pretrained generation/denoising demonstration is optional if resources permit; training is not required.
5. VAE encoder/decoder, latent operations, cross-attention, and pipeline diagram.
6. Sampling speed, quality, prompt control, data, copyright, bias, and an explicit pixel/latent setting comparison.

Required equations: Gaussian forward transition and the simplified expected squared noise-prediction loss. Required organization: Abstract, Introduction, Background/Paper Review, Method/Worked Example, Results and Discussion, Conclusion, References. Appendix A maps requirements to evidence. The user's English-language request supersedes the brief's Vietnamese-language request.

Latest template: https://www.overleaf.com/latex/templates/iccv2025-author-kit/nwnvrwcqwcsh

That page links the official kit: https://media.eventhosts.cc/Conferences/ICCV2025/ICCV2025-Author-Kit.zip

The active edition uses `\documentclass[10pt,twocolumn,letterpaper]{article}` and `\usepackage[pagenumbers]{iccv}`. US Letter follows the new author kit rather than the former A4 layout. It is a named CS420 report, **not** an anonymous review submission or a claim of ICCV acceptance. Keep upstream style files and attribution intact.

## Evidence boundaries: do not fabricate experiments

The user had not supplied completed Results. The delivered report contains original illustrations/calculations and clearly attributed published results. **No pretrained image generator, denoising benchmark, GPU runtime benchmark, peak-memory measurement, or prompt-adherence experiment was executed.** The future evaluation protocol is a proposal, not a completed study.

Original illustration: a procedural 28×28 grayscale house (no external dataset), NumPy seed 420, 1,000 Markov noising steps, beta linearly increasing from 0.0001 to 0.02, snapshots at 0/50/200/500/1000. Arrays remain unclipped; only displayed intensities are clipped. Tested generator versions: NumPy 2.3.5 and ReportLab 4.4.9 under Python 3.12. The other three diagrams are editable TikZ in `content/report.tex`.

Scalar worked example: x0=0.8, beta1=0.1, epsilon=-0.5 gives x1=0.6008327554; conditional mean=0.7589466384 and variance=0.1. This deliberately larger beta is separate from the image schedule.

Published comparison: **Rombach et al. (2022), LDM, arXiv v2, Table 6, Places inpainting**, pixel LDM-1 vs. KL-regularized LDM-4 with attention:

| Criterion | Pixel | Latent |
| --- | ---: | ---: |
| Training throughput, samples/s | 0.11 | 0.32 |
| Sampling throughput at 256², samples/s | 0.26 | 0.97 |
| Sampling throughput at 512², samples/s | 0.07 | 0.34 |
| Training + validation, hours/epoch | 20.66 | 7.66 |
| Validation FID@2k after epoch 6 | 24.74 | 15.21 |

Ratios: sampling 3.73× / 4.86×, epoch time 2.70×, training throughput 2.91×. The numerical FID reduction is 38.5%; this is **not** a percentage improvement in perceptual quality. Keep the fixed-epoch, GPU/batch-setting, and separate autoencoder-pretraining caveats. This inpainting comparison does not establish text-prompt superiority. Peak memory is not reported in that table; do not invent GB values.

Technical distinctions already handled correctly:

- Original LDM includes both KL- and VQ-regularized autoencoders; the report emphasizes the KL/VAE variant. Its perceptual/adversarial weak-KL training is not identical to a textbook VAE pixel-likelihood objective.
- VAE posterior noise and diffusion noise are different random variables. Encoded clean latents are not necessarily exactly standard normal.
- Pure text-to-image generation starts from latent noise; it does not require a real image or the image encoder. Decode once after iterative latent denoising.
- Cross-attention uses image queries and text keys/values, with explicit matrix shapes and row-vector convention.
- CFG uses epsilon_u + s(epsilon_c − epsilon_u), with s=1 ordinary conditional sampling; the CFG paper's w=s−1. Standard CFG uses two denoiser evaluations per step.
- Latent compression reduces per-evaluation spatial work; DDIM reduces sampling evaluations. Do not conflate these speedups.
- A 16:1 state-element ratio for illustrative f=4,c=3 is not a measured 16× total-memory or runtime improvement.
- Bias, memorization, and copyright claims have specific sources; avoid universal legal conclusions or implying that every generated image is copied. The cited U.S. policy analysis is not Vietnamese law.

## Build, inspect, and package

Run from the active source directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

To keep intermediate files separate, the build used:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../../../tmp/pdfs/iccv-build main.tex
```

Optional figure regeneration from the source directory:

```sh
python -m pip install -r code/requirements.txt
python code/make_figures.py
```

Python is not needed for Overleaf compilation. TeX Live/`latexmk`/`pdflatex` were available locally. Discover current bundled dependencies if needed rather than assuming a permanent runtime version/path.

After edits:

1. Compile to convergence with BibTeX; inspect the final log for missing references/citations, errors, and overflow.
2. Render the updated PDF and visually inspect affected pages. Follow the available PDF skill for artifact work.
3. Check equations, captions, float placement, two-column readability, author placeholders, and `LastBodyPage` before reporting page counts.
4. Refresh the delivered PDF and ZIP from the **active source**, and update its README if counts or instructions changed.
5. Build the ZIP with `main.tex` at archive root, alongside `content/`, `figures/`, `.bib`, `.sty`, `.bst`, code, and notices. Exclude build outputs/caches and unrelated historical files.
6. Extract to a fresh temporary directory and compile that copy to verify self-containment. This passed for the current delivery; its extracted build matched the delivered PDF's page text.

Layout details/pitfalls:

- Wide figures/tables use starred floats across both columns. Long equations are split rather than shrunk. Appendix A/C use full-width table blocks with two-column explanatory text.
- `balance` balances reference and appendix columns. `\hfuzz=0pt`, `\vfuzz=3pt` keep horizontal checks strict while allowing small column-balancing roundoff; upstream ICCV defaults are more permissive.
- Keep `\captionsetup{hypcap=false}` for appendix tables outside normal floating environments.
- A literal `[Full name ...]` immediately after a LaTeX `\\` can be parsed as an optional spacing argument. Existing `\mbox{...}` wrappers in the author block prevent this.
- Poppler fontconfig initially tried unwritable cache locations. `tmp/pdfs/fontconfig.conf` provides a writable cache in `/private/tmp/cs420-font-cache`; use `FONTCONFIG_FILE` pointing to that config when rendering if necessary. Do not repurpose `HOME`.
- `tmp/` contains historical builds, extracted ZIP checks, logs, and render PNGs. It is not the canonical source and should not be included in delivery ZIPs.

## Next-agent starting point

Read this file, the latest user message, and the active source README. Check `git status` and current file contents before editing. The report migration and delivery are complete; there is no pending automatic experiment, upload, or content rewrite. Future work should be scoped to the user's next request. Overleaf import instructions are: New Project → Upload Project → select ZIP → main.tex → pdfLaTeX. Actual author names/IDs and any real model results remain to be supplied if the user wants them added.
