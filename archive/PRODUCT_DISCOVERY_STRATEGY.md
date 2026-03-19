# Product Discovery Strategy - The Right Way

## ✅ THE BETTER APPROACH

**Use Amazon Product Advertising API for product discovery**  
**Use Camoufox ONLY for image extraction**

---

## 🎯 WHY THIS IS BETTER

### Amazon Product Advertising API
✅ **Official, reliable** - No breaking when Amazon changes UI  
✅ **Fast** - API responses vs browser automation  
✅ **Rich data** - Commission rates, trending status, ratings  
✅ **Legal & safe** - TOS-compliant  
✅ **Scalable** - Handle 1000s of products  

### Camoufox (Only for images)
✅ **Single purpose** - Get product image when needed  
✅ **Bypass bot detection** - For image extraction only  
✅ **Simple, focused** - One job, done well  

---

## 📋 REVISED WORKFLOW

### Step 1: Product Discovery (Amazon API) ⭐
```python
# Use Amazon Product Advertising API
products = amazon_api.search_items(
    keywords="trending electronics",
    min_price=500,
    max_price=5000,
    min_rating=3.5,
    sort_by="Relevance",
    resources=[
        "ItemInfo.Title",
        "ItemInfo.Features",
        "Offers.Listings.Price",
        "Images.Primary.Large",
        "ItemInfo.ProductInfo",
        "BrowseNodeInfo.BrowseNodes"
    ]
)
```

**Returns:**
```json
{
  "ASIN": "B0FN87F535",
  "Title": "Zebronics Wireless Keyboard & Mouse",
  "Price": {
    "Amount": 749,
    "Currency": "INR"
  },
  "Images": {
    "Primary": {
      "Large": {
        "URL": "https://m.media-amazon.com/images/I/61qM7Ie7KyL.jpg",
        "Height": 741,
        "Width": 317
      }
    }
  },
  "Features": [
    "Wireless 2.4GHz connectivity",
    "UV-Printed keys",
    "Retractable USB receiver"
  ],
  "Rating": 4.0,
  "ReviewCount": 1234
}
```

✅ **Everything we need!** Including image URL!

---

### Step 2: Image Extraction (Optional Fallback)

**IF Amazon API provides image URL:**
- ✅ Use it directly! (No Camoufox needed)

**IF image URL doesn't work / not available:**
- Use Camoufox as fallback:
```python
if not image_url or not url_accessible(image_url):
    # Fallback: Camoufox screenshot
    image_url = camoufox_extract_image(product_url)
```

---

## 🔧 PRODUCTION CODE

```python
class ProductDiscovery:
    def __init__(self, amazon_api_key, camoufox_token):
        self.amazon_api = AmazonProductAPI(amazon_api_key)
        self.camoufox = CamoufoxClient(camoufox_token)
    
    def discover_trending_products(self, category="Electronics", limit=10):
        """
        Find trending products using Amazon API
        """
        # Search using official API
        results = self.amazon_api.search_items(
            keywords=f"best selling {category}",
            search_index=category,
            min_price=500,
            max_price=5000,
            min_rating=3.5,
            sort_by="Featured",
            item_count=limit
        )
        
        products = []
        for item in results:
            # Extract from API response
            product = {
                'asin': item['ASIN'],
                'title': item['ItemInfo']['Title']['DisplayValue'],
                'price': item['Offers']['Listings'][0]['Price']['Amount'],
                'currency': 'INR',
                'rating': item['ItemInfo']['ContentRating']['AudienceRating']['DisplayValue'],
                'image_url': item['Images']['Primary']['Large']['URL'],
                'features': item['ItemInfo']['Features']['DisplayValues'],
                'url': f"https://amazon.in/dp/{item['ASIN']}/"
            }
            
            products.append(product)
        
        return products
    
    def get_product_image(self, product):
        """
        Get product image - try API first, Camoufox fallback
        """
        # Try API image first
        if product.get('image_url'):
            try:
                # Verify URL works
                response = requests.head(product['image_url'], timeout=5)
                if response.status_code == 200:
                    return product['image_url']
            except:
                pass
        
        # Fallback: Extract with Camoufox
        print(f"API image failed, using Camoufox for {product['asin']}")
        return self.camoufox.extract_product_image(product['url'])
    
    def select_best_products(self, products, count=3):
        """
        Filter and rank products by potential earnings
        """
        # Score each product
        scored = []
        for p in products:
            score = self.calculate_score(p)
            scored.append((score, p))
        
        # Sort by score
        scored.sort(reverse=True)
        
        # Return top N
        return [p for score, p in scored[:count]]
    
    def calculate_score(self, product):
        """
        Score product based on multiple factors
        """
        score = 0
        
        # Price factor (sweet spot: ₹1000-₹3000)
        price = product['price']
        if 1000 <= price <= 3000:
            score += 50
        elif 500 <= price <= 5000:
            score += 30
        
        # Rating factor
        rating = float(product['rating'])
        score += rating * 10
        
        # Review count (proxy for popularity)
        # reviews = product.get('review_count', 0)
        # score += min(reviews / 100, 30)
        
        # Category factor (higher commission categories)
        category = product.get('category', '')
        if 'Fashion' in category:
            score += 20  # 6-8% commission
        elif 'Home' in category:
            score += 15  # 3-5% commission
        elif 'Electronics' in category:
            score += 10  # 2-3% commission
        
        return score

# Usage
discovery = ProductDiscovery(
    amazon_api_key="YOUR_API_KEY",
    camoufox_token="YOUR_TOKEN"
)

# Discover products
all_products = discovery.discover_trending_products(
    category="Electronics",
    limit=20
)

# Select best 3
best_products = discovery.select_best_products(all_products, count=3)

# For each product
for product in best_products:
    # Get image (API or Camoufox fallback)
    image_url = discovery.get_product_image(product)
    
    # Generate marketing images
    marketing_images = generate_marketing_images(image_url)
    
    # Post to social media
    post_to_social(product, marketing_images)
```

