#!/usr/bin/env python3
"""Fix 会员权益.jpg from original — swap check/X colors only."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "BC落地页交付开发/UI/assets/会员权益_original.jpg"
OUT_DIRS = [
    ROOT / "BC落地页交付开发/UI/assets",
    ROOT / "UI/assets",
]

GOLD_CHECK_COLOR = (224, 158, 38)
GRAY_X_COLOR = (150, 150, 150)

X_MIN = 248
Y_MIN = 330


def local_bg(img: Image.Image, x: int, y: int, radius: int = 5) -> tuple[int, int, int]:
    px = img.load()
    samples: list[tuple[int, int, int]] = []
    w, h = img.size
    for dy in range(-radius, radius + 1, 2):
        for dx in range(-radius, radius + 1, 2):
            if dx == 0 and dy == 0:
                continue
            xx, yy = x + dx, y + dy
            if 0 <= xx < w and 0 <= yy < h:
                samples.append(px[xx, yy][:3])
    if not samples:
        return px[x, y][:3]
    samples.sort(key=lambda c: sum(c))
    return samples[len(samples) // 2]


def is_stroke(img: Image.Image, x: int, y: int) -> bool:
    px = img.load()
    c = px[x, y][:3]
    bg = local_bg(img, x, y, 6)
    return abs(sum(c) - sum(bg)) > 28


def is_gray_check(r: int, g: int, b: int) -> bool:
    avg = (r + g + b) / 3
    sat = max(r, g, b) - min(r, g, b)
    return 65 < avg < 205 and sat < 42


def is_gold_x(r: int, g: int, b: int, bg: tuple[int, int, int]) -> bool:
    if not (r > 155 and g > 75 and b < 145 and r >= g):
        return False
    bg_l = sum(bg) / 3
    px_l = (r + g + b) / 3
    sat = max(r, g, b) - min(r, g, b)
    if sat < 35:
        return False
    return px_l < bg_l - 6 or (r - bg[0] > 15 and b < bg[2] - 15)


def swap_mark_colors(img: Image.Image) -> Image.Image:
    out = img.copy()
    px = out.load()
    w, h = out.size

    for y in range(Y_MIN, h):
        for x in range(X_MIN, w):
            r, g, b = px[x, y][:3]
            bg = local_bg(out, x, y, 6)

            if is_gray_check(r, g, b) and is_stroke(out, x, y):
                px[x, y] = GOLD_CHECK_COLOR
            elif is_gold_x(r, g, b, bg) and is_stroke(out, x, y):
                px[x, y] = GRAY_X_COLOR

    return out


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    img = Image.open(SRC).convert("RGB")
    fixed = swap_mark_colors(img)
    for out_dir in OUT_DIRS:
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / "会员权益.jpg"
        fixed.save(dest, format="JPEG", quality=92, optimize=True)
        print(f"wrote {dest} ({fixed.size[0]}x{fixed.size[1]})")


if __name__ == "__main__":
    main()
