#!/usr/bin/env python3

import sys
import glob
from pathlib import Path

GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# OLED display dimensions
WIDTH = 128
HEIGHT = 64
BUFFER_SIZE = WIDTH * HEIGHT // 8  # 1024 bytes


def resolve_inputs(args):
    """Resolve input files or glob patterns to a list of Paths"""
    files = []

    for arg in args:
        matches = glob.glob(arg)

        if not matches:
            print(f"No matches for: {arg}")
            continue

        for match in matches:
            path = Path(match)
            if path.is_file() and path.suffix.lower() == ".txt":
                files.append(path)

    return files


def convert_txt_to_bin(txt_file: Path, output_dir: Path):
    """Convert a text file of pixel coordinates into a 1024-byte OLED framebuffer"""
    buffer = bytearray(BUFFER_SIZE)  # start with all zeros

    with open(txt_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            x_str, y_str = line.split(",")
            x = int(x_str)
            y = int(y_str)

            page = y // 8
            bit = y % 8
            index = x + page * WIDTH

            buffer[index] |= 1 << bit

    output_file = output_dir / f"{txt_file.stem}.bin"
    with open(output_file, "wb") as f:
        f.write(buffer)

    print(f"{GREEN}Saved binary frame:{RESET} {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python txt_to_bin.py <file|folder|pattern> [...]")
        sys.exit(1)

    input_args = sys.argv[1:]
    files = resolve_inputs(input_args)

    if not files:
        print("No text files found to convert.")
        sys.exit(1)

    output_dir = Path("output_bin_frames")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Files to process:")
    for file in files:
        print(f"{YELLOW}{file}{RESET}")
        convert_txt_to_bin(file, output_dir)


if __name__ == "__main__":
    main()
