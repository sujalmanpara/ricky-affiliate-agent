# Affiliate Content Automation Skill

## Overview
Complete automation pipeline for affiliate marketing: product research → image generation → multi-platform posting → performance tracking.

## Prerequisites
- Amazon Product Advertising API credentials
- Postiz API key with connected social accounts
- Image AI provider (Fal.ai or Replicate)
- Configuration in `config.json`

---

## Core Workflows

### 1. Find Trending Products

**User says:**
> "Ricky, find trending tech products"
> "Find 5 high-commission products in [category]"
> "Research products for today's posts"

**Execution:**

```python
# Pseudo-code for Amazon Product API call
def find_products(category, min_rating=4.0, min_reviews=1000, min_commission=5):
    """
    Search Amazon Product Advertising API
    """
    params = {
        "category": category,
        "sort_by": "relevance",  # or "rating", "price"
        "min_rating": min_rating,
        "min_reviews": min_reviews,
        "prime_eligible": True
    }
    
    products = amazon_api.search_items(params)
    
    # Filter by commission rate
    high_commission = [p for p in products if p.commission_rate >= min_commission]
    
    # Rank by score (rating × reviews × commission)
    scored = sorted(high_commission, 
                   key=lambda p: p.rating * log(p.reviews) * p.commission_rate,
                   reverse=True)
    
    return scored[:10]  # Top 10 products
```

**Response format:**

```
🔍 Found 10 trending tech products:

1. ⭐ Anker PowerCore 20000mAh
   - Rating: 4.7 stars (12,340 reviews)
   - Price: $39.99
   - Commission: 8% ($3.20 per sale)
   - Link: amzn.to/abc123
   
2. ⭐ Logitech MX Master 3S Mouse
   - Rating: 4.6 stars (8,456 reviews)
   - Price: $99.99
   - Commission: 6% ($6.00 per sale)
   - Link: amzn.to/def456
   
3. ⭐ USB-C Hub 7-in-1
   - Rating: 4.5 stars (5,234 reviews)
   - Price: $29.99
   - Commission: 7% ($2.10 per sale)
   - Link: amzn.to/ghi789

Top picks for posting:
✅ #1 (high commission + reviews)
✅ #2 (premium product, strong brand)
✅ #5 (trending, low competition)

Generate images for these 3?
```

**Store in MEMORY.md:**
```markdown
## Products Found (2026-03-17)

| Product | Rating | Reviews | Price | Commission | Status |
|---------|--------|---------|-------|------------|--------|
| Anker PowerCore | 4.7 | 12,340 | $39.99 | 8% | Selected |
| Logitech MX Master | 4.6 | 8,456 | $99.99 | 6% | Selected |
| USB-C Hub | 4.5 | 5,234 | $29.99 | 7% | Selected |
```

---

### 2. Generate Promotional Images

**User says:**
> "Ricky, create images for the Anker power bank"
> "Generate promo images for all 3 products"
> "Make lifestyle photos for these products"

**Execution:**

```python
def generate_product_images(product, styles=['minimalist', 'lifestyle', 'hero']):
    """
    Generate styled marketing images using AI
    """
    # Step 1: Download product image from Amazon
    product_image_url = product.images[0]  # Main product photo
    downloaded_image = download_image(product_image_url)
    
    generated_images = []
    
    for style in styles:
        # Scenario A: Image-to-Image (if product photo exists)
        if downloaded_image:
            prompt = build_img2img_prompt(product, style)
            image = fal_ai.image_to_image(
                image=downloaded_image,
                prompt=prompt,
                model="fal-ai/flux-pro",
                strength=0.7,  # How much to change (0.5-0.9)
                guidance_scale=7.5
            )
        
        # Scenario B: Text-to-Image (fallback)
        else:
            prompt = build_text2img_prompt(product, style)
            image = fal_ai.text_to_image(
                prompt=prompt,
                model="fal-ai/flux-pro",
                width=1024,
                height=1024
            )
        
        # Add text overlays, branding
        final_image = add_overlays(image, product)
        generated_images.append(final_image)
    
    return generated_images


def build_img2img_prompt(product, style):
    """
    Build image-to-image prompt for product enhancement
    """
    base = f"Professional product photography of {product.title}, high quality, 4k"
    
    style_prompts = {
        "minimalist": "white background, centered, studio lighting, clean, simple",
        "lifestyle": "on modern desk, laptop nearby, home office, natural light, cozy",
        "hero": "dramatic lighting, dark background, spotlight, premium feel, cinematic",
        "flat_lay": "top-down view, styled desk setup, organized, aesthetic",
        "comparison": "side by side with similar product, comparison shot"
    }
    
    return f"{base}, {style_prompts[style]}"


def build_text2img_prompt(product, style):
    """
    Build text-to-image prompt (no product photo)
    """
    return f"""High-quality product photography of {product.title}, 
    {product.description}, professional lighting, commercial style, 
    {style_prompts[style]}, 4k, sharp focus, detailed"""


def add_overlays(image, product):
    """
    Add text overlays, CTAs, branding
    """
    # Add text using PIL/Pillow
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial-Bold.ttf", 60)
    
    # Add product highlight text
    text = f"${product.price}"  # or benefit like "2X Battery Life"
    draw.text((50, 50), text, fill="white", font=font, stroke_width=2, stroke_fill="black")
    
    # Add CTA
    cta_font = ImageFont.truetype("Arial.ttf", 40)
    draw.text((50, img.height - 100), "Link in bio →", fill="white", font=cta_font)
    
    return img
```