---

## 🔑 AMAZON PRODUCT ADVERTISING API

### How to Get Access:

1. **Sign up:** https://affiliate.amazon.in/
2. **Create account** (you already have: counitinguniq-21)
3. **Request API access:** https://webservices.amazon.in/
4. **Get credentials:**
   - Access Key
   - Secret Key
   - Associate Tag (counitinguniq-21)

### Requirements:
- Amazon Associates account (✅ you have)
- API approval (usually instant for approved affiliates)
- 3 sales in 180 days (to maintain access)

### Free tier:
- 8,640 requests/day (6 requests/minute)
- More than enough for Ricky!

---

## 📊 API vs Camoufox Comparison

| Task | Best Tool | Why |
|------|-----------|-----|
| **Product search** | API ⭐ | Fast, reliable, structured data |
| **Product details** | API ⭐ | Complete data with one call |
| **Image URL** | API ⭐ | Provided in response |
| **Image download** | Direct ⭐ | Use URL from API |
| **Image fallback** | Camoufox | When API URL fails/blocked |
| **Login** | ❌ Neither | Not needed with API! |

---

## ✅ FINAL ARCHITECTURE

```
┌─────────────────────────────────────────┐
│ Amazon Product Advertising API         │
│ - Search trending products              │
│ - Get product details                   │
│ - Get image URLs                        │
│ - Get ratings, reviews, prices          │
└─────────────────────────────────────────┘
                ↓
         (Image URL)
                ↓
┌─────────────────────────────────────────┐
│ TRY: Direct download from API URL       │
└─────────────────────────────────────────┘
                ↓
         (If fails)
                ↓
┌─────────────────────────────────────────┐
│ FALLBACK: Camoufox screenshot           │
│ - Navigate to product page              │
│ - Extract image                         │
│ - Return image data                     │
└─────────────────────────────────────────┘
                ↓
         (Product Image)
                ↓
┌─────────────────────────────────────────┐
│ Seedream 5.0 img2img                    │
│ - Generate 3 marketing images           │
└─────────────────────────────────────────┘
```

**Clean, simple, reliable!**

---

## 🚀 IMPLEMENTATION STEPS

### 1. Get Amazon API Access (1-2 hours)
- Sign up / request access
- Get credentials
- Test basic search

### 2. Build Product Discovery (2-3 hours)
- Implement search function
- Parse API responses
- Filter & rank products

### 3. Build Image Extraction (1 hour)
- Try API URL first
- Camoufox fallback
- Return usable image URL

### 4. Integration (1 hour)
- Connect to img2img pipeline
- Test end-to-end
- Handle errors

**Total: 5-7 hours**

---

## 🎯 ADVANTAGES OF THIS APPROACH

✅ **Official & Legal** - Using Amazon's official API  
✅ **Fast** - No browser automation for discovery  
✅ **Reliable** - API doesn't break like web scraping  
✅ **Rich Data** - Complete product information  
✅ **Scalable** - Can handle 1000s of products  
✅ **Simple** - Camoufox only when needed  
✅ **Cost-effective** - Free API tier sufficient  

---

## 💡 BEST OF BOTH WORLDS

**Amazon API:** Product discovery, data extraction ⭐  
**Camoufox:** Image fallback, screenshot when needed ⭐  

**Result:** Reliable automation with fallback safety!

---

## 🎯 NEXT STEP

**Get Amazon Product Advertising API access!**

1. Request access: https://webservices.amazon.in/
2. Get credentials (Access Key, Secret Key)
3. Test with sample search
4. Build product discovery module

**Time:** 1-2 hours for API setup  
**Then:** Build discovery module (2-3 hours)

**Ready to get API access?** 🚀
