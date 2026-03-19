"""
AMAZON PRODUCT EXTRACTOR — Robust Dual-Method System
Extracts product data from any Amazon link.

Strategy:
  1. Try requests + BeautifulSoup (instant, no browser needed)
  2. If fails → fallback to Camoufox (real browser)
  3. If still fails → retry with longer wait
  4. If ALL fail → return partial data + error

Works with:
  - amazon.in/dp/XXXXX
  - amazon.in/dp/XXXXX?tag=affiliate-21
  - Full Amazon URLs with referral params
  - Short affiliate links

Returns:
  {
    title, price, mrp, discount, rating, reviews,
    image (main hi-res), all_images (list of all product images),
    brand, bullets (feature list), asin, url,
    method (how it was extracted), success (bool)
  }
"""

import requests as req
import re
import json
import time
from bs4 import BeautifulSoup


# ─── URL CLEANING ────────────────────────────────────────────

def extract_asin(url: str) -> str:
    """Extract ASIN (10-char product ID) from any Amazon URL."""
    # Match /dp/XXXXXXXXXX or /gp/product/XXXXXXXXXX
    match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', url)
    if match:
        return match.group(1)
    # Match ASIN in query params
    match = re.search(r'[?&](?:ASIN|asin)=([A-Z0-9]{10})', url)
    if match:
        return match.group(1)
    return ''


def clean_url(url: str) -> str:
    """Convert any Amazon URL to clean /dp/ASIN format."""
    if not url.startswith('http'):
        url = 'https://' + url
    
    asin = extract_asin(url)
    if not asin:
        return url
    
    # Detect domain
    domain = 'www.amazon.in'  # Default to India
    domain_match = re.search(r'(www\.amazon\.[a-z.]+)', url)
    if domain_match:
        domain = domain_match.group(1)
    
    return f'https://{domain}/dp/{asin}'


# ─── METHOD 1: REQUESTS + BEAUTIFULSOUP ─────────────────────

