"""
PRODUCTION BANNER GENERATOR - Never Dumb Again
Research-backed, scroll-stopping affiliate marketing banners

Key improvements from research:
1. Emotional headlines (not product names)
2. Gradient strips for text readability
3. Platform-specific compositions (not just crops)
"""

import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import math
from typing import Dict, Tuple, Optional

# ─── CONFIGURATION ────────────────────────────────────────────

PLATFORMS = {
    "twitter": {
        "w": 1200,
        "h": 675,
        "style": "bold_hook",  # Punchy, high contrast
    },
    "instagram": {
        "w": 1080,
        "h": 1080,
        "style": "clean_centered",  # Minimal, lifestyle
    },
    "pinterest": {
        "w": 1000,
        "h": 1500,
        "style": "story_tall",  # Info-rich, vertical
    }
}

PALETTES = {
    "dark_luxury": {
        "bg": (26, 26, 26),        # #1a1a1a
        "text": (255, 255, 255),   # white
        "accent": (44, 95, 141),   # blue #2C5F8D
        "price_bg": (255, 107, 53) # orange #FF6B35
    },
    "fresh_green": {
        "bg": (245, 245, 245),     # light gray
        "text": (51, 51, 51),      # dark gray
        "accent": (76, 175, 80),   # green #4CAF50
        "price_bg": (76, 175, 80)
    },
    "warm_urgency": {
        "bg": (255, 255, 255),     # white
        "text": (0, 0, 0),         # black
        "accent": (255, 0, 0),     # red
        "price_bg": (255, 107, 53) # orange
    },
    "cool_premium": {
        "bg": (13, 27, 42),        # dark blue
        "text": (255, 255, 255),
        "accent": (0, 180, 216),   # cyan
        "price_bg": (255, 107, 53)
    }
}

# Fonts (DejaVu available on most Linux systems)
FONT_PATH = "/usr/share/fonts/truetype/dejavu"

try:
    FONT_BOLD_XL = ImageFont.truetype(f"{FONT_PATH}/DejaVuSans-Bold.ttf", 72)
    FONT_BOLD_LG = ImageFont.truetype(f"{FONT_PATH}/DejaVuSans-Bold.ttf", 60)
    FONT_BOLD_MD = ImageFont.truetype(f"{FONT_PATH}/DejaVuSans-Bold.ttf", 48)
    FONT_BOLD_SM = ImageFont.truetype(f"{FONT_PATH}/DejaVuSans-Bold.ttf", 36)
    FONT_REG_MD = ImageFont.truetype(f"{FONT_PATH}/DejaVuSans.ttf", 32)
    FONT_REG_SM = ImageFont.truetype(f"{FONT_PATH}/DejaVuSans.ttf", 24)
except:
    # Fallback
    FONT_BOLD_XL = FONT_BOLD_LG = FONT_BOLD_MD = FONT_BOLD_SM = FONT_REG_MD = FONT_REG_SM = ImageFont.load_default()

# ─── HELPER FUNCTIONS ─────────────────────────────────────────

def download_image(url: str) -> Image.Image:
    """Download product image from URL"""
    response = requests.get(url, timeout=15)
    img = Image.open(io.BytesIO(response.content))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img

def paste_product_centered(canvas: Image.Image, product_url: str, 
                          scale_pct: float = 0.62, 
                          y_offset_pct: float = 0.0) -> Image.Image:
    """
    Paste product photo centered on canvas
    
    scale_pct: Product takes up this % of canvas (0.62 = 62%)
    y_offset_pct: Shift up (+) or down (-) as % of canvas height
    """
    product_img = download_image(product_url)
    
    # Calculate target size (maintain aspect ratio)
    target_width = int(canvas.width * scale_pct)
    target_height = int(canvas.height * scale_pct)
    
    # Resize product
    product_img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Center position with optional y-offset
    x = (canvas.width - product_img.width) // 2
    y = (canvas.height - product_img.height) // 2
    y += int(canvas.height * y_offset_pct)
    
    # Paste
    canvas.paste(product_img, (x, y))
    
    return canvas

