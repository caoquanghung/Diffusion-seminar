# Source and claim checks

## Colab evidence added to Section 5

The LSUN Churches timing and PyTorch CUDA allocation values come from the
per-model JSON records in `code/colab/`. The timed LDM function includes
the decoder. The ImageNet traces are from a separate class-conditioned
run. Its step-25 noise panel shows RGB epsilon for ADM and channel RMS
of guided epsilon for CompVis. The adjacent states for CompVis are
decoded images. The five paired samples support qualitative observations.

The supplementary text demo uses CompVis Stable Diffusion v1.4 and
identical initial latents across the four prompts within a seed. Its
checkpoint revision, scheduler, prompts, and latent hashes are in
`code/colab/sd14_prompt_run.json`. The manual review of all 16 images is
in `code/colab/sd14_prompt_review.csv`. These observations concern the
tested prompts and seeds. LSUN Churches provides the pixel-versus-latent
speed comparison.

## Explicit score-based model attribution, November 9, 2026

The score paragraph in subsection 3.3 now explicitly cites Song and Ermon
(2019), "Generative Modeling by Estimating Gradients of the Data Distribution"
(song2019score), for noise-conditional score learning and annealed Langevin
generation. This attributes the generative approach without claiming that
the paper invented score matching itself.

## Subsection 3.3 appendix-reference audit, November 9, 2026

The current user-edited 3.3 integrates noise/score prediction and reverse
sampling. Its existing structure and formulas were preserved while adding
proof/background references: C.2 for scores and Gaussian perturbations,
C.3 for the closed-form forward marginal, C.4 for DSM/MSE optimality and
the timestep-dependent conversion between score/noise losses, C.5 for the
full Gaussian covariance KL, C.6 for the true reverse-conditional-mean
identity, C.7 for interpreting predicted noise, and F for sampler pseudocode.
Only stable labels were added to C.3/C.7; no duplicate proof appendix was
restored. Two reverse references that resolved to "Sections 3.3 and 3.3"
were consolidated. Current numbering is 3.3 for the full DDPM discussion,
3.4 for the scalar example and 3.5 for the five-level illustration.

## Merged DDPM training subsection, November 9, 2026

The previous subsections 3.3 and 3.4 are now a single subsection 3.3,
"DDPM: Variational Training and the Simplified Noise Loss". The complete
variational objective, posterior targets, fixed-variance reduction, mean/noise
parameterization, weighted MSE, and simplified objective form one sequence
with paragraph headings. The transition to the simplified objective was
shortened to remove repetition; scientific equations and evidence remain.
The sec:objective label now points to the merged subsection alongside
sec:variational and sec:parameterization. Sampling is 3.4, the scalar example
is 3.5, and the five-level illustration is 3.6. Earlier subsection numbers
below record prior revisions. Counts remain 9 main pages plus 1 reference
page and 8 appendix pages (18 total).

## Removal of the duplicate DDPM derivation, November 9, 2026

The former Appendix C.6, "From the variational bound to weighted noise MSE",
has been removed because its objective/mean/noise derivation is already in
subsection 3.3. All five references to its app:vlb label were removed or
redirected to the main method and the sampler pseudocode. Subsection 3.4
now cites DDPM Sections 3.3-3.4 directly for the discretized decoder/endpoint
detail. The original 2015 objective and covariance KL remain in C.5; the
score-to-reverse-mean section is automatically renumbered C.6. Earlier
subsection numbers recorded below are historical. The document now contains
9 main pages, 1 reference page, and 8 appendix pages (18 total); Appendix F
is on page 18.

## DDPM-focused method revision, November 9, 2026

