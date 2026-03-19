"""
RICKY SCENE ENGINE — World-Class Marketing Image Generator
Handles ANY Amazon product category with category-specific creative scenes.

Architecture:
  1. Detect product category from title/bullets
  2. Select category-specific scene templates
  3. Smart-assign product images to scenes
  4. Generate AI creative images (Nano Banana Pro)
  5. Apply professional PIL overlays (text, badges, layouts)
  6. Build transform/comparison slides with PIL precision

Categories supported:
  - Electronics (cameras, phones, earbuds, laptops)
  - Beauty & Skincare (face wash, serums, creams)
  - Fashion (clothing, shoes, accessories)
  - Home & Kitchen (appliances, furniture, decor)
  - Sports & Fitness (equipment, supplements, wearables)
  - Books & Media
  - Gadgets & Accessories
  - Generic fallback
"""

import re

# ─── CATEGORY DETECTION ─────────────────────────────────────

CATEGORY_KEYWORDS = {
    'camera': ['camera', 'dslr', 'mirrorless', 'vlog', 'lens', 'tripod', 'gopro', 'webcam', 'camcorder'],
    'phone': ['phone', 'smartphone', 'iphone', 'galaxy', 'pixel', 'oneplus', 'redmi', 'realme', 'poco', 'mobile'],
    'earbuds': ['earbuds', 'tws', 'headphone', 'headset', 'earphone', 'airpods', 'neckband', 'bluetooth audio'],
    'laptop': ['laptop', 'notebook', 'macbook', 'chromebook', 'ultrabook'],
    'tablet': ['tablet', 'ipad', 'tab s', 'kindle'],
    'watch': ['smartwatch', 'watch', 'band', 'fitness tracker', 'apple watch', 'galaxy watch'],
    'speaker': ['speaker', 'soundbar', 'subwoofer', 'alexa', 'echo', 'home pod', 'jbl'],
    'beauty': ['face wash', 'serum', 'cream', 'moisturizer', 'sunscreen', 'cleanser', 'toner', 'mask', 'lotion',
               'shampoo', 'conditioner', 'hair oil', 'lip balm', 'foundation', 'concealer', 'skincare', 'beauty',
               'vitamin c', 'retinol', 'niacinamide', 'hyaluronic', 'spf', 'face pack'],
    'fashion_clothing': ['shirt', 't-shirt', 'tshirt', 'jeans', 'trouser', 'kurta', 'saree', 'dress', 'jacket',
                         'hoodie', 'sweatshirt', 'blazer', 'shorts', 'palazzo', 'legging', 'track pants'],
    'fashion_shoes': ['shoes', 'sneakers', 'sandals', 'boots', 'loafers', 'heels', 'slipper', 'floaters', 'running shoes'],
    'fashion_accessories': ['sunglasses', 'wallet', 'belt', 'handbag', 'backpack', 'purse', 'cap', 'hat', 'scarf'],
    'kitchen': ['mixer', 'grinder', 'blender', 'cooker', 'microwave', 'oven', 'toaster', 'kettle', 'air fryer',
                'induction', 'cookware', 'pan', 'pot', 'utensil', 'container', 'bottle', 'flask', 'lunch box'],
    'appliance': ['refrigerator', 'fridge', 'washing machine', 'ac', 'air conditioner', 'air purifier', 'vacuum',
                  'iron', 'geyser', 'water heater', 'fan', 'cooler', 'heater', 'dishwasher'],
    'fitness': ['protein', 'whey', 'supplement', 'dumbbell', 'yoga mat', 'resistance band', 'gym', 'treadmill',
                'exercise', 'creatine', 'bcaa', 'pre workout', 'mass gainer'],
    'gaming': ['gaming', 'controller', 'console', 'playstation', 'xbox', 'nintendo', 'gaming mouse', 'gaming keyboard'],
    'books': ['book', 'novel', 'guide', 'textbook', 'paperback', 'hardcover'],
    'toys': ['toy', 'lego', 'puzzle', 'board game', 'action figure', 'doll', 'remote control car'],
    'pet': ['dog food', 'cat food', 'pet', 'collar', 'leash', 'pet bed', 'aquarium'],
    'baby': ['diaper', 'baby', 'stroller', 'car seat', 'baby food', 'feeding bottle'],
    'helmet': ['helmet', 'riding gear', 'motorcycle', 'bike accessories'],
    'tools': ['drill', 'screwdriver', 'toolkit', 'wrench', 'plier', 'measuring tape', 'tool set'],
}

