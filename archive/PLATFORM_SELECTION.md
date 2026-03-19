# Dynamic Platform Selection Guide

Ricky can post to any combination of platforms you choose. Change them anytime!

---

## 🎯 How It Works

### **Method 1: Configure in config.json (Persistent)**

Edit `config.json`:

```json
{
  "posting": {
    "platforms": ["instagram", "pinterest", "twitter"],
    "platform_priority": {
      "instagram": true,
      "twitter": true,
      "pinterest": true,
      "facebook": false,     // Disabled
      "linkedin": false,
      "tiktok": false,
      "reddit": false
    }
  }
}
```

**Result:** Ricky will ONLY post to Instagram, Pinterest, Twitter going forward.

---

### **Method 2: Specify Per Command (One-Time)**

Tell Ricky which platforms for a specific post:

**Examples:**

> "Ricky, post this product to Instagram and Pinterest only"

> "Post to Twitter only"

> "Create posts for Instagram, TikTok, and Pinterest"

> "Skip Facebook for this one"

**Result:** That specific post goes to your chosen platforms. Doesn't change config.

---

### **Method 3: Update Default Platforms (Permanent Change)**

> "Ricky, from now on only post to Instagram and Pinterest"

Ricky will:
1. Update `config.json` automatically
2. Disable other platforms
3. All future posts use new selection

---

## 📱 Supported Platforms (via Postiz API)

| Platform | Best For | Recommended? |
|----------|----------|--------------|
| **Instagram** | Visual products, lifestyle | ⭐⭐⭐⭐⭐ |
| **Pinterest** | SEO traffic, evergreen | ⭐⭐⭐⭐⭐ |
| **Twitter** | Quick engagement, threads | ⭐⭐⭐⭐ |
| **Facebook** | Community, longer posts | ⭐⭐⭐ |
| **LinkedIn** | Professional/B2B products | ⭐⭐⭐ |
| **TikTok** | Video demos (beta) | ⭐⭐ |
| **Reddit** | Niche communities (careful!) | ⭐⭐ |

---

## 🎨 Platform-Specific Content

Ricky automatically adapts content for each platform:

### **Instagram**
- **Format:** 1:1 square feed post + 9:16 story
- **Caption:** Emoji-heavy, storytelling, 150 words
- **Hashtags:** 8-10 relevant
- **Best time:** 9am EST

### **Pinterest**
- **Format:** 2:3 vertical pin (1000x1500px)
- **Caption:** 200-300 words, SEO keywords
- **Description:** How-to angle, problem-solution
- **Best time:** 2pm EST

### **Twitter**
- **Format:** Image + 3-4 tweet thread
- **Caption:** 280 chars, question hook
- **Hashtags:** 1-2 max
- **Best time:** 9am, 5pm EST

### **Facebook**
- **Format:** Image + longer post
- **Caption:** 200 words, value-focused
- **Tone:** Community, conversational
- **Best time:** 1pm EST

### **LinkedIn**
- **Format:** Professional angle
- **Caption:** Productivity/efficiency focus
- **Tone:** Formal, business-oriented
- **Best time:** 8am, 12pm EST

### **TikTok** (Beta)
- **Format:** 15-60 second video
- **Style:** Fast-paced, trending sounds
- **Best time:** 6pm EST

---

## 💡 Common Use Cases

### **Use Case 1: Just Starting Out**
"I only want Instagram and Pinterest"

```json
"platforms": ["instagram", "pinterest"]
```

**Why:** Focus on 2 high-ROI platforms, master them first

---

### **Use Case 2: Maximum Reach**
"Post everywhere!"

```json
"platforms": ["instagram", "twitter", "pinterest", "facebook", "linkedin"]
```

**Why:** Cast wide net, see what sticks

---

### **Use Case 3: Data-Driven Optimization**
"Pinterest converts best, focus there"

```json
"platforms": ["pinterest"],
"platform_priority": {
  "pinterest": true,
  "instagram": false,  // Pause others temporarily
  "twitter": false
}
```

**Why:** Double down on winner, scale what works

---

### **Use Case 4: Platform Testing**
"Add TikTok for 1 week, see if it works"

> "Ricky, add TikTok to posting schedule for 7 days"

Ricky:
1. Enables TikTok
2. Posts there for 7 days
3. Reports performance
4. You decide: keep or remove

---

### **Use Case 5: Time-Saving**
"I only have time for 2 platforms"

```json
"platforms": ["instagram", "pinterest"],
"frequency": "2_per_day"
```

