"""
TEXT OVERLAY ENGINE — Layer 2 of the Two-Layer System
Adds perfect typography to AI-generated visual scenes.

Usage:
    from text_overlay_engine import apply_text_overlay
    final_img = apply_text_overlay(ai_image_path_or_url, text_config)
"""

from PIL import Image, ImageDraw, ImageFont
import requests, io


# ─── FONTS ──────────────────────────────────────────────────

def _load_fonts():
    """Load fonts with fallback."""
    paths = {
        'bold': "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        'regular': "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    }
    fonts = {}
    for style, path in paths.items():
        try:
            fonts[f'{style}_72'] = ImageFont.truetype(path, 72)
            fonts[f'{style}_56'] = ImageFont.truetype(path, 56)
            fonts[f'{style}_44'] = ImageFont.truetype(path, 44)
            fonts[f'{style}_36'] = ImageFont.truetype(path, 36)
            fonts[f'{style}_28'] = ImageFont.truetype(path, 28)
            fonts[f'{style}_22'] = ImageFont.truetype(path, 22)
            fonts[f'{style}_18'] = ImageFont.truetype(path, 18)
        except:
            default = ImageFont.load_default()
            for size in [72, 56, 44, 36, 28, 22, 18]:
                fonts[f'{style}_{size}'] = default
    return fonts

FONTS = _load_fonts()


# ─── HELPERS ────────────────────────────────────────────────

def _gradient_bar(img, y_start, height, color=(0,0,0), max_alpha=200):
    """Add semi-transparent gradient bar for text background."""
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(height):
        progress = i / max(height, 1)
        # Smooth ease-in/ease-out alpha
        if progress < 0.25:
            alpha = int(max_alpha * (progress / 0.25))
        elif progress > 0.75:
            alpha = int(max_alpha * ((1.0 - progress) / 0.25))
        else:
            alpha = max_alpha
        draw.line([(0, y_start+i), (img.width, y_start+i)], fill=(*color, min(alpha, 255)))
    return Image.alpha_composite(img.convert('RGBA'), overlay)


def _text_shadow(draw, pos, text, font, fill=(255,255,255), shadow_color=(0,0,0), shadow_alpha=160, offset=2):
    """Draw text with drop shadow for readability."""
    x, y = pos
    # Shadow
    draw.text((x+offset, y+offset), text, fill=(*shadow_color, shadow_alpha) if len(shadow_color) == 3 else shadow_color, font=font)
    # Main text
    draw.text((x, y), text, fill=fill, font=font)