This revision supersedes earlier subsection numbers recorded below. The
standalone main-text review of the 2015 loss has been removed; its complete
K/entropy/covariance treatment and minimized loss remain in Appendix C.5.
Subsections 3.1-3.2 introduce the common forward/reverse framework and the end
of 3.2 explicitly transitions to DDPM's variational training. The former 3.4
is now 3.3 and has been expanded: complete L_VLB, meaning of all three terms,
tractable training posterior, fixed-variance KL reduction, target posterior
mean expressed in epsilon, predicted mean expressed in epsilon_theta, and
the weighted noise-MSE coefficient obtained by subtracting the means.
These are DDPM Sections 2-3, Eqs. 5-12; the complete algebra is also retained
in Appendix C.6. New subsection 3.4 explains why dropping w_t changes relative
timestep weights even though w_t does not depend on theta, and points to the
published objective ablation rather than claiming universal optimality.
Sampling/variance choices and the brief score interpretation are now 3.5;
the scalar and five-level examples are 3.6/3.7. The main text remains 9 pages,
followed by 1 reference page and 9 appendix pages (19 total).

## DDPM reverse variance choices, November 9, 2026

Subsection 3.6 now explicitly contrasts the learned intermediate covariance
in the 2015 sampler with DDPM 2020's fixed isotropic reverse covariance.
Before the sampling update, it gives both sigma_t^2=beta_t and
sigma_t^2=tilde_beta_t=[(1-alpha_bar_{t-1})/(1-alpha_bar_t)] beta_t for t>1.
DDPM Section 3.2 reports similar results for the two choices. Both depend
only on the schedule; the posterior-variance choice does not require the
clean image at generation time. The text separates the predicted reverse
mean from fresh sampling noise, states u_1=0 and x_0=mu_theta(x_1,1), and
distinguishes that final display/sampling convention from the likelihood
decoder variance and the original 2015 endpoint. Appendix F now points to
the explicit main-text variance equation. Subsection 3.4 retains the
fixed-variance assumption used to derive mean/noise MSE. Sources: DDPM
Section 3.2 and Algorithm 2; original 2015 Section 2.2 and Appendix B.2.

## Forward/backward pseudocode, November 9, 2026

Appendix F adds two original expository algorithms, referenced from the end
of subsection 3.2. Algorithm 1 implements the Gaussian forward transition
with independent innovations. Algorithm 2 samples learned mean/covariance
transitions for t=T,...,2 and then the original prescribed stationary Gaussian
kernel at t=1 (Sohl-Dickstein et al., Secs. 2.1-2.2 and Appendix B.2).
The direct forward marginal and the changes needed for DDPM Algorithm 2 are
explained alongside the pseudocode. All sampled noise variables are fresh;
the backward procedure has no clean-image input. The user's screenshot of
DDPM Algorithms 3/4 (Sending/Receiving, Sec. 4.3) is a layout reference, not
the forward-noising or reverse-generation algorithm reproduced here.
No training or pretrained-model experiment is implied. The document has
9 main pages, 1 reference page, and 9 appendix pages (19 total).

## Figure 1 architecture diagram, November 9, 2026

Figure 1 now uses only editable vector TikZ blocks and arrows. The forward
lane explicitly shows the Gaussian kernel, beta schedule, fresh innovation,
and progression from data to noise. The backward lane runs right to left:
fresh Gaussian prior, current state, timestep-conditioned neural model,
predicted mean/covariance, Gaussian sampling with a new random draw, previous
state, and generated image. Outputs f_mu/f_Sigma follow the 2015 Gaussian
framework in subsection 3.2; the caption points to DDPM's later noise-based
mean parameterization in 3.4 and notes the final-step boundary convention.
Sources are the already-checked original 2015 forward/reverse definitions
and DDPM's inherited Gaussian construction. No specific U-Net architecture
or trained-model output is claimed. The former RGB illustration is superseded;
its files are retained but no longer referenced by Figure 1.

## Explicit loss decomposition, November 9, 2026

