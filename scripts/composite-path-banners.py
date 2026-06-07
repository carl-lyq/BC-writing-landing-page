#!/usr/bin/env python3
"""Resize path banners and composite official 躺着学 logo top-left."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GEN = Path("/Users/mac/.cursor/projects/Users-mac-Library-CloudStorage-OneDrive-AI-Projects-BC/assets")
LOGO_PATH = ROOT / "BC落地页交付开发/UI/assets/躺着学LOGO CHILLPREP.png"
TARGET_SIZE = (1580, 988)
LOGO_MAX_WIDTH = 210
LOGO_PADDING = (71, 50)

ASSET_DIRS = [
    ROOT / "BC落地页交付开发/UI/assets",
    ROOT / "UI/assets",
]


def load_logo(max_width: int) -> Image.Image:
    logo = Image.open(LOGO_PATH).convert("RGBA")
    scale = max_width / logo.width
    size = (max_width, max(1, round(logo.height * scale)))
    return logo.resize(size, Image.Resampling.LANCZOS)


def composite_banner(src: Path, dest: Path, logo: Image.Image) -> None:
    banner = Image.open(src).convert("RGBA")
    banner = banner.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
    x, y = LOGO_PADDING
    banner.alpha_composite(logo, (x, y))
    banner.convert("RGB").save(dest, format="PNG", optimize=True)


def main() -> None:
    logo = load_logo(LOGO_MAX_WIDTH)
    for asset_dir in ASSET_DIRS:
        asset_dir.mkdir(parents=True, exist_ok=True)
        for i in range(1, 7):
            src = GEN / f"path-banner-{i:02d}-v2.png"
            dest = asset_dir / f"path-banner-{i:02d}.png"
            if not src.exists():
                raise FileNotFoundError(src)
            composite_banner(src, dest, logo)
            print(f"wrote {dest}")


if __name__ == "__main__":
    main()
