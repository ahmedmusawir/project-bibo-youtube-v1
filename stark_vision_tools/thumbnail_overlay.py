from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json

# === Settings ===
FONT_PATH = Path("stark_vision_tools/fonts/Montserrat-SemiBold.ttf")
FONT_SIZE = 88
# FONT_SIZE = 72

# Layout mode can be: "stacked" or "split"
#  - "stacked": line1 directly above line2
#  - "split": line1 at top, line2 at bottom
LAYOUT_MODE = "split"

LINE_SPACING = 20
PADDING = 90
# PADDING = 40

# === Paths ===
THUMBNAIL_PATH = Path("stark_vision_tools/output/thumbnail.jpg")
FINAL_THUMBNAIL_PATH = Path("stark_vision_tools/output/thumbnail_final.png")
TITLE_PATH = Path("stark_vision_tools/output/titles.json")

# === Load Base Image ===
base = Image.open(THUMBNAIL_PATH).convert("RGBA")
width, height = base.size

# === Load Title ===
title_text = ""
if TITLE_PATH.exists():
    with open(TITLE_PATH, "r", encoding="utf-8") as f:
        titles = json.load(f)
        if titles:
            title_text = titles[0].upper()

# === Font Setup ===
from PIL import ImageFont
try:
    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
except:
    font = ImageFont.load_default()

# === Split into two lines if too long ===
words = title_text.split()
midpoint = len(words) // 2
line1 = " ".join(words[:midpoint])
line2 = " ".join(words[midpoint:])
lines = [line1, line2]

# === Create Overlay ===
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# === For each line, measure text size ===
text_sizes = [draw.textbbox((0, 0), line, font=font) for line in lines]
text_widths = [box[2] - box[0] for box in text_sizes]
text_heights = [box[3] - box[1] for box in text_sizes]

if LAYOUT_MODE == "stacked":
    # Same old approach: line1 above line2
    block_height = sum(text_heights) + LINE_SPACING

    # Place both lines near bottom, top, or middle if you want to change
    start_y = height - block_height - PADDING

    for i, line in enumerate(lines):
        text_width = text_widths[i]
        text_height = text_heights[i]
        x = (width - text_width) // 2
        y = start_y + i * (text_height + LINE_SPACING)

        # Background box
        draw.rectangle(
            [(x - PADDING, y - PADDING // 2),
             (x + text_width + PADDING, y + text_height + PADDING // 2)],
            fill=(0, 0, 0, 180)
        )
        # Text
        draw.text(
            (x, y),
            line,
            font=font,
            fill=(255, 255, 255, 255)
        )

elif LAYOUT_MODE == "split":
    # Draw line1 at top, line2 at bottom
    # 1) Calculate positions for each line independently

    # -- TOP LINE (line1) --
    text_width_top = text_widths[0]
    text_height_top = text_heights[0]
    x_top = (width - text_width_top) // 2
    y_top = PADDING  # some top padding

    # Draw background box
    draw.rectangle(
        [(x_top - PADDING, y_top - PADDING // 2),
         (x_top + text_width_top + PADDING, y_top + text_height_top + PADDING // 2)],
        fill=(0, 0, 0, 180)
    )
    draw.text(
        (x_top, y_top),
        line1,
        font=font,
        fill=(255, 255, 255, 255)
    )

    # -- BOTTOM LINE (line2) --
    text_width_bottom = text_widths[1]
    text_height_bottom = text_heights[1]
    x_bottom = (width - text_width_bottom) // 2
    y_bottom = height - text_height_bottom - PADDING  # near bottom

    # Background
    draw.rectangle(
        [(x_bottom - PADDING, y_bottom - PADDING // 2),
         (x_bottom + text_width_bottom + PADDING, y_bottom + text_height_bottom + PADDING // 2)],
        fill=(0, 0, 0, 180)
    )
    # Text
    draw.text(
        (x_bottom, y_bottom),
        line2,
        font=font,
        fill=(255, 255, 255, 255)
    )

# === Merge and Save ===
final_img = Image.alpha_composite(base, overlay)
final_img.convert("RGB").save(FINAL_THUMBNAIL_PATH)

print("✅ thumbnail_overlay.py complete. Final image saved as thumbnail_final.png")
