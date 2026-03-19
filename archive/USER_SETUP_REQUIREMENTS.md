# Ricky Setup - What User Needs to Provide

## ✅ YES, USER MUST GIVE RICKY ACCESS!

Ricky can't do anything without user's credentials and permissions.

---

## 🔑 WHAT USER PROVIDES (One-Time Setup)

### 1. Amazon Associates Account ⭐ REQUIRED

**What user needs:**
- Sign up at https://affiliate.amazon.in/
- Get approved (usually 1-3 days)
- Get affiliate tag (e.g., `counitinguniq-21`)

**What user gives to Ricky:**
```json
{
  "amazon_affiliate_tag": "counitinguniq-21",
  "amazon_api_key": "YOUR_ACCESS_KEY",
  "amazon_api_secret": "YOUR_SECRET_KEY"
}
```

**Why Ricky needs this:**
- Search for trending products (Amazon Product API)
- Generate affiliate links with user's tag

---

### 2. Social Media Accounts ⭐ REQUIRED

**What user needs:**
- Twitter account (or create new)
- Instagram account (or create new)
- Pinterest account (or create new)

**What user gives to Ricky:**

**Option A: Via Postiz (Recommended)**
```json
{
  "postiz_api_key": "YOUR_POSTIZ_KEY",
  "postiz_workspace": "your-workspace-id",
  "connected_accounts": ["twitter", "instagram", "pinterest"]
}
```

User signs up at https://postiz.com/ and connects their social accounts there.

**Option B: Direct API Keys (Advanced)**
```json
{
  "twitter": {
    "api_key": "xxx",
    "api_secret": "xxx",
    "access_token": "xxx",
    "access_secret": "xxx"
  },
  "instagram": {
    "username": "your_username",
    "password": "your_password"  // Or App Password
  },
  "pinterest": {
    "access_token": "xxx"
  }
}
```

**Why Ricky needs this:**
- Post images and captions to user's accounts
- Schedule posts
- Track engagement

---

### 3. Fal.ai API Key ⭐ REQUIRED

**What user needs:**
- Sign up at https://fal.ai/
- Get API key from dashboard

**What user gives to Ricky:**
```json
{
  "fal_api_key": "YOUR_FAL_KEY"
}
```

**Why Ricky needs this:**
- Generate marketing images (Seedream img2img)
- Cost: ~$0.10 per image

---

### 4. Camoufox Access (Built-in) ✅ INCLUDED

**What user needs:**
- Nothing! Already running on the server

**What Ricky uses:**
```json
{
  "camoufox_token": "auto_from_/data/browser-server-token"
}
```

**Why Ricky needs this:**
- Extract product images from Amazon (fallback)
- Bypass bot detection

---

## 📋 COMPLETE SETUP FLOW

### Step 1: User Signs Up for Required Services

```
1. Amazon Associates
   → affiliate.amazon.in
   → Get affiliate tag
   → Request Product API access

2. Postiz (for social media)
   → postiz.com
   → Connect Twitter, Instagram, Pinterest
   → Get API key

3. Fal.ai (for image generation)
   → fal.ai
   → Get API key
   → Add $10 credit (enough for 100 images)
```

**Time:** 1-2 hours

---

### Step 2: User Configures Ricky

**Create config file:**

```yaml
# config.yaml
affiliate:
  tag: "counitinguniq-21"
  amazon_api_key: "AKIAXXXXX"
  amazon_api_secret: "xxxxx"

social_media:
  postiz_api_key: "xxxxx"
  postiz_workspace: "workspace-id"
  platforms:
    - twitter
    - instagram
    - pinterest

image_generation:
  fal_api_key: "xxxxx"
  model: "seedream-5-lite"
  
camoufox:
  enabled: true
  fallback_only: true

automation:
  posts_per_day: 3
  products_per_day: 3
  schedule:
    - "10:00"  # Morning
    - "14:00"  # Afternoon
    - "18:00"  # Evening
    
categories:
  - "Electronics"
  - "Home & Kitchen"
  - "Fashion"
  
price_range:
  min: 500
  max: 5000
```

**Time:** 10 minutes

---

### Step 3: Ricky Validates Configuration

```python
# Ricky checks everything
ricky.validate_setup()

# Output:
✅ Amazon Associates: Connected (tag: counitinguniq-21)
✅ Amazon Product API: Valid credentials
✅ Postiz: Connected (3 accounts)
   ✅ Twitter: @your_handle
   ✅ Instagram: @your_handle
   ✅ Pinterest: @your_handle
✅ Fal.ai: Valid API key (Balance: $10.00)
✅ Camoufox: Running on port 9222

🎉 Setup complete! Ready to run.
```

