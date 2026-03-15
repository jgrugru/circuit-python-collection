#!/usr/bin/env python3

# if using uv, you can run the script with this command
# uv run --no-project --with pillow extract_pixels.py pixel_art_file.png
# ^ this just lets you run it with uv without creating a venv,
# much faster to setup since this is a one-off script

# Examples of how to run this script:
# ====================================
# uv run --no-project --with pillow python extract_pixels.py logo.png
# uv run --no-project --with pillow python extract_pixels.py logo.png icon.png
# uv run --no-project --with pillow python extract_pixels.py pixel_art/*.png

# if not using uv, just download Pillow from pypi and run the script

import sys
import glob
from typing import Iterable
from pathlib import Path
from PIL import Image

GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

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
    output_dir = Path("output")
    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print("Usage: python extract_pixels.py <file|folder|pattern> [...]")
        sys.exit(1)

    input_args = sys.argv[1:]
    files = resolve_inputs(input_args)

    print("Files to process:")
    for file in files:
        print(f"{YELLOW}Processing file:{RESET} {file}")
        with Image.open(file) as im:
            """This block of code loops through each pixel in the png.
            If it finds that the transparency value (a)
            is not 0, it will write the coordinates to a coords.txt file"""
            im = im.convert('RGBA')
            pix = im.load()
            width, height = im.size
            output_file = output_dir / f"{file.stem}.txt"
            with open(output_file, mode="w") as f:

                for x in range(width):
                    for y in range(height):
                        # RGBA tuple
                        rgba = pix[x, y]
                        r, g, b, a = rgba
                        if a != 0:
                            f.write(f"{x},{y}\n")
            print(f"{GREEN}Successfully saved {output_file}{RESET}")
    
if __name__ == "__main__":
    main()