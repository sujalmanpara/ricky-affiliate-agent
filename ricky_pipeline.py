"""
RICKY PIPELINE — Production-Grade End-to-End Marketing Image Generator

Usage:
  python3 ricky_pipeline.py "https://www.amazon.in/dp/XXXXXXXXXX"
  python3 ricky_pipeline.py "https://www.amazon.in/dp/XXXXXXXXXX?tag=affiliate-21"

Full flow:
  1. Extract product data from Amazon URL (dual-method)
  2. Detect product category
  3. Generate category-specific scene prompts
  4. Smart-select best product image per scene
  5. Generate 15 AI marketing images (Nano Banana Pro)
  6. Apply professional PIL text overlays
  7. Save final images organized by platform
"""

import sys
import os
import json
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amazon_extractor import extract_product
from smart_image_selector import (
    select_images_for_scenes, ALL_SCENES,
    TWITTER_SCENES, INSTAGRAM_SCENES, PINTEREST_SCENES
)
from scene_engine import detect_category, get_scene_prompts, get_overlay_config

# ─── CONFIG ──────────────────────────────────────────────────
FAL_KEY = os.environ.get('FAL_KEY', '9b753dc2-d088-4360-ac80-ccc0b6f5477b:b9158d1cccc64e9ce2e45b103a99e9d9')
NANO_BANANA_URL = "https://fal.run/fal-ai/nano-banana-pro/edit"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


# ─── PIL OVERLAY ENGINE ─────────────────────────────────────

