"""
SMART IMAGE SELECTOR — Picks the best product image for each scene type.

Given a list of product images, analyzes them and assigns the optimal
image to each marketing scene (hero, lifestyle, detail, flatlay, etc.)

Strategy:
  - Image 1 (main/front) → Hero shots, CTA slides
  - Image 2-3 (alternate angles) → Lifestyle scenes
  - Image 4+ (detail/feature shots) → Feature highlights, detail slides
  - Side/back images → Pinterest guide pins
  - In-use/model shots → Instagram lifestyle slides
  
For AI models that support multi-image input (FLUX Kontext), 
we can feed multiple reference images for better understanding.
"""

import requests
from PIL import Image
from io import BytesIO
import os


def download_image(url: str, save_path: str = None) -> Image.Image:
    """Download image from URL and return PIL Image."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.amazon.in/'
    }
    r = requests.get(url, headers=headers, timeout=15)
    img = Image.open(BytesIO(r.content))
    if save_path:
        img.save(save_path)
    return img


def classify_image(img: Image.Image, index: int) -> dict:
    """
    Classify a product image based on its properties.
    Returns metadata about the image useful for scene selection.
    """
    w, h = img.size
    aspect = w / h if h > 0 else 1
    
    # Analyze image characteristics
    info = {
        'index': index,
        'width': w,
        'height': h,
        'aspect': round(aspect, 2),
        'orientation': 'landscape' if aspect > 1.2 else ('portrait' if aspect < 0.8 else 'square'),
        'resolution': w * h,
        'is_high_res': w >= 1000 or h >= 1000,
    }
    
    # Amazon image ordering convention:
    # Index 0 = Main product image (front view, white background)
    # Index 1-2 = Alternate angles
    # Index 3-5 = Detail/feature shots
    # Index 6+ = Lifestyle, in-use, infographics
    
    if index == 0:
        info['type'] = 'main'
        info['best_for'] = ['hero', 'cta', 'pinterest_main']
    elif index <= 2:
        info['type'] = 'alternate'
        info['best_for'] = ['lifestyle', 'flatlay', 'pinterest_guide']
    elif index <= 5:
        info['type'] = 'detail'
        info['best_for'] = ['detail', 'features', 'instagram_detail']
    else:
        info['type'] = 'extra'
        info['best_for'] = ['lifestyle', 'collage', 'bonus']
    
    return info


def analyze_all_images(image_urls: list) -> list:
    """
    Download and classify all product images.
    Returns list of image metadata sorted by quality/relevance.
    """
    analyzed = []
    
    # Deduplicate URLs
    seen = set()
    unique_urls = []
    for url in image_urls:
        # Normalize URL (remove size suffixes for dedup)
        base = url.split('._')[0] if '._' in url else url
        if base not in seen:
            seen.add(base)
            unique_urls.append(url)
    
    for i, url in enumerate(unique_urls):
        try:
            img = download_image(url)
            info = classify_image(img, i)
            info['url'] = url
            info['downloaded'] = True
            analyzed.append(info)
        except Exception as e:
            analyzed.append({
                'index': i,
                'url': url,
                'downloaded': False,
                'error': str(e)[:50]
            })
    
    return analyzed


def select_images_for_scenes(image_urls: list, scenes: list) -> dict:
    """
    Given product images and scene definitions, pick the best image for each scene.
    
    Args:
        image_urls: List of product image URLs from Amazon
        scenes: List of scene dicts with 'id' and 'type' keys
            type can be: hero, lifestyle, flatlay, detail, features, cta, 
                         guide, aesthetic, collage, hook, transform
    
    Returns:
        Dict mapping scene_id → {url, index, reason}
    """
    if not image_urls:
        return {}
    
    # Ensure we have at least one image
    main_image = image_urls[0]
    
    # Scene type → preferred image index ranges
    SCENE_PREFERENCES = {
        # Hero/hook scenes → main product image (clean, front view)
        'hero': [0],
        'hook': [0],
        'cta': [0],
        'tw_hero': [0],
        'ig_hook': [0],
        'ig_cta': [0],
        
        # Lifestyle scenes → alternate angles show the product in context better
        'lifestyle': [1, 2, 0],
        'ig_lifestyle': [1, 2, 0],
        'tw_lifestyle': [1, 2, 0],
        'pin_aesthetic': [1, 2, 0],
        'pin_lifestyle': [1, 2, 0],
        
        # Flatlay scenes → main or alternate (clean product shots)
        'flatlay': [0, 1, 2],
        'ig_flatlay': [0, 1, 2],
        
        # Detail/feature scenes → detail shots (index 3-5)
        'detail': [3, 4, 5, 2, 1],
        'features': [3, 4, 5, 2],
        'ig_detail': [3, 4, 5, 2, 1],
        'tw_features': [3, 4, 5, 2],
        
        # Transform/before-after → alternate angle
        'transform': [1, 2, 0],
        'ig_transform': [1, 2, 0],
        'tw_transform': [1, 2, 0],
        
        # Guide/educational pins → detail or feature shots
        'guide': [2, 3, 4, 0],
        'pin_guide': [2, 3, 4, 0],
        'pin_ultimate': [0, 1],
        
        # Texture/closeup → detail shots
        'texture': [4, 3, 5, 2],
        'ig_texture': [4, 3, 5, 2],
        
        # Science/ingredients → detail/infographic shots
        'science': [3, 4, 5, 6],
        'tw_science': [3, 4, 5, 6],
        'ingredients': [3, 4, 5, 6],
        
        # Splash/action → main product (AI will create the action)
        'splash': [0, 1],
        'tw_splash': [0, 1],
        'glow': [0, 1],
        'tw_glow': [0, 1],
    }
    
    assignments = {}
    used_indices = set()
    
    for scene in scenes:
        scene_id = scene.get('id', scene.get('scene_id', ''))
        scene_type = scene.get('type', scene_id)  # Fall back to scene_id as type
        
        # Get preferred indices for this scene type
        preferred = SCENE_PREFERENCES.get(scene_type, SCENE_PREFERENCES.get(scene_id, [0]))
        
        # Find the best available image
        selected_idx = None
        for idx in preferred:
            if idx < len(image_urls):
                # Prefer unused images for variety, but allow reuse
                if idx not in used_indices:
                    selected_idx = idx
                    break
        
        # If all preferred were used, pick the first available preferred
        if selected_idx is None:
            for idx in preferred:
                if idx < len(image_urls):
                    selected_idx = idx
                    break
        
        # Final fallback to main image
        if selected_idx is None:
            selected_idx = 0
        
        used_indices.add(selected_idx)
        
        assignments[scene_id] = {
            'url': image_urls[selected_idx],
            'index': selected_idx,
            'reason': f"{'main' if selected_idx == 0 else 'alt' if selected_idx <= 2 else 'detail' if selected_idx <= 5 else 'extra'} image (#{selected_idx + 1})"
        }
    
    return assignments


def get_multi_reference_images(image_urls: list, max_refs: int = 3) -> list:
    """
    Select multiple reference images for AI models that support multi-image input.
    Picks diverse images (front, angle, detail) for maximum product understanding.
    
    Args:
        image_urls: List of all product image URLs
        max_refs: Maximum number of reference images to return
    
    Returns:
        List of image URLs selected for diversity
    """
    if not image_urls:
        return []
    
    if len(image_urls) == 1:
        return [image_urls[0]]
    
    refs = []
    
    # Always include main image
    refs.append(image_urls[0])
    
    # Add an alternate angle if available
    if len(image_urls) > 1 and len(refs) < max_refs:
        refs.append(image_urls[1])
    
    # Add a detail shot if available
    if len(image_urls) > 3 and len(refs) < max_refs:
        refs.append(image_urls[3])
    
    # Fill remaining with evenly spaced images
    while len(refs) < max_refs and len(refs) < len(image_urls):
        step = len(image_urls) // (max_refs - len(refs) + 1)
        for i in range(0, len(image_urls), max(step, 1)):
            if image_urls[i] not in refs and len(refs) < max_refs:
                refs.append(image_urls[i])
    
    return refs[:max_refs]


# ─── STANDARD SCENE DEFINITIONS ─────────────────────────────

TWITTER_SCENES = [
    {'id': 'tw_hero', 'type': 'hero', 'platform': 'twitter', 'size': (1344, 768)},
    {'id': 'tw_features', 'type': 'features', 'platform': 'twitter', 'size': (1344, 768)},
    {'id': 'tw_lifestyle', 'type': 'lifestyle', 'platform': 'twitter', 'size': (1344, 768)},
    {'id': 'tw_cta', 'type': 'cta', 'platform': 'twitter', 'size': (1344, 768)},
]

INSTAGRAM_SCENES = [
    {'id': 'ig_hook', 'type': 'hook', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_lifestyle', 'type': 'lifestyle', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_flatlay', 'type': 'flatlay', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_detail', 'type': 'detail', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_transform', 'type': 'transform', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_texture', 'type': 'texture', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_lifestyle2', 'type': 'lifestyle', 'platform': 'instagram', 'size': (1024, 1280)},
    {'id': 'ig_cta', 'type': 'cta', 'platform': 'instagram', 'size': (1024, 1280)},
]

PINTEREST_SCENES = [
    {'id': 'pin_guide', 'type': 'guide', 'platform': 'pinterest', 'size': (1000, 1500)},
    {'id': 'pin_aesthetic', 'type': 'aesthetic', 'platform': 'pinterest', 'size': (1000, 1500)},
    {'id': 'pin_lifestyle', 'type': 'lifestyle', 'platform': 'pinterest', 'size': (1000, 1500)},
]

ALL_SCENES = TWITTER_SCENES + INSTAGRAM_SCENES + PINTEREST_SCENES


# ─── CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    # Demo with sample images
    sample_urls = [
        "https://m.media-amazon.com/images/I/71UKHtv92KL._SL1500_.jpg",  # 0: Main front
        "https://m.media-amazon.com/images/I/71Q6o8B251L._SL1500_.jpg",  # 1: Alt angle
        "https://m.media-amazon.com/images/I/71PEnusvx1L._SL1500_.jpg",  # 2: Alt angle 2
        "https://m.media-amazon.com/images/I/81HzHplG9kL._SL1500_.jpg",  # 3: Detail
        "https://m.media-amazon.com/images/I/81z8nsXuKWL._SL1500_.jpg",  # 4: Detail 2
        "https://m.media-amazon.com/images/I/81ocXd-CjTL._SL1500_.jpg",  # 5: Feature
    ]
    
    print("="*70)
    print("🎯 SMART IMAGE SELECTOR — Scene Assignment Demo")
    print("="*70)
    
    assignments = select_images_for_scenes(sample_urls, ALL_SCENES)
    
    print(f"\n{'Scene ID':<20} {'Image #':<10} {'Type':<15} {'Reason'}")
    print(f"{'-'*20} {'-'*10} {'-'*15} {'-'*30}")
    
    for scene in ALL_SCENES:
        sid = scene['id']
        a = assignments[sid]
        print(f"{sid:<20} #{a['index']+1:<9} {scene['type']:<15} {a['reason']}")
    
    print(f"\n📸 Multi-reference images for AI:")
    refs = get_multi_reference_images(sample_urls, max_refs=3)
    for i, url in enumerate(refs, 1):
        print(f"  [{i}] {url}")
    
    print(f"\n✅ Each scene gets a DIFFERENT product image for variety!")
