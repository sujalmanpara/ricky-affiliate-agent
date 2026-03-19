# AI Image Generation Models - Configuration Guide

Ricky supports multiple AI providers and models. Choose what fits your budget and quality needs!

---

## 🎨 **Supported Providers**

### **Option 1: Fal.ai** (Recommended - Fast & Cheap)

**Models available:**
1. **FLUX Pro** (Best quality)
2. **FLUX Dev** (Good balance)
3. **FLUX Schnell** (Fastest)
4. **Stable Diffusion XL**
5. **Stable Diffusion 3**

**Pricing:**
- FLUX Pro: $0.03/image
- FLUX Dev: $0.01/image
- FLUX Schnell: $0.003/image
- SDXL: $0.01/image

**Speed:**
- FLUX Pro: 3-5 seconds
- FLUX Dev: 2-3 seconds
- FLUX Schnell: 1-2 seconds

**Best for:** Production use (fast + affordable)

---

### **Option 2: Replicate** (Flexible - Many Models)

**Models available:**
1. **FLUX Pro** (via black-forest-labs)
2. **SDXL** (stability-ai)
3. **Kandinsky 2.2**
4. **Playground v2.5**
5. **Proteus v0.2**

**Pricing:** $0.02-0.05/image (varies by model)

**Speed:** 5-15 seconds

**Best for:** Testing different models, specific needs

---

### **Option 3: Together AI** (Balance)

**Models available:**
1. **FLUX.1-schnell**
2. **SDXL**
3. **Stable Diffusion 2.1**

**Pricing:** $0.008-0.02/image

**Speed:** 2-5 seconds

**Best for:** Budget-conscious users

---

### **Option 4: Runpod** (Advanced - Cheapest at Scale)

**Models:** Any Stable Diffusion model
**Pricing:** GPU hourly ($0.20-0.80/hour)
**Speed:** 1-3 seconds per image

**Best for:** High volume (100+ images/day)

---

### **Option 5: Stability AI (Direct)**

**Models:**
1. **Stable Diffusion 3**
2. **SDXL Turbo**
3. **SD 1.6**

**Pricing:** $0.02-0.04/image

**Speed:** 3-6 seconds

**Best for:** Brand loyalty, specific SD needs

---

## 📝 **Configuration Options**

### **In config.json:**

```json
{
  "image_ai": {
    "provider": "fal",
    "primary_model": "fal-ai/flux-pro",
    "fallback_model": "fal-ai/flux-dev",
    "mode": "image-to-image",
    
    "models": {
      "flux_pro": {
        "provider": "fal",
        "model_id": "fal-ai/flux-pro",
        "cost_per_image": 0.03,
        "speed": "fast",
        "quality": "best"
      },
      "flux_dev": {
        "provider": "fal",
        "model_id": "fal-ai/flux-dev",
        "cost_per_image": 0.01,
        "speed": "very_fast",
        "quality": "good"
      },
      "flux_schnell": {
        "provider": "fal",
        "model_id": "fal-ai/flux-schnell",
        "cost_per_image": 0.003,
        "speed": "ultra_fast",
        "quality": "decent"
      },
      "sdxl": {
        "provider": "replicate",
        "model_id": "stability-ai/sdxl",
        "cost_per_image": 0.02,
        "speed": "medium",
        "quality": "excellent"
      }
    },
    
    "generation_settings": {
      "width": 1024,
      "height": 1024,
      "num_inference_steps": 30,
      "guidance_scale": 7.5,
      "seed": null,
      "negative_prompt": "low quality, blurry, watermark, text, logo"
    }
  }
}
```

---

## 🎯 **Model Selection Strategy**

### **Scenario 1: Best Quality (Recommended)**
```json
"primary_model": "fal-ai/flux-pro",
"fallback_model": "fal-ai/flux-dev"
```
**Cost:** $0.03/image  
**Speed:** 3-5 seconds  
**Use when:** Quality matters most (lifestyle, hero shots)

---

### **Scenario 2: Balanced (Budget-Friendly)**
```json
"primary_model": "fal-ai/flux-dev",
"fallback_model": "fal-ai/flux-schnell"
```
**Cost:** $0.01/image  
**Speed:** 2-3 seconds  
**Use when:** Good enough quality, lower cost

---

### **Scenario 3: Ultra Fast (High Volume)**
```json
"primary_model": "fal-ai/flux-schnell",
"fallback_model": "fal-ai/flux-dev"
```
**Cost:** $0.003/image  
**Speed:** 1-2 seconds  
**Use when:** Posting 10+ products/day, speed matters

---

### **Scenario 4: Testing Multiple Models**
```json
"models_to_test": ["flux_pro", "sdxl", "kandinsky"],
"test_mode": true
```
Ricky generates 1 image with each model, you pick winner.

---

## 🔧 **Advanced Settings**

### **Image-to-Image Settings**

