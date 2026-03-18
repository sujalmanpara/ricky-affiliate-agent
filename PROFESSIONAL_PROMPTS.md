# Professional Marketing Image Prompts - Designer-Level

## 🎯 THE SYSTEM: Smart Prompt Generation

Instead of generic prompts, we analyze the product and generate **psychologically-optimized prompts** based on:
1. Product category
2. Target audience  
3. Platform psychology
4. Proven design patterns

---

## 📱 TWITTER (16:9) - SCROLL STOPPERS

### Pattern: BEFORE/AFTER Split Screen

**Psychology:** Instant contrast = instant understanding = STOPS scrolling

**Template:**
```python
def generate_twitter_prompt(product):
    # Analyze product to find the "problem it solves"
    problem = detect_problem(product)
    
    return f"""Professional marketing split-screen photograph, 16:9 landscape format:

LEFT SIDE (Problem - 45% of frame):
- {problem['scene']}
- {problem['pain_point']} clearly visible
- Person showing {problem['emotion']} (frustrated/stressed/tired)
- Environment: {problem['setting']}
- Lighting: Slightly dim, muted colors
- Mood: "This is my struggle"

DIVIDER (10% of frame):
- Subtle vertical line or arrow pointing right
- Optional text space: "BEFORE → AFTER"

RIGHT SIDE (Solution - 45% of frame):
- Same setting but TRANSFORMED
- THIS EXACT {product['category']} from reference image in use
- Same person now {problem['solution_emotion']} (smiling/relaxed/happy)
- Environment: Clean, organized, bright
- Lighting: Natural window light, vibrant colors
- Mood: "Problem solved!"

Product placement: Right side, naturally integrated (on desk/in kitchen/in hand)
Product must match reference image EXACTLY (same color, design, branding)
Style: Lifestyle photography, relatable not corporate
Camera: Eye-level, realistic perspective
Overall vibe: "I can relate" → "I need this"

Text overlay suggestions (for caption, not in image):
- Center: "{problem['hook_text']}"
- Bottom right: "₹{product['price']}" with discount badge if available
"""
```

**Example Outputs:**

```
# ELECTRONICS (Keyboard/Mouse)
Professional marketing split-screen photograph, 16:9 landscape format:

LEFT SIDE (Problem - 45%):
- Cluttered home office desk with tangled wired keyboard and mouse cables
- Cables draped everywhere, creating visual chaos
- WFH professional looking frustrated, rubbing temples
- Environment: Cramped desk space, papers scattered
- Lighting: Dim overhead light, shadows
- Mood: "Cable hell"

DIVIDER (10%):
- Clean vertical line with subtle arrow
- Text space: "CUT THE CABLES"

RIGHT SIDE (Solution - 45%):
- Same desk completely transformed
- THIS EXACT wireless keyboard and mouse from reference image
- Same person now smiling, typing comfortably
- Environment: Organized, spacious, minimalist
- Lighting: Warm natural window light
- Mood: "Freedom!"

Product: Keyboard/mouse positioned naturally on clean desk mat
Style: Modern home office, professional but relatable
Vibe: WFH upgrade, productivity boost
```

```
# HOME APPLIANCE (Refrigerator)
Professional marketing split-screen photograph, 16:9 landscape format:

LEFT SIDE (Problem - 45%):
- Person opening old yellowed refrigerator
- Food items spoiled, visible mold, unpleasant smell indicated by person's expression
- Interior dim and dingy
- Kitchen: Outdated, cluttered
- Lighting: Harsh fluorescent, unflattering
- Mood: "Ugh, again?"

DIVIDER (10%):
- Vertical line
- Text: "UPGRADE TIME"

RIGHT SIDE (Solution - 45%):
- Person opening THIS EXACT Samsung refrigerator from reference image
- Interior bright with LED lighting, fresh organized food
- Same person smiling with relief
- Kitchen: Modern, clean (same space transformed)
- Lighting: Soft natural light, appealing
- Mood: "Finally!"

Product: Refrigerator in modern Indian kitchen context
Style: Real home photography, before/after transformation
Vibe: Kitchen upgrade, peace of mind
```

