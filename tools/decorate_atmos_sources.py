#!/usr/bin/env python3
"""Create hand-tuned atmOS nice!view source frames.

The generated source PNGs are already in the raw 140x68 LVGL orientation. Use
`tools/convert_nice_view_art.py --rotate 0 --safe-width 140 --margin 0` on the
approved outputs.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


RAW_SIZE = (140, 68)
MOUNTED_SIZE = (68, 140)
STATUS_HEIGHT = 28


@dataclass(frozen=True)
class Placement:
    moon_side: str
    moon_dx: int = 0
    moon_dy: int = 0
    scale: float = 1.0


PLACEMENTS: dict[str, Placement] = {
    "wizard_color": Placement("right", 2, 0, 0.96),
    "detective": Placement("right", 0, -1, 0.98),
    "chef": Placement("right", -1, 0, 0.98),
    "dj": Placement("left", 1, -1, 1.0),
    "pirate": Placement("left", 0, 0, 0.98),
    "gardener": Placement("right", -2, 1, 0.98),
    "designer": Placement("left", 1, 0, 1.0),
    "security": Placement("left", 0, -1, 0.99),
    "engineer": Placement("right", -2, 0, 1.0),
    "scientist": Placement("left", 1, 0, 0.98),
    "support": Placement("right", -1, 0, 1.0),
    "legal": Placement("left", 1, -1, 0.98),
    "finance": Placement("right", -1, 0, 0.98),
    "operations": Placement("left", 0, 0, 1.0),
    "data_analyst": Placement("right", -1, 0, 1.0),
    "product_manager": Placement("left", 1, 0, 0.99),
    "writer": Placement("right", -1, 0, 0.99),
    "scheduler": Placement("left", 1, -1, 1.0),
    "email": Placement("left", 0, 0, 0.99),
    "automation": Placement("right", -1, 0, 1.0),
}


def frame_name(path: Path) -> str:
    name = path.stem
    name = name.removeprefix("avatar-").removesuffix("-v1")
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()


def line_art(path: Path, threshold: int) -> Image.Image:
    src = Image.open(path).convert("RGB")
    gray = src.convert("L")
    mask = gray.point(lambda pixel: 0 if pixel < threshold else 255, mode="1")
    bbox = ImageOps.invert(mask.convert("L")).getbbox()
    if bbox is None:
        return Image.new("1", (1, 1), 1)
    return mask.crop(bbox)


def draw_star(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 1) -> None:
    draw.point((x, y), fill=0)
    for delta in range(1, size + 1):
        draw.point((x - delta, y), fill=0)
        draw.point((x + delta, y), fill=0)
        draw.point((x, y - delta), fill=0)
        draw.point((x, y + delta), fill=0)


def draw_crescent(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 8) -> None:
    draw.ellipse((x, y, x + size, y + size), fill=0)
    draw.ellipse((x + size // 2, y - 1, x + size + 2, y + size - 1), fill=1)


def decorate(canvas: Image.Image, art_bbox: tuple[int, int, int, int], placement: Placement) -> None:
    draw = ImageDraw.Draw(canvas)
    left, top, right, _ = art_bbox
    center = (left + right) // 2
    moon_y = max(STATUS_HEIGHT + 3, top - 18 + placement.moon_dy)

    if placement.moon_side == "left":
        moon_x = max(5, left - 2 + placement.moon_dx)
        star_positions = [
            (min(62, center + 9), moon_y + 1, 1),
            (min(62, center + 20), moon_y + 7, 0),
            (max(5, moon_x - 3), moon_y + 13, 0),
        ]
    else:
        moon_x = min(55, right - 8 + placement.moon_dx)
        star_positions = [
            (max(5, center - 9), moon_y + 1, 1),
            (max(5, center - 21), moon_y + 8, 0),
            (min(62, moon_x + 11), moon_y + 13, 0),
        ]

    draw_crescent(draw, moon_x, moon_y, 8)
    for x, y, size in star_positions:
        draw_star(draw, x, y, size)


def compose(path: Path, threshold: int) -> Image.Image:
    name = frame_name(path)
    placement = PLACEMENTS.get(name, Placement("right"))
    art = line_art(path, threshold)

    max_w = 62
    max_h = int(90 * placement.scale)
    art.thumbnail((max_w, max_h), Image.Resampling.NEAREST)

    canvas = Image.new("1", MOUNTED_SIZE, 1)
    x = (MOUNTED_SIZE[0] - art.width) // 2
    y = min(MOUNTED_SIZE[1] - art.height - 3, STATUS_HEIGHT + 18)
    canvas.paste(art, (x, y))
    decorate(canvas, (x, y, x + art.width, y + art.height), placement)
    return canvas


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--preview-dir", type=Path)
    parser.add_argument("--threshold", default=220, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)

    for image_path in args.images:
        mounted = compose(image_path, args.threshold)
        raw = mounted.rotate(-90, expand=True)
        name = frame_name(image_path)
        raw.save(args.output_dir / f"atmos_avatar_{name}_v1.png")

        if args.preview_dir:
            preview = ImageOps.invert(mounted.convert("L"))
            preview.save(args.preview_dir / f"atmos_avatar_{name}_v1.png")


if __name__ == "__main__":
    main()