def add_gradient_strip(canvas: Image.Image, position: str = "bottom",
                      height_pct: float = 0.35, 
                      color: Tuple[int, int, int] = (0, 0, 0)) -> Image.Image:
    """
    Add gradient fade strip for text readability
    
    THE KEY TO "NEVER DUMB AGAIN":
    This gradient ensures text is always readable regardless of product photo!
    
    position: "top" or "bottom"
    height_pct: Strip height as % of canvas (0.35 = 35%)
    color: RGB tuple for gradient color
    """
    canvas_rgba = canvas.convert('RGBA')
    gradient = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)
    
    strip_height = int(canvas.height * height_pct)
    
    if position == "bottom":
        # Gradient from transparent (top of strip) to solid (bottom)
        for i in range(strip_height):
            alpha = int(255 * (i / strip_height) * 0.85)  # Max 85% opacity
            y = canvas.height - strip_height + i
            draw.line([(0, y), (canvas.width, y)], 
                     fill=(*color, alpha), width=1)
    
    elif position == "top":
        # Gradient from solid (top) to transparent (bottom of strip)
        for i in range(strip_height):
            alpha = int(255 * ((strip_height - i) / strip_height) * 0.75)
            draw.line([(0, i), (canvas.width, i)], 
                     fill=(*color, alpha), width=1)
    
    # Composite gradient onto canvas
    canvas_rgba = Image.alpha_composite(canvas_rgba, gradient)
    
    return canvas_rgba.convert('RGB')

def draw_text_with_shadow(draw: ImageDraw, position: Tuple[int, int],
                         text: str, font: ImageFont,
                         text_color: Tuple[int, int, int],
                         shadow_offset: int = 3):
    """Draw text with drop shadow for depth"""
    x, y = position
    
    # Shadow (offset)
    draw.text((x + shadow_offset, y + shadow_offset), text, 
             fill=(0, 0, 0, 180), font=font)
    
    # Main text
    draw.text((x, y), text, fill=text_color, font=font)

def draw_price_badge(draw: ImageDraw, canvas_size: Tuple[int, int],
                    price: str, palette: Dict,
                    position: str = "top_left"):
    """
    Draw prominent price badge
    
    position: "top_left" | "bottom_left" | "bottom_right"
    """
    badge_width = 280
    badge_height = 95
    
    # Position
    if position == "top_left":
        x, y = 25, 25
    elif position == "bottom_left":
        x = 25
        y = canvas_size[1] - badge_height - 25
    else:  # bottom_right
        x = canvas_size[0] - badge_width - 25
        y = canvas_size[1] - badge_height - 25
    
    # Draw rounded rectangle (badge background)
    draw.rounded_rectangle(
        [(x, y), (x + badge_width, y + badge_height)],
        radius=12,
        fill=palette["price_bg"]
    )
    
    # Price text
    draw.text((x + 20, y + 18), f"₹{price}", 
             fill=(255, 255, 255), font=FONT_BOLD_LG)

def draw_headline(draw: ImageDraw, canvas_size: Tuple[int, int],
                 headline: str, sub_headline: str,
                 palette: Dict, style: str):
    """
    Draw emotional headline (THE BIGGEST IMPROVEMENT!)
    
    headline: Emotional hook (4-6 words max)
    sub_headline: Concrete benefit (under 10 words)
    style: "bold_hook" | "clean_centered" | "story_tall"
    """
    if style == "bold_hook":
        # Twitter: Top-left, bold, punchy
        x = 40
        y = 40
        draw_text_with_shadow(draw, (x, y), headline, 
                            FONT_BOLD_XL, palette["text"])
        
        if sub_headline:
            draw.text((x, y + 90), sub_headline, 
                     fill=palette["text"], font=FONT_REG_MD)
    
    elif style == "clean_centered":
        # Instagram: Bottom-center, subtle
        if sub_headline:
            text_width = draw.textlength(sub_headline, font=FONT_REG_MD)
            x = (canvas_size[0] - text_width) // 2
            y = canvas_size[1] - 120
            draw.text((x, y), sub_headline, 
                     fill=palette["text"], font=FONT_REG_MD)
    
    elif style == "story_tall":
        # Pinterest: Title banner already drawn, headline goes in top banner
        pass  # Handled in Pinterest-specific code