# Group categories
ELECTRONICS = ['camera', 'phone', 'earbuds', 'laptop', 'tablet', 'watch', 'speaker', 'gaming']
FASHION = ['fashion_clothing', 'fashion_shoes', 'fashion_accessories']
HOME = ['kitchen', 'appliance']


def detect_category(title: str, bullets: list = None) -> str:
    """Detect product category from title and bullet points."""
    text = title.lower()
    if bullets:
        text += ' ' + ' '.join(b.lower() for b in bullets[:5])
    
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                score += len(kw)  # Longer matches = more specific = higher score
        if score > 0:
            scores[cat] = score
    
    if not scores:
        return 'generic'
    
    return max(scores, key=scores.get)


# ─── SCENE TEMPLATES PER CATEGORY ───────────────────────────

def get_scene_prompts(category: str, product_name: str, features: list = None) -> dict:
    """
    Return scene prompts tailored to product category.
    Each prompt is designed for maximum marketing impact.
    """
    short = product_name[:40]
    feature_text = ', '.join(features[:3]) if features else ''
    
    # ─── ELECTRONICS (cameras, phones, earbuds, etc.) ───
    if category in ELECTRONICS:
        return _electronics_prompts(category, short, feature_text)
    
    # ─── BEAUTY & SKINCARE ───
    elif category == 'beauty':
        return _beauty_prompts(short, feature_text)
    
    # ─── FASHION ───
    elif category in FASHION:
        return _fashion_prompts(category, short, feature_text)
    
    # ─── HOME & KITCHEN ───
    elif category in HOME:
        return _home_prompts(category, short, feature_text)
    
    # ─── FITNESS ───
    elif category == 'fitness':
        return _fitness_prompts(short, feature_text)
    
    # ─── HELMET ───
    elif category == 'helmet':
        return _helmet_prompts(short, feature_text)
    
    # ─── GENERIC FALLBACK ───
    else:
        return _generic_prompts(short, feature_text)