**Response format:**

```
🎨 Generated 15 images for 3 products:

**Anker PowerCore** (5 images)
✅ minimalist-anker-1.jpg (1024x1024)
✅ lifestyle-anker-2.jpg (1024x1024)
✅ hero-anker-3.jpg (1024x1024)
✅ flatlay-anker-4.jpg (1024x1024)
✅ comparison-anker-5.jpg (1024x1024)

**Logitech MX Master** (5 images)
✅ minimalist-logitech-1.jpg
✅ lifestyle-logitech-2.jpg
...

**USB-C Hub** (5 images)
✅ minimalist-usbc-1.jpg
✅ lifestyle-usbc-2.jpg
...

Total cost: $0.45 (15 images × $0.03)
Ready to write captions and post?
```

**Error handling:**
```
If Fal.ai fails:
  → Retry once with simpler prompt
  → If still failing, switch to Replicate
  → If all AI fails, use original product image only
  → Log error in MEMORY.md
```

---

### 3. Write Platform-Specific Captions

**User says:**
> "Ricky, write captions for these products"
> "Create Instagram and Twitter captions"
> "Write a Pinterest description"

**Execution:**

```python
def write_captions(product, platforms=['instagram', 'twitter', 'pinterest']):
    """
    Generate platform-optimized captions with AI
    """
    captions = {}
    
    for platform in platforms:
        prompt = f"""Write a {platform} caption for this product:
        
        Product: {product.title}
        Price: {product.price}
        Rating: {product.rating} stars ({product.reviews} reviews)
        Key features: {product.features}
        
        Requirements:
        - {get_platform_requirements(platform)}
        - Include affiliate disclosure (#ad or "affiliate link")
        - Provide value, don't just sell
        - Use appropriate tone for {platform}
        - Add relevant emojis
        """
        
        caption = ai_generate(prompt)  # Use Claude/GPT for caption writing
        captions[platform] = caption
    
    return captions


def get_platform_requirements(platform):
    requirements = {
        "instagram": "150 words max, emoji-heavy, storytelling hook, 8-10 hashtags",
        "twitter": "280 chars, concise hook, question-based, 1-2 hashtags max",
        "pinterest": "300 words, SEO keywords, how-to angle, problem-solution format",
        "facebook": "200 words, value-focused, community feel, conversational tone",
        "linkedin": "Formal tone, professional angle, productivity/efficiency focus"
    }
    return requirements[platform]
```

**Example output:**

```
📝 Captions written for Anker PowerCore:

**Instagram:**
"Ever been stuck with a dead phone at the worst time? 😩

This power bank changed my life. 20,000mAh = charges my phone 4x, my laptop 2x. Perfect for travel, remote work, or just peace of mind.

✨ Why I love it:
• Charges 3 devices at once
• TSA-approved for flights
• Lasts 2 weeks between charges

Been using it for 3 months. Worth every penny.

Link in bio or DM me "POWER" for the link 🔋 #ad

#powerbank #techgadgets #remotework #travelessentials #productivity #wfh #techmusthaves #amazonfinds"

**Twitter (Thread):**
Tweet 1: "Your phone died. Meeting in 10 minutes. You're screwed.

Or are you? 🔋 [image]"

Tweet 2: "This $40 power bank has saved me countless times:

• 20,000mAh capacity
• Charges phone 4x
• 3 devices simultaneously  
• Lasts 2 weeks

Worth it? 100%. [link] #ad"

Tweet 3: "4.7 stars, 12k reviews. Not just me who loves it.

Grab it here: [affiliate link]"

**Pinterest:**
"The Ultimate Travel Power Bank: Never Run Out of Battery Again

Are you tired of hunting for outlets at airports? Does your phone die right when you need GPS the most? This 20,000mAh power bank is the solution every traveler needs.

**What makes it special:**
- Massive capacity: Charges iPhone 4 times, Android 3 times
- Fast charging: PD 18W output charges devices 2x faster
- Universal compatibility: Works with phones, tablets, laptops, cameras
- TSA-approved: Bring it on any flight without issues
- Durable build: Survived 100+ trips in my backpack

**Perfect for:**
✈️ International travel
🏕️ Camping and outdoor adventures
🏢 Long workdays away from outlets
🎒 College students
🚗 Road trips

**Real user experience:**
I've been using this for 6 months across 15 countries. Never once worried about battery life. Charges my phone, AirPods, and Kindle simultaneously.

**Price:** $39.99 (down from $59.99)
**Rating:** 4.7/5 stars from 12,340 reviews
**Commission disclosure:** I earn a small commission if you buy through my link (at no extra cost to you) #ad

[Affiliate Link: amzn.to/abc123]"
```

