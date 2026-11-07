"""Generate the original RGB scene/noise tiles used in Figure 1.

Python standard library only; no dataset, pretrained model, or GPU is used.
Run: python code/make_overview.py
The four frames are subsampled from the Gaussian Markov forward process.
Reverse arrows in the LaTeX figure are conceptual, not a model experiment.
"""
from pathlib import Path
import math
import random
import struct
import zlib

OUT = Path(__file__).resolve().parents[1] / "figures" / "diffusion_overview"
SIDE = 112
LEVELS = (0, 100, 300, 1000)


def polygon(x, y, vertices):
    inside = False
    previous = vertices[-1]
    for current in vertices:
        ax, ay = previous
        bx, by = current
        if (ay > y) != (by > y):
            if x < (bx - ax) * (y - ay) / (by - ay) + ax:
                inside = not inside
        previous = current
    return inside


def scene():
    pixels = []
    for iy in range(SIDE):
        for ix in range(SIDE):
            x, y = ix * 100 / SIDE, iy * 100 / SIDE
            color = (80 + y * 1.15, 158 + y * .65, 211 + y * .15)
            if (x - 78) ** 2 + (y - 20) ** 2 < 9 ** 2:
                color = (255, 212, 91)
            if polygon(x, y, [(-10, 70), (27, 16), (73, 70)]):
                color = (75, 106, 129)
            if polygon(x, y, [(17, 31), (27, 16), (42, 34), (31, 29), (27, 33), (23, 28)]):
                color = (239, 245, 237)
            if polygon(x, y, [(36, 73), (67, 30), (112, 73)]):
                color = (104, 140, 151)
            if polygon(x, y, [(57, 44), (67, 30), (81, 44), (70, 40), (66, 44), (63, 40)]):
                color = (236, 243, 232)
            if y > 67 + 3 * math.sin(x / 15):
                color = (86, 143, 98)
            if y > 81 + 2 * math.sin(x / 17):
                color = (65, 155, 176)
                if (int(y) in (88, 94) and 50 < x < 83) or (int(y) == 97 and 10 < x < 32):
                    color = (173, 217, 210)
            if 72 < x < 76 and 53 < y < 78:
                color = (90, 83, 61)
            for top, half, bottom in [(46, 8, 62), (53, 10, 71)]:
                if polygon(x, y, [(74, top), (74 - half, bottom), (74 + half, bottom)]):
                    color = (34, 101, 82)
            if 24 < x < 58 and 53 < y < 79:
                color = (242, 201, 140) if int(y) % 6 else (215, 165, 110)
            if 29 < x < 33 and 40 < y < 50:
                color = (119, 76, 66)
            if polygon(x, y, [(18, 55), (41, 35), (64, 55)]):
                color = (195, 76, 62)
            if polygon(x, y, [(18, 55), (41, 35), (41, 39), (23, 55)]):
                color = (236, 127, 91)
            if 37 < x < 46 and 63 < y < 79:
                color = (47, 103, 107)
            for left in (27, 49):
                if left < x < left + 6 and 61 < y < 68:
                    color = (255, 225, 126)
                    if abs(x - (left + 3)) < .5 or abs(y - 64.5) < .5:
                        color = (133, 104, 76)
            pixels.extend(2 * component / 255 - 1 for component in color)
    return pixels


def png(path, values):
    displayed = bytes(round(255 * (max(-1, min(1, value)) + 1) / 2) for value in values)
    stride = SIDE * 3
    raw = b"".join(b"\0" + displayed[row * stride:(row + 1) * stride] for row in range(SIDE))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)

    header = struct.pack(">IIBBBBB", SIDE, SIDE, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    alpha_bar = [1.0]
    for step in range(1000):
        beta = 1e-4 + step * (.02 - 1e-4) / 999
        alpha_bar.append(alpha_bar[-1] * (1 - beta))
    rng = random.Random(421)
    current = scene()
    previous = 0
    for level in LEVELS:
        if level:
            retained = alpha_bar[level] / alpha_bar[previous]
            signal, noise = math.sqrt(retained), math.sqrt(1 - retained)
            current = [signal * value + noise * rng.gauss(0, 1) for value in current]
        png(OUT / f"state_{level}.png", current)
        previous = level
    print(f"Wrote {len(LEVELS)} original forward-process tiles to {OUT}")


if __name__ == "__main__":
    main()