def _electronics_prompts(sub_cat: str, name: str, features: str) -> dict:
    
    context_map = {
        'camera': ('photographer', 'captures stunning photos', 'creative studio', 'photography workspace'),
        'phone': ('user', 'connects your world', 'modern lifestyle', 'tech-forward desk'),
        'earbuds': ('music lover', 'delivers immersive sound', 'gym & commute', 'minimalist desk'),
        'laptop': ('professional', 'powers your workflow', 'home office', 'productive workspace'),
        'tablet': ('creator', 'brings ideas to life', 'creative space', 'artistic desk'),
        'watch': ('athlete', 'tracks every move', 'active lifestyle', 'morning routine'),
        'speaker': ('music enthusiast', 'fills every room', 'party setup', 'living room'),
        'gaming': ('gamer', 'dominates every game', 'gaming battlestation', 'RGB setup'),
    }
    
    person, verb, scene, workspace = context_map.get(sub_cat, ('user', 'enhances your life', 'daily routine', 'modern desk'))
    
    return {
        # Twitter 16:9
        'tw_hero': f"Cinematic product photography of {name} on a sleek dark surface with dramatic rim lighting, studio quality, shallow depth of field, premium tech product shot, moody atmosphere, 16:9",
        'tw_features': f"Clean flat lay of {name} with matching accessories arranged symmetrically on matte black surface, overhead shot, studio lighting, tech reviewer aesthetic, organized grid layout, 16:9",
        'tw_lifestyle': f"Young {person} using {name} in a trendy urban cafe, natural window light, candid lifestyle moment, warm tones, cinematic shallow DOF, authentic social media content, 16:9",
        'tw_cta': f"{name} elegantly displayed on a {workspace} next to a coffee and plant, warm ambient golden hour lighting, aspirational lifestyle, premium feel, 16:9",
        
        # Instagram 4:5 portrait
        'ig_hook': f"Dramatic hero shot of {name} with vibrant neon light reflections, dark moody background with colored smoke, cyberpunk tech aesthetic, eye-catching product photography, vertical portrait",
        'ig_lifestyle': f"Stylish person enjoying {name} in a beautiful outdoor setting at golden hour, lifestyle portrait, warm natural lighting, aspirational social media content, vertical",
        'ig_flatlay': f"Aesthetic flat lay of {name} with coffee, notebook, plant, and headphones on white marble surface, overhead shot, Instagram-worthy styling, pastel accents, warm tones, vertical",
        'ig_detail': f"Extreme macro photography of {name} showing premium build quality, material texture, and design details, professional studio lighting with specular highlights, vertical",
        'ig_transform': f"Creative split composition: {name} product on left side, person enjoying the experience it creates on right side, {verb}, lifestyle transformation concept, vertical",
        'ig_texture': f"Artistic creative shot of {name} surrounded by dynamic abstract elements, particles, or nature elements, creative product photography with motion and energy, vertical",
        'ig_lifestyle2': f"Adventurous person using {name} during travel or outdoor activity, epic landscape or cityscape background, golden hour, aspirational wanderlust lifestyle, vertical",
        'ig_cta': f"Clean minimalist product shot of {name} centered on elegant gradient background, premium brand aesthetic, subtle shadow, high-end commercial photography, vertical",
        
        # Pinterest 2:3 tall
        'pin_guide': f"Educational product layout of {name} with clean design showing the product from best angle, informative buyer's guide aesthetic, white background, professional, tall vertical",
        'pin_aesthetic': f"Dreamy aesthetic photo of {name} in a beautifully styled setting with flowers, soft fabrics, and warm lighting, Pinterest-worthy creative flat lay, soft tones, tall vertical",
        'pin_lifestyle': f"Aspirational {workspace} setup featuring {name} alongside complementary items, organized and aesthetically pleasing, home goals inspiration, tall vertical",
    }


def _beauty_prompts(name: str, features: str) -> dict:
    return {
        # Twitter 16:9
        'tw_hero': f"Luxurious product photography of {name} with water droplets and fresh ingredients scattered around, clean spa-like aesthetic, soft studio lighting, premium beauty product shot, 16:9",
        'tw_features': f"Scientific editorial shot of {name} with ingredient highlights — fresh botanicals, vitamin extracts arranged artfully, clean white background, beauty editorial, 16:9",
        'tw_lifestyle': f"Beautiful woman with glowing radiant skin holding {name}, natural soft lighting, fresh dewy complexion, bathroom vanity background, authentic beauty content, 16:9",
        'tw_cta': f"Elegant display of {name} on marble bathroom counter with eucalyptus and candles, spa luxury aesthetic, warm ambient lighting, aspirational self-care, 16:9",
        
        # Instagram 4:5 portrait
        'ig_hook': f"Stunning hero shot of {name} with dramatic splash of water and light rays, fresh and clean energy, premium beauty advertising, eye-catching product photography, vertical",
        'ig_lifestyle': f"Woman applying {name} in a bright modern bathroom, morning skincare routine, natural glowing skin, soft daylight, authentic beauty lifestyle content, vertical",
        'ig_flatlay': f"Aesthetic skincare flat lay with {name} alongside jade roller, cotton pads, flowers, and candle on marble, overhead shot, beauty influencer style, pastel tones, vertical",
        'ig_detail': f"Extreme close-up of {name} product texture — creamy gel or foam being squeezed out, satisfying product texture photography, macro beauty shot, vertical",
        'ig_transform': f"Before and after skincare transformation: dull skin on top transforming to radiant glowing skin below, with {name} in center, beauty results concept, vertical",
        'ig_texture': f"Artistic shot of {name} surrounded by fresh fruits, honey drips, and botanical ingredients, colorful natural beauty flat lay, ingredient-focused creative photography, vertical",
        'ig_lifestyle2': f"Confident woman with perfect glowing skin in natural outdoor setting, golden hour selfie moment, radiant beauty result from using {name}, vertical",
        'ig_cta': f"Clean minimalist beauty product shot of {name} on soft pink or peach gradient background, premium skincare brand aesthetic, elegant shadows, vertical",
        
        # Pinterest 2:3 tall
        'pin_guide': f"Skincare routine guide layout featuring {name} as hero product, clean educational infographic aesthetic, step-by-step visual, beauty tips, tall vertical",
        'pin_aesthetic': f"Dreamy pink aesthetic photo of {name} surrounded by roses, pearls, and silk fabric, ultra-feminine beauty flat lay, Pinterest-worthy styling, tall vertical",
        'pin_lifestyle': f"Beautiful bathroom shelfie featuring {name} alongside other skincare products, organized beauty collection goals, aspirational self-care setup, tall vertical",
    }


