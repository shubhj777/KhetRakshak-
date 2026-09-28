"""Generates realistic sample crop leaf images for testing and judging demonstrations.
Includes:
- Maize leaf with Maydis Blight
- Paddy leaf with Bacterial Blight
- Healthy Maize leaf
- Blurry photo (to demonstrate quality rejection)
- Dark photo (to demonstrate low lighting rejection)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "sample_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_healthy_maize():
    img = Image.new("RGB", (600, 600), (34, 139, 34))
    draw = ImageDraw.Draw(img)
    # Background garden soil texture
    for y in range(600):
        shade = int(80 + 30 * math.sin(y / 40.0))
        draw.line([(0, y), (600, y)], fill=(30, shade, 25))

    # Leaf blade polygon
    leaf_poly = [
        (300, 30), (380, 150), (410, 320), (390, 480), (340, 580),
        (260, 580), (210, 480), (190, 320), (220, 150)
    ]
    draw.polygon(leaf_poly, fill=(46, 160, 67))
    
    # Midrib central vein
    draw.line([(300, 30), (300, 580)], fill=(120, 210, 130), width=6)
    
    # Parallel veins characteristic of monocot maize
    for offset in range(8, 100, 8):
        draw.line([(300 - offset, 40 + offset * 2), (300 - offset, 570)], fill=(70, 195, 90), width=2)
        draw.line([(300 + offset, 40 + offset * 2), (300 + offset, 570)], fill=(70, 195, 90), width=2)
    
    # Fine cross-striations for leaf cuticle texture
    for y in range(80, 550, 16):
        draw.line([(220, y), (380, y)], fill=(55, 175, 75), width=1)

    img.save(os.path.join(OUTPUT_DIR, "healthy_maize.jpg"), quality=95)

def generate_maize_maydis_blight():
    img = Image.new("RGB", (600, 600), (45, 120, 35))
    draw = ImageDraw.Draw(img)
    
    # Soil/canopy backdrop
    for y in range(600):
        draw.line([(0, y), (600, y)], fill=(35, int(90 + 20 * math.cos(y / 30.0)), 30))

    # Large maize leaf
    leaf_poly = [
        (300, 20), (390, 140), (420, 300), (400, 470), (350, 580),
        (250, 580), (200, 470), (180, 300), (210, 140)
    ]
    draw.polygon(leaf_poly, fill=(65, 145, 55))
    draw.line([(300, 20), (300, 580)], fill=(130, 195, 120), width=6)

    # Parallel veins
    for offset in range(15, 95, 12):
        draw.line([(300 - offset, 60 + offset * 2), (300 - offset, 560)], fill=(75, 160, 65), width=2)
        draw.line([(300 + offset, 60 + offset * 2), (300 + offset, 560)], fill=(75, 160, 65), width=2)

    # Maydis Leaf Blight lesions (Elongated rectangular straw/tan lesions with brown borders)
    lesions = [
        (240, 180, 30, 70), (320, 220, 26, 85), (260, 340, 32, 90),
        (335, 380, 28, 65), (230, 430, 35, 75), (310, 480, 25, 60)
    ]
    for (lx, ly, lw, lh) in lesions:
        # Outer dark brown necrotic ring
        draw.ellipse([lx - 4, ly - 4, lx + lw + 4, ly + lh + 4], fill=(95, 50, 20))
        # Inner tan / straw-colored water-soaked dead tissue
        draw.ellipse([lx, ly, lx + lw, ly + lh], fill=(195, 160, 90))
        # Central necrotic streak
        draw.line([(lx + lw//2, ly + 8), (lx + lw//2, ly + lh - 8)], fill=(120, 70, 30), width=2)

    img.save(os.path.join(OUTPUT_DIR, "maize_maydis_blight.jpg"), quality=92)

def generate_paddy_bacterial_blight():
    img = Image.new("RGB", (600, 600), (30, 80, 30))
    draw = ImageDraw.Draw(img)

    # Slender rice leaf blades
    draw.polygon([(280, 10), (340, 200), (350, 450), (330, 590), (270, 590), (250, 450), (260, 200)], fill=(50, 150, 60))
    draw.line([(300, 10), (300, 590)], fill=(90, 180, 100), width=3)

    # Wavy marginal blight lesions (leaves turning yellow-orange and dried at margin)
    for y in range(40, 520, 15):
        wave = int(12 * math.sin(y / 25.0))
        draw.ellipse([335 + wave, y, 360 + wave, y + 25], fill=(210, 175, 60))
        draw.ellipse([240 - wave, y + 10, 265 - wave, y + 35], fill=(195, 140, 40))

    img.save(os.path.join(OUTPUT_DIR, "paddy_bacterial_blight.jpg"), quality=92)

def generate_blurry_image():
    # Intentionally heavily blurred leaf to trigger BLURRY quality rejection
    img = Image.open(os.path.join(OUTPUT_DIR, "maize_maydis_blight.jpg"))
    img_blurred = img.filter(ImageFilter.GaussianBlur(radius=18))
    img_blurred.save(os.path.join(OUTPUT_DIR, "blurry_leaf_sample.jpg"), quality=85)

def generate_dark_image():
    # Intentionally underexposed dark photo to trigger TOO_DARK rejection
    img = Image.open(os.path.join(OUTPUT_DIR, "maize_maydis_blight.jpg"))
    arr = np.array(img, dtype=np.float32) * 0.12  # Very dark
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(os.path.join(OUTPUT_DIR, "dark_leaf_sample.jpg"), quality=85)

if __name__ == "__main__":
    generate_healthy_maize()
    generate_maize_maydis_blight()
    generate_paddy_bacterial_blight()
    generate_blurry_image()
    generate_dark_image()
    print("Sample images generated successfully.")