```
# MOBILE ACCESSORY (Power Bank)
Professional marketing split-screen photograph, 16:9 landscape format:

LEFT SIDE (Problem - 45%):
- Phone screen showing 2% battery with multiple notifications
- Person in taxi/outdoor setting, anxious expression
- Important call/meeting notification visible
- Environment: Travel/commute scenario
- Lighting: Dim interior car light
- Mood: "Oh no, not now!"

DIVIDER (10%):
- Arrow pointing right
- Text: "NEVER AGAIN"

RIGHT SIDE (Solution - 45%):
- Same person now relaxed, phone charging
- THIS EXACT power bank from reference connected to phone
- Phone screen showing charging icon and 45%
- Same environment but person is calm
- Lighting: Brighter, hopeful
- Mood: "Crisis averted"

Product: Power bank in hand, charging phone
Style: Real-life travel scenario, relatable moment
Vibe: Always prepared, freedom from battery anxiety
```

---

## 📸 INSTAGRAM (1:1) - AESTHETIC FIRST

### Pattern: LIFESTYLE HERO / FLAT LAY

**Psychology:** Aspiration = "I want that life/space"

**Template:**
```python
def generate_instagram_prompt(product):
    aesthetic = detect_aesthetic(product)
    
    return f"""Top-down aesthetic flat lay photograph, square 1:1 format:

SCENE COMPOSITION:
- View: Bird's eye view, 90° overhead
- Surface: {aesthetic['surface']} (wood desk/marble counter/concrete table)
- Lighting: Soft natural window light from top-right, gentle shadows
- Color palette: {aesthetic['colors']} (warm neutrals/cool minimalist/earthy tones)

MAIN SUBJECT (Center-right, rule of thirds):
- THIS EXACT {product['category']} from reference image
- Product: Naturally placed, not forced or staged
- Position: Slightly off-center (more interesting composition)
- Product must be clearly visible but not "ad-like"

COMPLEMENTARY ITEMS (arranged aesthetically):
- Top-left: {aesthetic['item_1']} (laptop/notebook/magazine)
- Bottom-left: {aesthetic['item_2']} (coffee cup/plant/phone)
- Right side: {aesthetic['item_3']} (pen/glasses/small object)
- Optional: Natural elements (leaf/flower/wood piece)

SPACING:
- Generous white/negative space (70% composition is surface)
- Items don't touch edges (breathing room)
- Balanced but not perfectly symmetrical

STYLE:
- Instagram aesthetic: Curated but natural
- NOT overly styled (avoid "catalog" look)
- Lived-in feeling: Coffee cup has coffee, notebook slightly open
- Authentic: Small imperfections okay (real life, not studio)

MOOD:
- {aesthetic['mood']} (productive morning/cozy afternoon/creative evening)
- Aspirational but attainable
- "This could be my space"

Product prominence: 40% of visual weight (product + context both important)
Overall vibe: Lifestyle inspiration, not advertisement
```

**Example Outputs:**

```
# TECH ACCESSORY (Keyboard)
Top-down aesthetic flat lay photograph, square 1:1 format:

SCENE:
- Wooden desk surface, light oak finish
- Natural window light from top-right, soft shadows
- Warm neutral palette (beige, white, light brown)

CENTER-RIGHT (Product):
- THIS EXACT wireless keyboard from reference
- Positioned diagonally for visual interest
- Matching wireless mouse beside it

COMPLEMENTARY ITEMS:
- Top-left: MacBook Pro (closed, silver)
- Bottom-left: White ceramic coffee cup (with coffee)
- Right: Succulent plant in minimal white pot
- Scattered: Airpods case, notepad with pen

SPACING:
- 70% clean wood surface visible
- Items create visual flow (eye moves naturally)

STYLE:
- Modern WFH aesthetic
- Productive yet calm
- Instagram-worthy but not fake

MOOD: Morning work session, focused creativity
Vibe: "My ideal workspace"
```

