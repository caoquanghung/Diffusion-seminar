# Source and claim checks

Sources initially consulted on November 5, 2026; the DDPM/LDM and historical foundations were rechecked for the November 7, 2026 revision. Performance statements are scoped to the reported historical experiments; no claim is made that these are current state-of-the-art models.

## Core technical sources

- **Ho, Jain, and Abbeel (2020), DDPM:** https://arxiv.org/abs/2006.11239. Read the forward/reverse definitions, closed-form marginal, epsilon parameterization, simplified loss, and original linear schedule (Sections 2–4; Eqs. 2, 4, 11, 14). The report adapts the equations with symbols defined locally and in Appendix C. Sections 3.4/4.1/4.2 and Tables 1/2 support the discussion of objective reweighting; the likelihood-bound derivation and endpoint caveat are kept in Appendix C.
- **Rombach et al. (2022), LDM, arXiv v2:** https://arxiv.org/abs/2112.10752. Read Sections 3.1–3.3 (perceptual autoencoder, KL/VQ variants, latent denoising, conditioning), Sections 4.1 and 4.5, and supplementary Sections E.2.2/E.3.5. Table 8 confirms the illustrative KL f=4, c=3 autoencoder shape. Table 6 is the selected quantitative pixel/latent inpainting baseline.
- **Kingma and Welling (2014), VAE:** https://arxiv.org/abs/1312.6114. Used for posterior/reparameterization/ELBO background. The report distinguishes this textbook objective from the perceptual/adversarial, weak-KL objective in LDM.
- **Ho and Salimans (2022), CFG:** https://arxiv.org/abs/2207.12598. Section 3.2 and Eq. 6 specify conditional dropout and guidance. The report's scale s is 1+w relative to that equation. The source also discusses diversity and extra denoiser evaluations.
- **Song, Meng, and Ermon (2021), DDIM:** https://arxiv.org/abs/2010.02502. Used to distinguish sampler acceleration from changing the representation to latent space; no new DDIM measurements are claimed.
- **Vaswani et al. (2017):** https://arxiv.org/abs/1706.03762. Scaled dot-product attention; report matrices use row-vector conventions. The toy example is newly constructed.
- **Heusel et al. (2017):** https://arxiv.org/abs/1706.08500. FID as a feature-distribution comparison; FID is not interpreted as prompt accuracy or an absolute percentage of image quality.
- **Goodfellow et al. (2014)** and **van den Oord et al. (2016):** the bibliography links the original GAN and PixelRNN papers for the qualitative family comparison.

## Historical and mathematical foundations added November 7, 2026

- **Sohl-Dickstein et al. (2015):** https://proceedings.mlr.press/v37/sohl-dickstein15.html. Foundation for gradual forward corruption and learned reverse diffusion.
- **Song and Ermon (2019):** https://arxiv.org/html/1907.05600v3. Sections 2-4 cover score estimation, Gaussian denoising targets, multiple noise levels, and annealed Langevin sampling. This provides a conceptual bridge, not a claim that DDPM historically starts from score matching.
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

Sourced: established equations/methods, historical paper findings, the explicitly transcribed inpainting table, the ICCV 2025 style and bibliography files. Sources are cited in the manuscript and figure/table captions. AI assistance is disclosed in Appendix B.3.


## Format migration, November 6, 2026

Scientific content, numerical data, and original figure/code assets are retained. The template entry in the bibliography now credits ICCV 2025. Long equations are reflowed and large floats span both columns. The archive and PDF are a separate edition; the previous HCMUS deliverables remain available.

## Narrative revision, November 7, 2026

The report now has seven main sections: Introduction; Background and Paper Review; Method: From Denoising to Generation; DDPM: Formulation and Worked Examples; LDM: Latent Space and Efficient Generation; Results and Discussion; Conclusion. The abstract, introduction, subtitle, and conclusion cover both DDPM and LDM. Qualitative family comparison remains in subsection 2.2. The main text is 8 pages (below the 10-page limit), followed by 1 reference page and 6 appendix pages. Upstream style files and original image/data/code remain unchanged.