---

### 4. Post to Multiple Platforms (Dynamic Platform Selection)

**User says:**
> "Ricky, post all 3 products to Instagram and Twitter"
> "Post this to Pinterest only"
> "Schedule posts for today at 9am, 2pm, 6pm"
> "Post to all platforms now"
> "Only use Instagram and Pinterest from now on"

**Execution:**

```python
def post_to_platforms(products, captions, images, platforms=None, schedule='now'):
    """
    Post via Postiz API to multiple platforms
    
    Args:
        platforms: List of platforms or None (uses config.json defaults)
    """
    # Dynamic platform selection
    if platforms is None:
        # Load from config.json
        platforms = config['posting']['platforms']
    elif isinstance(platforms, str):
        # Single platform specified: "instagram"
        platforms = [platforms]
    
    # Filter only active platforms from config
    active_platforms = [p for p in platforms if config['posting']['platform_priority'].get(p, False)]
    
    post_results = []
    
    for product in products:
        for platform in active_platforms:
            # Prepare post data
            post_data = {
                "text": captions[product.id][platform],
                "media": [images[product.id][platform]],
                "platforms": [platform],
                "schedule": schedule,  # 'now' or timestamp
                "settings": {
                    "instagram": {
                        "type": "feed",  # or "story", "reel"
                        "first_comment": generate_hashtag_comment(product)
                    },
                    "twitter": {
                        "thread": split_into_thread(captions[product.id]['twitter'])
                    },
                    "pinterest": {
                        "board_id": get_board_id(product.category),
                        "link": product.affiliate_link
                    }
                }
            }
            
            # Call Postiz API
            response = postiz_api.create_post(post_data)
            
            post_results.append({
                "product": product.title,
                "platform": platform,
                "post_id": response.id,
                "url": response.url,
                "scheduled_for": response.scheduled_time
            })
    
    return post_results
```

**Response format:**

```
✅ Posted 3 products to 4 platforms (12 posts total)

**Anker PowerCore:**
- Instagram: Posted (ID: inst_abc123) → instagram.com/p/abc123
- Twitter: Posted (ID: tw_def456) → twitter.com/you/status/def456
- Pinterest: Posted (ID: pin_ghi789) → pinterest.com/pin/ghi789
- Facebook: Posted (ID: fb_jkl012) → facebook.com/you/posts/jkl012

**Logitech MX Master:**
- Instagram: Scheduled for 2:00 PM
- Twitter: Scheduled for 2:00 PM
- Pinterest: Scheduled for 2:00 PM
- Facebook: Scheduled for 2:00 PM

**USB-C Hub:**
- Instagram: Scheduled for 6:00 PM
- Twitter: Scheduled for 6:00 PM
- Pinterest: Scheduled for 6:00 PM
- Facebook: Scheduled for 6:00 PM

Track performance via Postiz dashboard: postiz.com/analytics
```

**Tracking in MEMORY.md:**
```markdown
## Posts Created (2026-03-17)

| Product | Platform | Post ID | Scheduled | Link |
|---------|----------|---------|-----------|------|
| Anker PowerCore | Instagram | inst_abc123 | 9:00 AM | instagram.com/p/abc123 |
| Anker PowerCore | Twitter | tw_def456 | 9:00 AM | twitter.com/you/status/def456 |
...
```

---

### 5. Track Performance

**User says:**
> "Ricky, how are today's posts performing?"
> "Show me yesterday's affiliate clicks"
> "Which platform is converting best?"

**Execution:**