def add_gradient_bar(img, text, position='bottom', bar_height=80, opacity=180):
    """Semi-transparent bar with centered text."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    
    if position == 'bottom':
        y = h - bar_height
        draw.rectangle([(0, y), (w, h)], fill=(0, 0, 0, opacity))
    else:
        y = 0
        draw.rectangle([(0, 0), (w, bar_height)], fill=(0, 0, 0, opacity))
    
    try:
        font_size = min(32, max(18, w // 35))
        font = ImageFont.truetype(FONT_BOLD, font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # Truncate if text too wide
    while tw > w - 40 and len(text) > 10:
        text = text[:-4] + '...'
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
    
    if position == 'bottom':
        tx = (w - tw) // 2
        ty = y + (bar_height - th) // 2
    else:
        tx = (w - tw) // 2
        ty = (bar_height - th) // 2
    
    # Text shadow
    draw.text((tx + 1, ty + 1), text, fill=(0, 0, 0, 200), font=font)
    draw.text((tx, ty), text, fill=(255, 255, 255, 255), font=font)
    
    return Image.alpha_composite(img, overlay)


def add_price_badge(img, price, discount=''):
    """Price badge in top-right corner."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    
    badge_text = f"₹{price}"
    if discount:
        badge_text = f"{discount} ₹{price}"
    
    try:
        font_size = min(28, max(18, w // 40))
        font = ImageFont.truetype(FONT_BOLD, font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = font.getbbox(badge_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    padding = 12
    bw = tw + padding * 2
    bh = th + padding * 2
    bx = w - bw - 15
    by = 15
    
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=12, fill=(255, 50, 0, 220))
    draw.text((bx + padding, by + padding - 2), badge_text, fill=(255, 255, 255, 255), font=font)
    
    return Image.alpha_composite(img, overlay)


def add_ad_badge(img):
    """Small #ad FTC disclosure."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font = ImageFont.truetype(FONT_REG, 14)
    except:
        font = ImageFont.load_default()
    
    text = "#ad"
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x, y = 8, img.size[1] - th - 8
    draw.rectangle([(x - 3, y - 3), (x + tw + 3, y + th + 3)], fill=(0, 0, 0, 140))
    draw.text((x, y), text, fill=(200, 200, 200, 220), font=font)
    
    return Image.alpha_composite(img, overlay)


def apply_overlays(img: Image.Image, config: dict, price: str, discount: str) -> Image.Image:
    """Apply all configured overlays to an image."""
    img = img.convert('RGBA')
    
    if config.get('top'):
        img = add_gradient_bar(img, config['top'], position='top')
    
    if config.get('bottom'):
        img = add_gradient_bar(img, config['bottom'], position='bottom')
    
    if config.get('price'):
        img = add_price_badge(img, price, discount)
    
    img = add_ad_badge(img)
    
    return img


# ─── AI GENERATION ───────────────────────────────────────────

def generate_image(prompt: str, image_url: str, width: int, height: int) -> str:
    """Generate a single AI image. Returns URL or empty string on failure."""
    try:
        r = requests.post(
            NANO_BANANA_URL,
            headers={
                "Authorization": f"Key {FAL_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "image_urls": [image_url],
                "image_size": {"width": width, "height": height},
                "strength": 0.7,
                "num_images": 1,
                "enable_safety_checker": False
            },
            timeout=120
        )
        
        if r.status_code != 200:
            return ''
        
        data = r.json()
        if data.get('images') and len(data['images']) > 0:
            return data['images'][0].get('url', '')
        return ''
        
    except Exception:
        return ''


# ─── MAIN PIPELINE ───────────────────────────────────────────

def run_pipeline(url: str, output_dir: str = None) -> dict:
    """
    Run the complete Ricky pipeline for any Amazon product URL.
    
    Returns dict with results including file paths and statistics.
    """
    
    # ── Step 1: Extract ──
    print("="*70)
    print("🚀 RICKY PIPELINE — World-Class Marketing Images")
    print("="*70)
    
    print("\n📦 STEP 1: Extracting product data...")
    product = extract_product(url, verbose=True)
    
    if not product['success']:
        print(f"\n❌ EXTRACTION FAILED: {product['error']}")
        return {'success': False, 'error': product['error']}
    
    title = product['title']
    price = product['price']
    discount = product.get('discount', '')
    asin = product['asin']
    images = product['all_images']
    bullets = product.get('bullets', [])
    
    print(f"\n   ✅ {title[:60]}")
    print(f"   ₹{price} | {discount} | {product.get('rating', '?')}")
    print(f"   {len(images)} product images")
    
    # ── Step 2: Detect Category ──
    print(f"\n🏷️  STEP 2: Detecting product category...")
    category = detect_category(title, bullets)
    print(f"   Category: {category}")
    
    # ── Step 3: Generate Prompts ──
    print(f"\n🎨 STEP 3: Building {category}-specific scene prompts...")
    prompts = get_scene_prompts(category, title, bullets)
    overlay_configs = get_overlay_config(category, title, price, discount)
    print(f"   {len(prompts)} scene prompts generated")
    
    # ── Step 4: Select Images ──
    print(f"\n🎯 STEP 4: Smart-selecting images for each scene...")
    assignments = select_images_for_scenes(images, ALL_SCENES)
    unique_imgs = len(set(a['index'] for a in assignments.values()))
    print(f"   {unique_imgs} unique images across {len(ALL_SCENES)} scenes")
    
    # ── Step 5: Setup Output ──
    if output_dir is None:
        output_dir = os.path.expanduser(f"~/ricky-output/{asin}")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'twitter'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'instagram'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'pinterest'), exist_ok=True)
    
    # ── Step 6: Generate AI Images + Overlays ──
    print(f"\n🤖 STEP 5: Generating {len(ALL_SCENES)} AI marketing images...")
    print(f"   Model: Nano Banana Pro | Strength: 0.7")
    
    results = {}
    success_count = 0
    fail_count = 0
    
    for scene in ALL_SCENES:
        sid = scene['id']
        w, h = scene['size']
        platform = scene['platform']
        img_url = assignments[sid]['url']
        prompt = prompts[sid]
        
        print(f"\n   [{sid}] {w}×{h} | Img #{assignments[sid]['index']+1} | {platform}")
        
        # Generate
        gen_url = generate_image(prompt, img_url, w, h)
        
        if not gen_url:
            print(f"   ❌ Generation failed — retrying...")
            time.sleep(3)
            gen_url = generate_image(prompt, img_url, w, h)
        
        if not gen_url:
            print(f"   ❌ FAILED after retry")
            fail_count += 1
            continue
        
        print(f"   ✅ Generated")
        
        # Download + overlay
        try:
            img_r = requests.get(gen_url, timeout=30)
            img = Image.open(BytesIO(img_r.content)).convert('RGBA')
            
            # Apply overlays
            config = overlay_configs.get(sid, {})
            img = apply_overlays(img, config, price, discount)
            
            # Save to platform folder
            out_path = os.path.join(output_dir, platform, f"{sid}.png")
            img.convert('RGB').save(out_path, 'PNG')
            
            file_size = os.path.getsize(out_path) // 1024
            print(f"   💾 {out_path} ({file_size} KB)")
            
            results[sid] = {
                'url': gen_url,
                'file': out_path,
                'platform': platform,
                'size': f"{w}×{h}",
                'source_image': assignments[sid]['index'] + 1,
            }
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Overlay/save error: {str(e)[:60]}")
            fail_count += 1
        
        time.sleep(2)  # Rate limit
    
    # ── Summary ──
    print(f"\n{'='*70}")
    print(f"🎉 PIPELINE COMPLETE!")
    print(f"{'='*70}")
    print(f"   Product: {title[:50]}")
    print(f"   Category: {category}")
    print(f"   Price: ₹{price} ({discount})")
    print(f"   Generated: {success_count}/{len(ALL_SCENES)} scenes")
    print(f"   Failed: {fail_count}")
    print(f"   Output: {output_dir}/")
    
    tw_files = [r['file'] for r in results.values() if r['platform'] == 'twitter']
    ig_files = [r['file'] for r in results.values() if r['platform'] == 'instagram']
    pin_files = [r['file'] for r in results.values() if r['platform'] == 'pinterest']
    
    print(f"\n   🐦 Twitter:   {len(tw_files)}/4 images ({output_dir}/twitter/)")
    print(f"   📸 Instagram: {len(ig_files)}/8 images ({output_dir}/instagram/)")
    print(f"   📌 Pinterest: {len(pin_files)}/3 images ({output_dir}/pinterest/)")
    
    # Save metadata
    meta = {
        'product': {
            'title': title,
            'price': price,
            'discount': discount,
            'rating': product.get('rating', ''),
            'reviews': product.get('reviews', ''),
            'brand': product.get('brand', ''),
            'asin': asin,
            'url': url,
            'category': category,
            'total_images': len(images),
        },
        'generation': {
            'model': 'nano-banana-pro',
            'strength': 0.7,
            'total_scenes': len(ALL_SCENES),
            'success': success_count,
            'failed': fail_count,
        },
        'files': {sid: r for sid, r in results.items()},
    }
    
    meta_path = os.path.join(output_dir, 'pipeline_meta.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    print(f"\n   📄 Metadata: {meta_path}")
    print(f"{'='*70}")
    
    return {
        'success': True,
        'product': meta['product'],
        'generation': meta['generation'],
        'output_dir': output_dir,
        'twitter_files': tw_files,
        'instagram_files': ig_files,
        'pinterest_files': pin_files,
    }


# ─── POST TO SOCIAL MEDIA ────────────────────────────────────

def post_results(pipeline_result: dict, config: dict = None):
    """Post generated images to all configured platforms."""
    from caption_engine import generate_all_captions
    from postiz_poster import PostizPoster
    
    if config is None:
        try:
            from ricky_config import load_config
            config = load_config()
        except:
            print("❌ No config found. Run: python3 ricky_config.py setup")
            return
    
    postiz_key = config.get('postiz', {}).get('api_key', '')
    if not postiz_key:
        print("❌ No Postiz API key. Run: python3 ricky_config.py setup")
        return
    
    product = pipeline_result['product']
    product['affiliate_tag'] = config.get('amazon', {}).get('affiliate_tag', 'counitinguniq-21')
    category = product.get('category', 'generic')
    
    # Generate captions
    print(f"\n📝 Generating platform captions...")
    captions = generate_all_captions(product, category)
    
    # Initialize poster
    poster = PostizPoster(
        api_key=postiz_key,
        base_url=config.get('postiz', {}).get('base_url', 'https://api.postiz.com/public/v1')
    )
    
    integrations = config.get('postiz', {}).get('integrations', {})
    
    files = {
        'twitter': pipeline_result.get('twitter_files', []),
        'instagram': pipeline_result.get('instagram_files', []),
        'pinterest': pipeline_result.get('pinterest_files', []),
    }
    
    # Post to all platforms
    print(f"\n📡 Posting to social media...")
    results = poster.post_product_all_platforms(captions, files, integrations, product)
    
    print(f"\n{'='*50}")
    print(f"📡 POSTING RESULTS:")
    for platform, result in results.items():
        status = "✅" if result.get('success') else "❌"
        print(f"   {status} {platform}: {result.get('post_id', result.get('error', '?'))}")
    print(f"{'='*50}")
    
    return results


# ─── CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 ricky_pipeline.py <amazon_url>             # Generate images only")
        print("  python3 ricky_pipeline.py <amazon_url> --post      # Generate + post")
        print("  python3 ricky_pipeline.py <amazon_url> --post-only # Post existing output")
        sys.exit(1)
    
    url = sys.argv[1]
    should_post = '--post' in sys.argv
    post_only = '--post-only' in sys.argv
    
    if post_only:
        # Load existing results and post
        from amazon_extractor import extract_asin
        asin = extract_asin(url)
        output_dir = os.path.expanduser(f"~/ricky-output/{asin}")
        meta_path = os.path.join(output_dir, 'pipeline_meta.json')
        
        if not os.path.exists(meta_path):
            print(f"❌ No results found at {meta_path}. Run pipeline first.")
            sys.exit(1)
        
        with open(meta_path) as f:
            meta = json.load(f)
        
        result = {
            'success': True,
            'product': meta['product'],
            'twitter_files': [r['file'] for r in meta['files'].values() if r['platform'] == 'twitter'],
            'instagram_files': [r['file'] for r in meta['files'].values() if r['platform'] == 'instagram'],
            'pinterest_files': [r['file'] for r in meta['files'].values() if r['platform'] == 'pinterest'],
        }
        post_results(result)
    else:
        result = run_pipeline(url)
        
        if result['success'] and should_post:
            post_results(result)
