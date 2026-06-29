#!/usr/bin/env python3
"""Crop an image into a circle with a transparent background.

The image is first center-cropped to a square (using the shorter side),
then masked with an anti-aliased circle and saved as a PNG so the corners
outside the circle are fully transparent.

Usage:
    python circle_crop.py input.jpg
    python circle_crop.py input.jpg -o avatar.png
    python circle_crop.py input.jpg --size 512
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

# Super-sampling factor for a smooth, anti-aliased circle edge.
_SSAA = 4


def crop_to_circle(image: Image.Image, size: int | None = None) -> Image.Image:
    """Return a square RGBA image cropped to a circle with transparent corners."""
    img = image.convert("RGBA")

    # Center-crop to a square using the shorter side.
    side = min(img.size)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))

    if size:
        img = img.resize((size, size), Image.LANCZOS)
        side = size

    # Build an anti-aliased circular mask via super-sampling.
    big = side * _SSAA
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big - 1, big - 1), fill=255)
    mask = mask.resize((side, side), Image.LANCZOS)

    result = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crop an image into a circle.")
    parser.add_argument("input", type=Path, help="Path to the input image.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PNG path (default: <input>_circle.png).",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=None,
        help="Optional output diameter in pixels (square).",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        return 1

    output = args.output or args.input.with_name(f"{args.input.stem}_circle.png")

    with Image.open(args.input) as image:
        result = crop_to_circle(image, size=args.size)
        result.save(output, format="PNG")

    print(f"Saved circular crop to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
