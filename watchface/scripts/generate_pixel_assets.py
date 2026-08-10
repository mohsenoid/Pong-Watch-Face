"""Generates original pixel-art assets for the arcade-theme watch face.

Everything here is hand-authored/procedurally generated (a pixel-grid
digit font transcribed from a user-provided reference, plus original
shapes for the background and a Pong-style bouncing arena: a dashed
center divider, two paddle bars, and a bouncing ball) - nothing is
traced or derived from any copyrighted game's art.

Run with: python3 watchface/scripts/generate_pixel_assets.py
Outputs into watchface/src/main/res/drawable/.
"""

import os

from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DRAWABLE_DIR = os.path.join(SCRIPT_DIR, "..", "src", "main", "res", "drawable")

ACCENT_COLOR = (255, 106, 0, 255)  # Atari-style orange/red (time display only)
DIVIDER_COLOR = (240, 240, 240, 255)  # bright white arena barrier
PADDLE_COLOR = (245, 245, 245, 255)  # classic white Pong paddles
BALL_COLOR = (255, 230, 0, 255)  # bright yellow bouncing ball
CANVAS_SIZE = 450
ARENA_BAND_HEIGHT = 48  # matches the paddle height so they align

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
DIGIT_SCALE = 13  # pixels per grid cell (was 15 - shrunk so the digit row
                   # has real margin inside the circular watch face instead
                   # of nearly touching the clip boundary)
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

    colon_width = 2 * DIGIT_SCALE  # was hardcoded 30, exactly 2x the old scale
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


def generate_divider():
    # Small square dots down the column - Pong's classic center-court line -
    # instead of a solid bar.
    width, height = 6, ARENA_BAND_HEIGHT
    dash, gap = 4, 4
    period = dash + gap
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()
    for y in range(height):
        if y % period < dash:
            for x in range(width):
                pixels[x, y] = DIVIDER_COLOR
    img.save(os.path.join(DRAWABLE_DIR, "arena_divider.png"))


PADDLE_WIDTH = 10
PADDLE_HEIGHT = 40


def generate_paddles():
    left = Image.new("RGBA", (PADDLE_WIDTH, PADDLE_HEIGHT), PADDLE_COLOR)
    left.save(os.path.join(DRAWABLE_DIR, "arena_paddle_left.png"))

    right = Image.new("RGBA", (PADDLE_WIDTH, PADDLE_HEIGHT), PADDLE_COLOR)
    right.save(os.path.join(DRAWABLE_DIR, "arena_paddle_right.png"))


def generate_ball():
    size = 16
    img = Image.new("RGBA", (size, size), BALL_COLOR)
    img.save(os.path.join(DRAWABLE_DIR, "arena_ball.png"))


def main():
    os.makedirs(DRAWABLE_DIR, exist_ok=True)
    generate_digits()
    generate_scanline_background()
    generate_divider()
    generate_paddles()
    generate_ball()
    print("Generated pixel-art assets in", os.path.abspath(DRAWABLE_DIR))


if __name__ == "__main__":
    main()