```
# HOME APPLIANCE (Refrigerator - Lifestyle Context)
Professional lifestyle photograph, square 1:1 format:

SCENE:
- Modern Indian kitchen, mid-shot view
- Natural daylight from window, bright and airy
- Color palette: Whites, stainless steel, natural wood accents

FOCUS (Rule of thirds, right):
- THIS EXACT Samsung refrigerator from reference
- Positioned in clean kitchen corner
- Door slightly open showing LED interior light

CONTEXT (lifestyle, not catalog):
- Left side: Kitchen counter with fresh vegetables
- Foreground: Glass of cold water with condensation
- Background: Blurred kitchen elements (depth)
- Optional: Person's hand reaching for fridge (human element)

COMPOSITION:
- Refrigerator: 50% of frame but naturally integrated
- Kitchen context: 50% establishes lifestyle

STYLE:
- Real home feeling, not showroom
- Lived-in but tidy
- Aspirational Indian kitchen

MOOD: Fresh start, healthy living, pride of ownership
Vibe: "This is my modern kitchen"
```

```
# FASHION/ACCESSORY (Backpack - if applicable)
Top-down flat lay photograph, square 1:1 format:

SCENE:
- Concrete or terrazzo surface
- Natural outdoor light, crisp shadows
- Urban cool palette (greys, black, pops of color)

CENTER:
- THIS EXACT backpack from reference, unzipped showing interior
- Organized contents displayed: Laptop, book, water bottle

AROUND (travel/lifestyle context):
- Passport and boarding pass
- Phone with maps app visible
- Sunglasses
- Headphones
- Travel-size toiletries

COMPOSITION:
- Organized chaos (stuff laid out for trip)
- Not perfectly aligned (realistic packing moment)

STYLE:
- Travel lifestyle
- Urban explorer aesthetic
- Functional + stylish

MOOD: Adventure ready, organized traveler
Vibe: "Travel essentials"
```

---

## 📌 PINTEREST (2:3) - INFORMATION VALUE

### Pattern: INFO-RICH PRODUCT SHOWCASE

**Psychology:** "I'm researching, give me VALUE"

**Template:**
```python
def generate_pinterest_prompt(product):
    features = product['key_features'][:5]
    
    return f"""Professional product infographic photograph, vertical 2:3 format:

LAYOUT STRUCTURE:

TOP SECTION (25% of height):
- Clean solid background: {product['category_color']} (tech=blue/food=green/fashion=warm)
- Large bold text space for: "Best {product['category']} Under ₹{product['price']} in 2026"
- Subtitle space: "{product['title']}"
- Text: Sans-serif, bold, high contrast

MIDDLE SECTION (50% of height):
- THIS EXACT {product['category']} from reference image
- Product: Center-focused, hero shot
- Background: Clean, solid or subtle gradient
- Product takes 60% of section width
- Professional product photography style
- Slight shadow for depth (not floating)

SIDE PANELS (flanking product):
- Left & Right: Circular badges with icons
  Badge 1: "⭐ {product['rating']}" (rating)
  Badge 2: "💰 {product['price']}" (price)
  Badge 3: "✓ {features[0]}" (key feature 1)
  Badge 4: "✓ {features[1]}" (key feature 2)
  Badge 5: "🔥 {product['discount']}% OFF" (if applicable)

BOTTOM SECTION (25% of height):
- Feature list area (text space):
  "Why it's great:"
  "✓ {features[0]}"
  "✓ {features[1]}"
  "✓ {features[2]}"
  "Perfect for: {product['use_cases']}"
- Call-to-action area: "Full specs & buy link ↓"

VISUAL STYLE:
- Clean and organized (Pinterest users are researchers)
- High information density but not cluttered
- Scannable at a glance
- Professional but approachable
- Colors: Brand-appropriate + high contrast

TYPOGRAPHY:
- Headline: Bold, large (40pt equivalent)
- Features: Medium (24pt equivalent)
- Price: Large, attention-grabbing
- Consistent spacing, easy to read

Product prominence: 50% of visual attention (info is equally important)
Overall vibe: "Complete review + guide"
```

**Example Outputs:**