```json
"image_to_image": {
  "strength": 0.7,
  "guidance_scale": 7.5,
  "num_inference_steps": 30,
  "seed": null
}
```

**Strength:** How much to change the original image
- `0.5` = Minor changes (keep original closely)
- `0.7` = Balanced (recommended)
- `0.9` = Major changes (almost new image)

**Guidance Scale:** How closely to follow prompt
- `5.0` = More creative/random
- `7.5` = Balanced (recommended)
- `10.0` = Very strict adherence

**Steps:** Quality vs speed tradeoff
- `20` = Fast but lower quality
- `30` = Balanced (recommended)
- `50` = Slower but highest quality

**Seed:** Reproducibility
- `null` = Random (different each time)
- `12345` = Fixed (same seed = same output)

---

### **Text-to-Image Settings**

```json
"text_to_image": {
  "width": 1024,
  "height": 1024,
  "guidance_scale": 7.5,
  "num_inference_steps": 30,
  "negative_prompt": "low quality, blurry, watermark, text",
  "seed": null
}
```

**Negative Prompt:** What to avoid
```
Common negatives:
- "low quality, blurry, pixelated"
- "watermark, text, logo, signature"
- "deformed, distorted, bad anatomy"
- "ugly, bad proportions, extra limbs"
```

---

## 💰 **Cost Comparison**

**Per 1000 images:**

| Model | Provider | Cost | Quality | Speed |
|-------|----------|------|---------|-------|
| FLUX Schnell | Fal.ai | $3 | Good | ⚡⚡⚡⚡⚡ |
| FLUX Dev | Fal.ai | $10 | Great | ⚡⚡⚡⚡ |
| FLUX Pro | Fal.ai | $30 | Excellent | ⚡⚡⚡⚡ |
| SDXL | Replicate | $20 | Excellent | ⚡⚡⚡ |
| SDXL | Together AI | $8 | Great | ⚡⚡⚡⚡ |
| SD 1.5 | Runpod | $5 | Good | ⚡⚡⚡⚡⚡ |

**Recommendation for different volumes:**

- **< 100 images/month:** FLUX Pro (best quality)
- **100-500 images/month:** FLUX Dev (balanced)
- **500-1000 images/month:** FLUX Schnell or Together AI
- **> 1000 images/month:** Runpod (cheapest at scale)

---

## 🎨 **Model Characteristics**

### **FLUX Pro**
**Best for:** Lifestyle images, realistic products, hero shots  
**Strengths:** Best realism, lighting, details  
**Weaknesses:** Most expensive  
**Example:** Product on modern desk with natural lighting

---

### **FLUX Dev**
**Best for:** General use, most product photos  
**Strengths:** Good balance of quality/speed/cost  
**Weaknesses:** Slightly less realistic than Pro  
**Example:** Product with styled background

---

### **FLUX Schnell**
**Best for:** High volume, simple products  
**Strengths:** Super fast, ultra cheap  
**Weaknesses:** Less detail, simpler compositions  
**Example:** Product on white background

---

### **SDXL (Stable Diffusion XL)**
**Best for:** Artistic styles, specific aesthetics  
**Strengths:** Highly customizable, many fine-tuned versions  
**Weaknesses:** Slower than FLUX  
**Example:** Cyberpunk-styled product shots

---

### **Kandinsky 2.2**
**Best for:** Unique artistic styles  
**Strengths:** Different aesthetic than FLUX/SD  
**Weaknesses:** Less realistic, more artistic  
**Example:** Illustrated product mockups

---

## 🔄 **Dynamic Model Selection**

Ricky can choose models dynamically based on context:

```python
def select_model(product_type, image_style, budget):
    """
    Smart model selection based on requirements
    """
    if budget == "unlimited" and image_style == "lifestyle":
        return "flux_pro"  # Best quality for hero shots
    
    elif budget == "tight" and volume > 500:
        return "flux_schnell"  # Cheap at scale
    
    elif product_type == "premium" and price > 100:
        return "flux_pro"  # Premium products deserve best images
    
    else:
        return "flux_dev"  # Default balanced choice
```

**User can override:**
> "Ricky, use FLUX Pro for this product only"
> "Switch to FLUX Schnell to save costs"
> "Try SDXL for more artistic images"

---

## 📊 **A/B Testing Models**

**Test multiple models to find your winner:**

```json
{
  "ab_testing": {
    "enabled": true,
    "models_to_compare": ["flux_pro", "flux_dev", "sdxl"],
    "test_duration_days": 7,
    "metric": "conversion_rate"
  }
}
```

**Ricky will:**
1. Generate images with all 3 models
2. Post them to platforms
3. Track which model's images convert best
4. Recommend winner after 7 days

