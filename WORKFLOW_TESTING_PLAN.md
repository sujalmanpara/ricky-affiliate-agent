# Ricky Agent - Complete Workflow Testing Plan

## ✅ COMPLETED PARTS

### 1. Image Generation (DONE ✅)
- ✅ Camoufox extracts product image from Amazon
- ✅ Seedream 5.0 img2img generates marketing images
- ✅ 3 platform formats (16:9, 1:1, 2:3)
- ✅ 10/10 product accuracy
- ✅ ~55s per product

**Status:** Production-ready, tested with Samsung refrigerator

---

## 🔄 REMAINING WORKFLOW PARTS TO TEST

### 2. Product Research (NEXT ⏭️)
**Goal:** Find trending/profitable Amazon India products

**What to test:**
- [ ] Amazon Product Advertising API integration
- [ ] OR: Manual product selection (simpler for v1.0)
- [ ] Extract product details (title, price, features, rating)
- [ ] Generate affiliate link with tag `counitinguniq-21`

**Test case:**
```python
# Input: Product category or manual URL
product = research_product("electronics", "under_1000")

# Output:
{
    'title': 'Zebronics Wireless Keyboard & Mouse',
    'price': '₹749',
    'original_price': '₹1,499',
    'discount': '50%',
    'rating': '4.0',
    'url': 'https://amazon.in/dp/B0FN87F535/',
    'affiliate_url': 'https://amazon.in/dp/B0FN87F535/?tag=counitinguniq-21',
    'features': ['Wireless', 'UV-Printed', '2.4GHz']
}
```

---

### 3. Caption Generation (TODO 📝)
**Goal:** Create platform-optimized captions

