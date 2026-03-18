# TOOLS.md - API Configuration

## Configuration Status

- [ ] Amazon Product Advertising API configured
- [ ] Postiz API connected
- [ ] Image AI provider configured (Fal.ai or Replicate)
- [ ] Social media accounts linked

---

## Your Niche

**Primary Focus:** Tech & Productivity  
*(Update this after setup)*

**Product Categories:**
- [ ] Tech gadgets (keyboards, mice, power banks)
- [ ] Productivity tools (desk accessories, planners)
- [ ] Home office (standing desks, chairs, lighting)
- [ ] Fitness equipment (resistance bands, yoga mats)
- [ ] Other: ___________

**Price Range:** $20-150  
**Commission Target:** 5%+ minimum

---

## API Configuration

### Amazon Product Advertising API

**Location:** `config.json`

```json
{
  "amazon": {
    "access_key": "YOUR_ACCESS_KEY",
    "secret_key": "YOUR_SECRET_KEY",
    "affiliate_tag": "yourname-20",
    "region": "us-east-1",
    "categories": ["Electronics", "HomeOffice", "Sports"]
  }
}
```

**Get credentials:**
1. Sign up: https://affiliate-program.amazon.com
2. Register for Product Advertising API: https://webservices.amazon.com/paapi5/documentation/
3. Get Access Key, Secret Key, and your Affiliate Tag

**Rate limits:**
- 1 request per second (free tier)
- 8,640 requests per day

---

### Postiz API

**Location:** `config.json`

```json
{
  "postiz": {
    "api_key": "YOUR_POSTIZ_API_KEY",
    "workspace_id": "YOUR_WORKSPACE_ID",
    "accounts": {
      "instagram": "account_id_1",
      "twitter": "account_id_2",
      "pinterest": "account_id_3",
      "facebook": "account_id_4"
    }
  }
}
```

**Get API key:**
1. Sign up: https://postiz.com
2. Connect social media accounts
3. Go to Settings → API → Generate Key
4. Copy API key and workspace ID

**Connected accounts (check which ones you want to use):**
- [ ] Instagram
- [ ] Twitter  
- [ ] Pinterest
- [ ] Facebook
- [ ] LinkedIn (optional)
- [ ] TikTok (optional)
- [ ] Reddit (optional)

**Active platforms for posting:**
Update `config.json` → `posting.platforms` with your selection.

Example:
```json
"posting": {
  "platforms": ["instagram", "pinterest"],  // Only these 2
  "frequency": "3_per_day"
}
```

Ricky will automatically post only to your selected platforms!

---

### Image Generation AI

**Option A: Fal.ai (Recommended)**

```json
{
  "image_ai": {
    "provider": "fal",
    "api_key": "YOUR_FAL_API_KEY",
    "model": "fal-ai/flux-pro",
    "default_mode": "image-to-image",
    "fallback_mode": "text-to-image"
  }
}
```

**Get API key:**
1. Sign up: https://fal.ai
2. Dashboard → API Keys → Create
3. Add credits (starts at $10)

**Cost:** ~$0.01-0.03 per image  
**Speed:** 2-4 seconds per image  
**Best for:** Fast, high-quality product enhancement

---

**Option B: Replicate**

```json
{
  "image_ai": {
    "provider": "replicate",
    "api_key": "YOUR_REPLICATE_API_KEY",
    "model": "stability-ai/sdxl",
    "default_mode": "text-to-image",
    "fallback_mode": "image-to-image"
  }
}
```

**Get API key:**
1. Sign up: https://replicate.com
2. Account → API Tokens → Create
3. Pay-per-use billing

**Cost:** ~$0.02-0.05 per image  
**Speed:** 5-10 seconds per image  
**Best for:** Flexible model selection

---

## Content Strategy

### Daily Posting Schedule

**6:00 AM** - Product research
- Find 3 trending products via Amazon API
- Filter: >4 stars, >1000 reviews, 5%+ commission

**6:30 AM** - Image generation
- Download product images
- Generate 5 styled variations per product (15 images total)
- Styles: Minimalist, lifestyle, comparison, flat lay, hero