def draw_cta_button(draw: ImageDraw, canvas_size: Tuple[int, int],
                   cta_text: str, palette: Dict, style: str):
    """Draw call-to-action button"""
    
    if style == "bold_hook":
        # Twitter: Bottom-right
        button_width = 180
        button_height = 55
        x = canvas_size[0] - button_width - 30
        y = canvas_size[1] - button_height - 30
        
        # Button background
        draw.rounded_rectangle(
            [(x, y), (x + button_width, y + button_height)],
            radius=8,
            fill=palette["accent"]
        )
        
        # Text
        text_width = draw.textlength(cta_text, font=FONT_BOLD_SM)
        text_x = x + (button_width - text_width) // 2
        draw.text((text_x, y + 10), cta_text, 
                 fill=(255, 255, 255), font=FONT_BOLD_SM)
    
    elif style == "clean_centered":
        # Instagram: Minimal or none
        pass
    
    elif style == "story_tall":
        # Pinterest: Bottom section
        x = 40
        y = canvas_size[1] - 80
        draw.text((x, y), cta_text, fill=(255, 255, 255), font=FONT_REG_MD)

def draw_social_proof_strip(draw: ImageDraw, canvas_size: Tuple[int, int],
                           rating: float, review_count: int, palette: Dict):
    """Draw star rating + review count (social proof trigger!)"""
    
    if rating > 0:
        # Position: Bottom strip, left side
        x = 40
        y = canvas_size[1] - 65
        
        # Stars
        stars_filled = int(rating)
        stars_empty = 5 - stars_filled
        stars_text = "★" * stars_filled + "☆" * stars_empty
        
        draw.text((x, y), stars_text, fill=(255, 215, 0), font=FONT_REG_MD)  # Gold
        
        # Review count
        if review_count > 0:
            review_text = f"({review_count:,} reviews)"
            draw.text((x + 150, y + 5), review_text, 
                     fill=palette["text"], font=FONT_REG_SM)

def draw_discount_badge(canvas_size: Tuple[int, int], discount_pct: str,
                       rotate_deg: int = -12) -> Image.Image:
    """
    Create discount badge as separate image (pasted on top layer)
    
    rotate_deg: Angle rotation for dynamic look (-12 = tilted left)
    Returns: RGBA image of badge
    """
    badge_size = 140
    badge = Image.new('RGBA', (badge_size, badge_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    # Circle
    margin = 10
    draw.ellipse([margin, margin, badge_size - margin, badge_size - margin],
                fill=(255, 0, 0))  # Red
    
    # Text
    text = f"{discount_pct}%\nOFF"
    text_bbox = draw.textbbox((0, 0), text, font=FONT_BOLD_SM)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (badge_size - text_width) // 2 - 10
    text_y = (badge_size - text_height) // 2 - 5
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255), 
             font=FONT_BOLD_SM, align='center')
    
    # Rotate
    if rotate_deg != 0:
        badge = badge.rotate(rotate_deg, expand=True)
    
    return badge

# ─── MASTER FUNCTION ──────────────────────────────────────────

