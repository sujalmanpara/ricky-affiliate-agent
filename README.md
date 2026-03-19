# 🚀 Ricky — AI Affiliate Marketing Agent

**Paste an Amazon link → Get 15 AI marketing images → Auto-post to Instagram, Twitter, Pinterest.**

Ricky turns any Amazon product into a complete social media marketing campaign in under 5 minutes.

## ✨ Features

- **🛒 Smart Extraction** — Paste any Amazon URL, get full product data instantly
- **🎨 AI Image Generation** — 15 creative marketing images per product using Nano Banana Pro
- **🎯 Category Detection** — Auto-detects product type (electronics, beauty, fashion, etc.)
- **📐 Platform-Optimized** — Twitter 16:9, Instagram 4:5, Pinterest 2:3
- **🖼️ Smart Image Selection** — Uses DIFFERENT product images for each scene
- **📝 Caption Generation** — Platform-specific captions, hashtags, CTAs
- **📡 Auto-Posting** — Post to all platforms via Postiz API
- **✅ FTC Compliant** — #ad disclosure on every image

## 🏗️ Architecture

```
Amazon URL → Extract → Detect Category → Select Images
                                              ↓
                                   Generate 15 AI Scenes
                                              ↓
                                    Apply PIL Overlays
                                              ↓
                                  Generate Captions
                                              ↓
                              Post to Twitter + Instagram + Pinterest
```

## 📦 Quick Start

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 Pillow pyyaml
```

### 2. Setup
```bash
python3 ricky_config.py setup
```

### 3. Run
```bash
# Generate images only
python3 ricky_pipeline.py "https://www.amazon.in/dp/B0BZJ9D5W3"

# Generate + auto-post
python3 ricky_pipeline.py "https://www.amazon.in/dp/B0BZJ9D5W3" --post
```

## 📊 Output

Each run creates:
```
~/ricky-output/B0BZJ9D5W3/
├── twitter/          # 4 images (1344×768)
│   ├── tw_hero.png
│   ├── tw_features.png
│   ├── tw_lifestyle.png
│   └── tw_cta.png
├── instagram/        # 8 images (1024×1280)
│   ├── ig_hook.png
│   ├── ig_lifestyle.png
│   ├── ig_flatlay.png
│   ├── ig_detail.png
│   ├── ig_transform.png
│   ├── ig_texture.png
│   ├── ig_lifestyle2.png
│   └── ig_cta.png
├── pinterest/        # 3 images (1000×1500)
│   ├── pin_guide.png
│   ├── pin_aesthetic.png
│   └── pin_lifestyle.png
└── pipeline_meta.json
```

## 🎯 Supported Categories

| Category | Example Products | Scene Style |
|----------|-----------------|-------------|
| Camera | Sony ZV-1F, GoPro | Creator lifestyle, studio shots |
| Earbuds | Fire-Boltt, boAt | Music lover, gym, commute |
| Phone | iPhone, Samsung | Urban lifestyle, tech forward |
| Beauty | Face wash, serum | Spa aesthetic, glow-up |
| Fashion | Shoes, clothing | Street style, OOTD |
| Appliance | Fridge, AC | Modern home, family |
| Kitchen | Mixer, cookware | Food photography, chef |
| Fitness | Protein, gym gear | Gym motivation, active |
| Helmet | Steelbird, Studds | Biker lifestyle, road |

## 💰 Cost

~$1.50 per product (15 AI image generations via Fal.ai)

## 📡 Supported Platforms (via Postiz)

- ✅ Twitter/X (4-image grid)
- ✅ Instagram (carousel up to 10 slides)
- ✅ Pinterest (pins with SEO title + link)
- 🔜 Facebook, LinkedIn, TikTok

## ⚖️ Compliance

- FTC #ad disclosure on every image
- "Affiliate link" disclosure in captions
- Amazon Associates TOS compliant

## 📁 Files

| File | Purpose |
|------|---------|
| `ricky_pipeline.py` | Main pipeline — one command |
| `amazon_extractor.py` | Product data extraction |
| `smart_image_selector.py` | Image-to-scene matching |
| `scene_engine.py` | Category-specific prompts |
| `caption_engine.py` | Caption & hashtag generation |
| `postiz_poster.py` | Social media posting |
| `ricky_config.py` | Config & setup wizard |

## 📜 License

MIT