```python
def track_performance(date_range='today'):
    """
    Gather performance data from Postiz + Amazon Associates
    """
    # Get Postiz analytics
    postiz_data = postiz_api.get_analytics(date_range)
    
    # Get Amazon clicks/conversions
    amazon_data = amazon_associates_api.get_report(date_range)
    
    # Combine data
    performance = {
        "engagement": {
            "likes": sum(p.likes for p in postiz_data),
            "comments": sum(p.comments for p in postiz_data),
            "shares": sum(p.shares for p in postiz_data),
            "reach": sum(p.reach for p in postiz_data)
        },
        "clicks": {
            "total": amazon_data.total_clicks,
            "by_platform": group_by_platform(amazon_data.clicks)
        },
        "conversions": {
            "sales": amazon_data.ordered_items,
            "revenue": amazon_data.commission_earned,
            "conversion_rate": (amazon_data.ordered_items / amazon_data.total_clicks) * 100
        }
    }
    
    return performance
```

**Response format:**

```
📊 Performance Report (Yesterday)

**Engagement:**
- Total reach: 12,450 people
- Likes: 234
- Comments: 18
- Shares: 12
- Saves: 45 (Instagram)

**Affiliate Clicks:**
- Total: 89 clicks
- By platform:
  - Pinterest: 43 clicks (48%) ⭐
  - Instagram: 28 clicks (31%)
  - Twitter: 12 clicks (13%)
  - Facebook: 6 clicks (7%)

**Conversions:**
- Sales: 4 purchases
- Items sold: 6 total (2 people bought 2 items)
- Revenue: $167.96
- Commission: $11.80 (7% avg)
- Conversion rate: 4.5% (good!)

**Top Performer:**
🏆 Anker PowerCore on Pinterest
- 31 clicks → 3 sales = 9.7% conversion
- $89.97 revenue → $7.20 commission

**Insights:**
✅ Pinterest is your winner (48% of clicks, highest conversion)
✅ 4.5% conversion rate is above average (target: 3-5%)
⚠️ Facebook underperforming (only 7% of clicks)

**Action Items:**
- Focus 50% of tomorrow's posts on Pinterest
- A/B test Facebook captions (may need different angle)
- Anker products convert well → find similar items
```

---

### 6. Weekly Revenue Report & Deep Analysis

**User says:**
> "Ricky, give me this week's report"
> "How much did I earn this week?"
> "What's the strategy for next week?"

**Response format:**

