# CLAUDE.md

General repository context and report rules are in `AGENTS.md`. This file adds rules for the slide deck.

## Slides and presentation script must stay consistent

The Beamer deck `slide/main.tex` has a companion presenter script, `slide/presentation-script.md`. **Whenever you edit the slides, update the script in the same change** so that the two never drift apart.

After any slide edit, check and update these parts of the script:

- **Skeleton table**: slide number, title, speaker, timing, one-line message. Also update the total time and the per-speaker totals in the checklist.
- **"Bố cục" line** of each affected slide: what is placed where (boxes, columns, figures, colours, labels).
- **👉 pointing cues**: every cue must name a region that still exists on the slide, using the slide's current wording, box titles and positions.
- **Spoken lines (English)**: numbers, equations, labels and claims must match the slide exactly. Keep the PAPER REPORTS / OUR RUN / OUR EXAMPLE attributions.
- **Cross-references** such as "slide 6" and "as on slide 4", the **transitions and speaker handovers**, and the **Q&A table's "Quay về" column**. Renumber these if slides are added, removed or reordered.
- **⚠️ Đừng nói** warnings: keep them aligned with the evidence boundaries in `AGENTS.md`.

Conventions for the script: stage directions are in Vietnamese, spoken lines are in English. Use **👉 [...]** for pointing, **✋** for emphasis, **(cắt được)** for optional lines. If a slide change makes a spoken claim unsupported, remove or rewrite that claim; do not leave it in.

## Vietnamese script

`slide/presentation-script-vi.md` is the Vietnamese version of the same script. It mirrors `slide/presentation-script.md` section by section (layout lines, 👉 cues, ✋, (cắt được), ⚠️, skeleton, Q&A, checklist), with spoken lines in Vietnamese and technical terms kept in the original English (forward noising, latent, score, guidance, FID, U-Net, VAE, encoder, decoder, sampler, …). Box titles and labels in 👉 cues stay in English, as on the slides. Write team members' names exactly as they appear on slide 1.

**Whenever you update the English script, apply the same change to the Vietnamese script** so that the two stay equivalent.

When you report a slide edit to the user, also say what changed in the script. If the script needed no change, say that too.