**Why:** Quality > quantity, focus on best performers

---

## 🔄 Changing Platforms Mid-Campaign

### **Scenario: Facebook not performing**

**Week 4 report shows:**
```
Facebook: 52 clicks (6%), 2 sales (7%)
Instagram: 289 clicks (32%), 8 sales (29%)
Pinterest: 427 clicks (48%), 15 sales (54%)
```

**Action:**

> "Ricky, stop posting to Facebook. Focus on Instagram and Pinterest."

Ricky updates:
```json
"platforms": ["instagram", "pinterest"],
"platform_priority": {
  "facebook": false  // Disabled
}
```

**Result:** More focus on high-performers, no wasted effort

---

## 📊 Platform Performance Tracking

Ricky tracks each platform separately:

**Weekly report shows:**
```
Platform Performance:
1. Pinterest: 427 clicks, 15 sales, $167.40 commission ⭐⭐⭐⭐⭐
2. Instagram: 289 clicks, 8 sales, $112.60 commission ⭐⭐⭐⭐
3. Twitter: 124 clicks, 3 sales, $47.20 commission ⭐⭐⭐
4. Facebook: 52 clicks, 2 sales, $20.20 commission ⭐

Recommendation: Consider dropping Facebook (lowest ROI)
```

You can then say:
> "Ricky, remove Facebook from posting"

---

## 🎯 Smart Defaults

If you don't specify platforms, Ricky uses smart defaults based on your niche:

**Tech & Productivity:**
- Primary: Instagram, Pinterest
- Secondary: Twitter
- Skip: Facebook (poor tech engagement)

**Fitness & Health:**
- Primary: Instagram, Pinterest
- Secondary: TikTok, Facebook
- Skip: LinkedIn (not relevant)

**Home & Office:**
- Primary: Pinterest, Instagram
- Secondary: Facebook
- Skip: Twitter (less visual)

**B2B/Professional:**
- Primary: LinkedIn, Twitter
- Secondary: Instagram
- Skip: TikTok (not professional)

---

## ⚡ Quick Commands Reference

| Command | Result |
|---------|--------|
| "Post to Instagram only" | One-time Instagram post |
| "Use Instagram and Pinterest from now on" | Updates config permanently |
| "Add TikTok to the mix" | Enables TikTok posting |
| "Stop posting to Facebook" | Disables Facebook |
| "Post everywhere" | Enables all connected platforms |
| "What platforms am I using?" | Shows current active platforms |
| "Which platform performs best?" | Shows performance ranking |

---

## 🔧 Technical Details

### **How Ricky Determines Platforms:**

1. **Check command** - Did user specify platforms in this request?
2. **Check config** - What's in `posting.platforms`?
3. **Check priority** - Which platforms have `platform_priority: true`?
4. **Check connected** - Is account still connected in Postiz?

**Final list:** Intersection of all 4 checks

### **Example Logic:**
```python
# User says: "Post to Instagram and Pinterest"
requested = ["instagram", "pinterest"]

# Config says:
config_platforms = ["instagram", "twitter", "pinterest"]
priority = {"instagram": True, "pinterest": True, "twitter": False}

# Connected in Postiz:
connected = ["instagram", "pinterest", "twitter"]

# Result: Instagram + Pinterest
# (requested ∩ config ∩ priority ∩ connected)
final_platforms = ["instagram", "pinterest"]
```

---

## 💡 Best Practices

**Start Small:**
- Week 1-2: Master 2 platforms (Instagram + Pinterest)
- Week 3-4: Add 1 more if time allows
- Week 5+: Optimize based on data

**Data-Driven Decisions:**
- Check Week 4 report
- Keep top 2 platforms by ROI
- Drop bottom performer
- Test new platform quarterly

**Platform-Specific Content:**
- Let Ricky adapt content automatically
- Don't use same caption everywhere
- Trust the platform-specific optimization

**Time Management:**
- More platforms ≠ more revenue
- 2 platforms done well > 5 platforms half-assed
- Focus on quality, not quantity

---

## 🎉 Summary

✅ **Flexible:** Change platforms anytime  
✅ **Smart:** Adapts content per platform  
✅ **Data-Driven:** Tracks performance separately  
✅ **Easy:** Just tell Ricky what you want  

**Default recommendation:** Start with Instagram + Pinterest (highest ROI for affiliates)

---

**Ready to configure your platforms?**

1. Edit `config.json` → `posting.platforms`
2. Or just tell Ricky: "Only use Instagram and Pinterest"
3. Ricky handles the rest! 🚀
