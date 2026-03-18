# Ricky - AI Affiliate Content Automation Agent

> **Your 24/7 Affiliate Marketing Machine** — Finds trending products, generates stunning promo images, and posts to all social platforms automatically.

---

## 🎯 What is This?

**Ricky** is an AI agent that automates your entire affiliate marketing workflow:

✅ **Product Discovery** - Scans Amazon Affiliate API for high-commission trending products  
✅ **AI Image Generation** - Creates eye-catching promotional images (product photos → styled marketing images)  
✅ **Smart Captions** - Writes engaging copy with affiliate links and CTAs  
✅ **Multi-Platform Posting** - Auto-posts to Instagram, Twitter, Pinterest, Facebook, LinkedIn via Postiz  
✅ **Performance Tracking** - Monitors clicks, conversions, and commissions daily  

**Realistic goal:** $200-500/month affiliate income within 60 days, fully automated.

---

## 💰 Why This Works

**Traditional affiliate marketing:**
- ❌ Hours finding products
- ❌ Manual image creation (Canva, Photoshop)
- ❌ Writing captions for each platform
- ❌ Posting manually 3-5x per day
- ❌ Forgetting to track what works

**With Ricky:**
- ✅ Finds top products in 30 seconds (API automation)
- ✅ Generates pro images in 10 seconds (AI image generation)
- ✅ Platform-optimized captions automatically
- ✅ Posts to 5+ platforms simultaneously
- ✅ Tracks everything, optimizes based on data

**Setup once → Runs forever → Earn commissions while you sleep**

---

## 📦 What's Included

```
ricky-affiliate-agent/
├── SOUL.md          # Agent personality & strategy
├── IDENTITY.md      # Agent introduction
├── TOOLS.md         # API configuration guide
├── SKILL.md         # Complete automation workflow
├── setup.sh         # One-click setup script
├── config.example.json  # Configuration template
└── README.md        # This file
```

---

## 🚀 Quick Start (10 minutes)

### Prerequisites

You need API keys (all have free tiers):

1. **Amazon Product Advertising API** (free for affiliates)
2. **Postiz API** (multi-platform posting)
3. **Image Generation** (pick provider + model):
   - **Fal.ai** (Recommended):
     - FLUX Pro: $0.03/image (best quality)
     - FLUX Dev: $0.01/image (balanced) ⭐
     - FLUX Schnell: $0.003/image (fastest)
   - **Replicate**: SDXL, Kandinsky ($0.02-0.05/image)
   - **Together AI**: FLUX Schnell ($0.008/image, budget)
   - **Runpod**: Any SD model (cheapest at scale)

### Installation

**Step 1: Run Setup Script**
```bash
cd ~/ricky-affiliate-agent
bash setup.sh
```

This will prompt you for:
- Amazon Affiliate credentials
- Postiz API key
- Image AI provider (Fal.ai or Replicate)
- Social media accounts to connect

**Step 2: Install in OpenClaw**
```bash
# Copy agent files
cp ~/ricky-affiliate-agent/SOUL.md ~/.openclaw/workspace/
cp ~/ricky-affiliate-agent/IDENTITY.md ~/.openclaw/workspace/
cp ~/ricky-affiliate-agent/TOOLS.md ~/.openclaw/workspace/

# Copy skill
mkdir -p ~/.openclaw/skills/affiliate-automation
cp ~/ricky-affiliate-agent/SKILL.md ~/.openclaw/skills/affiliate-automation/
```

**Step 3: Configure Niche**

Edit `TOOLS.md`:
```markdown
## Your Niche
- Primary: Tech gadgets
- Secondary: Productivity tools
- Budget: $20-100 products
```

**Step 4: Test Run**

In OpenClaw:
> "Ricky, find 3 trending tech products and create promotional posts"

---

## 🤖 How Ricky Works

### Daily Automation Flow

**6:00 AM** - Product Research
```
1. Scan Amazon Affiliate API
2. Filter: >4 stars, >1000 reviews, 5%+ commission
3. Find 3 trending products in your niche
4. Check commission rates & profitability
```

**6:10 AM** - Content Creation (for each product)
```
1. Download product image from Amazon
2. Generate styled marketing image:
   - If product image exists → Image-to-image (enhance/style)
   - If no image → Text-to-image (generate from description)
3. Add text overlays, branding, call-to-action
4. Write platform-specific captions:
   - Instagram: Emoji-heavy, storytelling
   - Twitter: Concise, question-based
   - Pinterest: SEO keywords, how-to angle
   - Facebook: Longer, value-focused
```