def _badge(draw, pos, text, font, bg_color=(255,107,53), text_color=(255,255,255), padding=10, radius=8):
    """Draw a rounded badge with text."""
    x, y = pos
    bbox = draw.textbbox((0,0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle(
        [(x, y), (x + w + padding*2, y + h + padding*2)],
        radius=radius, fill=bg_color
    )
    draw.text((x + padding, y + padding), text, fill=text_color, font=font)
    return w + padding * 2  # Return badge width


def _center_text(draw, y, text, font, img_width, fill=(255,255,255)):
    """Draw centered text."""
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (img_width - w) // 2
    _text_shadow(draw, (x, y), text, font, fill=fill)
    return x


def _load_image(source):
    """Load image from file path or URL."""
    if source.startswith('http'):
        data = requests.get(source, timeout=30).content
        img = Image.open(io.BytesIO(data))
    else:
        img = Image.open(source)
    return img.convert('RGBA')


# ─── TEXT OVERLAY FUNCTIONS (one per text_config type) ──────

def _overlay_tw_hero(img, tc):
    """Twitter hero: title top-left, price badge, rating."""
    img = _gradient_bar(img, 0, 140, (0,0,0), 210)
    img = _gradient_bar(img, img.height - 80, 80, (0,0,0), 180)
    draw = ImageDraw.Draw(img)
    
    title = tc.get('title', '')
    _text_shadow(draw, (30, 20), title, FONTS['bold_44'], fill=(255,255,255))
    
    # Price badge
    price = tc.get('price', '')
    if price:
        badge_x = 30
        badge_w = _badge(draw, (badge_x, 80), f"₹{price}", FONTS['bold_36'], bg_color=(255,107,53))
        # Discount badge next to price
        discount = tc.get('discount')
        if discount and discount != 'N/A':
            _badge(draw, (badge_x + badge_w + 15, 80), discount, FONTS['bold_28'], bg_color=(0,160,0))
    
    # Rating bottom-left
    rating = tc.get('rating')
    if rating and rating != 'N/A':
        draw.text((30, img.height - 55), f"⭐ {rating}", fill=(255,215,0), font=FONTS['bold_28'])
    
    return img


def _overlay_tw_features(img, tc):
    """Twitter features: subtle title bottom."""
    img = _gradient_bar(img, img.height - 80, 80, (0,0,0), 180)
    draw = ImageDraw.Draw(img)
    
    title = tc.get('title', '')
    draw.text((30, img.height - 55), title, fill=(200,200,200), font=FONTS['regular_28'])
    
    return img


def _overlay_ig_hook(img, tc):
    """Instagram hook: big bold headline + price badge."""
    img = _gradient_bar(img, 0, 200, (0,0,0), 220)
    img = _gradient_bar(img, img.height - 140, 140, (0,0,0), 210)
    draw = ImageDraw.Draw(img)
    
    title = tc.get('title', '')
    _text_shadow(draw, (40, 40), title, FONTS['bold_44'], fill=(255,255,255))
    
    # Price at bottom
    price = tc.get('price', '')
    if price:
        _badge(draw, (40, img.height - 120), f"₹{price}", FONTS['bold_44'], bg_color=(255,107,53))
    
    discount = tc.get('discount')
    if discount and discount != 'N/A':
        _badge(draw, (40, img.height - 55), discount, FONTS['bold_28'], bg_color=(0,160,0))
    
    return img


def _overlay_ig_lifestyle(img, tc):
    """Instagram lifestyle: subtle bottom caption."""
    img = _gradient_bar(img, img.height - 90, 90, (0,0,0), 180)
    draw = ImageDraw.Draw(img)
    
    draw.text((40, img.height - 70), tc.get('title', ''), fill=(255,255,255), font=FONTS['bold_28'])
    draw.text((40, img.height - 35), "#affiliate #ad", fill=(160,160,160), font=FONTS['regular_18'])
    
    return img


def _overlay_ig_flatlay(img, tc):
    """Instagram flat lay: clean top title."""
    img = _gradient_bar(img, 0, 90, (0,0,0), 170)
    draw = ImageDraw.Draw(img)
    
    _text_shadow(draw, (40, 25), tc.get('title', ''), FONTS['bold_36'], fill=(255,255,255))
    
    return img


def _overlay_ig_detail(img, tc):
    """Instagram detail: bottom feature text."""
    img = _gradient_bar(img, img.height - 100, 100, (0,0,0), 190)
    draw = ImageDraw.Draw(img)
    
    _text_shadow(draw, (40, img.height - 80), tc.get('title', ''), FONTS['bold_36'], fill=(255,255,255))
    
    return img


def _overlay_ig_proof(img, tc):
    """Instagram proof/transformation: top title."""
    img = _gradient_bar(img, 0, 100, (0,0,0), 190)
    draw = ImageDraw.Draw(img)
    
    _text_shadow(draw, (40, 30), tc.get('title', ''), FONTS['bold_36'], fill=(255,255,255))
    
    return img


def _overlay_ig_cta(img, tc):
    """Instagram CTA: big centered price + Link in Bio."""
    img = _gradient_bar(img, 0, 170, (0,0,0), 180)
    img = _gradient_bar(img, img.height - 120, 120, (0,0,0), 180)
    draw = ImageDraw.Draw(img)
    
    # Big centered price
    price = tc.get('price', '')
    if price:
        price_text = f"Just ₹{price}"
        _center_text(draw, 40, price_text, FONTS['bold_72'], img.width, fill=(255,215,0))
    
    # Discount under price
    discount = tc.get('discount')
    if discount and discount != 'N/A':
        _center_text(draw, 120, discount, FONTS['bold_36'], img.width, fill=(0,220,0))
    
    # CTA at bottom
    _center_text(draw, img.height - 85, "Link in Bio →", FONTS['bold_44'], img.width, fill=(255,255,255))
    
    return img


def _overlay_pin_guide(img, tc):
    """Pinterest guide: top title + bottom features + price badge."""
    img = _gradient_bar(img, 0, 150, (0,0,0), 220)
    img = _gradient_bar(img, img.height - 200, 200, (0,0,0), 220)
    draw = ImageDraw.Draw(img)
    
    # Title at top
    _text_shadow(draw, (30, 20), tc.get('title', ''), FONTS['bold_44'], fill=(255,255,255))
    
    # Price badge
    price = tc.get('price', '')
    if price:
        _badge(draw, (30, 80), f"₹{price}", FONTS['bold_36'], bg_color=(255,107,53))
    
    discount = tc.get('discount')
    if discount and discount != 'N/A':
        _badge(draw, (220, 80), discount, FONTS['bold_28'], bg_color=(0,160,0))
    
    # Rating at bottom
    rating = tc.get('rating')
    if rating and rating != 'N/A':
        draw.text((30, img.height - 55), f"⭐ {rating}", fill=(255,215,0), font=FONTS['bold_28'])
    
    return img


def _overlay_pin_editorial(img, tc):
    """Pinterest editorial: elegant top title + bottom price."""
    img = _gradient_bar(img, 0, 120, (0,0,0), 200)
    img = _gradient_bar(img, img.height - 150, 150, (0,0,0), 220)
    draw = ImageDraw.Draw(img)
    
    _text_shadow(draw, (30, 30), tc.get('title', ''), FONTS['bold_44'], fill=(255,255,255))
    
    # Price + rating at bottom
    price = tc.get('price', '')
    if price:
        _badge(draw, (30, img.height - 130), f"₹{price}", FONTS['bold_44'], bg_color=(255,107,53))
    
    rating = tc.get('rating')
    if rating and rating != 'N/A':
        draw.text((30, img.height - 55), f"⭐ {rating}", fill=(255,215,0), font=FONTS['bold_28'])
    
    return img


def _overlay_pin_aesthetic(img, tc):
    """Pinterest aesthetic: subtle bottom price + CTA."""
    img = _gradient_bar(img, img.height - 130, 130, (0,0,0), 210)
    draw = ImageDraw.Draw(img)
    
    price = tc.get('price', '')
    if price:
        _badge(draw, (30, img.height - 115), f"₹{price}", FONTS['bold_44'], bg_color=(255,107,53))
    
    draw.text((30, img.height - 40), "Tap to Shop →", fill=(255,255,255), font=FONTS['bold_28'])
    
    return img


# ─── DISPATCHER ─────────────────────────────────────────────

_OVERLAY_MAP = {
    'tw_hero': _overlay_tw_hero,
    'tw_features': _overlay_tw_features,
    'ig_hook': _overlay_ig_hook,
    'ig_lifestyle': _overlay_ig_lifestyle,
    'ig_flatlay': _overlay_ig_flatlay,
    'ig_detail': _overlay_ig_detail,
    'ig_proof': _overlay_ig_proof,
    'ig_cta': _overlay_ig_cta,
    'pin_guide': _overlay_pin_guide,
    'pin_editorial': _overlay_pin_editorial,
    'pin_aesthetic': _overlay_pin_aesthetic,
}


def apply_text_overlay(image_source, text_config, output_path=None):
    """
    Apply text overlay to an AI-generated image.
    
    Args:
        image_source: file path or URL to the AI-generated image
        text_config: dict with 'type' key and overlay-specific data
        output_path: optional path to save result (default: None, returns Image)
    
    Returns:
        PIL.Image in RGB mode (or saves to output_path and returns path)
    """
    img = _load_image(image_source)
    
    overlay_type = text_config.get('type', '')
    overlay_fn = _OVERLAY_MAP.get(overlay_type)
    
    if overlay_fn:
        img = overlay_fn(img, text_config)
    else:
        print(f"⚠️ Unknown overlay type: {overlay_type}")
    
    result = img.convert('RGB')
    
    if output_path:
        result.save(output_path, 'PNG', quality=95)
        return output_path
    
    return result