```
📊 Ricky's Weekly Report (Mar 10-16, 2026) - Week 12

═══════════════════════════════════════════════════════
📈 REVENUE SUMMARY
═══════════════════════════════════════════════════════

**Commission Earned: $347.40** (+42% vs Week 11)
- Products promoted: 21
- Posts published: 84 (4 platforms)
- Total reach: 47,230 people
- Affiliate clicks: 892
- Conversions: 28 sales (3.1% conversion rate)
- Items sold: 34 total

**Cost Analysis:**
- Image AI: $3.15 (105 images @ $0.03)
- Postiz: $39/month (prorated: $9.00)
- Total costs: $12.15
- **Net profit: $335.25** ✅

**ROI:** 2,760% (earned $347.40, spent $12.15)

═══════════════════════════════════════════════════════
🏆 TOP PERFORMERS
═══════════════════════════════════════════════════════

**Best Products:**
1. 🥇 Anker PowerCore 20k
   - 67 clicks → 8 sales (11.9% conversion!) 🔥
   - $319.84 revenue → $28.80 commission
   - Posted 3x (Instagram, Pinterest, Twitter)
   - Why it worked: High demand + trusted brand + lifestyle images

2. 🥈 Logitech MX Master 3S
   - 43 clicks → 5 sales (11.6% conversion)
   - $499.95 revenue → $30.00 commission
   - Premium product, strong margins

3. 🥉 USB-C Hub 7-in-1
   - 89 clicks → 4 sales (4.5% conversion)
   - $119.96 revenue → $8.40 commission
   - High clicks but average conversion (price resistance?)

**Best Platforms:**
1. 📍 Pinterest: 427 clicks, 15 sales, $167.40 commission (48% of total!)
   - Why: SEO keywords driving organic traffic
   - Avg post lifespan: 30+ days (keeps earning)
   
2. 📸 Instagram: 289 clicks, 8 sales, $112.60 commission
   - Why: Visual platform, lifestyle shots perform best
   - Stories outperform feed posts (1.8x conversion)

3. 🐦 Twitter: 124 clicks, 3 sales, $47.20 commission
   - Why: Quick engagement, threads work well
   - Morning posts (9am) convert 2x better

4. 📘 Facebook: 52 clicks, 2 sales, $20.20 commission
   - ⚠️ Underperforming (only 6% of clicks)
   - Action: Test different content angle next week

**Best Content Types:**
- 📷 Lifestyle images: 2.1x engagement vs minimalist
- 📝 "Problem-solution" captions: 1.8x clicks
- 💰 Posts with price callout: 1.5x conversions
- ⚖️ Comparison shots: 1.3x shares

═══════════════════════════════════════════════════════
📊 TREND ANALYSIS
═══════════════════════════════════════════════════════

**What's Working (Keep Doing):**
✅ Tech accessories (power banks, hubs, mice) = 67% of revenue
✅ Pinterest focus = highest ROI platform
✅ Lifestyle/comparison images = 2x engagement
✅ Morning posts (9am) = 1.8x conversion vs evening
✅ Price range $30-100 = sweet spot (not too cheap, not intimidating)

**What's Improving (Momentum Building):**
📈 Conversion rate: 3.1% (up from 2.4% Week 11) - above industry avg!
📈 Avg commission per sale: $12.41 (up from $9.80) - promoting higher-ticket items
📈 Pinterest traffic: +34% week-over-week (content gaining traction)
📈 Instagram Stories: 1.8x conversion vs feed (discovered this week)

**What's Declining (Needs Attention):**
📉 Facebook engagement: -18% (algorithm change? or content mismatch?)
📉 Twitter clicks: -12% (audience fatigue? need fresh angles)
📉 Click-to-conversion on budget items (<$30): Only 1.9% (people browse but don't buy)

**What's Risky (Watch Closely):**
⚠️ Anker products = 33% of revenue (too concentrated, diversify!)
⚠️ 3 products got 0 clicks (wrong niche fit)
⚠️ Weekend posts = 40% fewer clicks (audience behavior pattern)

═══════════════════════════════════════════════════════
🎯 DEEP INSIGHTS
═══════════════════════════════════════════════════════

**1. Platform Efficiency Analysis**

| Platform  | Time Investment | Revenue | ROI Score |
|-----------|----------------|---------|-----------|
| Pinterest | 15 min/day     | $167.40 | ⭐⭐⭐⭐⭐ |
| Instagram | 20 min/day     | $112.60 | ⭐⭐⭐⭐ |
| Twitter   | 10 min/day     | $47.20  | ⭐⭐⭐ |
| Facebook  | 10 min/day     | $20.20  | ⭐ |

**Recommendation:** Shift 50% of effort to Pinterest (highest ROI)

**2. Product Category Performance**

- **Tech Accessories** (power, cables, hubs): 67% of revenue ⭐
  - High demand, trusted brands, clear value prop
  - Commission: 6-8% avg
  - Conversion: 7.2%
  
- **Computer Peripherals** (mice, keyboards): 23% of revenue
  - Premium products, higher ticket
  - Commission: 5-7% avg
  - Conversion: 5.8%

- **Office Supplies** (desk pads, organizers): 10% of revenue
  - Lower margins, impulse buys
  - Commission: 4-5% avg
  - Conversion: 3.1%

**Recommendation:** Focus 70% on tech accessories (proven winner)

**3. Image Style Performance Matrix**

| Style        | Engagement | Clicks | Conversion | Best Platform |
|--------------|-----------|--------|------------|---------------|
| Lifestyle    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Instagram     |
| Comparison   | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Pinterest     |
| Hero/Dramatic| ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Twitter       |
| Flat lay     | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Instagram     |
| Minimalist   | ⭐⭐ | ⭐⭐ | ⭐⭐ | Facebook      |

**Recommendation:** 50% lifestyle, 30% comparison, 20% hero shots

**4. Caption Formula Success Rate**

- "Problem → Solution → CTA": 11.2% click rate ⭐⭐⭐⭐⭐
- "Feature list + price": 8.7% click rate ⭐⭐⭐⭐
- "Storytelling + emotional hook": 7.3% click rate ⭐⭐⭐
- "Direct pitch": 4.1% click rate ⭐⭐

**Recommendation:** Lead with problem-solution format

**5. Posting Time Optimization**

Best times (based on 12 weeks of data):
- Pinterest: 2pm EST (pins get indexed faster)
- Instagram: 9am EST (morning scroll)
- Twitter: 9am, 5pm EST (commute times)
- Facebook: 1pm EST (lunch break)

Worst times:
- Late night (11pm-6am): 73% fewer clicks
- Sunday morning: 58% fewer clicks
- Friday evening: 41% fewer clicks (people going out)

═══════════════════════════════════════════════════════
🔮 PREDICTIVE ANALYSIS
═══════════════════════════════════════════════════════

**Next Week Projection (Mar 17-23):**
- Expected commission: $420-480 (+25% growth)
- Based on: Current momentum + Pinterest growth + optimized posting times

**Month-End Projection (Week 16):**
- Monthly commission: $1,680-1,920
- On track for: $2,000/month by Week 20 ✅

**Confidence level:** 85% (based on 12 weeks of data)

**Key assumptions:**
✅ Continue current posting frequency (3 products/day)
✅ Maintain Pinterest focus (50% of content)
✅ No major platform algorithm changes
⚠️ Risk: Easter week might see 15-20% dip (historical pattern)

═══════════════════════════════════════════════════════
⚡ ACTION ITEMS (Next 7 Days)
═══════════════════════════════════════════════════════

**🎯 High Priority (Do This Week):**

1. **Double Down on Winners**
   - Find 3 more Anker products (proven brand)
   - Post 5x to Pinterest (best ROI platform)
   - Use lifestyle image style exclusively (2x engagement)

2. **Fix Facebook Underperformance**
   - Test longer-form posts (200-300 words vs 100)
   - Add more "community" tone (less salesy)
   - Post to Facebook Groups (not just Page)
   - A/B test times: Try 7pm instead of 1pm

3. **Optimize Conversion Funnel**
   - Add "limited time deal" angle to captions (urgency)
   - Test Instagram Stories with poll stickers (engagement)
   - Create comparison posts for top 3 products (vs alternatives)

**💡 Medium Priority (Consider):**

4. **Diversify Product Mix**
   - Reduce Anker dependency (currently 33% of revenue)
   - Test 2 new brands: Ugreen, Baseus
   - Add 1 premium product ($150-200 range)

5. **Expand Content Formats**
   - Try carousel posts on Instagram (3-5 images)
   - Create "Top 5" roundup posts (multiple products)
   - Test Pinterest video pins (new feature)

6. **Build Retargeting Assets**
   - Start collecting emails (offer free guide)
   - Create custom audience pixels
   - Prepare for Q2 scaling

**🔬 Experiments to Run:**

7. **A/B Tests:**
   - Caption format: Problem-solution vs Feature-list
   - CTA placement: Top vs bottom of caption
   - Hashtag count: 8-10 vs 3-5 (Instagram)
   - Post frequency: 3/day vs 4/day

8. **New Platform Test:**
   - Try TikTok (product demos, 15-sec clips)
   - Expected: 500-1000 views/video, 20-40 clicks

═══════════════════════════════════════════════════════
⚠️ RISK ALERTS
═══════════════════════════════════════════════════════

**High Risk:**
🔴 **Revenue Concentration:** 33% from Anker products
   - Fix: Diversify to 3-5 brands (max 20% per brand)
   - Timeline: This week

**Medium Risk:**
🟡 **Facebook Decline:** -18% engagement
   - Fix: Revamp content strategy (see Action #2)
   - Timeline: Test new approach by Week 13

🟡 **Weekend Gap:** 40% fewer clicks Sat-Sun
   - Fix: Schedule best-performing content for weekends
   - Timeline: Implement starting next Saturday

**Low Risk:**
🟢 **Seasonal Dip:** Easter week approaching
   - Impact: Expected 15-20% revenue dip
   - Mitigation: Pre-schedule extra content, holiday-themed products

═══════════════════════════════════════════════════════
📈 BENCHMARKING
═══════════════════════════════════════════════════════

**Your Performance vs Industry Average:**

| Metric              | You    | Industry Avg | Status |
|---------------------|--------|--------------|--------|
| Conversion Rate     | 3.1%   | 2-3%         | ✅ Above |
| Avg Commission      | $12.41 | $8-10        | ✅ Above |
| Click-through Rate  | 4.8%   | 3-5%         | ✅ On Target |
| Return Customer %   | 8%     | 5-10%        | ✅ On Target |

**Your Performance vs Your Goals:**

- Goal: $500/month by Week 16
- Current: $347/week = $1,388/month pace
- Status: **🎉 Goal crushed! (278% of target)**
- New goal: $2,000/month by Week 20

═══════════════════════════════════════════════════════
🎯 NEXT WEEK STRATEGY
═══════════════════════════════════════════════════════

**Focus Areas (70-20-10 rule):**

**70% - What's Working**
- Tech accessories (power banks, hubs, cables)
- Pinterest + Instagram (top 2 platforms)
- Lifestyle + comparison images
- Morning posts (9am slot)
- Problem-solution captions

**20% - What Needs Improvement**
- Facebook content strategy
- Weekend posting optimization
- Brand diversification (reduce Anker dependency)

**10% - Experiments**
- TikTok test
- Carousel posts
- "Top 5" roundup content
- Email list building

**Target Metrics:**
- Revenue: $420-480 (+25%)
- Conversion rate: 3.3%+ (maintain high performance)
- Pinterest clicks: 500+ (grow best channel)
- Facebook fix: 100+ clicks (2x current)

**Stretch Goal:**
Break $500/week commission 🚀

═══════════════════════════════════════════════════════
💭 STRATEGIC INSIGHTS
═══════════════════════════════════════════════════════

**What I Learned This Week:**

1. **Pinterest is the affiliate goldmine**
   - Longest content lifespan (30+ days vs 24 hours on other platforms)
   - SEO-driven organic traffic (passive income even after posting)
   - Higher purchase intent (people actively searching for solutions)

2. **Brand trust matters more than features**
   - Anker products convert 2x better than no-name brands
   - Even at 20% higher price, trusted brands win

3. **Lifestyle > Product shots**
   - People buy the lifestyle, not the product
   - "Person using product" beats "product on white background" every time

4. **Urgency works** (but don't overuse)
   - "Deal ends tonight" posts: 1.4x conversion
   - But using it daily kills trust (use sparingly)

**Quote of the Week:**
"Your best content should go on your best platform. We're all-in on Pinterest because that's where the money is." 💰

═══════════════════════════════════════════════════════

**Questions? Reply with:**
- "Explain [metric]" for details
- "Show [product] performance" for deep dive
- "What should I do about [issue]?" for advice

**Next report:** Monday, March 24, 9:00 AM

Keep crushing it! 🚀
```

