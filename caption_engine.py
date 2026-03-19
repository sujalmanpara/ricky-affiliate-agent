"""
RICKY CAPTION ENGINE — Platform-Specific Captions & Hashtags

Generates optimized captions for each platform:
  - Twitter/X: Short, punchy, 280 chars, 3-5 hashtags
  - Instagram: Storytelling, emoji-rich, 30 hashtags (3-tier strategy)
  - Pinterest: SEO-optimized title + description, keyword-rich
"""


# ─── HASHTAG STRATEGY ───────────────────────────────────────

CATEGORY_HASHTAGS = {
    'camera': {
        'broad': ['#photography', '#camera', '#tech', '#gadgets', '#contentcreator'],
        'mid': ['#vlogging', '#cameragear', '#photogear', '#videography', '#filmmaking'],
        'niche': ['#camerasetup', '#vlogcamera', '#techreview', '#camerarecommendation', '#budgetcamera'],
    },
    'earbuds': {
        'broad': ['#earbuds', '#music', '#tech', '#audio', '#wireless'],
        'mid': ['#tws', '#bluetooth', '#gaming', '#earphones', '#bassboost'],
        'niche': ['#wirelessearbuds', '#budgetearbuds', '#gamingearbuds', '#audiophile', '#earbудс'],
    },
    'phone': {
        'broad': ['#smartphone', '#mobile', '#tech', '#gadgets', '#phone'],
        'mid': ['#android', '#iphone', '#newphone', '#phonedeals', '#mobilephotography'],
        'niche': ['#phoneunboxing', '#budgetphone', '#phonereview', '#smartphonedeals', '#bestphone'],
    },
    'beauty': {
        'broad': ['#skincare', '#beauty', '#selfcare', '#glowingskin', '#beautytips'],
        'mid': ['#skincareroutine', '#facewash', '#cleanbeauty', '#healthyskin', '#beautyhacks'],
        'niche': ['#skincareproducts', '#affordableskincare', '#indianskincare', '#skincareaddict', '#beautyfinds'],
    },
    'fashion_clothing': {
        'broad': ['#fashion', '#style', '#ootd', '#clothing', '#trending'],
        'mid': ['#mensfashion', '#womensfashion', '#streetstyle', '#fashioninspo', '#outfitideas'],
        'niche': ['#affordablefashion', '#fashionfinds', '#styleinspo', '#fashiondeals', '#wardrobeessentials'],
    },
    'fashion_shoes': {
        'broad': ['#shoes', '#sneakers', '#fashion', '#footwear', '#style'],
        'mid': ['#sneakerhead', '#runningshoes', '#shoestyle', '#kicks', '#shoesoftheday'],
        'niche': ['#budgetsneakers', '#shoefinds', '#sneakerdeals', '#comfortshoes', '#shoereview'],
    },
    'appliance': {
        'broad': ['#home', '#kitchen', '#appliances', '#homedecor', '#interiordesign'],
        'mid': ['#homeappliances', '#kitchenappliances', '#smartkitchen', '#homeupgrade', '#modernhome'],
        'niche': ['#appliancereview', '#kitchenessentials', '#homedeals', '#energyefficient', '#homehacks'],
    },
    'kitchen': {
        'broad': ['#kitchen', '#cooking', '#food', '#homecooking', '#chef'],
        'mid': ['#kitchenware', '#cookware', '#homechef', '#foodie', '#kitchentools'],
        'niche': ['#kitchenessentials', '#cookingtools', '#budgetkitchen', '#kitchenfinds', '#mealprep'],
    },
    'fitness': {
        'broad': ['#fitness', '#gym', '#health', '#workout', '#bodybuilding'],
        'mid': ['#protein', '#supplement', '#gymlife', '#fitnessmotivation', '#gains'],
        'niche': ['#wheyprotein', '#gymsupplement', '#fitnessdeals', '#proteinshake', '#musclebuilding'],
    },
    'helmet': {
        'broad': ['#motorcycle', '#bikelife', '#riding', '#safety', '#biker'],
        'mid': ['#helmet', '#ridersafety', '#bikerlife', '#motorcyclegear', '#twowheel'],
        'niche': ['#helmetreview', '#budgethelmet', '#ridinggear', '#ISIhelmet', '#bikeaccessories'],
    },
    'laptop': {
        'broad': ['#laptop', '#tech', '#computer', '#productivity', '#workfromhome'],
        'mid': ['#gaming', '#programming', '#coding', '#techreview', '#bestlaptop'],
        'niche': ['#budgetlaptop', '#laptopreview', '#studentlaptop', '#laptopdeals', '#worksetup'],
    },
    'generic': {
        'broad': ['#deals', '#shopping', '#amazon', '#bestdeals', '#trending'],
        'mid': ['#amazonfinds', '#onlineshopping', '#musthave', '#recommendations', '#review'],
        'niche': ['#affordableproducts', '#productreview', '#dailydeals', '#smartshopping', '#bestbuy'],
    },
}