Subsections 3.3-3.5 now introduce the original 2015 maximized bound K and
the minimized loss -K, including the directed posterior-to-model KL and
the schedule-dependent entropy term in subsection 3.3. Before any DDPM mean/noise
parameterization, the start of subsection 3.4 presents the complete prior, reverse-step,
and decoder decomposition with L_T, L_{t-1}, and L_0, following DDPM Eq. 5.
The expectation is distributed over the three terms, so each label is an
expected contribution. The user-supplied screenshot is DDPM Eq. 5, not a
literal 2015 equation; the original stationary-kernel endpoint is explicitly
distinguished from DDPM's learned decoder. Subsection 3.4 transforms only
the intermediate KL terms, states the fixed-schedule/variance assumptions,
and gives w_t explicitly. Subsection 3.5 distinguishes the simplified
surrogate from the full likelihood bound and explains the t=1 boundary.
Checks: Sohl-Dickstein et al., Sec. 2.4 and Appendix B; Ho et al., Secs. 2-3,
Eqs. 5, 8-14. Proof details remain in Appendix C.

## Figure 1 visual revision, November 7, 2026

The first Figure 1 reference and its source block now follow the reverse-process
and sampling explanation at the end of subsection 3.2. Subsection 3.1 ends with
the forward process approaching a Gaussian prior. The wide figure floats to
page 4, after both directions have been introduced in the text.

The diffusion overview now uses a procedural RGB mountain/cabin scene with
forward-corruption tiles at 0/100/300/1000, seed 421, and the DDPM linear schedule
from 0.0001 to 0.02. `code/make_overview.py` uses the Python standard library;
subsampled Gaussian Markov transitions are composed analytically. Internal
values remain unclipped; PNG display values are clipped to [-1,1]. Blue arrows
show known forward corruption; orange arrows show conceptual learned reverse
sampling. No trained denoiser was run and the caption explicitly distinguishes
this schematic from generated-model evidence. Editable labels/arrows are in
`content/report.tex`; tiles are in `figures/diffusion_overview/`. The main text
is 9 pages, with 1 reference page and 8 appendix pages (18 total).

Sources initially consulted on November 5, 2026; the DDPM/LDM and historical foundations were rechecked for the November 7, 2026 revision. Performance statements are scoped to the reported historical experiments; no claim is made that these are current state-of-the-art models.

## Core technical sources

- **Ho, Jain, and Abbeel (2020), DDPM:** https://arxiv.org/abs/2006.11239. Read the forward/reverse definitions, closed-form marginal, epsilon parameterization, simplified loss, and original linear schedule (Sections 2–4; Eqs. 2, 4, 11, 14). The report adapts the equations with symbols defined locally and in Appendix C. Sections 3.4/4.1/4.2 and Tables 1/2 support the discussion of objective reweighting; the likelihood-bound derivation and endpoint caveat are kept in Appendix C.
- **Rombach et al. (2022), LDM, arXiv v2:** https://arxiv.org/abs/2112.10752. Read Sections 3.1–3.3 (perceptual autoencoder, KL/VQ variants, latent denoising, conditioning), Sections 4.1 and 4.5, and supplementary Sections E.2.2/E.3.5. Table 8 confirms the illustrative KL f=4, c=3 autoencoder shape. Table 6 is the selected quantitative pixel/latent inpainting baseline.
- **Kingma and Welling (2014), VAE:** https://arxiv.org/abs/1312.6114. Used for posterior/reparameterization/ELBO background. The report distinguishes this textbook objective from the perceptual/adversarial, weak-KL objective in LDM.
- **Ho and Salimans (2022), CFG:** https://arxiv.org/abs/2207.12598. Section 3.2 and Eq. 6 specify conditional dropout and guidance. The report's scale s is 1+w relative to that equation. The source also discusses diversity and extra denoiser evaluations.
- **Song, Meng, and Ermon (2021), DDIM:** https://arxiv.org/abs/2010.02502. Used to distinguish sampler acceleration from changing the representation to latent space. The paper and our Colab timings have separate protocols.
- **Vaswani et al. (2017):** https://arxiv.org/abs/1706.03762. Scaled dot-product attention; report matrices use row-vector conventions. The toy example is newly constructed.
- **Heusel et al. (2017):** https://arxiv.org/abs/1706.08500. FID as a feature-distribution comparison; FID is not interpreted as prompt accuracy or an absolute percentage of image quality.
- **Goodfellow et al. (2014)** and **van den Oord et al. (2016):** the bibliography links the original GAN and PixelRNN papers for the qualitative family comparison.