---

## Dynamic Platform Selection

### Change Platforms Anytime

**User says:**
> "Ricky, from now on only post to Instagram and Pinterest"
> "Add TikTok to the posting schedule"
> "Stop posting to Facebook"
> "Post this product to Twitter only"

**Execution:**

```python
def update_active_platforms(user_request):
    """
    Update active platforms based on user request
    """
    if "only" in user_request.lower():
        # Replace all platforms
        requested_platforms = extract_platforms(user_request)
        config['posting']['platforms'] = requested_platforms
        
        # Update priority
        for platform in ALL_PLATFORMS:
            config['posting']['platform_priority'][platform] = (platform in requested_platforms)
        
        save_config()
        return f"✅ Updated! Now posting only to: {', '.join(requested_platforms)}"
    
    elif "add" in user_request.lower():
        # Add platform to existing
        platform_to_add = extract_platform(user_request)
        if platform_to_add not in config['posting']['platforms']:
            config['posting']['platforms'].append(platform_to_add)
            config['posting']['platform_priority'][platform_to_add] = True
            save_config()
        return f"✅ Added {platform_to_add}! Now posting to: {', '.join(config['posting']['platforms'])}"
    
    elif "stop" in user_request.lower() or "remove" in user_request.lower():
        # Remove platform
        platform_to_remove = extract_platform(user_request)
        config['posting']['platforms'].remove(platform_to_remove)
        config['posting']['platform_priority'][platform_to_remove] = False
        save_config()
        return f"✅ Removed {platform_to_remove}! Now posting to: {', '.join(config['posting']['platforms'])}"


def post_with_platform_override(product, platforms_override=None):
    """
    Post to specific platforms (overrides config for this post only)
    """
    if platforms_override:
        # One-time override
        platforms = platforms_override
    else:
        # Use config defaults
        platforms = [p for p in config['posting']['platforms'] 
                    if config['posting']['platform_priority'][p]]
    
    for platform in platforms:
        post_to_platform(product, platform)
```