def _fashion_prompts(sub_cat: str, name: str, features: str) -> dict:
    if sub_cat == 'fashion_shoes':
        return {
            'tw_hero': f"Editorial fashion photography of {name} shoes on textured concrete with dramatic side lighting, sneaker culture aesthetic, premium product shot, 16:9",
            'tw_features': f"Clean overhead shot of {name} shoes showing sole detail and construction, on clean background, sneaker review style, 16:9",
            'tw_lifestyle': f"Stylish person walking on urban street wearing {name} shoes, street style fashion photography, candid movement shot, city backdrop, 16:9",
            'tw_cta': f"Artistic shot of {name} shoes on a wooden shelf with plants and accessories, lifestyle display, warm ambient lighting, 16:9",
            
            'ig_hook': f"Dramatic hero shot of {name} shoes with dynamic lighting and smoke effects, streetwear culture aesthetic, bold and eye-catching, vertical",
            'ig_lifestyle': f"Full outfit of the day featuring {name} shoes, street style fashion, urban background, natural lighting, OOTD content, vertical",
            'ig_flatlay': f"Flat lay of {name} shoes with matching outfit pieces — jeans, watch, sunglasses, wallet, overhead styled shot, vertical",
            'ig_detail': f"Close-up of {name} shoes showing stitching, material texture, and brand details, premium craftsmanship photography, vertical",
            'ig_transform': f"Creative transition from casual old shoes to fresh new {name}, upgrade your style concept, side by side comparison, vertical",
            'ig_texture': f"Artistic shot of {name} shoes in puddle reflection or with creative lighting, moody fashion photography, vertical",
            'ig_lifestyle2': f"Person at gym or outdoor activity wearing {name} shoes, action shot, dynamic lifestyle photography, vertical",
            'ig_cta': f"Clean product shot of {name} shoes on solid color background, minimal fashion commercial aesthetic, vertical",
            
            'pin_guide': f"Style guide showing {name} shoes with 3 different outfit combinations, fashion inspiration, educational layout, tall vertical",
            'pin_aesthetic': f"Aesthetic flat lay of {name} shoes with seasonal flowers and accessories, fashion mood board style, tall vertical",
            'pin_lifestyle': f"Closet organization featuring {name} shoes as hero, shoe collection goals, aspirational wardrobe, tall vertical",
        }
    elif sub_cat == 'fashion_clothing':
        return {
            'tw_hero': f"Fashion editorial shot of {name} on a mannequin or hanger with professional studio lighting, clean commercial style, 16:9",
            'tw_features': f"Close-up fabric detail of {name} showing texture and quality, premium fashion photography, 16:9",
            'tw_lifestyle': f"Stylish model wearing {name} in urban setting, street fashion photography, candid lifestyle, 16:9",
            'tw_cta': f"Styled outfit featuring {name} displayed on wooden rack with accessories, boutique shopping aesthetic, 16:9",
            
            'ig_hook': f"Striking fashion editorial of model wearing {name}, dramatic lighting, bold pose, high fashion energy, vertical",
            'ig_lifestyle': f"Casual outfit of the day featuring {name}, natural setting, authentic street style, Instagram fashion content, vertical",
            'ig_flatlay': f"Aesthetic outfit flat lay with {name} as centerpiece alongside accessories, shoes, and jewelry, overhead shot, vertical",
            'ig_detail': f"Close-up fabric and stitching detail of {name}, showcasing quality and craftsmanship, macro fashion photography, vertical",
            'ig_transform': f"Before and after styling — plain look transforms to chic outfit with {name}, fashion makeover concept, vertical",
            'ig_texture': f"Creative shot of {name} with flowing fabric movement, artistic fashion photography with motion, vertical",
            'ig_lifestyle2': f"Person wearing {name} at brunch, cafe, or social event, authentic lifestyle moment, warm tones, vertical",
            'ig_cta': f"Clean minimal product shot of {name} neatly folded on neutral background, premium fashion e-commerce style, vertical",
            
            'pin_guide': f"How to style {name} — 4 different ways, outfit inspiration board, fashion tips layout, tall vertical",
            'pin_aesthetic': f"Seasonal aesthetic flat lay featuring {name} with matching accessories and decor, Pinterest fashion mood, tall vertical",
            'pin_lifestyle': f"Wardrobe goals featuring {name}, organized closet aesthetic, capsule wardrobe inspiration, tall vertical",
        }
    else:  # accessories
        return _generic_prompts(name, features)