**7:00 AM** - Caption writing & posting
- Write platform-specific captions
- Post via Postiz to all connected accounts
- Schedule: Immediate + staggered (9am, 2pm, 6pm)

**7:00 PM** - Performance check
- Review today's post engagement
- Track affiliate clicks via Amazon Associates dashboard
- Update strategy based on data

---

## Platform-Specific Settings

### Instagram
- **Post type:** Feed (1:1) + Story (9:16)
- **Hashtags:** 8-10 per post
- **Caption length:** 100-150 words
- **Best times:** 9am, 2pm, 6pm EST

### Twitter
- **Post type:** Image + thread (3-4 tweets)
- **Caption length:** 280 chars max
- **Hashtags:** 1-2 only
- **Best times:** 9am, 12pm, 5pm EST

### Pinterest
- **Post type:** Vertical pin (1000x1500px)
- **Description:** 200-300 words, keyword-rich
- **Boards:** Organize by category
- **Best times:** 2pm, 8pm EST

### Facebook
- **Post type:** Image + text post
- **Caption length:** 150-200 words
- **Link placement:** In post text
- **Best times:** 1pm, 3pm EST

---

## Image Generation Prompts

### Image-to-Image (Product Photo Enhancement)
```
Base prompt: "Professional product photography, {product_name}, 
minimalist background, soft natural lighting, high detail, 
4k quality, commercial style"

Styles to test:
- Minimalist: "white background, centered, studio lighting"
- Lifestyle: "on modern desk, laptop nearby, home office setting"
- Dramatic: "dark background, spotlight, premium feel"
- Flat lay: "top-down view, styled desk setup, organized"
```

### Text-to-Image (No Product Photo)
```
Prompt template: "High-quality product photo of {product_name}, 
{product_description}, professional lighting, commercial photography, 
white background, 4k, sharp focus"

Example: "High-quality product photo of wireless keyboard, 
sleek black aluminum design, RGB backlit keys, 
professional lighting, commercial photography, 
white background, 4k, sharp focus"
```

---

## Performance Tracking

### Metrics to Monitor (Daily)

**Engagement:**
- Likes, comments, shares per platform
- Click-through rate on affiliate links
- Follower growth

**Revenue:**
- Total clicks to Amazon
- Conversion rate (clicks → sales)
- Commission earned per product

**Content:**
- Best-performing image style
- Best-performing caption format
- Best-performing platform

### Update in MEMORY.md Weekly

```markdown
## Week 12 Performance

Products posted: 21
Total posts: 105 (5 platforms)
Affiliate clicks: 1,234
Conversions: 28 sales
Commission: $287.40

Top products:
1. Anker PowerBank: $89.20
2. Logitech Mouse: $47.60
3. Standing Desk Pad: $38.40

Top platform: Pinterest (48% of conversions)
Top image style: Lifestyle shots (2x engagement vs minimalist)
```

---

## Commands

### Find Products
```bash
# Ricky uses Amazon Product API
# Filters: >4 stars, >1000 reviews, 5%+ commission
# Returns: Top 10 products in your niche
```

### Generate Images
```bash
# For each product:
# 1. Download product image from Amazon
# 2. Call Fal.ai/Replicate API
# 3. Generate 5 style variations
# 4. Save to ./images/ directory
```

### Post to Social Media
```bash
# Via Postiz API:
# 1. Upload images
# 2. Write platform-specific captions
# 3. Schedule/publish to all accounts
# 4. Return post IDs for tracking
```

---

## Troubleshooting

**"No products found"**
- Verify Amazon API credentials in `config.json`
- Check category spelling (must match Amazon categories)
- Broaden search (lower star rating or review count)

**"Image generation failed"**
- Check AI provider API key
- Verify credits/balance
- Try fallback provider
- Use original product image without enhancement

**"Post failed"**
- Check Postiz API key
- Verify social accounts still connected (re-auth if needed)
- Check platform-specific limits (Instagram: 25 posts/day)

**"Low clicks"**
- Review image quality (A/B test styles)
- Improve captions (test different hooks)
- Post at different times
- Focus on best-performing platform

---

**First time setup?** Run `bash setup.sh` to configure everything automatically.
