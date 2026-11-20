"""
Script to create sample image assets for Annadata frontend.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

assets_dir = Path(r"C:\Users\aksha\.gemini\antigravity\scratch\annadata_app\frontend\assets")
assets_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate Logo (Annadata Logo - Golden Wheat + Green Sprout)
logo_img = Image.new('RGB', (120, 120), color=(26, 92, 42))
d = ImageDraw.Draw(logo_img)
# Draw circular badge
d.ellipse([10, 10, 110, 110], fill=(34, 139, 34), outline=(245, 197, 24), width=3)
# Draw plant symbol
d.polygon([(60, 25), (75, 55), (60, 50), (45, 55)], fill=(245, 197, 24))
d.polygon([(60, 45), (78, 75), (60, 70), (42, 75)], fill=(245, 220, 90))
d.rectangle([57, 65, 63, 100], fill=(240, 240, 240))
logo_img.save(assets_dir / "annadatalogo.jpg", quality=95)
logo_img.save(assets_dir / "annadatalogo.png")

# 2. Generate Homepage Hero Banner (homepageimg.jpg - Green Lush Farm with Sunrise)
hero_img = Image.new('RGB', (900, 360), color=(74, 150, 80))
d_hero = ImageDraw.Draw(hero_img)
# Sky gradient
for y in range(160):
    r = int(100 + (y / 160.0) * 120)
    g = int(180 + (y / 160.0) * 50)
    b = int(220 - (y / 160.0) * 80)
    d_hero.line([(0, y), (900, y)], fill=(r, g, b))

# Sun
d_hero.ellipse([650, 40, 750, 140], fill=(255, 215, 0), outline=(255, 235, 120), width=4)

# Green hills & fields
d_hero.polygon([(0, 140), (300, 110), (600, 150), (900, 120), (900, 360), (0, 360)], fill=(34, 112, 45))
d_hero.polygon([(0, 190), (400, 170), (750, 210), (900, 180), (900, 360), (0, 360)], fill=(46, 139, 87))

# Crops rows
for x in range(30, 880, 25):
    d_hero.line([(x, 260), (x - 20, 360)], fill=(30, 90, 35), width=4)
    d_hero.ellipse([x - 28, 245, x + 8, 275], fill=(220, 180, 40))

hero_img.save(assets_dir / "homepageimg.jpg", quality=95)

# 3. Generate Sample Leaf (leaf.jpg - Leaf with Rust pustules)
leaf_img = Image.new('RGB', (400, 400), color=(240, 245, 240))
d_leaf = ImageDraw.Draw(leaf_img)
# Draw green leaf blade
d_leaf.polygon([(200, 30), (330, 160), (280, 340), (200, 380), (120, 340), (70, 160)], fill=(76, 153, 0), outline=(50, 100, 0), width=3)
d_leaf.line([(200, 30), (200, 380)], fill=(120, 180, 50), width=4)

# Rust orange pustules / spots
import random
random.seed(42)
for _ in range(60):
    sx = random.randint(110, 290)
    sy = random.randint(70, 330)
    rad = random.randint(4, 12)
    d_leaf.ellipse([sx - rad, sy - rad, sx + rad, sy + rad], fill=(204, 85, 0), outline=(139, 58, 0))

leaf_img.save(assets_dir / "leaf.jpg", quality=95)

# 4. Generate help icon
help_img = Image.new('RGBA', (80, 80), color=(0, 0, 0, 0))
d_help = ImageDraw.Draw(help_img)
d_help.ellipse([5, 5, 75, 75], fill=(255, 152, 0))
d_help.ellipse([25, 25, 55, 55], fill=(255, 255, 255))
d_help.rectangle([36, 32, 44, 52], fill=(255, 152, 0))
help_img.save(assets_dir / "help.png")

print("Generated all assets successfully.")