def _home_prompts(sub_cat: str, name: str, features: str) -> dict:
    if sub_cat == 'appliance':
        return {
            'tw_hero': f"Professional product photography of {name} in a modern kitchen or living room, clean interior design, natural lighting, premium home appliance shot, 16:9",
            'tw_features': f"Detailed shot of {name} showing control panel and key features, clean informative angle, tech review style, 16:9",
            'tw_lifestyle': f"Happy family using {name} in a beautiful modern home, warm lifestyle photography, authentic domestic scene, 16:9",
            'tw_cta': f"{name} perfectly placed in a styled modern kitchen, aspirational home interior, warm ambient lighting, 16:9",
            
            'ig_hook': f"Stunning hero shot of {name} in a luxurious modern kitchen with dramatic lighting, premium home appliance photography, vertical",
            'ig_lifestyle': f"Person using {name} while cooking a meal, warm kitchen atmosphere, lifestyle content, authentic and inviting, vertical",
            'ig_flatlay': f"Overhead shot of kitchen scene with {name} surrounded by fresh ingredients and utensils, cooking lifestyle flat lay, vertical",
            'ig_detail': f"Close-up of {name} showing build quality, finish, and design details, premium material photography, vertical",
            'ig_transform': f"Before and after kitchen transformation — messy kitchen becomes organized with {name}, home improvement concept, vertical",
            'ig_texture': f"Artistic shot of {name} with steam, water splashes, or cooking action, dynamic appliance photography, vertical",
            'ig_lifestyle2': f"Morning routine in beautiful kitchen featuring {name}, coffee, and breakfast spread, cozy home lifestyle, vertical",
            'ig_cta': f"Clean minimal product shot of {name} on clean background, premium appliance e-commerce style, vertical",
            
            'pin_guide': f"Complete buyer's guide for {name} showing features and dimensions, informative home appliance layout, tall vertical",
            'pin_aesthetic': f"Beautiful modern kitchen interior featuring {name} as centerpiece, home decor inspiration, tall vertical",
            'pin_lifestyle': f"Dream kitchen setup with {name} and matching appliances, kitchen goals, aspirational home, tall vertical",
        }
    else:  # kitchen
        return {
            'tw_hero': f"Professional product photography of {name} on marble kitchen counter with fresh ingredients, warm food styling, premium kitchen product, 16:9",
            'tw_features': f"Detailed overhead shot of {name} with food being prepared, cooking action shot, recipe content style, 16:9",
            'tw_lifestyle': f"Someone cooking a beautiful meal using {name}, warm kitchen lighting, authentic foodie lifestyle, 16:9",
            'tw_cta': f"{name} displayed in a styled modern kitchen with herbs and spices, culinary aspirational, 16:9",
            
            'ig_hook': f"Eye-catching shot of {name} with steaming freshly cooked food, delicious and inviting, food photography meets product shot, vertical",
            'ig_lifestyle': f"Home chef using {name} in action, cooking a colorful healthy meal, kitchen lifestyle content, vertical",
            'ig_flatlay': f"Recipe flat lay with {name} surrounded by fresh colorful ingredients, overhead food styling, cooking content, vertical",
            'ig_detail': f"Close-up of {name} showing quality craftsmanship and material details, kitchen product macro photography, vertical",
            'ig_transform': f"Raw ingredients on top transforming into beautiful finished dish below, with {name} in center, cooking transformation, vertical",
            'ig_texture': f"Artistic food photography with {name}, spices flying, liquids pouring, dynamic cooking action, vertical",
            'ig_lifestyle2': f"Family dinner table scene with food prepared using {name}, warm gathering, togetherness, vertical",
            'ig_cta': f"Clean styled product shot of {name} on neutral background, premium kitchenware aesthetic, vertical",
            
            'pin_guide': f"Recipe guide featuring {name}, step-by-step cooking layout, food and product combined, tall vertical",
            'pin_aesthetic': f"Beautiful kitchen styling with {name} surrounded by seasonal produce and decor, foodie Pinterest aesthetic, tall vertical",
            'pin_lifestyle': f"Kitchen organization goals featuring {name} in a tidy pantry or counter setup, tall vertical",
        }