**Example result:**
```
📊 A/B Test Results (7 days):

FLUX Pro: 3.4% conversion (23 sales from 679 clicks)
FLUX Dev: 3.1% conversion (19 sales from 612 clicks)
SDXL: 2.7% conversion (15 sales from 551 clicks)

Winner: FLUX Pro (12% higher conversion than Dev)
Recommendation: Use FLUX Pro for all future posts
Extra cost: $20/month, Extra revenue: $180/month
ROI: 900% ✅

Switch to FLUX Pro?
```

---

## 🎛️ **Per-Style Model Selection**

Different styles may work better with different models:

```json
{
  "style_model_mapping": {
    "minimalist": "flux_schnell",
    "lifestyle": "flux_pro",
    "hero": "flux_pro",
    "flat_lay": "flux_dev",
    "comparison": "sdxl"
  }
}
```

**Result:** Ricky uses best model for each style automatically!

---

## 🚀 **Setup Examples**

### **Example 1: Budget Setup**
```json
{
  "image_ai": {
    "provider": "together",
    "primary_model": "black-forest-labs/FLUX.1-schnell",
    "cost_per_image": 0.008,
    "generation_settings": {
      "num_inference_steps": 20,
      "guidance_scale": 7.0
    }
  }
}
```
**Monthly cost (300 images):** $2.40

---

### **Example 2: Quality Setup**
```json
{
  "image_ai": {
    "provider": "fal",
    "primary_model": "fal-ai/flux-pro",
    "fallback_model": "fal-ai/flux-dev",
    "cost_per_image": 0.03,
    "generation_settings": {
      "num_inference_steps": 40,
      "guidance_scale": 8.0
    }
  }
}
```
**Monthly cost (300 images):** $9

---

### **Example 3: Balanced Setup (Recommended)**
```json
{
  "image_ai": {
    "provider": "fal",
    "primary_model": "fal-ai/flux-dev",
    "fallback_model": "fal-ai/flux-schnell",
    "cost_per_image": 0.01,
    "generation_settings": {
      "num_inference_steps": 30,
      "guidance_scale": 7.5
    }
  }
}
```
**Monthly cost (300 images):** $3

---

## 🔧 **Model-Specific Prompts**

Different models need different prompt styles:

### **FLUX Models (Best Prompts)**
```
"Professional product photography of {product}, 
minimalist background, soft natural lighting, 
commercial style, high detail, 4k quality"
```

### **SDXL (More Descriptive)**
```
"High-resolution commercial photograph of {product}, 
placed on modern desk, natural window light from left, 
depth of field, bokeh background, professional studio quality, 
8k, photorealistic, trending on artstation"
```

### **Kandinsky (Artistic)**
```
"Artistic illustration of {product}, 
vibrant colors, modern aesthetic, 
digital art style, clean composition"
```

Ricky uses model-appropriate prompts automatically!

---

## ✅ **Quick Start Recommendations**

**For Beginners:**
- Start with: FLUX Dev (balanced)
- Provider: Fal.ai (easy, fast)
- Settings: Default (30 steps, 7.5 guidance)

**For Budget-Conscious:**
- Use: FLUX Schnell
- Provider: Together AI or Fal.ai
- Settings: 20 steps, 7.0 guidance

**For Quality-Focused:**
- Use: FLUX Pro
- Provider: Fal.ai
- Settings: 40 steps, 8.0 guidance

**For High Volume:**
- Use: Runpod with SD 1.5
- Provider: Runpod
- Settings: Optimized for speed

---

## 💡 **Tips & Tricks**

1. **Start with FLUX Dev** - Test for 2 weeks, see results
2. **A/B test models** - Don't assume, measure performance
3. **Different products, different models** - Premium products = FLUX Pro, budget products = Schnell
4. **Monitor costs** - Check monthly burn rate in weekly reports
5. **Use fallbacks** - If primary fails, fallback saves the day
6. **Adjust steps** - Lower steps = faster but lower quality
7. **Fixed seeds** - Use for consistent brand aesthetic
8. **Negative prompts** - Clean up unwanted artifacts

---

## 📞 **Get API Keys**

**Fal.ai:**
- Sign up: https://fal.ai
- Dashboard → API Keys
- Add credits (starts $10)

**Replicate:**
- Sign up: https://replicate.com
- Account → API Tokens
- Pay-per-use

**Together AI:**
- Sign up: https://api.together.xyz
- API Keys → Create
- $25 free credits

**Runpod:**
- Sign up: https://runpod.io
- Deploy → Serverless
- Configure model

---

## 🎯 **Summary**

**Best overall:** FLUX Dev (Fal.ai)  
**Cheapest:** FLUX Schnell (Together AI)  
**Highest quality:** FLUX Pro (Fal.ai)  
**Most flexible:** SDXL (Replicate)  
**High volume:** Runpod (any SD model)

**Default recommendation:** Start with FLUX Dev, optimize later based on data!

---

**Ready to configure?** Update `config.json` with your preferred model! 🎨