```
# ELECTRONICS (Keyboard)
Professional product infographic, vertical 2:3 format:

TOP (25%):
- Background: Deep blue (#2C5F8D)
- Text: "Best Wireless Keyboard Under ₹1000 in 2026"
- Subtitle: "Zebronics Companion 304 Complete Review"
- Font: Sans-serif bold, white text

MIDDLE (50%):
- THIS EXACT keyboard+mouse from reference
- Clean white background
- Product centered, professional photography
- Slight drop shadow for depth

SIDE BADGES (6 circular badges):
Left column:
- ⭐ 4.0 Rating
- 🎯 Wireless 2.4GHz
- ⌨️ UV-Printed Keys

Right column:
- 💰 ₹749
- 🔥 50% OFF
- ✓ 1-Year Warranty

BOTTOM (25%):
Background: Light grey
Text: 
"Why Zebronics Companion 304?"
✓ Wireless freedom - no cable clutter
✓ Full-size layout - comfortable typing
✓ Retractable receiver - no dongles lost
✓ UV-printed keys - long-lasting design
✓ Spill-resistant - built for daily use

Perfect for: WFH professionals, students, home offices

"Complete specs & best price ↓"
"#WorkFromHome #Keyboard #Deals"

Style: Clean, information-focused, Pinterest-friendly
```

```
# HOME APPLIANCE (Refrigerator)
Professional product infographic, vertical 2:3 format:

TOP (25%):
- Background: Fresh green (#4CAF50)
- Text: "Best Single-Door Refrigerator Under ₹20,000"
- Subtitle: "Samsung 223L Direct Cool - Complete Guide"

MIDDLE (50%):
- THIS EXACT Samsung refrigerator from reference
- Clean white background
- Product: Clear view of doors and design

BADGES (6 circular):
Left:
- ⭐ 3.5 Rating
- ❄️ 223 Liter
- ⚡ Direct Cool

Right:
- 💰 ₹18,990
- 🔥 26% OFF  
- 🛡️ 1Y+9Y Warranty

BOTTOM (25%):
"Why Samsung RR24C2723S8?"
✓ Stabilizer-free operation (voltage protection)
✓ 5-liter chiller section (extra cold storage)
✓ Base stand drawer (vegetable storage)
✓ Direct cool technology (lower power bills)
✓ 223L capacity (perfect for 2-3 people)

Perfect for: Small families, budget-conscious, first home

Energy rating: 3★ | Power: ~200W/day
"Full comparison & buy link ↓"
"#Refrigerator #HomeAppliances #Samsung"
```

```
# MOBILE ACCESSORY (Power Bank)
Professional product infographic, vertical 2:3 format:

TOP (25%):
- Background: Orange gradient (#FF6B35 to #F7931E)
- Text: "Best Power Bank for Heavy Users - 2026"
- Subtitle: "Anker PowerCore 20000mAh Review"

MIDDLE (50%):
- THIS EXACT Anker power bank from reference
- Clean surface with phone beside it (scale reference)
- Product clearly visible

BADGES (6 circular):
Left:
- ⭐ 4.5 Rating
- ⚡ 20000mAh
- 📱 2 Ports

Right:
- 💰 ₹2,999
- 🔥 25% OFF
- ✓ 18-Month

BOTTOM (25%):
"Why Anker PowerCore 20000?"
✓ 20,000mAh - charge phone 4-5 times
✓ Fast charging - PowerIQ technology
✓ Dual ports - charge 2 devices simultaneously
✓ Compact design - fits in pocket/bag
✓ Anker reliability - premium build quality

Perfect for: Travelers, heavy users, long commutes, outdoor

Charges: iPhone 14 (4x), Galaxy S23 (3.5x)
"Reviews & best price ↓"
"#PowerBank #Anker #TravelEssentials"
```

---

## 🎯 THE SMART PROMPT GENERATOR (Code)