UNIVERSAL_HASHTAGS = ['#amazonfinds', '#deals', '#ad']


def get_hashtags(category: str, platform: str) -> list:
    """Get platform-appropriate hashtags."""
    cats = CATEGORY_HASHTAGS.get(category, CATEGORY_HASHTAGS['generic'])
    
    if platform == 'twitter':
        # Twitter: 3-5 hashtags max
        return cats['broad'][:2] + cats['niche'][:1] + ['#ad', '#deals']
    
    elif platform == 'instagram':
        # Instagram: 20-30 hashtags (3-tier)
        return cats['broad'] + cats['mid'] + cats['niche'] + UNIVERSAL_HASHTAGS
    
    elif platform == 'pinterest':
        # Pinterest: SEO keywords, not traditional hashtags
        return cats['broad'][:3] + cats['mid'][:2]
    
    return cats['broad'][:5]


# ─── CAPTION TEMPLATES ──────────────────────────────────────

def generate_twitter_caption(product: dict, category: str) -> str:
    """Short, punchy Twitter caption with 4 images."""
    title = product['title'][:60]
    price = product.get('price', '')
    discount = product.get('discount', '')
    asin = product.get('asin', '')
    tag = product.get('affiliate_tag', 'counitinguniq-21')
    
    # Key feature from bullets
    feature = ''
    bullets = product.get('bullets', [])
    if bullets:
        feature = bullets[0][:50]
    
    hashtags = ' '.join(get_hashtags(category, 'twitter'))
    
    link = f"https://www.amazon.in/dp/{asin}?tag={tag}" if asin else ''
    
    caption = f"🔥 {title}\n\n"
    if price:
        caption += f"💰 ₹{price}"
    if discount:
        caption += f" ({discount})"
    caption += "\n"
    if feature:
        caption += f"✅ {feature}\n"
    caption += f"\n🔗 {link}\n\n{hashtags}"
    
    # Twitter 280 char limit — truncate if needed
    if len(caption) > 280:
        # Remove some hashtags
        hashtags_short = ' '.join(get_hashtags(category, 'twitter')[:3])
        caption = f"🔥 {title[:50]}\n💰 ₹{price} {discount}\n\n🔗 {link}\n\n{hashtags_short}"
    
    return caption