**6:20 AM** - Multi-Platform Posting
```
Via Postiz API, post to:
- Instagram (Feed + Story)
- Twitter (Tweet + thread)
- Pinterest (Pin with rich description)
- Facebook (Page post)
- LinkedIn (Professional angle)
```

**7:00 PM** - Performance Check
```
1. Check Postiz analytics
2. Track Amazon clicks via affiliate dashboard
3. Update strategy based on data
```

**Monday 9:00 AM** - Weekly Deep Analysis Report
```
📊 Week 12 Comprehensive Analysis:

Commission Earned: $347.40 (+42% growth)
Net Profit: $335.25 (after costs)

═══ INSIGHTS ═══
📈 What's Working: Tech accessories (67% revenue), Pinterest (48% clicks)
📉 Needs Fix: Facebook engagement down 18%
⚠️ Risk: Over-reliance on Anker (33% of revenue)

═══ PREDICTIONS ═══
Next week: $420-480 projected (+25%)
Month-end: $1,680-1,920 on current trajectory

═══ ACTION ITEMS ═══
1. Double down on tech accessories
2. Test new Facebook content angle
3. Diversify brands (add Ugreen, Baseus)
4. Run A/B test: lifestyle vs comparison images
5. Goal: Break $500/week

Includes: Trend analysis, ROI by platform, product performance matrix,
caption success rates, posting time optimization, competitive benchmarks,
risk alerts, and 8 prioritized action items.

Full report: 300+ data points analyzed every Monday!
```

---

## 🎨 Image Generation Explained

### Two Scenarios

**Scenario 1: Product Image Available**
```
Amazon provides product photo
↓
Download image
↓
Image-to-Image AI (Fal.ai FLUX)
↓
Enhanced marketing image:
- Professional lighting
- Lifestyle context (desk/home)
- Subtle text overlay
- Brand colors
```

**Scenario 2: No Product Image**
```
Product title + description
↓
Text-to-Image AI (FLUX Pro)
↓
Generated marketing image:
- Product visualization
- Styled background
- Text overlays
- Call-to-action
```

### Supported AI Providers

**Fal.ai** (Recommended)
- Fast: 2-4 seconds/image
- Cost: $0.01/image
- Models: FLUX Pro, FLUX Dev, Stable Diffusion
- Best for: Image-to-image refinement

**Replicate**
- Flexible: Many models
- Cost: Pay-per-use
- Models: SDXL, Kandinsky, Flux
- Best for: Text-to-image generation

**RunPod** (Advanced)
- Cheapest: GPU hourly rates
- Setup: Requires API setup
- Best for: High-volume (100+ images/day)

---

## 🔧 Configuration

### Amazon Product Advertising API

**Get credentials:**
1. Sign up: https://affiliate-program.amazon.com
2. Register for Product Advertising API
3. Get: Access Key, Secret Key, Affiliate Tag

**Configure in `config.json`:**
```json
{
  "amazon": {
    "access_key": "YOUR_ACCESS_KEY",
    "secret_key": "YOUR_SECRET_KEY",
    "affiliate_tag": "yourname-20",
    "region": "us-east-1"
  }
}
```

### Postiz API

**Get API key:**
1. Sign up: https://postiz.com
2. Connect social accounts (Instagram, Twitter, etc.)
3. Get API key from Settings → Integrations

**Configure:**
```json
{
  "postiz": {
    "api_key": "YOUR_POSTIZ_KEY",
    "accounts": {
      "instagram": "connected",
      "twitter": "connected",
      "pinterest": "connected",
      "facebook": "connected"
    }
  }
}
```

### Image Generation

**Option A: Fal.ai (Recommended)**
```json
{
  "image_ai": {
    "provider": "fal",
    "api_key": "YOUR_FAL_KEY",
    "model": "fal-ai/flux-pro",
    "mode": "image-to-image"
  }
}
```

**Option B: Replicate**
```json
{
  "image_ai": {
    "provider": "replicate",
    "api_key": "YOUR_REPLICATE_KEY",
    "model": "stability-ai/sdxl",
    "mode": "text-to-image"
  }
}
```

---

## 💵 Pricing

**One-time purchase:** $49

**Why this price?**
- Complete automation (research + design + posting)
- Multi-platform reach (5+ channels)
- Production-ready (not just prompts)
- ROI in 30-60 days at $200/month target

**Cost breakdown (monthly):**
- Amazon API: Free
- Postiz: $19-39/month (unlimited posts)
- Image AI: $10-30/month (~300-1000 images)
- **Total:** ~$40/month infrastructure
- **Target revenue:** $200-500/month
- **Net profit:** $160-460/month

---

