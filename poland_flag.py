#!/usr/bin/env python3
"""Generate a Poland flag icon (white over red) as a rounded-corner PNG."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

# Official Polish national colors.
WHITE = (255, 255, 255, 255)
RED = (212, 33, 61, 255)  # #D4213D

_SSAA = 4


def make_flag(size: int = 512, radius_ratio: float = 0.18) -> Image.Image:
    """Return a square RGBA flag icon with rounded corners."""
    big = size * _SSAA
    flag = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(flag)

    half = big // 2
    draw.rectangle((0, 0, big, half), fill=WHITE)
    draw.rectangle((0, half, big, big), fill=RED)

    # Rounded-corner mask.
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, big - 1, big - 1), radius=int(big * radius_ratio), fill=255
    )

    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    out.paste(flag, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a Poland flag icon.")
    parser.add_argument("-o", "--output", type=Path, default=Path("poland_flag.png"))
    parser.add_argument("--size", type=int, default=512, help="Icon size in pixels.")
    parser.add_argument(
        "--radius",
        type=float,
        default=0.18,
        help="Corner radius as a fraction of size (0 = square).",
    )
    args = parser.parse_args(argv)

    make_flag(args.size, args.radius).save(args.output, format="PNG")
    print(f"Saved {args.output} ({args.size}x{args.size})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
