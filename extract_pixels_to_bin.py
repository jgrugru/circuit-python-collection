#!/usr/bin/env python3

# if using uv, you can run the script with this command
# uv run --no-project --with pillow extract_pixels_to_bin.py pixel_art_file.png
# ^ this just lets you run it with uv without creating a venv,
# much faster to setup since this is a one-off script

# Examples of how to run this script:
# ====================================
# uv run --no-project --with pillow python extract_pixels_to_bin.py logo.png
# uv run --no-project --with pillow python extract_pixels_to_bin.py logo.png icon.png
# uv run --no-project --with pillow python extract_pixels_to_bin.py pixel_art/*.png

# if not using uv, just download Pillow from pypi and run the script

import sys
import glob
from typing import Iterable
from pathlib import Path
from PIL import Image

GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

WIDTH = 128
HEIGHT = 64
BUFFER_SIZE = WIDTH * HEIGHT // 8  # 1024 bytes


# the ssd1306 actually expects a length of 1025 bytes. The first byte is a control byte, so in our case we'll have to have the first byte be 0x40
# or just leave as is and in your code, you can do this: `oled.buffer[1:] = buffer``
# 0x00 → the following bytes are commands
# 0x40 → the following bytes are pixel data
def resolve_inputs(args: Iterable[str]) -> list[Path]:
    files = []

    for arg in args:
        matches = glob.glob(arg)

        if not matches:
            print(f"No matches for: {arg}")
            continue

        for match in matches:
            path = Path(match)

            if path.is_dir():
                files.extend(path.glob("*.png"))

            elif path.is_file() and path.suffix.lower() == ".png":
                files.append(path)

    return files


def main():
    output_dir = Path("output_pixel_coords")
    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print("Usage: python extract_pixels_to_bin.py <file|folder|pattern> [...]")
        sys.exit(1)

    input_args = sys.argv[1:]
    files = resolve_inputs(input_args)

    for file in files:
        print(f"{YELLOW}Processing file:{RESET} {file}")
        buffer = bytearray(BUFFER_SIZE)  # start with all zeros

        output_file = output_dir / f"{file.stem}.bin"

        with Image.open(file) as im:
            """This block of code loops through each pixel in the png.
            If it finds that the transparency value (a)
            is not 0, it will turn the pixel on in the buffer at said coordinates."""
            im = im.convert("RGBA")
            pix = im.load()
            width, height = im.size

            for x in range(width):
                for y in range(height):
                    # RGBA tuple
                    rgba = pix[x, y]
                    _r, _g, _b, a = rgba
                    if a != 0:
                        page = y // 8
                        bit = y % 8
                        index = x + page * WIDTH
                        buffer[index] |= 1 << bit

        with open(output_file, "wb") as f:
            f.write(buffer)
        print(f"{GREEN}Successfully saved {output_file}{RESET}")


if __name__ == "__main__":
    main()
