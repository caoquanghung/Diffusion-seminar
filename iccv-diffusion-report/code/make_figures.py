"""Reproduce the report's original 28x28 forward-noising illustration.

No dataset, pretrained model, GPU, or network access is required.
Run from any directory: python code/make_figures.py
Dependencies: numpy, reportlab. The arrays are never clipped; clipping is
used only to display each image on the same [-1, 1] intensity scale.
"""
from pathlib import Path
import csv
import json
import numpy as np
from reportlab.pdfgen import canvas
from reportlab import Version as reportlab_version

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
SEED, T = 420, 1000
LEVELS = [0, 50, 200, 500, 1000]


def main():
    rng = np.random.default_rng(SEED)
    # Original geometric house: background=-1, foreground=+1.
    yy, xx = np.mgrid[:28, :28]
    house = ((yy >= 12) & (yy <= 23) & (xx >= 7) & (xx <= 21))
    roof = ((yy >= 4) & (yy <= 12) & (np.abs(xx - 14) <= yy - 3))
    x0 = np.where(house | roof, 1.0, -1.0)
    x0[17:24, 13:17] = -1.0
    x0[14:17, 9:12] = -1.0
    x0[14:17, 18:21] = -1.0
    beta = np.linspace(1e-4, 0.02, T, dtype=np.float64)
    abar = np.concatenate(([1.0], np.cumprod(1.0 - beta)))
    current = x0.copy()
    frames = {0: current.copy()}
    for t in range(1, T + 1):
        current = np.sqrt(1.0 - beta[t-1]) * current + np.sqrt(beta[t-1]) * rng.standard_normal(x0.shape)
        if t in LEVELS:
            frames[t] = current.copy()
    np.savez_compressed(OUT / "noise_arrays.npz", beta=beta, alpha_bar=abar,
                        timesteps=np.array(LEVELS), images=np.stack([frames[t] for t in LEVELS]))
    rows = []
    for t in LEVELS:
        rows.append({"t": t, "alpha_bar": float(abar[t]),
                     "signal_multiplier": float(np.sqrt(abar[t])),
                     "noise_std": float(np.sqrt(1.0 - abar[t])),
                     "snr_coefficient": None if t == 0 else float(abar[t]/(1.0-abar[t]))})
    with (OUT / "noise_levels.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    c = canvas.Canvas(str(OUT / "noise_sequence.pdf"), pagesize=(610, 152), invariant=1)
    c.setTitle("Original 28x28 forward diffusion illustration; seed 420")
    for index, t in enumerate(LEVELS):
        left, bottom, side = 12 + index*122, 27, 98
        cell = side / 28
        c.setFillColorRGB(.08, .13, .21)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(left + side/2, 136, f"t = {t}")
        frame = (np.clip(frames[t], -1, 1) + 1)/2
        for iy in range(28):
            for ix in range(28):
                c.setFillGray(float(frame[iy, ix]))
                c.rect(left + ix*cell, bottom+(27-iy)*cell, cell+.015, cell+.015, fill=1, stroke=0)
        c.setStrokeColorRGB(.75, .78, .82)
        c.rect(left, bottom, side, side, stroke=1, fill=0)
        c.setFillColorRGB(.08, .13, .21)
        c.setFont("Helvetica", 9)
        shown_alpha = f"{abar[t]:.4f}" if abar[t] >= 1e-3 else f"{abar[t]:.2e}"
        c.drawCentredString(left + side/2, 10, f"alpha_bar = {shown_alpha}")
    c.save()
    # Arithmetic derived from the published inpainting baseline, not timings
    # measured by this script. Source: Rombach et al. (2022), Table 6.
    analysis = {
        "seed": SEED, "T": T, "levels": rows,
        "worked_example": {"x0": .8, "beta1": .1, "epsilon": -.5,
                           "x1": float(np.sqrt(.9)*.8 + np.sqrt(.1)*(-.5)),
                           "mean": float(np.sqrt(.9)*.8), "variance": .1},
        "table6_derived": {"sampling_speedup_256": .97/.26,
                           "sampling_speedup_512": .34/.07,
                           "training_throughput_ratio": .32/.11,
                           "epoch_time_speedup": 20.66/7.66,
                           "FID_relative_reduction": (24.74-15.21)/24.74},
        "versions": {"numpy": np.__version__, "reportlab": reportlab_version},
    }
    (OUT / "analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