**What to test:**
- [ ] Twitter caption (280 chars, casual, CTA)
- [ ] Instagram caption (2200 chars, hashtags, story)
- [ ] Pinterest caption (500 chars, SEO-focused)
- [ ] Include FTC disclosure (#ad, "affiliate link")
- [ ] Price & discount mention
- [ ] Call-to-action

**Test case:**
```python
# Input: Product data
captions = generate_captions(product_data)

# Output:
{
    'twitter': "Still using that old keyboard? 🖱️\n\nUpgraded to this Zebronics wireless combo. ₹749.\nNo more cable mess...",
    'instagram': "Desk setup upgrade complete ✨\n\nGot this wireless keyboard & mouse...",
    'pinterest': "Best Wireless Keyboard Under ₹1000 in 2026\n\nZebronics Companion 304..."
}
```

---

### 4. Social Media Posting (TODO 🚀)
**Goal:** Post to Instagram, Twitter, Pinterest via Postiz API

**What to test:**
- [ ] Postiz API authentication
- [ ] Upload images to platforms
- [ ] Post with captions
- [ ] Schedule posts (or post immediately)
- [ ] Handle rate limits
- [ ] Error handling (API failures, auth issues)

**Test case:**
```python
# Input: Images + captions + platforms
result = post_to_social({
    'twitter': {'image': twitter_url, 'caption': twitter_caption},
    'instagram': {'image': ig_url, 'caption': ig_caption},
    'pinterest': {'image': pin_url, 'caption': pin_caption}
})

# Output:
{
    'twitter': {'status': 'posted', 'post_id': '123456', 'url': 'https://twitter.com/...'},
    'instagram': {'status': 'posted', 'post_id': '789012'},
    'pinterest': {'status': 'posted', 'pin_id': '345678'}
}
```

---

### 5. Performance Tracking (TODO 📊)
**Goal:** Track clicks, conversions, revenue

**What to test:**
- [ ] Store posted products in database/JSON
- [ ] Track affiliate link clicks (Amazon reports)
- [ ] Calculate revenue (Amazon Associates dashboard)
- [ ] Generate daily/weekly reports

**Test case:**
```python
# Track product post
track_post({
    'product': product_data,
    'images': generated_images,
    'platforms': ['twitter', 'instagram', 'pinterest'],
    'timestamp': '2026-03-18 06:54 UTC'
})

# Generate report
report = generate_report(period='week')

# Output:
{
    'products_posted': 21,
    'platforms': {'twitter': 21, 'instagram': 21, 'pinterest': 21},
    'estimated_clicks': 450,
    'estimated_revenue': '₹3,600',
    'top_product': 'Zebronics Keyboard'
}
```

---

### 6. Weekly Analysis (TODO 📈)
**Goal:** Comprehensive performance analysis

**What to test:**
- [ ] Aggregate data from tracking
- [ ] Platform performance comparison
- [ ] Product category analysis
- [ ] Revenue breakdown
- [ ] Recommendations for next week

**Test case:**
```python
# Generate weekly analysis
analysis = generate_weekly_analysis()

# Output: 9 sections (like MoneyPrinterV2)
1. Executive Summary
2. Revenue & Conversion Metrics
3. Platform Performance
4. Product Category Analysis
5. Top Performing Products
6. Engagement Metrics
7. Growth Trends
8. Issues & Challenges
9. Recommendations
```

---

## 🎯 TESTING PRIORITY

### Phase 1: Core Workflow (This Week)
1. ✅ Image Generation (DONE)
2. ⏭️ Product Research (NEXT - 2-3 hours)
3. 📝 Caption Generation (2 hours)
4. 🚀 Social Media Posting (3-4 hours)

**Goal:** End-to-end workflow working (manual product input → automated posting)

### Phase 2: Automation (Next Week)
5. 📊 Performance Tracking (2-3 hours)
6. 📈 Weekly Analysis (2-3 hours)

**Goal:** Full automation with reporting

---

## 🧪 TESTING APPROACH

### For Each Part:

1. **Write test script** (`test_<part>.py`)
2. **Test with real data** (actual Amazon products)
3. **Handle errors** (API failures, rate limits)
4. **Document results** (success/failure, timing, cost)
5. **Integrate into Ricky** (update SKILL.md)

### Test Products:
- Zebronics Keyboard (₹749) - Electronics
- Samsung Refrigerator (₹18,990) - Home appliances
- Anker Power Bank (₹2,999) - Mobile accessories

---

## 📋 NEXT IMMEDIATE STEPS

### Step 2: Product Research
**Options:**

**A) Manual (Simpler for v1.0):**
```python
# User provides Amazon URL
product = extract_product_data(
    "https://amazon.in/dp/B0FN87F535/"
)
```
- ✅ Simple, reliable
- ✅ No API needed
- ⚠️ Manual product selection

**B) Automated (Better for v2.0):**
```python
# Agent finds trending products
products = amazon_api.search(
    category="electronics",
    price_range="500-1500",
    rating_min=3.5,
    limit=10
)
```
- ✅ Full automation
- ⚠️ Requires Amazon Product API
- ⚠️ More complex

**Recommendation:** Start with A (manual) for v1.0, add B later

---

## 🎯 TODAY'S GOAL

Test & implement **Product Research (Manual)**:

1. User provides Amazon URL
2. Camoufox extracts product data
3. Generate affiliate link
4. Output: Complete product object

**Time:** 2-3 hours  
**Output:** Working product extraction + affiliate link generation

**Then move to Caption Generation!**

---

## 📊 COMPLETION STATUS

| Part | Status | Time Est. | Actual |
|------|--------|-----------|--------|
| 1. Image Generation | ✅ DONE | 4-6h | ~6h |
| 2. Product Research | ⏭️ NEXT | 2-3h | - |
| 3. Caption Generation | 📝 TODO | 2h | - |
| 4. Social Posting | 🚀 TODO | 3-4h | - |
| 5. Tracking | 📊 TODO | 2-3h | - |
| 6. Analysis | 📈 TODO | 2-3h | - |
| **TOTAL** | **17% done** | **15-21h** | **~6h** |

**Estimated completion:** 2-3 days (if we work 6-8h/day)

---

## 🚀 LET'S TEST PRODUCT RESEARCH NEXT!

Ready to build the product extraction + affiliate link generator? 🎯
