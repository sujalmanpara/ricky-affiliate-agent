# Ricky — Amazon Affiliate Marketing Agent

## Overview
Ricky automates affiliate marketing: paste an Amazon link → get 15 AI-generated marketing images + captions → auto-post to Instagram, Twitter/X, Pinterest.

## Prerequisites
- **Fal.ai API key** — for AI image generation (https://fal.ai/dashboard/keys)
- **Amazon Associates account** — for affiliate tag
- **Postiz account** (optional) — for auto-posting to social media (https://postiz.com)

## First-Time Setup
```bash
cd ~/ricky-affiliate-agent
python3 ricky_config.py setup
```
This creates `~/.ricky/config.yaml` (chmod 600) with your credentials.

## Quick Start
```bash
# Generate images only
python3 ricky_pipeline.py "https://www.amazon.in/dp/XXXXXXXXXX"

# Generate + post to all platforms
python3 ricky_pipeline.py "https://www.amazon.in/dp/XXXXXXXXXX" --post
```

## What Ricky Does

### 1. Extract Product Data
Paste any Amazon URL → Ricky extracts:
- Title, price, discount, rating, reviews
- ALL product images (20-50 high-res images)
- Brand, features, bullet points
- ASIN for affiliate link generation

Dual-method: requests + BeautifulSoup (instant) → Camoufox fallback (browser).

### 2. Detect Product Category
Auto-detects from 8 categories:
- Electronics (camera, phone, earbuds, laptop, watch, speaker, gaming)
- Beauty & Skincare
- Fashion (clothing, shoes, accessories)
- Home & Kitchen (appliances, cookware)
- Fitness & Supplements
- Motorcycle (helmets, gear)
- Generic fallback

### 3. Generate 15 AI Marketing Images
Category-specific creative prompts for 3 platforms:

**Twitter/X (4 images, 1344×768, 16:9)**
- Hero shot, features flat lay, lifestyle, CTA

**Instagram (8 images, 1024×1280, 4:5 portrait)**
- Hook, lifestyle, flat lay, detail, transform, texture, lifestyle 2, CTA

**Pinterest (3 images, 1000×1500, 2:3 tall)**
- Buyer's guide, aesthetic, lifestyle

Each scene uses a DIFFERENT product image (smart selection).

### 4. Apply Professional Overlays
PIL text overlays on every image:
- Price badge (top-right, red)
- Text bars (top/bottom, semi-transparent)
- CTA text (platform-specific)
- #ad FTC disclosure badge

### 5. Generate Captions
Platform-optimized captions:
- Twitter: Short, punchy, 280 chars, 3-5 hashtags
- Instagram: Storytelling, emoji, 20-30 hashtags (3-tier strategy)
- Pinterest: SEO-optimized title + description

### 6. Auto-Post via Postiz
Upload images + create posts on all platforms simultaneously:
- Twitter: 4-image grid post
- Instagram: Carousel post (up to 10 slides)
- Pinterest: Pin with title, description, affiliate link

## File Structure
```
ricky-affiliate-agent/
├── ricky_pipeline.py       # Main pipeline — one command does everything
├── amazon_extractor.py     # Dual-method product extraction
├── smart_image_selector.py # Best image per scene
├── scene_engine.py         # Category-specific prompts (8 categories)
├── caption_engine.py       # Platform-specific captions & hashtags
├── postiz_poster.py        # Social media posting via Postiz API
├── ricky_config.py         # Config management + setup wizard
├── SKILL.md                # This file
└── README.md               # Setup guide
```

## Agent Commands

**User says:** "Post this product" + Amazon link
```
→ Extract → Detect Category → Generate 15 Images → Captions → Post
```

**User says:** "Generate images for [link]"
```
→ Extract → Generate Images → Save (no posting)
```

**User says:** "Setup Ricky" / "Configure Ricky"
```
→ Run interactive setup wizard
```

## Models Used
- **Nano Banana Pro** (primary) — Creative lifestyle scenes, 0 failures in testing
- **Seedream 5.0 Lite** (backup) — More reliable, slightly less creative
- **Strength: 0.7** — Preserves product identity while creating creative scenes

## Cost Per Product
- ~15 AI generations × ~$0.10 = **~$1.50 per product**
- Postiz: Free tier or paid plan
- Total: **$1.50-2.00 per product for 15 images + 3 platform posts**

## Compliance
- ✅ #ad FTC disclosure on every image
- ✅ "Affiliate link" text in captions
- ✅ Amazon Associates TOS compliant
- ✅ No clicking own affiliate links

## Tested Products
- ✅ Sony ZV-1F Camera (electronics) — 15/15
- ✅ Fire-Boltt Earbuds (earbuds) — 15/15
- ✅ ZEE-C Face Wash (beauty) — 12/12
- ✅ Samsung Refrigerator (appliance) — 9/9
- ✅ Steelbird Helmet (helmet) — extraction confirmed