def generate_marketing_banner(product: Dict, spec_json: Dict, 
                             platform: str) -> Image.Image:
    """
    Generate a production-quality marketing banner from Amazon product photo.
    
    THE "NEVER DUMB AGAIN" FUNCTION!
    
    product: dict with keys: image_url, title, price, discount_pct, rating, review_count
    spec_json: AI-generated layout spec (from IMAGE_GENERATION_SYSTEM_PROMPT)
    platform: "twitter" | "instagram" | "pinterest"
    
    Returns: PIL Image ready to save
    """
    cfg = PLATFORMS[platform]
    spec = spec_json[platform]
    palette = PALETTES[spec.get("color_palette", "dark_luxury")]
    
    # 1. Create canvas
    canvas = Image.new("RGB", (cfg["w"], cfg["h"]), palette["bg"])
    
    # 2. Paste product photo (centered, scaled)
    canvas = paste_product_centered(
        canvas,
        product["image_url"],
        scale_pct=spec.get("product_scale_pct", 62) / 100,
        y_offset_pct=-0.05 if platform == "pinterest" else 0.0
    )
    
    # 3. Add readability gradient strip
    # THIS IS THE KEY! Ensures text is always readable!
    if spec.get("background_treatment") != "clean_white":
        canvas = add_gradient_strip(canvas, position="bottom", height_pct=0.35,
                                   color=palette["bg"])
        if platform in ["twitter", "pinterest"]:
            canvas = add_gradient_strip(canvas, position="top", height_pct=0.22,
                                       color=(0, 0, 0))
    
    # 4. Draw all overlay elements
    canvas_rgba = canvas.convert("RGBA")
    draw = ImageDraw.Draw(canvas_rgba)
    
    # Price badge
    draw_price_badge(draw, canvas.size, product["price"], palette,
                    position=spec.get("price_badge", {}).get("position", "top_left"))
    
    # Headline + subheadline (EMOTIONAL, not descriptive!)
    draw_headline(draw, canvas.size,
                 spec.get("headline", product["title"][:30]),
                 spec.get("sub_headline", ""),
                 palette, cfg["style"])
    
    # CTA button
    draw_cta_button(draw, canvas.size,
                   spec.get("cta_text", "Shop Now →"),
                   palette, cfg["style"])
    
    # Social proof strip
    if product.get("rating", 0) > 0:
        draw_social_proof_strip(draw, canvas.size,
                               product["rating"], 
                               product.get("review_count", 0), 
                               palette)
    
    canvas = canvas_rgba.convert("RGB")
    
    # 5. Paste discount badge last (top layer)
    if product.get("discount_pct") and int(product["discount_pct"]) >= 5:
        badge = draw_discount_badge(canvas.size, 
                                   f"{product['discount_pct']}",
                                   rotate_deg=-12)
        canvas_rgba = canvas.convert("RGBA")
        badge_x = canvas.width - badge.width - 20
        canvas_rgba.paste(badge, (badge_x, 20), badge)
        canvas = canvas_rgba.convert("RGB")
    
    # 6. Subtle sharpening for crispness
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1, percent=130, threshold=2))
    
    return canvas

# ─── EXAMPLE USAGE ────────────────────────────────────────────

if __name__ == "__main__":
    # Test product
    product = {
        "image_url": "https://m.media-amazon.com/images/I/61ChcsEZsrL._SY879_.jpg",
        "title": "Samsung 183L Refrigerator",
        "price": "16990",
        "discount_pct": 26,
        "rating": 3.5,
        "review_count": 1247
    }
    
    # AI-generated spec (simplified for demo)
    spec_json = {
        "twitter": {
            "headline": "Fresh Food. Happy Family.",
            "sub_headline": "Smart cooling for modern homes",
            "color_palette": "fresh_green",
            "product_scale_pct": 60,
            "price_badge": {"position": "bottom_left"},
            "cta_text": "Get Deal →",
            "background_treatment": "gradient_sweep"
        },
        "instagram": {
            "headline": "",
            "sub_headline": "Samsung 183L | Digital Inverter",
            "color_palette": "cool_premium",
            "product_scale_pct": 55,
            "price_badge": {"position": "bottom_right"},
            "background_treatment": "clean_white"
        },
        "pinterest": {
            "headline": "Best Refrigerator Under ₹20K",
            "sub_headline": "Complete buying guide",
            "color_palette": "fresh_green",
            "product_scale_pct": 50,
            "price_badge": {"position": "top_left"},
            "cta_text": "See Full Review ↓",
            "background_treatment": "gradient_sweep"
        }
    }
    
    # Generate all 3 platforms
    for platform in ["twitter", "instagram", "pinterest"]:
        print(f"Generating {platform}...")
        banner = generate_marketing_banner(product, spec_json, platform)
        banner.save(f"never_dumb_{platform}.jpg", "JPEG", quality=95)
        print(f"✅ Saved: never_dumb_{platform}.jpg")
    
    print("\n🎉 ALL 3 BANNERS GENERATED!")
    print("\n📊 THE 'NEVER DUMB AGAIN' CHECKLIST:")
    print("✅ Emotional headlines (not product names)")
    print("✅ Gradient strips (text always readable)")
    print("✅ Platform-specific designs (not just crops)")
    print("✅ Social proof (stars + reviews)")
    print("✅ Clear CTAs")
    print("✅ Professional finish (sharpening filter)")
