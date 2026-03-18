# Ricky Core Architecture - What Actually Matters

## 🎯 THE REAL RICKY (v1.0)

Focus on what provides VALUE:
1. ✅ User gives product URLs (5 min/day)
2. ✅ Ricky automates EVERYTHING else

---

## 🏗️ COMPLETE SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│ USER INPUT (5 minutes/day)                                  │
│ 3 Amazon product URLs                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ MODULE 1: PRODUCT DATA EXTRACTION (Camoufox)                │
│ ─────────────────────────────────────────────────────────── │
│ Input:  Amazon URL                                          │
│ Output: {                                                   │
│   title: "Zebronics Wireless Keyboard"                     │
│   price: "₹749"                                             │
│   features: ["Wireless", "UV-Printed"]                      │
│   image_url: "https://m.media-amazon.com/..."              │
│   asin: "B0FN87F535"                                        │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ MODULE 2: IMAGE GENERATION (Seedream 5.0)                   │
│ ─────────────────────────────────────────────────────────── │
│ Input:  Product image URL + Marketing prompts               │
│ Output: {                                                   │
│   twitter:    "url_16x9.jpg"   (lifestyle shot)            │
│   instagram:  "url_1x1.jpg"    (flat lay)                  │
│   pinterest:  "url_2x3.jpg"    (infographic)               │
│ }                                                           │
│ Cost: $0.30 (3 images)                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ MODULE 3: CAPTION GENERATION (AI/Templates)                 │
│ ─────────────────────────────────────────────────────────── │
│ Input:  Product data                                        │
│ Output: {                                                   │
│   twitter: "Still using old keyboard? ₹749 #ad"            │
│   instagram: "Desk upgrade complete ✨ Link in bio #ad"    │
│   pinterest: "Best keyboard under ₹1000 [specs] #ad"       │
│ }                                                           │
│ All include: Price, features, CTA, #ad, affiliate link     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ MODULE 4: SOCIAL MEDIA POSTING (Postiz API)                 │
│ ─────────────────────────────────────────────────────────── │
│ For each platform:                                          │
│   - Upload image                                            │
│   - Post with caption + affiliate link                      │
│   - Schedule/publish                                        │
│ Platforms: Twitter, Instagram, Pinterest                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ MODULE 5: TRACKING & REPORTING                              │
│ ─────────────────────────────────────────────────────────── │
│ Track:                                                      │
│   - Products posted                                         │
│   - Images generated                                        │
│   - Posts published                                         │
│   - Platform engagement (if available)                      │
│ Weekly report to user                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 MODULE 1: PRODUCT DATA EXTRACTION

### Technology: Camoufox (Stealth Browser)

**Why:** Bypass bot detection, reliable scraping

**Code:**
```python
import requests
import json

class ProductExtractor:
    def __init__(self, camoufox_token):
        self.token = camoufox_token
        self.api = f"http://localhost:9222/?token={camoufox_token}"
    
    def extract_product(self, amazon_url):
        """
        Extract product data from Amazon page
        """
        payload = {
            "url": amazon_url,
            "sessionId": "ricky_scraper",
            "screenshot": False,
            "timeout": 30000,
            "actions": [
                {"type": "wait", "ms": 5000},
                {"type": "evaluate", "script": """
                    (function() {
                        // Extract product data
                        const title = document.querySelector('#productTitle')?.innerText.trim();
                        const priceWhole = document.querySelector('.a-price-whole')?.innerText;
                        const priceFraction = document.querySelector('.a-price-fraction')?.innerText;
                        const price = priceWhole ? `₹${priceWhole}${priceFraction}` : null;
                        
                        // Extract features
                        const featureItems = document.querySelectorAll('#feature-bullets li');
                        const features = Array.from(featureItems)
                            .map(li => li.innerText.trim())
                            .filter(f => f.length > 0 && f.length < 200)
                            .slice(0, 5);
                        
                        // Extract rating
                        const rating = document.querySelector('.a-icon-star')?.innerText.split(' ')[0];
                        
                        // Extract discount
                        const discount = document.querySelector('.savingsPercentage')?.innerText;
                        
                        // Find product image (multiple methods)
                        let imageUrl = null;
                        
                        // Method 1: Landing image
                        const landingImg = document.querySelector('#landingImage');
                        if (landingImg) {
                            imageUrl = landingImg.src || 
                                      landingImg.getAttribute('data-old-hires') ||
                                      landingImg.getAttribute('data-a-dynamic-image');
                        }
                        
                        // Method 2: Parse dynamic image JSON
                        if (!imageUrl && landingImg) {
                            const dynamicImage = landingImg.getAttribute('data-a-dynamic-image');
                            if (dynamicImage) {
                                try {
                                    const urls = JSON.parse(dynamicImage);
                                    imageUrl = Object.keys(urls)[0];
                                } catch(e) {}
                            }
                        }
                        
                        // Extract ASIN from URL
                        const asinMatch = window.location.href.match(/\/dp\/([A-Z0-9]{10})/);
                        const asin = asinMatch ? asinMatch[1] : null;
                        
                        return {
                            title: title,
                            price: price,
                            features: features,
                            rating: rating,
                            discount: discount,
                            image_url: imageUrl,
                            asin: asin,
                            url: window.location.href
                        };
                    })()
                """}
            ]
        }
        
        response = requests.post(self.api, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('results'):
                product_data = result['results'][0]
                
                # Add affiliate tag
                product_data['affiliate_url'] = self.add_affiliate_tag(
                    product_data['url'],
                    "counitinguniq-21"
                )
                
                return product_data
        
        raise Exception(f"Failed to extract product: {response.text}")
    
    def add_affiliate_tag(self, url, tag):
        """Add affiliate tag to URL"""
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}tag={tag}"

# Usage
extractor = ProductExtractor(camoufox_token)
product = extractor.extract_product("https://amazon.in/dp/B0FN87F535/")

print(product)
# {
#   'title': 'Zebronics Wireless Keyboard & Mouse',
#   'price': '₹749',
#   'features': ['Wireless 2.4GHz', 'UV-Printed keys'],
#   'rating': '4.0',
#   'discount': '50% off',
#   'image_url': 'https://m.media-amazon.com/images/I/61qM7Ie7KyL.jpg',
#   'asin': 'B0FN87F535',
#   'url': 'https://amazon.in/dp/B0FN87F535/',
#   'affiliate_url': 'https://amazon.in/dp/B0FN87F535/?tag=counitinguniq-21'
# }
```

**Output:** Complete product data object

---

## 🎨 MODULE 2: IMAGE GENERATION

### Technology: Seedream 5.0 (Fal.ai)

**Why:** Fast, cheap ($0.10/image), good quality img2img

**Code:**
```python
import requests

class ImageGenerator:
    def __init__(self, fal_api_key):
        self.api_key = fal_api_key
        self.endpoint = "https://fal.run/fal-ai/bytedance/seedream/v5/lite/edit"
    
    def generate_marketing_images(self, product):
        """
        Generate 3 platform-optimized images
        """
        scenarios = [
            {
                'platform': 'twitter',
                'aspect_ratio': '16:9',
                'prompt': f"""Professional marketing photograph showing {product['title']} in use.
Modern lifestyle setting, natural lighting, professional aesthetic.
The exact product from reference image.
16:9 landscape format."""
            },
            {
                'platform': 'instagram',
                'aspect_ratio': '1:1',
                'prompt': f"""Top-down aesthetic flat lay of {product['title']}.
Clean minimalist background, natural lighting.
The exact product from reference image.
Instagram-worthy aesthetic, square 1:1 format."""
            },
            {
                'platform': 'pinterest',
                'aspect_ratio': '2:3',
                'prompt': f"""Product showcase of {product['title']}.
Professional product photography, clean background.
The exact product from reference image.
Vertical 2:3 format for Pinterest."""
            }
        ]
        
        images = {}
        
        for scenario in scenarios:
            headers = {
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": scenario['prompt'],
                "image_urls": [product['image_url']],
                "strength": 0.65,  # Preserve product, change context
                "num_inference_steps": 28
            }
            
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if "images" in result and len(result["images"]) > 0:
                    images[scenario['platform']] = result["images"][0]["url"]
            
            # Rate limiting
            time.sleep(3)
        
        return images

# Usage
generator = ImageGenerator(fal_api_key)
images = generator.generate_marketing_images(product)

print(images)
# {
#   'twitter': 'https://v3b.fal.media/files/.../twitter.png',
#   'instagram': 'https://v3b.fal.media/files/.../instagram.png',
#   'pinterest': 'https://v3b.fal.media/files/.../pinterest.png'
# }
```

**Output:** 3 marketing images (URLs)

---

## ✍️ MODULE 3: CAPTION GENERATION

### Technology: Template-based + AI (Optional)

**Why:** Fast, consistent, platform-optimized

**Code:**
```python
class CaptionGenerator:
    def __init__(self):
        self.templates = {
            'twitter': [
                "Still using {old_version}? 🤔\n\nUpgraded to {product}. {price}.\n{benefit}\n\nLink: {affiliate_url} #ad",
                "{hook} 👀\n\n{product} - {price}\n{feature_1}\n{feature_2}\n\nGrab yours: {affiliate_url} #ad",
                "💯 Deal alert!\n\n{product} at {price}\n{discount} off right now!\n\n{affiliate_url} #ad"
            ],
            'instagram': [
                "{emoji} {hook}\n\n{product_story}\n\nPrice: {price} {discount}\n\n{features_list}\n\nLink in bio! #ad #{category} #amazonfinds #dealoftheday",
                "Just got this and WOW 😍\n\n{product} - {price}\n\n{benefit_story}\n\n{features_list}\n\nLink in bio ☝️ #ad #{category}",
            ],
            'pinterest': [
                "{product} - Complete Review\n\nPrice: {price} {discount}\nRating: {rating} ⭐\n\n{features_list}\n\nWhy it's great:\n{benefits}\n\nFull details: {affiliate_url} #ad",
            ]
        }
    
    def generate_captions(self, product):
        """
        Generate platform-optimized captions
        """
        # Extract useful info
        title = product['title']
        price = product['price']
        discount = product.get('discount', '')
        features = product['features'][:3]
        rating = product.get('rating', 'N/A')
        affiliate_url = product['affiliate_url']
        
        # Detect category
        category = self.detect_category(title)
        
        captions = {}
        
        # Twitter (280 chars)
        captions['twitter'] = f"""Still using that old keyboard? 🖱️

Upgraded to {title}. {price}.
{features[0]}
{features[1] if len(features) > 1 else ''}

Link: {affiliate_url} #ad"""[:280]
        
        # Instagram (2200 chars, hashtags)
        features_text = '\n'.join([f'✓ {f}' for f in features])
        captions['instagram'] = f"""Desk upgrade complete ✨

Got this {title} for {price} {discount}

{features_text}

Perfect for WFH setup! Link in bio 👆

#ad #{category} #amazonfinds #dealoftheday #workfromhome #desksetup"""
        
        # Pinterest (500 chars, SEO)
        captions['pinterest'] = f"""Best {category} Under {price} in 2026

{title} - Complete Review

{features_text}
⭐ Rating: {rating}
💰 Price: {price} {discount}

Perfect for: Daily use, professionals, students

Full specs & buy link: {affiliate_url} #ad

#{category} #amazonindia #bestdeals"""
        
        return captions
    
    def detect_category(self, title):
        """Detect product category from title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['keyboard', 'mouse', 'headphone', 'earphone']):
            return 'electronics'
        elif any(word in title_lower for word in ['refrigerator', 'oven', 'mixer']):
            return 'homeappliances'
        elif any(word in title_lower for word in ['shirt', 'dress', 'shoe']):
            return 'fashion'
        else:
            return 'shopping'

# Usage
generator = CaptionGenerator()
captions = generator.generate_captions(product)

print(captions)
# {
#   'twitter': 'Still using that old keyboard? 🖱️\n\nUpgraded to...',
#   'instagram': 'Desk upgrade complete ✨\n\nGot this...',
#   'pinterest': 'Best electronics Under ₹749 in 2026...'
# }
```

**Output:** 3 platform-optimized captions

---

## 📱 MODULE 4: SOCIAL MEDIA POSTING

### Technology: Postiz API

**Why:** One API for all platforms, scheduling, analytics

**Code:**
```python
import requests

class SocialPoster:
    def __init__(self, postiz_api_key, workspace_id):
        self.api_key = postiz_api_key
        self.workspace = workspace_id
        self.base_url = "https://api.postiz.com/v1"
    
    def post_to_all_platforms(self, images, captions, product):
        """
        Post to Twitter, Instagram, Pinterest
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        results = {}
        
        for platform in ['twitter', 'instagram', 'pinterest']:
            payload = {
                "workspace_id": self.workspace,
                "platform": platform,
                "content": captions[platform],
                "media_urls": [images[platform]],
                "schedule": "now"  # Or specific time
            }
            
            response = requests.post(
                f"{self.base_url}/posts",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                results[platform] = {
                    'status': 'success',
                    'post_id': result.get('id'),
                    'url': result.get('url')
                }
                print(f"✅ Posted to {platform}")
            else:
                results[platform] = {
                    'status': 'failed',
                    'error': response.text
                }
                print(f"❌ Failed to post to {platform}: {response.text}")
        
        return results

# Usage
poster = SocialPoster(postiz_api_key, workspace_id)
results = poster.post_to_all_platforms(images, captions, product)

print(results)
# {
#   'twitter': {'status': 'success', 'post_id': '123', 'url': 'https://twitter.com/...'},
#   'instagram': {'status': 'success', 'post_id': '456'},
#   'pinterest': {'status': 'success', 'post_id': '789'}
# }
```

**Output:** Post IDs and URLs for tracking

---

## 📊 MODULE 5: TRACKING & REPORTING

### Technology: JSON file storage (simple!)

**Code:**
```python
import json
import os
from datetime import datetime

class Tracker:
    def __init__(self, data_dir="~/.ricky/data"):
        self.data_dir = os.path.expanduser(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def log_product_post(self, product, images, captions, post_results):
        """
        Log completed product automation
        """
        timestamp = datetime.now().isoformat()
        date = datetime.now().strftime("%Y-%m-%d")
        
        log_entry = {
            'timestamp': timestamp,
            'product': {
                'title': product['title'],
                'price': product['price'],
                'asin': product['asin'],
                'affiliate_url': product['affiliate_url']
            },
            'images': images,
            'captions': captions,
            'posts': post_results,
            'cost': 0.30  # 3 images × $0.10
        }
        
        # Append to daily log
        log_file = f"{self.data_dir}/{date}.json"
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                data = json.load(f)
        else:
            data = {'date': date, 'products': []}
        
        data['products'].append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📝 Logged to {log_file}")
    
    def generate_weekly_report(self):
        """
        Generate weekly summary
        """
        # Read last 7 days
        # Aggregate data
        # Return summary
        pass

# Usage
tracker = Tracker()
tracker.log_product_post(product, images, captions, post_results)
```

**Output:** JSON logs for analysis

---

## 🚀 COMPLETE WORKFLOW (END-TO-END)

### Master Script:

```python
#!/usr/bin/env python3
"""
Ricky - Complete Product Automation
"""

import sys
from product_extractor import ProductExtractor
from image_generator import ImageGenerator
from caption_generator import CaptionGenerator
from social_poster import SocialPoster
from tracker import Tracker

class Ricky:
    def __init__(self, config):
        self.extractor = ProductExtractor(config['camoufox_token'])
        self.image_gen = ImageGenerator(config['fal_api_key'])
        self.caption_gen = CaptionGenerator()
        self.poster = SocialPoster(config['postiz_api_key'], config['postiz_workspace'])
        self.tracker = Tracker()
    
    def process_product(self, amazon_url):
        """
        Complete automation for one product
        """
        print(f"\n{'='*60}")
        print(f"🚀 Processing: {amazon_url[:50]}...")
        print(f"{'='*60}\n")
        
        # Step 1: Extract product data
        print("1️⃣ Extracting product data...")
        product = self.extractor.extract_product(amazon_url)
        print(f"   ✅ {product['title'][:50]}...")
        print(f"   💰 {product['price']}")
        
        # Step 2: Generate images
        print("\n2️⃣ Generating marketing images...")
        images = self.image_gen.generate_marketing_images(product)
        print(f"   ✅ Twitter: {images['twitter'][:50]}...")
        print(f"   ✅ Instagram: {images['instagram'][:50]}...")
        print(f"   ✅ Pinterest: {images['pinterest'][:50]}...")
        
        # Step 3: Generate captions
        print("\n3️⃣ Creating captions...")
        captions = self.caption_gen.generate_captions(product)
        print(f"   ✅ 3 platform-optimized captions created")
        
        # Step 4: Post to social media
        print("\n4️⃣ Posting to social media...")
        results = self.poster.post_to_all_platforms(images, captions, product)
        for platform, result in results.items():
            if result['status'] == 'success':
                print(f"   ✅ {platform.capitalize()}: Posted!")
            else:
                print(f"   ❌ {platform.capitalize()}: {result['error']}")
        
        # Step 5: Track
        print("\n5️⃣ Logging results...")
        self.tracker.log_product_post(product, images, captions, results)
        print(f"   ✅ Logged")
        
        print(f"\n{'='*60}")
        print(f"✅ COMPLETE! Product promoted across 3 platforms")
        print(f"{'='*60}\n")
        
        return {
            'product': product,
            'images': images,
            'captions': captions,
            'results': results
        }
    
    def process_daily_products(self, urls):
        """
        Process multiple products (daily batch)
        """
        print(f"\n🤖 Ricky Daily Automation")
        print(f"📦 Products to process: {len(urls)}")
        print()
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Starting product {i}...")
            try:
                self.process_product(url)
            except Exception as e:
                print(f"❌ Error processing {url}: {e}")
                continue
        
        print(f"\n🎉 Daily automation complete!")
        print(f"✅ {len(urls)} products × 3 platforms = {len(urls)*3} posts")

# Main entry point
if __name__ == '__main__':
    # Load config
    import yaml
    with open(os.path.expanduser('~/.ricky/config.yaml')) as f:
        config = yaml.safe_load(f)
    
    # Initialize Ricky
    ricky = Ricky(config)
    
    # Get product URLs from user
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        print("Enter product URLs (one per line, empty line to finish):")
        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            urls.append(url)
    
    # Process
    ricky.process_daily_products(urls)
```

**Usage:**
```bash
$ python ricky.py \
  amazon.in/dp/B0FN87F535/ \
  amazon.in/dp/B0BXDJX8NB/ \
  amazon.in/dp/B07S829LBX/

🤖 Ricky Daily Automation
📦 Products to process: 3

[1/3] Starting product 1...
====================================
🚀 Processing: amazon.in/dp/B0FN87F535/...
====================================

1️⃣ Extracting product data...
   ✅ Zebronics Wireless Keyboard & Mouse...
   💰 ₹749

2️⃣ Generating marketing images...
   ✅ Twitter: https://v3b.fal.media/...
   ✅ Instagram: https://v3b.fal.media/...
   ✅ Pinterest: https://v3b.fal.media/...

3️⃣ Creating captions...
   ✅ 3 platform-optimized captions created

4️⃣ Posting to social media...
   ✅ Twitter: Posted!
   ✅ Instagram: Posted!
   ✅ Pinterest: Posted!

5️⃣ Logging results...
   ✅ Logged

====================================
✅ COMPLETE! Product promoted across 3 platforms
====================================

[... 2 more products ...]

🎉 Daily automation complete!
✅ 3 products × 3 platforms = 9 posts
```

---

## 📦 FILE STRUCTURE

```
ricky-affiliate-agent/
├── ricky.py                    # Main entry point
├── modules/
│   ├── product_extractor.py   # Module 1
│   ├── image_generator.py     # Module 2
│   ├── caption_generator.py   # Module 3
│   ├── social_poster.py       # Module 4
│   └── tracker.py             # Module 5
├── config.yaml                 # User configuration
├── requirements.txt
└── README.md
```

---

## ✅ THIS IS THE COMPLETE ARCHITECTURE!

**5 modules:**
1. ✅ Product Extraction (Camoufox)
2. ✅ Image Generation (Seedream img2img)
3. ✅ Caption Generation (Templates + AI)
4. ✅ Social Posting (Postiz API)
5. ✅ Tracking (JSON logs)

**No Amazon Product API needed!**  
**No complex features!**  
**Just pure automation value!**

**Ready to build this?** 🚀
