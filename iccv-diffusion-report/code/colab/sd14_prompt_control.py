#@title Stable Diffusion v1.4 | Prompt-based control (16 images)
"""Run only this cell on a Colab GPU to reproduce the prompt comparison."""

import hashlib
import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import torch

if not torch.cuda.is_available():
    raise RuntimeError("Select a GPU runtime before running this cell.")

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "diffusers==0.35.2",
     "transformers==4.57.3", "accelerate", "safetensors"],
    check=True,
)

import diffusers
import transformers
from diffusers import DDIMScheduler, StableDiffusionPipeline
from huggingface_hub import HfApi
from IPython.display import display
from PIL import Image, ImageDraw, ImageFont

MODEL_ID = "CompVis/stable-diffusion-v1-4"
SEEDS = (2026, 2027, 2028, 2029)
CONDITIONS = {
    "Baseline": "A bus and a car.",
    "Reference": "A red bus to the left of a blue car.",
    "Change color": "A green bus to the left of a blue car.",
    "Change side": "A red bus to the right of a blue car.",
}
OUTPUT = Path("/content/sd14_prompt_control")
OUTPUT.mkdir(parents=True, exist_ok=True)

print(f"Loading {MODEL_ID} on {torch.cuda.get_device_name()}", flush=True)
revision = HfApi().model_info(MODEL_ID, token=False).sha
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, revision=revision, variant="fp16", torch_dtype=torch.float16,
    use_safetensors=True, token=False,
).to("cuda")
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
pipe.set_progress_bar_config(disable=True)
print(f"Checkpoint loaded at {revision}. Starting the 16 samples.", flush=True)

samples = []
with torch.inference_mode():
    for seed in SEEDS:
        rng = torch.Generator(device="cuda").manual_seed(seed)
        latent = torch.randn((1, 4, 64, 64), generator=rng, device="cuda", dtype=torch.float16)
        latent_sha = hashlib.sha256(latent.cpu().numpy().tobytes()).hexdigest()
        for condition, prompt in CONDITIONS.items():
            result = pipe(
                prompt=prompt, latents=latent.clone(), height=512, width=512,
                num_inference_steps=50, guidance_scale=7.5, eta=0.0,
            )
            filename = f"{seed}_{condition.lower().replace(' ', '_')}.png"
            result.images[0].save(OUTPUT / filename)
            flagged = bool(result.nsfw_content_detected and result.nsfw_content_detected[0])
            samples.append({"seed": seed, "condition": condition, "prompt": prompt,
                            "file": filename, "latent_sha256": latent_sha, "flagged": flagged})
            print(f"[{len(samples):02d}/16] {seed} | {condition}" +
                  (" | flagged by safety checker" if flagged else ""), flush=True)

tile, gap, left, top = 284, 12, 76, 148
width = left + len(CONDITIONS) * (tile + gap)
height = top + len(SEEDS) * (tile + gap) + 12
grid = Image.new("RGB", (width, height), "#f5f5f2")
draw = ImageDraw.Draw(grid)
title = ImageFont.load_default(size=29)
label = ImageFont.load_default(size=20)
small = ImageFont.load_default(size=16)
draw.text((15, 10), "Stable Diffusion v1.4 | Changing the prompt", fill="#171717", font=title)
draw.text((15, 49), "Same initial latent within each row. 512 x 512, DDIM 50, CFG 7.5.",
          fill="#454545", font=small)
for col, (condition, prompt) in enumerate(CONDITIONS.items()):
    x = left + col * (tile + gap)
    draw.text((x, 78), condition, fill="#171717", font=label)
    draw.multiline_text((x, 104), textwrap.fill(prompt, width=31), fill="#454545", font=small)
for row, seed in enumerate(SEEDS):
    y = top + row * (tile + gap)
    draw.text((15, y + 5), str(seed), fill="#171717", font=label)
    for col, sample in enumerate(samples[row * len(CONDITIONS):(row + 1) * len(CONDITIONS)]):
        with Image.open(OUTPUT / sample["file"]) as frame:
            grid.paste(frame.resize((tile, tile), Image.Resampling.LANCZOS), (left + col * (tile + gap), y))
grid.save(OUTPUT / "comparison.png")
metadata = {
    "model": MODEL_ID, "revision": revision, "gpu": torch.cuda.get_device_name(),
    "torch": torch.__version__, "diffusers": diffusers.__version__,
    "transformers": transformers.__version__, "dtype": "fp16",
    "resolution": [512, 512], "steps": 50, "guidance_scale": 7.5, "eta": 0.0,
    "scheduler": dict(pipe.scheduler.config), "samples": samples,
}
(OUTPUT / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")
archive = shutil.make_archive("/content/sd14_prompt_control_results", "zip", OUTPUT)
print(f"Completed {len(samples)}/16. Download from Colab Files: {archive}", flush=True)
display(grid)