**Response examples:**

```
User: "Only use Instagram and Pinterest from now on"

Ricky:
✅ Updated posting configuration!

Active platforms: Instagram, Pinterest
Disabled: Twitter, Facebook, LinkedIn

This change is permanent. All future posts will go to Instagram and Pinterest only.

Want to test other platforms later? Just say:
"Ricky, add Twitter back"
```

```
User: "Post this product to Twitter only"

Ricky:
✅ Posting Anker PowerCore to Twitter only (one-time override)

Your default platforms (Instagram, Pinterest) remain unchanged.
This is just for this specific post.

Tweet posted: twitter.com/you/status/abc123
```

---

## Advanced Workflows

### Batch Product Research

**User says:**
> "Ricky, find 20 products for this week"
> "Research trending items in tech, fitness, and home office"

```python
def batch_research(categories, count_per_category=10):
    all_products = []
    
    for category in categories:
        products = find_products(category, limit=count_per_category)
        all_products.extend(products)
    
    # Rank by potential (rating × reviews × commission × price)
    ranked = rank_by_potential(all_products)
    
    # Select diverse mix (don't post 20 power banks)
    diverse_selection = select_diverse(ranked, max_per_subcategory=3)
    
    return diverse_selection
```

---

### A/B Testing

**User says:**
> "Ricky, A/B test two caption styles for this product"
> "Test minimalist vs lifestyle images"