def _fitness_prompts(name: str, features: str) -> dict:
    return {
        'tw_hero': f"Powerful product shot of {name} in a gym setting with dramatic lighting, fitness motivation aesthetic, strong and bold, 16:9",
        'tw_features': f"Clean detailed shot of {name} showing nutrition facts or product features, informative health & fitness style, 16:9",
        'tw_lifestyle': f"Fit athletic person using {name} during intense workout, gym action shot, motivational fitness content, 16:9",
        'tw_cta': f"{name} displayed with gym gear — towel, shaker, dumbbells, pre-workout setup, fitness lifestyle, 16:9",
        
        'ig_hook': f"Dramatic hero shot of {name} with explosive energy effect — powder burst or dynamic splash, powerful fitness product photography, vertical",
        'ig_lifestyle': f"Athletic person with {name} at the gym, post-workout or pre-workout moment, motivational fitness lifestyle, vertical",
        'ig_flatlay': f"Gym bag essentials flat lay with {name} as hero alongside shaker, towel, earbuds, and keys, fitness lifestyle overhead, vertical",
        'ig_detail': f"Close-up of {name} showing ingredients, texture, or quality details, health and fitness product macro, vertical",
        'ig_transform': f"Fitness transformation — before (tired/weak) to after (strong/energized) with {name} in center, motivation concept, vertical",
        'ig_texture': f"Creative shot of {name} with protein powder explosion or liquid splash, dynamic fitness product photography, vertical",
        'ig_lifestyle2': f"Outdoor workout or running scene with {name}, sunrise fitness session, healthy active lifestyle, vertical",
        'ig_cta': f"Clean minimal product shot of {name} with subtle gym background blur, premium fitness brand aesthetic, vertical",
        
        'pin_guide': f"Complete guide to {name} — benefits, usage, and results, informative fitness infographic layout, tall vertical",
        'pin_aesthetic': f"Healthy lifestyle flat lay with {name} alongside fruits, smoothie, and yoga mat, wellness aesthetic, tall vertical",
        'pin_lifestyle': f"Home gym setup featuring {name} and workout equipment, fitness goals inspiration, tall vertical",
    }