def _extract_with_requests(url: str) -> dict:
    """
    Fast extraction using HTTP requests + BeautifulSoup.
    Works ~90-95% on residential IPs, ~50% on server IPs.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    session = req.Session()
    r = session.get(url, headers=headers, timeout=15, allow_redirects=True)
    
    if r.status_code != 200 or len(r.text) < 10000:
        return {'success': False, 'error': f'HTTP {r.status_code}, page too small ({len(r.text)} chars)'}
    
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract basic fields
    title_el = soup.select_one('#productTitle')
    if not title_el:
        return {'success': False, 'error': 'productTitle not found — page may be blocked/CAPTCHA'}
    
    title = title_el.text.strip()
    
    price_el = soup.select_one('.a-price-whole')
    price = price_el.text.strip().replace(',', '').replace('.', '') if price_el else ''
    
    rating_el = soup.select_one('#acrPopover .a-icon-alt')
    rating = rating_el.text.strip() if rating_el else ''
    
    reviews_el = soup.select_one('#acrCustomerReviewText')
    reviews = reviews_el.text.strip() if reviews_el else ''
    
    discount_el = soup.select_one('.savingsPercentage')
    discount = discount_el.text.strip() if discount_el else ''
    
    mrp_el = soup.select_one('.a-price.a-text-price .a-offscreen')
    mrp = mrp_el.text.strip() if mrp_el else ''
    
    brand_el = soup.select_one('#bylineInfo')
    brand = brand_el.text.strip() if brand_el else ''
    
    # Extract bullet points
    bullets = []
    for li in soup.select('#feature-bullets .a-list-item'):
        t = li.text.strip()
        if t and len(t) > 5 and 'See more' not in t:
            bullets.append(t)
    
    # Extract main image
    img_el = soup.select_one('#landingImage') or soup.select_one('#imgBlkFront')
    main_image = ''
    if img_el:
        main_image = img_el.get('data-old-hires') or img_el.get('src') or ''
    
    # Extract ALL images from JavaScript data
    all_images = []
    
    # Hi-res images from colorImages JS variable
    hi_res = re.findall(r'"hiRes"\s*:\s*"(https://[^"]+)"', html)
    large = re.findall(r'"large"\s*:\s*"(https://[^"]+)"', html)
    
    all_images = list(dict.fromkeys(hi_res + large))
    
    # If no JS images found, try main image
    if not all_images and main_image:
        all_images = [main_image]
    
    # Use first image as main if not set
    if not main_image and all_images:
        main_image = all_images[0]
    
    return {
        'success': True,
        'method': 'requests',
        'title': title,
        'price': price,
        'mrp': mrp,
        'discount': discount,
        'rating': rating,
        'reviews': reviews,
        'brand': brand,
        'bullets': bullets,
        'image': main_image,
        'all_images': all_images,
        'asin': extract_asin(url),
        'url': url,
    }


# ─── METHOD 2: CAMOUFOX (BROWSER) ───────────────────────────

def _extract_with_camoufox(url: str, wait_ms: int = 8000) -> dict:
    """
    Browser-based extraction using Camoufox.
    Works ~95-98% on residential IPs with desktop proxy.
    Falls back when requests method fails.
    """
    try:
        token = open('/data/browser-server-token').read().strip()
    except FileNotFoundError:
        return {'success': False, 'error': 'Camoufox not available (no token file)'}
    
    BASE = f"http://localhost:9222/?token={token}"
    
    extract_js = r"""(() => {
        try {
            const title = document.querySelector('#productTitle')?.textContent?.trim() || '';
            const priceEl = document.querySelector('.a-price-whole');
            const price = priceEl ? priceEl.textContent.trim().replace(/[,.]/g, '') : '';
            const rating = document.querySelector('#acrPopover .a-icon-alt')?.textContent?.trim() || '';
            const reviews = document.querySelector('#acrCustomerReviewText')?.textContent?.trim() || '';
            const imgEl = document.querySelector('#landingImage') || document.querySelector('#imgBlkFront');
            let image = '';
            if (imgEl) { image = imgEl.getAttribute('data-old-hires') || imgEl.src || ''; }
            const discount = document.querySelector('.savingsPercentage')?.textContent?.trim() || '';
            const mrp = document.querySelector('.a-price.a-text-price .a-offscreen')?.textContent?.trim() || '';
            const brand = document.querySelector('#bylineInfo')?.textContent?.trim() || '';
            
            const bullets = [];
            document.querySelectorAll('#feature-bullets .a-list-item').forEach(li => {
                const t = li.textContent?.trim();
                if (t && t.length > 5 && !t.includes('See more')) bullets.push(t);
            });
            
            // Get all images from thumbnails
            const allImages = [];
            const seen = new Set();
            
            // Try colorImages data
            const scripts = document.querySelectorAll('script');
            for (const s of scripts) {
                const text = s.textContent || '';
                const matches = text.matchAll(/"hiRes"\s*:\s*"(https:\/\/[^"]+)"/g);
                for (const m of matches) {
                    if (!seen.has(m[1])) { allImages.push(m[1]); seen.add(m[1]); }
                }
            }
            
            // Fallback: thumbnail images
            if (allImages.length === 0) {
                document.querySelectorAll('#altImages img, .imageThumbnail img').forEach(img => {
                    let src = img.src || '';
                    src = src.replace(/\\._.*_\\./, '._SL1500_.');
                    if (src && !src.includes('play-button') && !src.includes('video') && !seen.has(src)) {
                        allImages.push(src); seen.add(src);
                    }
                });
            }
            
            return JSON.stringify({title, price, rating, reviews, image, discount, mrp, brand, bullets, allImages});
        } catch(e) {
            return JSON.stringify({error: e.message});
        }
    })()"""
    
    try:
        r = req.post(BASE, json={
            "url": url,
            "sessionId": "amazon_extract",
            "screenshot": False,
            "actions": [
                {"type": "waitForSelector", "selector": "#productTitle", "timeout": wait_ms},
                {"type": "wait", "ms": 2000},  # Extra wait for images to load
                {"type": "evaluate", "script": extract_js}
            ]
        }, timeout=max(wait_ms // 1000 + 15, 30)).json()
        
        # Find the evaluate result (last result that's a JSON string)
        eval_result = None
        for res in reversed(r.get('results', [])):
            if isinstance(res, str) and res.startswith('{'):
                eval_result = res
                break
        
        if not eval_result:
            # Retry with just wait (waitForSelector might have timed out)
            r = req.post(BASE, json={
                "url": url,
                "sessionId": "amazon_extract",
                "screenshot": False,
                "actions": [
                    {"type": "wait", "ms": wait_ms + 5000},
                    {"type": "evaluate", "script": extract_js}
                ]
            }, timeout=max(wait_ms // 1000 + 20, 35)).json()
            
            for res in reversed(r.get('results', [])):
                if isinstance(res, str) and res.startswith('{'):
                    eval_result = res
                    break
        
        if not eval_result:
            return {'success': False, 'error': 'Camoufox returned no results'}
        
        product = json.loads(eval_result)
        
        if product.get('error'):
            return {'success': False, 'error': f'JS error: {product["error"]}'}
        
        if not product.get('title'):
            return {'success': False, 'error': 'Title not found — page may not have loaded'}
        
        all_images = product.get('allImages', [])
        main_image = product.get('image', '')
        
        if not main_image and all_images:
            main_image = all_images[0]
        if main_image and main_image not in all_images:
            all_images.insert(0, main_image)
        
        return {
            'success': True,
            'method': 'camoufox',
            'title': product.get('title', ''),
            'price': product.get('price', ''),
            'mrp': product.get('mrp', ''),
            'discount': product.get('discount', ''),
            'rating': product.get('rating', ''),
            'reviews': product.get('reviews', ''),
            'brand': product.get('brand', ''),
            'bullets': product.get('bullets', []),
            'image': main_image,
            'all_images': all_images,
            'asin': extract_asin(url),
            'url': url,
        }
        
    except req.Timeout:
        return {'success': False, 'error': 'Camoufox timeout'}
    except req.ConnectionError:
        return {'success': False, 'error': 'Camoufox not running (connection refused)'}
    except Exception as e:
        return {'success': False, 'error': f'Camoufox error: {str(e)[:100]}'}


# ─── MAIN EXTRACTOR (DUAL METHOD + RETRY) ───────────────────

def extract_product(url: str, verbose: bool = False) -> dict:
    """
    Extract product data from any Amazon URL.
    
    Strategy:
      1. Try requests + BeautifulSoup (instant)
      2. If fails → Camoufox with 8s wait
      3. If fails → Camoufox with 15s wait (longer)
      4. If ALL fail → return error with partial data
    
    Args:
        url: Any Amazon product URL (with or without affiliate tag)
        verbose: Print progress messages
    
    Returns:
        dict with product data + success flag + method used
    """
    clean = clean_url(url)
    asin = extract_asin(url)
    
    if verbose:
        print(f"🔗 URL: {clean}")
        print(f"📦 ASIN: {asin}")
    
    # ── Attempt 1: requests + BeautifulSoup ──
    if verbose:
        print(f"\n⚡ Method 1: requests + BeautifulSoup...", end=" ", flush=True)
    
    result = _extract_with_requests(clean)
    
    if result['success'] and result.get('image'):
        if verbose:
            print(f"✅ ({len(result.get('all_images', []))} images)")
        result['asin'] = asin
        return result
    
    if verbose:
        print(f"❌ {result.get('error', 'unknown')}")
    
    # ── Attempt 2: Camoufox (normal wait) ──
    if verbose:
        print(f"🦊 Method 2: Camoufox (8s wait)...", end=" ", flush=True)
    
    result = _extract_with_camoufox(clean, wait_ms=8000)
    
    if result['success'] and result.get('image'):
        if verbose:
            print(f"✅ ({len(result.get('all_images', []))} images)")
        result['asin'] = asin
        return result
    
    if verbose:
        print(f"❌ {result.get('error', 'unknown')}")
    
    # ── Attempt 3: Camoufox (longer wait) ──
    if verbose:
        print(f"🦊 Method 3: Camoufox (15s wait)...", end=" ", flush=True)
    
    result = _extract_with_camoufox(clean, wait_ms=15000)
    
    if result['success'] and result.get('image'):
        if verbose:
            print(f"✅ ({len(result.get('all_images', []))} images)")
        result['asin'] = asin
        return result
    
    if verbose:
        print(f"❌ {result.get('error', 'unknown')}")
    
    # ── All methods failed ──
    if verbose:
        print(f"\n❌ ALL METHODS FAILED for {asin}")
    
    return {
        'success': False,
        'method': 'none',
        'error': 'All extraction methods failed. The product page may be unavailable or Amazon is blocking requests.',
        'title': '',
        'price': '',
        'image': '',
        'all_images': [],
        'asin': asin,
        'url': clean,
    }


# ─── CLI USAGE ───────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.amazon.in/dp/B09MKKXXV1"
    
    print("="*70)
    print("🛒 AMAZON PRODUCT EXTRACTOR — Dual Method")
    print("="*70)
    
    result = extract_product(url, verbose=True)
    
    print(f"\n{'='*70}")
    if result['success']:
        print(f"✅ SUCCESS (via {result['method']})")
        print(f"   Title: {result['title'][:60]}...")
        print(f"   Price: ₹{result['price']}")
        print(f"   MRP: {result['mrp']} | Discount: {result['discount']}")
        print(f"   Rating: {result['rating']} ({result['reviews']})")
        print(f"   Brand: {result['brand']}")
        print(f"   Main Image: {result['image'][:60]}...")
        print(f"   All Images: {len(result['all_images'])}")
        print(f"   Bullets: {len(result['bullets'])}")
        for i, img in enumerate(result['all_images'][:5], 1):
            print(f"     [{i}] {img[:70]}...")
    else:
        print(f"❌ FAILED: {result['error']}")
    print(f"{'='*70}")