```python
class ProfessionalPromptGenerator:
    """
    Generates designer-quality prompts based on product analysis
    """
    
    def __init__(self):
        # Problem/solution mappings for before/after
        self.problem_solutions = {
            'keyboard': {
                'problem': 'Tangled cables, cramped desk, wrist strain',
                'scene': 'Cluttered home office with wired keyboard',
                'emotion': 'frustrated',
                'solution_emotion': 'relaxed and productive',
                'hook_text': 'CUT THE CABLES'
            },
            'refrigerator': {
                'problem': 'Food spoilage, high electricity, old appliance',
                'scene': 'Opening yellowed old refrigerator',
                'emotion': 'disgusted',
                'solution_emotion': 'satisfied and proud',
                'hook_text': 'UPGRADE YOUR KITCHEN'
            },
            'power_bank': {
                'problem': 'Phone dying, missing calls, battery anxiety',
                'scene': 'Phone at 2% during important moment',
                'emotion': 'anxious and stressed',
                'solution_emotion': 'relieved and confident',
                'hook_text': 'NEVER MISS A MOMENT'
            },
            'headphones': {
                'problem': 'Noise pollution, distraction, poor sound',
                'scene': 'Noisy environment, person distracted',
                'emotion': 'annoyed',
                'solution_emotion': 'focused and immersed',
                'hook_text': 'FIND YOUR FOCUS'
            }
        }
        
        # Aesthetic mappings for Instagram
        self.aesthetics = {
            'tech': {
                'surface': 'Light oak wooden desk',
                'colors': 'Warm neutrals (beige, white, light wood)',
                'item_1': 'Laptop (closed, silver/space grey)',
                'item_2': 'Coffee cup (white ceramic with coffee)',
                'item_3': 'Succulent plant in minimal pot',
                'mood': 'Productive morning, focused creativity'
            },
            'home_appliance': {
                'surface': 'Modern kitchen counter',
                'colors': 'Clean whites, stainless steel accents',
                'item_1': 'Fresh vegetables in basket',
                'item_2': 'Glass of water with condensation',
                'item_3': 'Kitchen towel or herb plant',
                'mood': 'Fresh start, healthy living'
            },
            'fashion': {
                'surface': 'Concrete or light fabric background',
                'colors': 'Urban cool (greys, blacks, accent colors)',
                'item_1': 'Magazine or book',
                'item_2': 'Sunglasses',
                'item_3': 'Phone or accessories',
                'mood': 'Style-conscious, urban lifestyle'
            }
        }
        
        # Category colors for Pinterest
        self.category_colors = {
            'electronics': '#2C5F8D',  # Trust blue
            'home_appliance': '#4CAF50',  # Fresh green
            'fashion': '#FF6B9D',  # Stylish pink
            'mobile_accessory': '#FF6B35',  # Energetic orange
            'kitchen': '#8BC34A',  # Food green
            'beauty': '#E91E63',  # Beauty pink
        }
    
    def detect_category(self, product_title):
        """Detect product category from title"""
        title_lower = product_title.lower()
        
        if any(kw in title_lower for kw in ['keyboard', 'mouse', 'headphone', 'speaker']):
            return 'keyboard' if 'keyboard' in title_lower else 'headphones'
        elif any(kw in title_lower for kw in ['refrigerator', 'fridge', 'oven', 'microwave']):
            return 'refrigerator'
        elif any(kw in title_lower for kw in ['power bank', 'charger', 'battery']):
            return 'power_bank'
        else:
            return 'generic'
    
    def generate_twitter_prompt(self, product):
        """Generate professional Twitter prompt"""
        category = self.detect_category(product['title'])
        ps = self.problem_solutions.get(category, self.problem_solutions['power_bank'])
        
        return f"""Professional marketing split-screen photograph, 16:9 landscape format:

LEFT SIDE (Problem - 45%):
- {ps['scene']}
- {ps['problem']} clearly visible
- Person showing {ps['emotion']} expression
- Environment: Cluttered/stressful
- Lighting: Dim, muted colors
- Mood: Relatable struggle

DIVIDER (10%):
- Subtle vertical line or arrow
- Text space: "{ps['hook_text']}"

RIGHT SIDE (Solution - 45%):
- Same setting transformed
- THIS EXACT {product['title']} from reference image in use
- Same person now {ps['solution_emotion']}
- Environment: Clean, organized
- Lighting: Bright natural light
- Mood: Problem solved

Product: Right side, naturally integrated
Style: Lifestyle photography, relatable
Vibe: Before/after transformation

CRITICAL: Product from reference image must be EXACTLY preserved (img2img strength 0.65)
Only change context and environment, NOT the product itself!"""
    
    def generate_instagram_prompt(self, product):
        """Generate professional Instagram prompt"""
        # Detect aesthetic category
        title_lower = product['title'].lower()
        
        if any(kw in title_lower for kw in ['keyboard', 'mouse', 'tech', 'laptop']):
            aes = self.aesthetics['tech']
        elif any(kw in title_lower for kw in ['refrigerator', 'kitchen', 'oven']):
            aes = self.aesthetics['home_appliance']
        else:
            aes = self.aesthetics['fashion']
        
        return f"""Top-down aesthetic flat lay photograph, square 1:1 format:

SCENE:
- View: Bird's eye, 90° overhead
- Surface: {aes['surface']}
- Lighting: Soft natural window light, gentle shadows
- Palette: {aes['colors']}

CENTER-RIGHT (Rule of thirds):
- THIS EXACT {product['title']} from reference image
- Naturally placed, not forced
- Clearly visible but not ad-like

COMPLEMENTARY ITEMS:
- Top-left: {aes['item_1']}
- Bottom-left: {aes['item_2']}
- Right: {aes['item_3']}
- Optional natural elements

SPACING:
- 70% surface visible (breathing room)
- Balanced but natural arrangement

STYLE:
- Instagram aesthetic: Curated but real
- Lived-in feeling (coffee in cup, notebook open)
- NOT catalog/studio look

MOOD: {aes['mood']}
Vibe: "This could be my space"

CRITICAL: Preserve EXACT product from reference (img2img 0.65)"""
    
    def generate_pinterest_prompt(self, product):
        """Generate professional Pinterest prompt"""
        category = self.detect_category(product['title'])
        color = self.category_colors.get('electronics', '#2C5F8D')
        
        features = product.get('features', [])[:5]
        features_text = '\n'.join([f'✓ {f}' for f in features])
        
        return f"""Professional product infographic, vertical 2:3 format:

TOP SECTION (25%):
- Background: {color}
- Bold text: "Best {product['title']} Under ₹{product.get('price', 'X')} - 2026"
- Subtitle: Complete Review & Guide
- Font: Bold sans-serif, white text

MIDDLE SECTION (50%):
- THIS EXACT {product['title']} from reference image
- Clean white/gradient background
- Product centered, professional photography
- Slight shadow for depth

SIDE BADGES (6 circular icons):
Left column:
- ⭐ {product.get('rating', 'N/A')} Rating
- First key feature icon
- Second key feature icon

Right column:
- 💰 ₹{product.get('price', 'X')}
- 🔥 {product.get('discount', 'X')}% OFF
- ✓ Warranty/guarantee badge

BOTTOM SECTION (25%):
Background: Light grey
"Why {product['title'].split()[0]}?"
{features_text if features else '✓ High quality\n✓ Great value\n✓ Reliable brand'}

Perfect for: [Target users]
CTA: "Full specs & buy link ↓"
Hashtags: #{category} #deals #shopping

STYLE: Information-rich, scannable, Pinterest-optimized

CRITICAL: Product from reference EXACTLY preserved (img2img 0.65)"""
    
    def generate_all_prompts(self, product):
        """Generate all 3 platform prompts"""
        return {
            'twitter': self.generate_twitter_prompt(product),
            'instagram': self.generate_instagram_prompt(product),
            'pinterest': self.generate_pinterest_prompt(product)
        }

# Usage
generator = ProfessionalPromptGenerator()

product = {
    'title': 'Zebronics Wireless Keyboard & Mouse Combo',
    'price': '749',
    'discount': '50',
    'rating': '4.0',
    'features': [
        'Wireless 2.4GHz connectivity',
        'UV-Printed keys',
        'Retractable USB receiver',
        'Spill-resistant design'
    ]
}

prompts = generator.generate_all_prompts(product)

print("TWITTER PROMPT:")
print(prompts['twitter'])
print("\n" + "="*60 + "\n")
print("INSTAGRAM PROMPT:")
print(prompts['instagram'])
print("\n" + "="*60 + "\n")
print("PINTEREST PROMPT:")
print(prompts['pinterest'])
```

---

## ✅ THIS IS WORLD-CLASS MARKETING DESIGN!

**Based on:**
- ✅ Real designer psychology
- ✅ Platform-specific user behavior
- ✅ Proven design patterns
- ✅ Professional composition principles
- ✅ Color psychology
- ✅ Conversion optimization

**Not just "AI makes pretty picture" - this is STRATEGIC MARKETING DESIGN!** 🎨🚀