def _helmet_prompts(name: str, features: str) -> dict:
    return {
        'tw_hero': f"Professional product shot of {name} helmet on dark surface with dramatic rim lighting, premium motorcycle gear, safety meets style, 16:9",
        'tw_features': f"Detailed shot of {name} helmet showing visor mechanism, ventilation, and safety features, technical product review style, 16:9",
        'tw_lifestyle': f"Rider on a motorcycle wearing {name} helmet, open road ahead, adventure and freedom, cinematic motorcycle photography, 16:9",
        'tw_cta': f"{name} helmet displayed alongside motorcycle gloves and keys, riding gear lifestyle, warm lighting, 16:9",
        
        'ig_hook': f"Dramatic hero shot of {name} helmet with lens flare and motion blur effect, speed and adrenaline, eye-catching motorcycle gear photography, vertical",
        'ig_lifestyle': f"Motorcyclist holding {name} helmet next to their bike, golden hour, adventurous rider lifestyle, vertical",
        'ig_flatlay': f"Rider's essentials flat lay — {name} helmet with gloves, jacket, keys, and sunglasses, overhead biker lifestyle, vertical",
        'ig_detail': f"Close-up of {name} helmet showing ISI certification, visor quality, and interior padding, safety-focused detail shot, vertical",
        'ig_transform': f"Before and after: regular ride vs safe ride with {name} helmet, safety awareness concept, rider protection, vertical",
        'ig_texture': f"Artistic shot of {name} helmet with rain droplets or dust particles, all-weather riding concept, moody motorcycle photography, vertical",
        'ig_lifestyle2': f"Group of riders on mountain road, lead rider wearing {name} helmet, epic landscape, brotherhood of bikers, vertical",
        'ig_cta': f"Clean product shot of {name} helmet on neutral background with subtle shadow, premium safety gear aesthetic, vertical",
        
        'pin_guide': f"Helmet buying guide featuring {name} — safety ratings, features checklist, informative motorcycle gear layout, tall vertical",
        'pin_aesthetic': f"Styled motorcycle lifestyle photo with {name} helmet on vintage bike, retro biker aesthetic, tall vertical",
        'pin_lifestyle': f"Garage or workshop setup with {name} helmet alongside motorcycle and gear, rider's den goals, tall vertical",
    }


def _generic_prompts(name: str, features: str) -> dict:
    return {
        'tw_hero': f"Professional commercial product photography of {name} with dramatic studio lighting on dark elegant surface, premium product shot, high-end advertising, 16:9",
        'tw_features': f"Clean detailed overhead shot of {name} showing key features and design, informative product review style photography, 16:9",
        'tw_lifestyle': f"Person happily using {name} in everyday life setting, authentic lifestyle photography, warm natural lighting, relatable content, 16:9",
        'tw_cta': f"{name} beautifully displayed on a styled surface with complementary lifestyle items, aspirational product placement, warm tones, 16:9",
        
        'ig_hook': f"Eye-catching dramatic hero shot of {name} with vibrant lighting effects and bold composition, stop-scrolling product photography, vertical",
        'ig_lifestyle': f"Authentic lifestyle scene featuring {name} in natural daily use, warm and inviting, relatable social media content, vertical",
        'ig_flatlay': f"Aesthetic flat lay of {name} with complementary items on textured surface, Instagram-worthy overhead styling, warm tones, vertical",
        'ig_detail': f"Extreme close-up of {name} showing quality craftsmanship, material texture, and fine details, macro product photography, vertical",
        'ig_transform': f"Before and after concept showing life improvement with {name}, creative split composition, transformation concept, vertical",
        'ig_texture': f"Creative artistic shot of {name} with dynamic elements — particles, light trails, or nature elements, visually striking, vertical",
        'ig_lifestyle2': f"Person enjoying {name} in an outdoor or social setting, candid lifestyle moment, golden hour lighting, vertical",
        'ig_cta': f"Clean minimalist product shot of {name} centered on elegant gradient background, premium brand commercial aesthetic, vertical",
        
        'pin_guide': f"Complete buyer's guide for {name} showing product features and benefits, clean informative layout, tall vertical",
        'pin_aesthetic': f"Dreamy aesthetic styled photo of {name} with flowers, fabrics, and soft lighting, Pinterest-worthy flat lay, tall vertical",
        'pin_lifestyle': f"Aspirational lifestyle setup featuring {name} in a beautifully organized space, goals inspiration, tall vertical",
    }


