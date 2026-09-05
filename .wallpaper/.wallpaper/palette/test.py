#!/usr/bin/env python3
import os
import sys
import argparse
from PIL import Image
from ImageGoNord import GoNord
import ImageGoNord.utility.palette_loader as pl

DEFAULT_PALETTE = os.path.expanduser("~/.config/nvim/onedark-dark.txt")
FALLBACK_PALETTE = os.path.expanduser("~/onedark-dark.txt")


def load_custom_palette(go_nord, palette_path: str):
    """Load palette via add_color_to_palette (avoids PALETTE_LOOKUP_PATH relativity)."""
    with open(palette_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") is False:
                continue
            if len(line) == 7 and line[0] == "#":
                go_nord.add_color_to_palette(line)
            elif len(line) == 6:
                go_nord.add_color_to_palette(f"#{line}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to OneDark-dark palette (navarasu/onedark.nvim dark + custom opts.colors) using ImageGoNord."
    )
    parser.add_argument("-i", "--input", required=True, help="Input image file path")
    parser.add_argument("-o", "--output", required=True, help="Output image file path")
    parser.add_argument(
        "-a",
        "--avg",
        action="store_true",
        help="Use average algorithm (smoother for photos)",
    )
    parser.add_argument(
        "-q", "--quantize", action="store_true", help="Use Pillow quantization (faster)"
    )
    parser.add_argument(
        "--dither",
        choices=["floyd", "none"],
        default="floyd",
        help="Dithering for -q: floyd (default, smooth but patterned) or none (flat, best of both)",
    )
    parser.add_argument(
        "--blur",
        action="store_true",
        help="Apply Gaussian blur(1) after convert (smooths banding without dithering)",
    )
    parser.add_argument(
        "-p",
        "--palette",
        default=DEFAULT_PALETTE,
        help=f"Palette file (one #hex per line). Default: {DEFAULT_PALETTE}",
    )
    parser.add_argument(
        "--nord",
        action="store_true",
        help="Use default Nord palette instead of OneDark-dark",
    )

    args = parser.parse_args()

    go_nord = GoNord()
    go_nord.reset_palette()

    if args.nord:
        go_nord.set_default_nord_palette()
    else:
        palette_path = os.path.expanduser(args.palette)
        if not os.path.isfile(palette_path):
            if os.path.isfile(FALLBACK_PALETTE):
                palette_path = FALLBACK_PALETTE
            else:
                parser.error(
                    f"Palette file not found: {args.palette} (tried {palette_path} and {FALLBACK_PALETTE}). "
                    f"Create it or use --nord."
                )
        load_custom_palette(go_nord, palette_path)

    if args.avg:
        go_nord.enable_avg_algorithm()
    if args.blur:
        go_nord.enable_gaussian_blur()

    image = go_nord.open_image(args.input)

    if args.quantize:
        if args.dither == "none":
            data_colors = pl.create_data_colors(go_nord.get_palette_data())
            while len(data_colors) < 768:
                data_colors.extend(pl.export_tripletes_from_color("2E3440"))
            palimage = Image.new("P", (1, 1))
            palimage.putpalette(data_colors)
            if image.mode != "RGB":
                image = image.convert("RGB")
            quant = image.quantize(colors=256, method=0, kmeans=5, palette=palimage, dither=Image.Dither.NONE)
            quant = quant.convert("RGB")
            go_nord.save_image_to_file(quant, args.output)
        else:
            go_nord.quantize_image(image, save_path=args.output)
    else:
        go_nord.convert_image(image, save_path=args.output)


if __name__ == "__main__":
    main()
