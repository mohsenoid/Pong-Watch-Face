"""Generates original pixel-art assets for the arcade-theme watch face.

Everything here is hand-authored/procedurally generated (a classic
seven-segment LED-scoreboard digit renderer, plus original shapes for the
background, river strip, and sprite) - nothing is traced or derived from
any copyrighted game's art.

Run with: python3 watchface/scripts/generate_pixel_assets.py
Outputs into watchface/src/main/res/drawable/.
"""

import math
import os

from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DRAWABLE_DIR = os.path.join(SCRIPT_DIR, "..", "src", "main", "res", "drawable")

ACCENT_COLOR = (255, 106, 0, 255)  # Atari-style orange/red
SPRITE_COLOR = (235, 235, 235, 255)  # off-white jet body
SPRITE_SHADOW = (25, 45, 60, 140)  # soft shadow cast on the water
RIVER_COLOR = (16, 82, 122, 255)
RIVER_WAVE_COLOR = (54, 140, 180, 255)
BANK_COLOR = (58, 130, 62, 255)
BANK_SHADE_COLOR = (44, 104, 48, 255)
CANVAS_SIZE = 450

# Atari 2600-style 6x8 digit font, transcribed from a byte-table reference
# the user provided and cross-checked bit-for-bit (each byte's bits 6..1
# are one 6-pixel-wide row; bit 7 and bit 0 are always unused padding).
DIGIT_ROWS = {
    "0": ["111111", "100001", "100001", "100011", "100011", "100011", "111111", "000000"],
    "1": ["001100", "000100", "000100", "000100", "001110", "001110", "001110", "000000"],
    "2": ["111111", "100011", "000011", "111111", "100000", "100000", "111111", "000000"],
    "3": ["111110", "000010", "000010", "011111", "000011", "000011", "111111", "000000"],
    "4": ["100010", "100010", "100010", "111111", "000110", "000110", "000110", "000000"],
    "5": ["111111", "100000", "100000", "111111", "000011", "100011", "111111", "000000"],
    "6": ["111110", "100010", "100000", "111111", "100011", "100011", "111111", "000000"],
    "7": ["011111", "000001", "000001", "000011", "000011", "000011", "000011", "000000"],
    "8": ["011110", "010010", "010010", "111111", "100011", "100011", "111111", "000000"],
    "9": ["111111", "100001", "100001", "111111", "000011", "000011", "000011", "000000"],
}

GRID_COLS = 6
GRID_ROWS = 8
DIGIT_SCALE = 15  # pixels per grid cell
DIGIT_WIDTH = GRID_COLS * DIGIT_SCALE
DIGIT_HEIGHT = GRID_ROWS * DIGIT_SCALE


def render_digit(rows, color, scale=DIGIT_SCALE):
    width = len(rows[0]) * scale
    height = len(rows) * scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()
    for row_index, row in enumerate(rows):
        for col_index, bit in enumerate(row):
            if bit != "1":
                continue
            for dy in range(scale):
                for dx in range(scale):
                    pixels[col_index * scale + dx, row_index * scale + dy] = color
    return img


def generate_digits():
    for digit, rows in DIGIT_ROWS.items():
        img = render_digit(rows, ACCENT_COLOR)
        img.save(os.path.join(DRAWABLE_DIR, f"digit_{digit}.png"))

    # The hour-tens digit is only ever blank or "1" in 12-hour time, so it's
    # shown as a plain PartImage gated by an hour Condition instead of a
    # TimeText token. It needs its own drawable copy, separate from
    # digit_1.png: on this WFF runtime, a drawable referenced by both a
    # BitmapFont Character mapping and a plain PartImage fails to render in
    # the PartImage - the BitmapFont-mapped copy renders fine as a text
    # glyph but the standalone image usage silently shows nothing.
    one_img = render_digit(DIGIT_ROWS["1"], ACCENT_COLOR)
    one_img.save(os.path.join(DRAWABLE_DIR, "hour_leading_one.png"))

    colon_width = 30
    colon_img = Image.new("RGBA", (colon_width, DIGIT_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(colon_img)
    dot = DIGIT_SCALE
    cx = colon_width / 2
    for cy in (DIGIT_HEIGHT * 0.32, DIGIT_HEIGHT * 0.68):
        draw.rectangle(
            (cx - dot / 2, cy - dot / 2, cx + dot / 2, cy + dot / 2),
            fill=ACCENT_COLOR,
        )
    colon_img.save(os.path.join(DRAWABLE_DIR, "digit_colon.png"))


def generate_scanline_background():
    img = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 255))
    pixels = img.load()
    for y in range(CANVAS_SIZE):
        # Faint scanline every 4px; keeps the background readably dark.
        if y % 4 == 0:
            shade = 24
        else:
            shade = 8
        for x in range(CANVAS_SIZE):
            pixels[x, y] = (shade, shade, shade, 255)
    img.save(os.path.join(DRAWABLE_DIR, "bg_scanlines.png"))


def generate_river_strip():
    width, height = CANVAS_SIZE, 64
    bank_h = 9
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if y < bank_h or y >= height - bank_h:
                # Grassy riverbank, with a slightly darker shoreline row
                # right at the water's edge for definition.
                is_edge = y == bank_h - 1 or y == height - bank_h
                pixels[x, y] = BANK_SHADE_COLOR if is_edge else BANK_COLOR
            else:
                # Undulating wave bands (a sine offset per column) instead
                # of a flat diagonal weave, so it actually reads as water.
                y_rel = y - bank_h
                wave = 2.5 * math.sin((x / 22.0) + (y_rel / 5.0))
                band = int(y_rel + wave) % 10
                pixels[x, y] = RIVER_WAVE_COLOR if band < 3 else RIVER_COLOR
    img.save(os.path.join(DRAWABLE_DIR, "river_strip.png"))


# A top-down jet silhouette (nose, fuselage, swept wings, twin tail fins) on
# a 21-wide x 11-tall grid, defined as filled column ranges per row so the
# shape is unambiguous - no hand-counted ASCII art to mistype.
JET_GRID_WIDTH = 21
JET_GRID_HEIGHT = 11
JET_ROWS = {
    0: [(10, 10)],
    1: [(10, 10)],
    2: [(9, 11)],
    3: [(9, 11)],
    4: [(8, 12)],
    5: [(2, 3), (8, 12), (17, 18)],
    6: [(0, 4), (8, 12), (16, 20)],
    7: [(2, 3), (8, 12), (17, 18)],
    8: [(8, 12)],
    9: [(7, 8), (12, 13)],
    10: [(6, 7), (13, 14)],
}


def generate_sprite_jet():
    scale = 4
    width = JET_GRID_WIDTH * scale
    height = JET_GRID_HEIGHT * scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()
    for row_index in range(JET_GRID_HEIGHT):
        for start, end in JET_ROWS.get(row_index, []):
            for col_index in range(start, end + 1):
                for dy in range(scale):
                    for dx in range(scale):
                        pixels[col_index * scale + dx, row_index * scale + dy] = SPRITE_COLOR
    img.save(os.path.join(DRAWABLE_DIR, "sprite_jet.png"))


def main():
    os.makedirs(DRAWABLE_DIR, exist_ok=True)
    generate_digits()
    generate_scanline_background()
    generate_river_strip()
    generate_sprite_jet()
    print("Generated pixel-art assets in", os.path.abspath(DRAWABLE_DIR))


if __name__ == "__main__":
    main()