## Historical and mathematical foundations added November 7, 2026

- **Sohl-Dickstein et al. (2015):** https://proceedings.mlr.press/v37/sohl-dickstein15.html and https://proceedings.mlr.press/v37/sohl-dickstein15-supp.pdf. Sections 2.1/2.2/2.4/2.4.1 define forward/reverse processes, variational training and learned Gaussian rates (beta_1 fixed, beta_2:T learned; a footnote also supports fixed schedules). Supplement B.2 specifies the stationary-kernel endpoint; B.3 derives the KL/entropy bound; Table C.1 gives Gaussian transitions/targets; D.2 confirms learned diagonal covariance and the multiscale architecture. The user's Human_note/original_method.md was used to guide exposition and cross-checked against these primary sources.
- **Song and Ermon (2019):** https://arxiv.org/html/1907.05600v3. Sections 2-4 cover score estimation, Gaussian denoising targets, multiple noise levels, and annealed Langevin sampling. This supplies optional Appendix C background and the brief post-method score interpretation; the main exposition follows DDPM's probabilistic construction.
- **Vincent (2011):** https://doi.org/10.1162/NECO_a_00142. Original denoising score-matching connection. The author-hosted PDF was indexed but direct access was blocked; publication metadata were checked, and the conditional/marginal identity is explicitly derived in Appendix C and cross-checked against Song and Ermon's formulation.

## Published DDPM objective comparison

From DDPM Table 1 (unconditional CIFAR-10), epsilon prediction with fixed isotropic reverse variance:

| Objective | FID | NLL upper bound, bits/dimension |
| --- | ---: | ---: |
| Variational bound L | 13.51 | 3.70 |
| Simplified L_simple | 3.17 | 3.75 |

Table 2 supports the interpretation as an objective/parameterization ablation. The FID reference is the training set; DDPM Section 4.1 also reports 5.24 against the test set for the simplified model. Lower FID in this setting is evidence about sample quality, not proof of better likelihood, fewer sampling steps, or lower inference cost. These published results are separate from the LDM inpainting task and from the team's original noising illustration.

## Exact benchmark transcription

From LDM Table 6, pixel LDM-1 and LDM-4 (KL, with attention), respectively:

| Quantity | Pixel | Latent |
| --- | ---: | ---: |
| Training samples/s | 0.11 | 0.32 |
| Sampling samples/s, 256² | 0.26 | 0.97 |
| Sampling samples/s, 512² | 0.07 | 0.34 |
| Training + validation hours/epoch | 20.66 | 7.66 |
| FID@2k, epoch 6 | 24.74 | 15.21 |

The PDF table was visually checked against the source paper. Ratios in the report are recalculated rather than attributed as new model measurements: 3.7308, 4.8571, 2.9091, and 2.6971, respectively, and a 38.5206% relative reduction in the numerical FID value. Parameter count is matched in the paper's comparison. GPU/batch-setting caveats and the fixed-epoch endpoint are retained. No peak-memory or text-adherence number is inferred from that table.

## Data and societal limitations