---

### Step 4: User Starts Ricky

```bash
# Start Ricky agent
openclaw run ricky-affiliate-agent

# Or schedule it
openclaw cron add --schedule "daily 9am" --task "run ricky daily automation"
```

**That's it!** Ricky runs automatically from now on.

---

## 🔐 SECURITY & PERMISSIONS

### What Ricky CAN Do (With Permissions):

✅ **Read:** Search Amazon products (API)  
✅ **Create:** Generate affiliate links (your tag)  
✅ **Generate:** Create marketing images (Fal.ai)  
✅ **Post:** Publish to your social media (Postiz/APIs)  
✅ **Track:** Log what was posted (local database)  

### What Ricky CANNOT Do:

❌ **Access Amazon earnings** (no API for that)  
❌ **Change your passwords**  
❌ **Transfer money**  
❌ **Delete your accounts**  
❌ **Post without your consent** (you control config)  

---

## 🛡️ SAFETY MEASURES

### 1. API Key Storage
```
Config file: ~/.ricky/config.yaml
Permissions: 600 (only you can read)
Encrypted: Optional (user's choice)
```

### 2. Rate Limiting
```python
# Ricky respects limits
amazon_api_calls: 6/minute (within free tier)
social_posts: 3/day per platform (natural pace)
image_generation: On-demand (cost-conscious)
```

### 3. Review Mode (Optional)
```yaml
automation:
  review_before_post: true  # User approves each post
  # Or
  review_before_post: false  # Fully automated
```

---

## 📱 TYPICAL USER SETUP TIME

### Total Time Breakdown:

| Task | Time | Difficulty |
|------|------|------------|
| Amazon Associates signup | 30 min | Easy |
| Amazon Product API access | 15 min | Medium |
| Postiz signup + connect accounts | 20 min | Easy |
| Fal.ai signup + API key | 5 min | Easy |
| Configure Ricky | 10 min | Easy |
| Test & validate | 10 min | Easy |
| **TOTAL** | **90 min** | **Easy** |

**One afternoon = Fully automated affiliate marketing system!**

---

## 🎯 WHAT USER DOES AFTER SETUP

### Daily: NOTHING! ✅
- Ricky finds products
- Ricky generates images
- Ricky posts to social media
- All automatic

### Weekly (Optional): 5 minutes
- Check Amazon Associates dashboard (see earnings)
- Review Ricky's performance report
- Adjust config if needed (categories, price range)

### Monthly: 10 minutes
- Check earnings
- Get paid by Amazon
- Celebrate! 🎉

---

## 💡 MINIMUM REQUIREMENTS

### To Use Ricky:

**Must Have:**
1. ✅ Amazon Associates account (free)
2. ✅ At least ONE social media account (free)
3. ✅ Fal.ai account with $10 credit ($10)
4. ✅ OpenClaw with Ricky installed (free)

**Optional:**
5. Postiz (easier social posting) - $19/month
6. More social accounts (more reach)
7. Existing followers (helps, but not required)

**Total startup cost:** $10-30

---

## 🚀 ALTERNATIVE: POSTIZ-FREE SETUP

If user doesn't want to pay for Postiz:

**Direct API Setup:**

```yaml
social_media:
  twitter:
    api_key: "xxx"
    api_secret: "xxx"
    access_token: "xxx"
    access_secret: "xxx"
  
  instagram:
    # Use Instagram Graph API (free for creators)
    access_token: "xxx"
  
  pinterest:
    access_token: "xxx"
```

**Cost:** $0 (just API setup time)  
**Complexity:** Higher (need to setup each API)  

---

## ✅ FINAL CHECKLIST

Before user can earn money with Ricky:

- [ ] Amazon Associates account created
- [ ] Affiliate tag obtained (e.g., counitinguniq-21)
- [ ] Amazon Product API access granted
- [ ] Social media accounts created/connected
- [ ] Postiz OR direct API keys configured
- [ ] Fal.ai account with API key
- [ ] Ricky config.yaml created
- [ ] Setup validated (all green checks)
- [ ] First test post successful
- [ ] Automation started

**When all checkboxes are ticked:** Money machine activated! 💰

---

## 🎯 SUMMARY

**Q: Does user have to login and give Ricky something?**  
**A: YES! User provides:**

1. **Amazon affiliate tag** (so Ricky can earn for them)
2. **Amazon API keys** (so Ricky can find products)
3. **Social media access** (so Ricky can post for them)
4. **Fal.ai API key** (so Ricky can generate images)

**Without these:** Ricky can't do anything!  
**With these:** Ricky runs fully automated! 🚀

---

**Setup is ONE-TIME, ~90 minutes, then passive income forever!**