# ─── OVERLAY TEMPLATES PER CATEGORY ─────────────────────────

def get_overlay_config(category: str, product_name: str, price: str, discount: str) -> dict:
    """Return text overlay configuration per scene, adapted to category."""
    
    short = product_name[:35]
    
    # Category-specific CTA text
    cta_map = {
        'camera': 'Capture Every Moment',
        'phone': 'Upgrade Your Life', 
        'earbuds': 'Sound Like Never Before',
        'laptop': 'Power Your Workflow',
        'watch': 'Time for an Upgrade',
        'speaker': 'Feel Every Beat',
        'gaming': 'Level Up Your Game',
        'beauty': 'Glow Up Starts Here',
        'fashion_clothing': 'Elevate Your Style',
        'fashion_shoes': 'Step Into Style',
        'appliance': 'Upgrade Your Home',
        'kitchen': 'Cook Like a Pro',
        'fitness': 'Train Harder',
        'helmet': 'Ride Safe, Ride Bold',
    }
    
    cta = cta_map.get(category, 'Get Yours Today')
    
    return {
        'tw_hero': {'bottom': f'{short} | {cta}', 'price': True},
        'tw_features': {'bottom': 'Everything You Need to Know ⬇️', 'price': True},
        'tw_lifestyle': {'top': cta.upper(), 'price': False},
        'tw_cta': {'bottom': f'Get {short} → Link Below 🔗', 'price': True},
        
        'ig_hook': {'top': f'🔥 {cta.upper()}', 'price': True},
        'ig_lifestyle': {'bottom': cta, 'price': False},
        'ig_flatlay': {'bottom': f'{short} ✨', 'price': True},
        'ig_detail': {'top': 'PREMIUM QUALITY', 'price': False},
        'ig_transform': {'bottom': 'See the Difference →', 'price': False},
        'ig_texture': {'top': f'{cta.upper()} 🚀', 'price': False},
        'ig_lifestyle2': {'bottom': f'{cta} 🌟', 'price': False},
        'ig_cta': {'bottom': f'₹{price} | Link in Bio | #ad', 'price': True},
        
        'pin_guide': {'top': f'{short} GUIDE', 'price': True},
        'pin_aesthetic': {'bottom': f'{short} | {cta}', 'price': False},
        'pin_lifestyle': {'top': f'{cta.upper()} GOALS', 'price': True},
    }


# ─── CLI TEST ────────────────────────────────────────────────

if __name__ == "__main__":
    test_products = [
        ("Sony Digital Camera ZV-1F for Content Creators", ['Ultra-wide 20mm lens', 'Vlog camera']),
        ("Fire-Boltt Aero TWS Earbuds Custom EQ", ['50H Playtime', 'Bluetooth 5.4']),
        ("ZEE-C Vitamin C Face Wash for Glowing Skin", ['Brightening', 'For all skin types']),
        ("Samsung 183L Digital Inverter Refrigerator", ['5 Star Rating', 'Direct Cool']),
        ("Nike Air Max Running Shoes for Men", ['Mesh upper', 'Air cushioning']),
        ("Steelbird SBA-7 ISI Certified Flip-Up Helmet", ['ISI Certified', 'Clear visor']),
        ("Optimum Nutrition Gold Standard Whey Protein", ['24g protein', 'Muscle recovery']),
        ("boAt Rockerz 450 Bluetooth Headphones", ['40mm drivers', '15H battery']),
    ]
    
    print("="*70)
    print("🎭 SCENE ENGINE — Category Detection Test")
    print("="*70)
    
    for title, bullets in test_products:
        cat = detect_category(title, bullets)
        prompts = get_scene_prompts(cat, title, bullets)
        print(f"\n📦 {title[:50]}")
        print(f"   Category: {cat}")
        print(f"   Scenes: {len(prompts)}")
        print(f"   Sample (tw_hero): {prompts['tw_hero'][:80]}...")