## 📊 Expected Results

| Timeline | Posts Created | Clicks | Revenue | Status |
|----------|---------------|--------|---------|--------|
| Week 1 | 21 (3/day × 7) | 50-150 | $5-20 | Learning phase |
| Week 4 | 84 posts | 400-800 | $50-120 | Optimization |
| Week 8 | 168 posts | 1200-2000 | $150-300 | Growth phase |
| Week 12 | 252 posts | 2000-3000 | $250-500 | Stable income |

**Key factors:**
- Niche matters (tech = high commissions)
- Platform mix (Pinterest often converts best)
- Consistency (daily posts compound)
- Product selection (trending > evergreen)

---

## 🎯 Niches That Work Best

### High-Commission Niches
1. **Tech Gadgets** (5-10% commission, $20-200 products)
   - Power banks, keyboards, monitors, cables
   
2. **Productivity Tools** (5-8% commission, $30-150)
   - Standing desks, ergonomic chairs, lighting

3. **Fitness Equipment** (4-8% commission, $40-300)
   - Resistance bands, yoga mats, smart scales

4. **Home Improvement** (3-5% commission, $50-500)
   - Smart home devices, tools, organizers

### Easy to Start (Low Competition)
- Phone accessories
- Desk organizers
- Travel gear
- Pet products

---

## 🛡️ Safety & Compliance

**Ricky follows all platform rules:**
- ✅ FTC disclosure (all posts include "#ad" or "affiliate link")
- ✅ Amazon TOS (proper link formatting, no cloaking)
- ✅ Platform limits (respects rate limits, no spam)
- ✅ Authentic content (no fake reviews, real value)

**Error handling:**
- API rate limit → Waits and retries
- Image generation fail → Falls back to product image only
- Post failed → Logs error, retries 3x
- Account suspended → Alerts you immediately

---

## 🐛 Troubleshooting

**"No products found"**
- Check Amazon API credentials
- Verify niche has products with >1000 reviews
- Try broader category

**"Image generation failed"**
- Check AI provider API key
- Verify credits/balance
- Switch to fallback provider

**"Posting failed"**
- Check Postiz account connections
- Verify social media accounts are still connected
- Check platform-specific limits

**"Low click-through rate"**
- Improve image quality (test different AI prompts)
- A/B test captions
- Try different posting times
- Focus on best-performing platform

---

## 📈 Optimization Tips

### Week 1-2: Learn
- Post consistently (3 products/day minimum)
- Track everything (which products, platforms, times work)
- Don't change strategy yet

### Week 3-4: Optimize
- Double down on best-performing products
- Focus on top-converting platform (likely Pinterest)
- Test different posting times
- Improve image prompts for AI

### Week 5-8: Scale
- Increase to 5 products/day
- Add more platforms (TikTok, Reddit)
- Build email list (offer free guide)
- Create comparison posts (vs alternatives)

### Week 9-12: Compound
- Expand niche (related categories)
- Create "best of" roundups
- Build brand presence
- Consider paid ads for top posts

---

## 🎓 Success Strategies

**1. Platform-Specific Content**
- Instagram: Lifestyle shots, stories with swipe-ups
- Pinterest: How-to angles, problem-solution
- Twitter: Quick tips, threads
- Facebook: Longer reviews, community posts

**2. Product Selection**
- New releases (less competition)
- Seasonal items (holidays, back-to-school)
- Bestsellers with reviews (trust factor)
- High-commission items (>5%)

**3. Content Variety**
- 60%: Single product promotions
- 20%: Product comparisons
- 10%: Listicles ("Top 5 gadgets...")
- 10%: Educational (how-to use products)

---

## 🚀 Advanced Features (Post-Launch)

**v2.0 Planned:**
- TikTok integration
- Video generation (product demos)
- Email list automation
- A/B testing framework
- Multi-niche support

---

## 📞 Support

**Included:**
- Complete setup guide
- API documentation
- Troubleshooting section
- Example configurations

**External:**
- Amazon API docs: https://webservices.amazon.com/paapi5/documentation/
- Postiz docs: https://docs.postiz.com
- Fal.ai docs: https://fal.ai/models

---

## 📜 License & Disclaimer

For educational purposes. Users responsible for:
- FTC disclosure compliance (affiliate links)
- Amazon Associates TOS
- Social media platform guidelines
- Image licensing (product photos)

Results vary by niche, effort, and market conditions. No guarantee of specific revenue.

---

## ✅ Ready to Launch?

**Buy → Setup (10 min) → Let Ricky run → Check revenue in 7 days**

*First commission usually arrives within 48-72 hours.* 🚀