```python
def ab_test(product, test_type='caption'):
    if test_type == 'caption':
        # Generate 2 caption styles
        captions = [
            write_caption(product, style='storytelling'),
            write_caption(product, style='feature-list')
        ]
        
        # Post both to Instagram (split audience)
        post_variant_a = post_to_instagram(product, captions[0])
        post_variant_b = post_to_instagram(product, captions[1])
        
        # Track for 24 hours
        schedule_check(after=24, compare=[post_variant_a, post_variant_b])
    
    elif test_type == 'image':
        # Generate 2 image styles
        images = [
            generate_image(product, style='minimalist'),
            generate_image(product, style='lifestyle')
        ]
        
        # Post both, track performance
        ...
```

---

### Seasonal Campaigns

**User says:**
> "Ricky, create a Black Friday campaign"
> "Find holiday gift ideas under $50"

```python
def seasonal_campaign(event='black_friday'):
    if event == 'black_friday':
        # Find deals
        products = find_products(filters={
            "deal_percentage": ">20%",
            "price_range": "$20-$200"
        })
        
        # Generate "deal" themed images
        for product in products:
            generate_image(product, overlay_text=f"{product.discount}% OFF")
        
        # Write urgent captions
        captions = write_captions(products, tone='urgent', cta='Deal ends soon!')
        
        # Post throughout the day
        schedule_posts(products, frequency='every 2 hours')
```

---

## Error Handling

### API Failures

```python
def handle_api_error(error, operation):
    if error.type == 'rate_limit':
        wait_time = error.retry_after or 3600
        log(f"Rate limit hit. Waiting {wait_time}s")
        schedule_retry(operation, after=wait_time)
    
    elif error.type == 'authentication':
        alert_user("API key invalid. Please check config.json")
        pause_automation()
    
    elif error.type == 'service_down':
        # Try fallback provider
        if operation == 'image_generation':
            switch_to_fallback_image_provider()
            retry(operation)
        else:
            log_error(error)
            schedule_retry(operation, after=900)
```

---

## Performance Optimization

### Smart Posting Times

```python
def optimize_posting_schedule():
    """
    Analyze historical data to find best posting times
    """
    historical_data = get_past_30_days_performance()
    
    # Group by hour of day
    by_hour = group_by(historical_data, 'hour')
    
    # Find top 3 hours for each platform
    best_times = {}
    for platform in ['instagram', 'twitter', 'pinterest', 'facebook']:
        platform_data = filter(by_hour, platform=platform)
        sorted_hours = sort_by(platform_data, key='engagement_rate', desc=True)
        best_times[platform] = sorted_hours[:3]
    
    # Update posting schedule
    update_config('posting_schedule', best_times)
```

---

## Integration with OpenClaw

### Cron Schedule

```cron
# Daily product research & posting
0 6 * * * openclaw-agent "Ricky, find 3 products and post to all platforms"

# Evening performance check
0 19 * * * openclaw-agent "Ricky, check today's performance"

# Weekly report (Monday 9am)
0 9 * * 1 openclaw-agent "Ricky, generate weekly revenue report"
```

### Memory Persistence

Store in `MEMORY.md`:
- Product history (what's been posted)
- Performance metrics (clicks, conversions, revenue)
- A/B test results
- Best-performing content styles
- Platform preferences

---

## Success Checklist

**Week 1:**
- [ ] Posted 21 products (3/day × 7 days)
- [ ] Generated 105 images
- [ ] Tracked all clicks in Amazon Associates
- [ ] Identified best-performing platform

**Week 2:**
- [ ] Doubled down on top platform
- [ ] A/B tested image styles
- [ ] Earned first $50 in commissions

**Week 4:**
- [ ] Consistent $100+/week revenue
- [ ] Optimized posting schedule
- [ ] 500+ followers across platforms

**Week 8:**
- [ ] $200-300/week stable income
- [ ] Proven content formula
- [ ] Considering scaling to more niches

---

**Ready to automate?** Say: "Ricky, let's start making money" 🚀