- **LAION-5B:** https://arxiv.org/abs/2210.08402. Used as an example of large image–text training corpora, not as a blanket claim about every original LDM experiment's data.
- **Bianchi et al. (2023):** https://arxiv.org/abs/2211.03759. Evidence of demographic stereotype amplification in the systems studied. The report does not claim a new bias audit.
- **Carlini et al. (2023):** https://www.usenix.org/conference/usenixsecurity23/presentation/carlini. Evidence that some diffusion training examples can be extracted; not evidence that all outputs are copied.
- **U.S. Copyright Office (May 2025), Part 3, pre-publication:** https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf. Used to distinguish collection, training, outputs, and licensing questions. The report makes no legal determination and does not present U.S. analysis as Vietnamese law.

## Original versus sourced material

Original: prose synthesis, geometric house, five-level sequence, scalar noising calculation, attention/guidance toy calculations, three editable TikZ diagrams, cost decomposition, storage-ratio arithmetic, and future evaluation protocol.

Sourced: established equations/methods, historical paper findings, the explicitly transcribed inpainting table, the ICCV 2025 style and bibliography files. Sources are cited in the manuscript and figure/table captions. AI assistance is disclosed in Appendix B.


## Format migration, November 6, 2026

Scientific content, numerical data, and original figure/code assets are retained. The template entry in the bibliography now credits ICCV 2025. Long equations are reflowed and large floats span both columns. The archive and PDF are a separate edition; the previous HCMUS deliverables remain available.

## Narrative revision, November 7, 2026

The report has six main sections: Introduction; Background and Paper Review; DDPM: Method and Worked Examples; LDM: Latent Space and Efficient Generation; Results and Discussion; Conclusion. The abstract, introduction, subtitle, and conclusion cover both DDPM and LDM. Qualitative family comparison remains in subsection 2.2. The main text is 8 pages (below the 10-page limit), followed by 1 reference page and 6 appendix pages. Upstream style files and original image/data/code remain unchanged.

## Qualitative comparison illustration, November 7, 2026

The user supplied `qualitative comparison.png`; an unchanged copy is included as `figures/qualitative_comparison.png`. It replaces the former main-text family-comparison table and appears as Figure 5 in Appendix E, referenced from subsection 2.2 and the requirement map. It is credited as user-supplied rather than attributed as an original team drawing. Its labels describe typical model behavior, not measured or universal quality rankings. Related GAN, PixelRNN and DDPM references remain in the figure caption. The main text remains 8 pages; the complete PDF now has 16 pages (1 reference page, 7 appendix pages).

## Probabilistic method flow, November 7, 2026

The user approved moving away from a score-first exposition. Section 3 now proceeds through forward corruption, the Gaussian reverse generative model, the variational negative-log-likelihood bound, reverse-mean noise parameterization, the simplified objective and its evidence, then sampling. Subsection 3.6 gives the score connection only after the method is established. The model estimate -epsilon_theta/sqrt(1-alpha_bar_t) is distinguished from the true noisy marginal score and from the clean-data score; ideal equality requires the MSE-optimal predictor. Score/Langevin/additive-Gaussian background is in Appendix C.2, with derivations following it. Neither DDPM nor LDM requires an extra explicit score-evaluation step. The complete PDF remains 16 pages: 8 body, 1 references, 7 appendices.

## 2015 foundation versus DDPM contributions, November 7, 2026

Subsections 3.1-3.3 now review the Gaussian branch of the original 2015 framework. They use later alpha/alpha-bar notation for continuity without attributing new forward-process ideas to DDPM. The reverse network predicts mean and covariance; it is not the epsilon predictor used by DDPM. The original bound K_2015 is a log-likelihood lower bound with expected posterior KLs plus schedule-dependent entropy terms. Appendix C records its normalization/boundary assumptions and full diagonal Gaussian KL. Those entropy terms cannot be discarded when optimizing beta.

Subsections 3.4-3.6 isolate DDPM's fixed schedule/variance choices, epsilon parameterization, weighted noise-MSE derivation, simplified loss and sampling/score connection. The 2015 stationary-kernel endpoint is distinguished from DDPM's endpoint likelihood and final noise-free update. The complete delivery is 17 pages: 8 main text, 1 references, 8 appendices.