def generate_instagram_caption(product: dict, category: str) -> str:
    """Storytelling Instagram caption with hashtag strategy."""
    title = product['title'][:60]
    price = product.get('price', '')
    discount = product.get('discount', '')
    asin = product.get('asin', '')
    tag = product.get('affiliate_tag', 'counitinguniq-21')
    rating = product.get('rating', '')
    reviews = product.get('reviews', '')
    bullets = product.get('bullets', [])
    
    # Category-specific hooks
    hooks = {
        'camera': "📸 Your content creation game is about to change!",
        'earbuds': "🎧 Sound that hits different!",
        'phone': "📱 Your next phone upgrade is here!",
        'beauty': "✨ Glow-up alert! Your skin deserves this.",
        'fashion_clothing': "👗 Style upgrade incoming!",
        'fashion_shoes': "👟 Step into something amazing!",
        'appliance': "🏠 Home upgrade that changes everything!",
        'kitchen': "🍳 Cook like a pro with this!",
        'fitness': "💪 Level up your fitness game!",
        'helmet': "🏍️ Ride safe, ride in style!",
        'laptop': "💻 Power meets portability!",
    }
    
    hook = hooks.get(category, "🔥 Found something amazing!")
    
    caption = f"{hook}\n\n"
    caption += f"📦 {title}\n\n"
    
    if bullets:
        caption += "What makes it special:\n"
        for b in bullets[:4]:
            caption += f"✅ {b[:60]}\n"
        caption += "\n"
    
    if price:
        caption += f"💰 Price: ₹{price}"
        if discount:
            caption += f" ({discount} OFF!)"
        caption += "\n"
    
    if rating:
        caption += f"⭐ {rating}"
        if reviews:
            caption += f" {reviews}"
        caption += "\n"
    
    caption += "\n🔗 Link in bio! Comment 'LINK' and I'll DM you directly.\n"
    caption += "\n📌 Save this post for later!\n"
    caption += "\n.\n.\n.\n"
    
    hashtags = ' '.join(get_hashtags(category, 'instagram'))
    caption += hashtags
    
    return caption


def generate_pinterest_caption(product: dict, category: str) -> str:
    """SEO-optimized Pinterest description."""
    title = product['title'][:60]
    price = product.get('price', '')
    discount = product.get('discount', '')
    bullets = product.get('bullets', [])
    
    # Pinterest = SEO, not social
    caption = f"{title}\n\n"
    
    if price:
        caption += f"Price: ₹{price}"
        if discount:
            caption += f" ({discount} off)"
        caption += "\n\n"
    
    if bullets:
        caption += "Key Features:\n"
        for b in bullets[:5]:
            caption += f"• {b[:60]}\n"
        caption += "\n"
    
    # SEO keywords
    keywords = get_hashtags(category, 'pinterest')
    caption += "Tags: " + ', '.join(kw.replace('#', '') for kw in keywords)
    
    caption += "\n\n#ad | Affiliate link"
    
    return caption


def generate_pinterest_title(product: dict, category: str) -> str:
    """Short SEO title for Pinterest pin."""
    title = product['title'][:50]
    price = product.get('price', '')
    discount = product.get('discount', '')
    
    if discount:
        return f"{title} — {discount} OFF | ₹{price}"
    elif price:
        return f"{title} — ₹{price}"
    return title


# ─── MAIN FUNCTION ───────────────────────────────────────────

def generate_all_captions(product: dict, category: str) -> dict:
    """Generate captions for all platforms."""
    return {
        'twitter': generate_twitter_caption(product, category),
        'instagram': generate_instagram_caption(product, category),
        'pinterest_title': generate_pinterest_title(product, category),
        'pinterest_description': generate_pinterest_caption(product, category),
    }


# ─── CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    # Demo
    product = {
        'title': 'Fire-Boltt Aero TWS Earbuds Custom EQ, Wireless Bluetooth 5.4',
        'price': '699',
        'discount': '-92%',
        'rating': '3.8 out of 5 stars',
        'reviews': '(1,234)',
        'asin': 'B0FVS76HKH',
        'bullets': [
            '50H Playtime with fast charging',
            'Bluetooth 5.4 for stable connection',
            '50ms Low Latency for gaming',
            'IPX4 Waterproof',
        ],
        'affiliate_tag': 'counitinguniq-21',
    }
    
    captions = generate_all_captions(product, 'earbuds')
    
    print("="*60)
    print("🐦 TWITTER CAPTION:")
    print("="*60)
    print(captions['twitter'])
    print(f"\n({len(captions['twitter'])} chars)")
    
    print("\n" + "="*60)
    print("📸 INSTAGRAM CAPTION:")
    print("="*60)
    print(captions['instagram'])
    
    print("\n" + "="*60)
    print("📌 PINTEREST TITLE:")
    print("="*60)
    print(captions['pinterest_title'])
    print("\n📌 PINTEREST DESCRIPTION:")
    print(captions['pinterest_description'])
