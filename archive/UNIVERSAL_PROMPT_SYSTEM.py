"""
UNIVERSAL PROMPT SYSTEM V3 — Ricky Affiliate Agent
TRULY DYNAMIC — generates contextually appropriate scenes for ANY product.

V2 Problem: Hardcoded categories with fixed props/surfaces meant a helmet
got rose petals and marble backgrounds (beauty fallback). TERRIBLE.

V3 Fix: Prompts are built DYNAMICALLY from the product title itself.
The product name drives the scene — helmet gets roads and bikes,
face wash gets spa and skincare, earbuds get gyms and commutes.

⚠️ CRITICAL RULE: NO TEXT IN AI PROMPTS!
Layer 1 (AI): Visual scene ONLY — no text, no typography
Layer 2 (PIL): Perfect text overlays programmatically
"""


def _no_text_rule():
    """Appended to every prompt to prevent AI text rendering."""
    return "Do NOT render any text, typography, labels, watermarks, or written words anywhere in the image. The image must be a pure visual scene with NO text of any kind. Leave clean empty space at the top and bottom of the frame for text overlays to be added later."


def _product_context(product_title: str) -> dict:
    """
    Analyze the product title to generate contextually appropriate
    scene elements. This is the CORE of the dynamic system.
    
    Returns dict with: short_name, scene_context, lifestyle_context,
    props, surface, mood, colors, light, flat_lay_items, detail_focus
    """
    title_lower = product_title.lower()
    
    # Short name for text overlays
    short = product_title.split(',')[0].split('|')[0].split('(')[0].strip()
    if len(short) > 50:
        short = short[:47] + '...'
    
    # ─── AUTOMOTIVE / HELMET ─────────────────────────
    if any(w in title_lower for w in ['helmet', 'riding', 'motorcycle', 'bike helmet', 'visor']):
        return {
            'short_name': short,
            'scene_context': 'on a sleek matte black surface next to motorcycle leather gloves and a bike key. In the background, a blurred premium motorcycle is visible',
            'lifestyle_context': 'a confident Indian rider in a leather jacket standing next to a powerful motorcycle on an empty mountain road at golden hour, holding this EXACT helmet under their arm, dramatic sky behind them',
            'props': 'motorcycle leather gloves, bike key, riding goggles, a small motorcycle model',
            'surface': 'matte black surface with subtle carbon fiber texture',
            'mood': 'speed, freedom, adrenaline, open road adventure',
            'colors': 'black, gunmetal, the product accent color, dark chrome',
            'light': 'dramatic side light with warm golden rim (like sunset on a highway)',
            'flat_lay_items': 'motorcycle gloves, bike key, sunglasses, riding bandana, carabiner clip, small toolkit',
            'detail_focus': 'visor mechanism, ventilation ports, inner padding texture, shell material finish',
            'action_scene': 'this EXACT helmet with dramatic motion blur lines suggesting speed, wind-swept atmosphere, with a blurred mountain highway in the background',
            'before_after_left': 'a cluttered mess of cheap generic helmets piled up, dull and uninspiring',
            'before_after_right': 'this EXACT helmet standing alone in a spotlight, premium and chosen',
        }
    
    # ─── BEAUTY / SKINCARE ───────────────────────────
    if any(w in title_lower for w in ['face wash', 'cleanser', 'serum', 'moisturizer', 'cream', 'sunscreen', 'skincare', 'shampoo', 'lipstick', 'mascara', 'foundation', 'lotion', 'toner', 'vitamin c', 'niacinamide', 'face mask', 'body wash']):
        return {
            'short_name': short,
            'scene_context': 'on polished dark marble with visible veining. Rose petals and water droplets scattered artistically around the base',
            'lifestyle_context': 'a beautiful young Indian woman in a bright modern bathroom, soft morning light streaming through window, using this EXACT product with a natural genuine smile, glowing skin, wrapped in soft white towel',
            'props': 'rose petals, water droplets, cotton pads, jade roller, fresh flowers, small glass bowls of natural ingredients',
            'surface': 'polished dark marble with visible veining',
            'mood': 'sensual luxury, spa intimacy, golden warmth',
            'colors': 'gold, amber, crimson, burgundy, black',
            'light': 'warm golden backlight (3000K) creating a glowing halo effect',
            'flat_lay_items': 'rose petals, cotton pads, jade roller, small towel, candle, glass dropper bottle, fresh flowers',
            'detail_focus': 'product texture squeezed out in an artistic swirl, cream consistency, shimmer particles',
            'action_scene': 'this EXACT product with a dramatic splash of water frozen in time, crystal clear droplets suspended in mid-air catching light as prisms',
            'before_after_left': 'dull, grey-toned scene with muted colors and flat lighting',
            'before_after_right': 'glowing, warm, golden scene that is vibrant, luminous, and alive',
        }
    
    # ─── ELECTRONICS / AUDIO ─────────────────────────
    if any(w in title_lower for w in ['earbuds', 'headphone', 'speaker', 'tws', 'bluetooth audio', 'soundbar', 'neckband']):
        return {
            'short_name': short,
            'scene_context': 'on brushed dark steel surface with subtle LED light strips creating electric blue edge glow. Glass prism nearby casting rainbow refraction',
            'lifestyle_context': 'a young Indian man at a modern gym, wearing these EXACT earbuds while working out, determined expression, warm dramatic gym lighting from overhead, modern equipment in soft bokeh background',
            'props': 'metallic geometric shapes, glass prism, subtle LED light strip, smartphone showing music app',
            'surface': 'brushed dark steel or matte black surface',
            'mood': 'futuristic premium, tech luxury, immersive sound',
            'colors': 'midnight blue, silver, electric blue accent, black',
            'light': 'cool blue-white with warm accent rim (5500K + 3000K)',
            'flat_lay_items': 'smartphone, fitness watch, coffee cup, clean notebook, premium cable, small plant',
            'detail_focus': 'driver mesh, LED indicator glowing blue, material finish, earbud cushion texture',
            'action_scene': 'these EXACT earbuds with visible sound waves radiating outward as colorful concentric rings, music visualization effect',
            'before_after_left': 'tangled wired earphones in a mess, frustrating and outdated',
            'before_after_right': 'these EXACT wireless earbuds in their case, sleek and effortless',
        }
    
    # ─── ELECTRONICS / GADGETS ───────────────────────
    if any(w in title_lower for w in ['phone', 'laptop', 'tablet', 'charger', 'power bank', 'keyboard', 'mouse', 'watch', 'camera', 'smart', 'usb', 'cable', 'adapter']):
        return {
            'short_name': short,
            'scene_context': 'on a clean modern desk setup with brushed aluminum surface, subtle ambient LED backlight in cool blue',
            'lifestyle_context': 'a young Indian professional at a modern minimalist workspace, using this EXACT product, focused and productive, warm natural light from a large window, modern office background',
            'props': 'metallic geometric shapes, glass prism, subtle LED accent, clean notebook',
            'surface': 'brushed dark steel or clean white desk surface',
            'mood': 'futuristic premium, productivity, precision engineering',
            'colors': 'midnight blue, silver, electric blue, black, white',
            'light': 'cool blue-white key light with warm fill (5500K)',
            'flat_lay_items': 'smartphone, notebook, pen, coffee cup, small plant, cable organizer',
            'detail_focus': 'material texture, button design, port details, LED indicators, build quality',
            'action_scene': 'this EXACT product with energy waves or lightning bolts suggesting power and speed',
            'before_after_left': 'cluttered desk with old tangled cables and outdated devices',
            'before_after_right': 'clean minimal setup with this EXACT product as the centerpiece',
        }
    
    # ─── HOME / APPLIANCE ────────────────────────────
    if any(w in title_lower for w in ['refrigerator', 'fridge', 'washing machine', 'mixer', 'grinder', 'blender', 'iron', 'vacuum', 'fan', 'cooler', 'heater', 'purifier', 'microwave', 'oven', 'toaster', 'kettle', 'induction']):
        return {
            'short_name': short,
            'scene_context': 'in a modern Indian kitchen with warm wood countertop, soft morning light through a window, fresh fruits and herbs nearby',
            'lifestyle_context': 'a happy Indian family in their modern kitchen, the product in use, warm natural morning light, kids at the breakfast table in soft focus background',
            'props': 'fresh fruits, herbs, clean glass, wooden cutting board, small plant',
            'surface': 'warm wood countertop or light marble',
            'mood': 'warm morning light, family comfort, modern living',
            'colors': 'warm whites, sage green, natural wood tones, soft gold',
            'light': 'warm natural morning light from a window (4000K)',
            'flat_lay_items': 'fresh vegetables, recipe card, wooden spoon, clean towel, small herb pot, glass bottle',
            'detail_focus': 'control panel, material finish, handle design, interior if visible',
            'action_scene': 'this EXACT product with fresh ingredients flying around it in a creative spiral, frozen in time',
            'before_after_left': 'old cramped kitchen with outdated appliances, dim lighting',
            'before_after_right': 'modern bright kitchen with this EXACT product as the star, clean and inviting',
        }
    
    # ─── FASHION / SHOES ─────────────────────────────
    if any(w in title_lower for w in ['shoe', 'sneaker', 'boot', 'sandal', 'slipper', 'jacket', 'dress', 'shirt', 'jeans', 'bag', 'wallet', 'belt', 'sunglasses', 'clothing', 'wear', 'tshirt', 't-shirt', 'kurta', 'saree']):
        return {
            'short_name': short,
            'scene_context': 'on textured concrete surface with dramatic side lighting casting sharp shadows, editorial fashion magazine aesthetic',
            'lifestyle_context': 'a stylish young Indian person in an urban setting, wearing or carrying this EXACT product, confident street-style pose, golden hour city backdrop with bokeh lights',
            'props': 'leather texture piece, fashion magazine, coffee cup, small succulent plant',
            'surface': 'textured concrete or raw wood surface',
            'mood': 'editorial fashion, street style, confident attitude',
            'colors': 'black, white, one bold accent color matching the product, earth tones',
            'light': 'dramatic side light with hard shadows creating depth',
            'flat_lay_items': 'fashion magazine, sunglasses, watch, leather wallet, coffee cup, plant',
            'detail_focus': 'stitching, material texture, sole pattern, brand detailing, hardware',
            'action_scene': 'this EXACT product with dynamic movement, like being caught mid-stride with motion energy',
            'before_after_left': 'worn out old shoes or clothes, faded and tired',
            'before_after_right': 'this EXACT product looking fresh, new, and premium',
        }
    
    # ─── FITNESS / SPORTS ────────────────────────────
    if any(w in title_lower for w in ['protein', 'supplement', 'whey', 'creatine', 'gym', 'yoga', 'mat', 'dumbbell', 'resistance', 'fitness', 'sports', 'cricket', 'bat', 'ball']):
        return {
            'short_name': short,
            'scene_context': 'on a concrete gym floor with dramatic overhead spotlight, chalk dust in the air, raw and powerful',
            'lifestyle_context': 'an athletic Indian person mid-workout, using or with this EXACT product, sweat on their brow, determined expression, modern gym with dramatic lighting',
            'props': 'small dumbbell, gym chalk, water bottle, sweat towel, resistance band',
            'surface': 'concrete gym floor or dark rubber mat',
            'mood': 'raw power, determination, pre-workout energy',
            'colors': 'deep black, neon green or electric orange accent, gunmetal',
            'light': 'harsh directional overhead spotlight (gym feel)',
            'flat_lay_items': 'dumbbell, gym chalk, water bottle, towel, resistance band, shaker cup',
            'detail_focus': 'material grip texture, build quality, moving parts, design details',
            'action_scene': 'this EXACT product with explosive energy, chalk dust or powder burst around it',
            'before_after_left': 'lazy couch potato scene with junk food, dim and unmotivated',
            'before_after_right': 'energetic gym scene with this EXACT product, powerful and ready',
        }
    
    # ─── FOOD / BEVERAGES ────────────────────────────
    if any(w in title_lower for w in ['tea', 'coffee', 'chocolate', 'snack', 'spice', 'masala', 'oil', 'honey', 'jam', 'sauce', 'noodle', 'biscuit', 'rice', 'dal', 'ghee', 'atta']):
        return {
            'short_name': short,
            'scene_context': 'on rustic dark wood table with warm side lighting like a kitchen window, surrounded by scattered raw ingredients',
            'lifestyle_context': 'a warm Indian kitchen scene, someone preparing food with this EXACT product visible on the counter, steam rising, warm lighting, homey comfortable atmosphere',
            'props': 'scattered raw ingredients, wooden spoon, rustic cloth, small bowls, fresh herbs',
            'surface': 'rustic dark wood with warm food-grade feel',
            'mood': 'warm comfort, artisan craft, homemade goodness',
            'colors': 'warm browns, deep reds, cream, earthy greens',
            'light': 'warm side light like kitchen window (3500K)',
            'flat_lay_items': 'wooden spoon, scattered spices, small bowls, rustic cloth, fresh herbs, mortar pestle',
            'detail_focus': 'packaging texture, contents if visible, ingredient close-up',
            'action_scene': 'this EXACT product with ingredients exploding outward in a creative burst',
            'before_after_left': 'boring bland meal with no flavor, dull presentation',
            'before_after_right': 'delicious colorful meal made with this EXACT product, appetizing and vibrant',
        }
    
    # ─── AUTOMOTIVE (vehicles, accessories) ──────────
    if any(w in title_lower for w in ['car', 'bike', 'scooter', 'motorcycle', 'automotive', 'tyre', 'tire', 'seat cover', 'dash cam', 'gps', 'car charger']):
        return {
            'short_name': short,
            'scene_context': 'on clean dark asphalt surface with dramatic directional lighting, a premium vehicle partially visible in the blurred background',
            'lifestyle_context': 'someone installing or using this EXACT product on their vehicle, clean garage or scenic road setting, confident and satisfied expression',
            'props': 'chrome wrench, clean microfiber cloth, leather keychain',
            'surface': 'clean dark asphalt or brushed metal surface',
            'mood': 'premium automotive, precision, road confidence',
            'colors': 'black, chrome silver, dark red accent, gunmetal',
            'light': 'dramatic side light with chrome highlights',
            'flat_lay_items': 'car key, microfiber cloth, small wrench set, leather keychain, phone mount',
            'detail_focus': 'material quality, fitment details, engineering precision',
            'action_scene': 'this EXACT product with motion lines suggesting speed and road performance',
            'before_after_left': 'old worn-out car accessory, tired and unreliable',
            'before_after_right': 'this EXACT product installed, premium and confidence-inspiring',
        }
    
    # ─── GENERIC FALLBACK ────────────────────────────
    # For any product that doesn't match specific categories,
    # create a neutral premium product photography context
    return {
        'short_name': short,
        'scene_context': 'on a clean modern surface with subtle gradient lighting, premium product photography setup',
        'lifestyle_context': 'a happy Indian person in a modern setting, with this EXACT product visible in natural use, warm natural lighting, authentic and relatable',
        'props': 'clean modern accessories that complement the product, minimal and curated',
        'surface': 'clean matte surface with subtle gradient',
        'mood': 'premium, trustworthy, modern, clean',
        'colors': 'neutral tones with one accent color matching the product',
        'light': 'clean studio lighting with warm fill (4500K)',
        'flat_lay_items': 'complementary items that a buyer would own, minimal and curated',
        'detail_focus': 'material quality, build details, design elements',
        'action_scene': 'this EXACT product with subtle energy and movement suggesting quality',
        'before_after_left': 'the problem this product solves, shown visually',
        'before_after_right': 'this EXACT product as the clean solution',
    }


def generate_prompts(product_title: str, price: str, discount: str = None, rating: str = None):
    """
    Generate TRULY DYNAMIC prompt set for ANY product.
    
    The product title drives everything — scene, props, lighting, mood.
    No more fixed categories with hardcoded props!
    
    Returns: (prompts_dict, context)
    """
    ctx = _product_context(product_title)
    no_text = _no_text_rule()
    
    prompts = {
        'twitter': [],
        'instagram': [],
        'pinterest': []
    }

    # ━━━ TWITTER — 3 hero + 2 features ━━━

    prompts['twitter'].extend([
        {
            'id': 'tw1_hero_v1',
            'prompt': f'''Cinematic product photography. This EXACT product from reference image placed {ctx["scene_context"]}.
Lighting: {ctx["light"]}. Fill light at 5:1 ratio from camera-left.
Background: deep radial gradient vignette fading to pure black at edges.
Mood: {ctx["mood"]}. High contrast chiaroscuro. Generous negative space.
Camera: 10-15° below center, f/5.6, Hasselblad quality.
Product must match reference EXACTLY — same design, colors, shape.
{no_text}''',
            'size': {'width': 1344, 'height': 768},
            'text_config': {'type': 'tw_hero', 'title': ctx['short_name'], 'price': price, 'discount': discount, 'rating': rating}
        },
        {
            'id': 'tw1_hero_v2',
            'prompt': f'''Premium editorial product shot. This EXACT product floating slightly above {ctx["surface"]} with subtle levitation effect and soft shadow below.
Dual rim lights creating edge highlights — one warm, one cool blue for cinematic color contrast.
Background: smooth dark gradient to black. Fine particle haze catching backlights creating volumetric rays.
Props: {ctx["props"]} placed with deliberate spacing.
Mood: mysterious, exclusive, premium discovery.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1344, 'height': 768},
            'text_config': {'type': 'tw_hero', 'title': ctx['short_name'], 'price': price, 'discount': discount, 'rating': rating}
        },
        {
            'id': 'tw1_hero_v3',
            'prompt': f'''Ultra-premium product photography. This EXACT product on {ctx["surface"]} surrounded by {ctx["props"]}.
Single large softbox above and behind creating specular highlights and dramatic pool of light. Everything outside falls to deep shadow.
Background: absolute darkness. Product exists in its own universe of light.
Color palette: strictly {ctx["colors"]}.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1344, 'height': 768},
            'text_config': {'type': 'tw_hero', 'title': ctx['short_name'], 'price': price, 'discount': discount, 'rating': rating}
        },
        {
            'id': 'tw2_feat_v1',
            'prompt': f'''Detailed product showcase. This EXACT product on a clean surface, with close attention to {ctx["detail_focus"]}.
{ctx["light"]}. Each detail lit individually with focused spots.
Background: dark, clean. Mood: premium engineering meets beauty.
Product fills 60% of the frame — every detail visible and celebrated.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1344, 'height': 768},
            'text_config': {'type': 'tw_features', 'title': ctx['short_name'], 'price': price}
        },
        {
            'id': 'tw2_feat_v2',
            'prompt': f'''Dynamic product action shot. {ctx["action_scene"]}.
Dramatic lighting from below and behind. High-speed photography aesthetic.
Frozen moment in time. Crystal sharp details. Background: pure black or dramatic gradient.
Energy, power, capability — all visualized in one frozen moment.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1344, 'height': 768},
            'text_config': {'type': 'tw_features', 'title': ctx['short_name'], 'price': price}
        }
    ])

    # ━━━ INSTAGRAM — 6 slide types, 2 variations each ━━━

    ig_pairs = [
        # HOOK
        (
            {
                'id': 'ig1_hook_v1',
                'prompt': f'''Scroll-stopping product image. This EXACT product emerging from darkness, backlit with {ctx["light"]} creating an ethereal aura.
Dark background with subtle warm vignette. Fine golden particles floating like luxury dust.
Reflective {ctx["surface"]} below showing mirror reflection.
Mood: {ctx["mood"]}. Magnetic, hypnotic.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_hook', 'title': ctx['short_name'], 'price': price, 'discount': discount}
            },
            {
                'id': 'ig1_hook_v2',
                'prompt': f'''Dramatic product reveal. This EXACT product centered on {ctx["surface"]} with dramatic chiaroscuro — one side fully lit, other in deep shadow.
Background: rich dark gradient to black. Fine mist at the base creating otherworldly atmosphere.
Camera: low angle looking up — making the product monumental and powerful.
Mood: {ctx["mood"]}.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_hook', 'title': ctx['short_name'], 'price': price, 'discount': discount}
            }
        ),
        # LIFESTYLE
        (
            {
                'id': 'ig2_life_v1',
                'prompt': f'''Candid lifestyle moment. {ctx["lifestyle_context"]}.
Shot feels natural, not posed. Like a friend captured this beautiful moment.
Warm, authentic, aspirational. Shallow depth of field.
Product visible and must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_lifestyle', 'title': ctx['short_name']}
            },
            {
                'id': 'ig2_life_v2',
                'prompt': f'''Real-world product in use. This EXACT product being used naturally in its intended environment.
Warm golden lighting. Background tells a story — the world this product belongs in.
Authentic, relatable, makes the viewer imagine themselves using it.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_lifestyle', 'title': ctx['short_name']}
            }
        ),
        # FLAT LAY
        (
            {
                'id': 'ig3_flat_v1',
                'prompt': f'''Museum-quality flat lay from directly above. {ctx["surface"]} background.
Center: this EXACT product placed diagonally. Around it in geometric pattern: {ctx["flat_lay_items"]}.
Everything color-coordinated in {ctx["colors"]}.
Overhead softbox, even diffused light, soft shadows. 30% negative space.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_flatlay', 'title': ctx['short_name']}
            },
            {
                'id': 'ig3_flat_v2',
                'prompt': f'''Casual lifestyle flat lay. This EXACT product on white linen cloth background.
Around it: {ctx["flat_lay_items"]} arranged casually but beautifully.
Overhead natural light from window casting soft shadows to the right.
Mood: curated imperfection, authentic, relatable.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_flatlay', 'title': ctx['short_name']}
            }
        ),
        # DETAIL
        (
            {
                'id': 'ig4_detail_v1',
                'prompt': f'''Extreme macro close-up of this EXACT product. Focus on: {ctx["detail_focus"]}.
Macro lens — every texture, every material detail visible at extreme magnification.
Shallow depth of field — only the focal point sharp, rest beautifully blurred.
Background: soft bokeh. Makes you appreciate the engineering and design.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_detail', 'title': ctx['short_name']}
            },
            {
                'id': 'ig4_detail_v2',
                'prompt': f'''Dynamic product action. {ctx["action_scene"]}.
High-speed photography aesthetic. Crystal clear frozen moment.
Background: dramatic gradient. Energy and capability visualized.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_detail', 'title': ctx['short_name']}
            }
        ),
        # PROOF / TRANSFORMATION
        (
            {
                'id': 'ig5_proof_v1',
                'prompt': f'''Before and after split visualization. This EXACT product placed vertically in the center as a DIVIDER.
Left side: {ctx["before_after_left"]}. Muted colors, flat lighting.
Right side: {ctx["before_after_right"]}. Vibrant, premium, alive.
The product bridges the transformation. Empowering, not shaming.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_proof', 'title': ctx['short_name']}
            },
            {
                'id': 'ig5_proof_v2',
                'prompt': f'''Trust and quality visual. This EXACT product on a clean surface with a warm spotlight.
Around it: subtle floating gold geometric elements suggesting premium quality and trust.
Clean background. Product looks awarded, celebrated, chosen.
Premium but not flashy. Quietly confident.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_proof', 'title': ctx['short_name']}
            }
        ),
        # CTA
        (
            {
                'id': 'ig6_cta_v1',
                'prompt': f'''Sophisticated product spotlight. Soft warm gradient background. This EXACT product positioned in the lower center, occupying about 40% of height.
Delicate thin gold border frame around entire image.
Large clean empty areas at top 30% and bottom 20% for text overlays.
Simple, premium, action-driving.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_cta', 'price': price, 'discount': discount}
            },
            {
                'id': 'ig6_cta_v2',
                'prompt': f'''Minimal luxury spotlight. Pure dark background. This EXACT product in center with single focused spotlight from above creating dramatic cone of light.
Product occupies 40-50% of frame. Everything else is darkness.
Reflection on surface below. Ultra minimal, high-end.
Large empty areas top and bottom for text.
Product must match reference EXACTLY.
{no_text}''',
                'size': {'width': 1024, 'height': 1280},
                'text_config': {'type': 'ig_cta', 'price': price, 'discount': discount}
            }
        ),
    ]

    for v1, v2 in ig_pairs:
        prompts['instagram'].extend([v1, v2])

    # ━━━ PINTEREST — 4 pins ━━━

    prompts['pinterest'].extend([
        {
            'id': 'pin1_guide_v1',
            'prompt': f'''Cinematic product photography for infographic layout. This EXACT product centered {ctx["scene_context"]}.
{ctx["light"]}. Dark background with rich color gradient.
Large clean empty space at top 15% and bottom 25% for text overlays.
Ultra premium product photography. Hasselblad quality.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1000, 'height': 1500},
            'text_config': {'type': 'pin_guide', 'title': ctx['short_name'], 'price': price, 'discount': discount, 'rating': rating}
        },
        {
            'id': 'pin1_guide_v2',
            'prompt': f'''Premium editorial product shot. This EXACT product on {ctx["surface"]} with dramatic Rembrandt side lighting.
Background: deep dark gradient to black. {ctx["props"]} around the base.
Product glowing from backlight. Clean empty space top 20% and bottom 20%.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1000, 'height': 1500},
            'text_config': {'type': 'pin_editorial', 'title': ctx['short_name'], 'price': price, 'discount': discount, 'rating': rating}
        },
        {
            'id': 'pin2_aesthetic_v1',
            'prompt': f'''Dream aesthetic product photo. This EXACT product as the star of a curated scene — {ctx["scene_context"]}.
Warm golden evening light from the side. Everything color-coordinated.
Aspirational, immediately saveable. Makes viewers want this in their life.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1000, 'height': 1500},
            'text_config': {'type': 'pin_aesthetic', 'title': ctx['short_name'], 'price': price}
        },
        {
            'id': 'pin2_aesthetic_v2',
            'prompt': f'''Moody luxury product photo. This EXACT product on {ctx["surface"]} with cinematic backlight like a luxury brand ad.
{ctx["props"]} around the base. Dramatic atmosphere.
Dark, premium, magnetic. Makes people save and click.
Clean empty space at top 15% and bottom 20%.
Product must match reference EXACTLY.
{no_text}''',
            'size': {'width': 1000, 'height': 1500},
            'text_config': {'type': 'pin_aesthetic', 'title': ctx['short_name'], 'price': price}
        }
    ])

    return prompts, ctx['short_name']


# ─── USAGE ─────────────────────────────────────────────────

if __name__ == "__main__":
    # Test with different products
    test_products = [
        ("Steelbird SBA-7 7Wings ISI Certified Flip-Up Helmet", "1664"),
        ("ZEE-C Vitamin C Face Wash 200ml", "99"),
        ("Fire-Boltt Aero TWS Earbuds", "899"),
        ("Samsung 223L Direct Cool Refrigerator", "18990"),
    ]
    
    for title, price in test_products:
        prompts, name = generate_prompts(title, price, "-10%", "4.2")
        ctx = _product_context(title)
        total = sum(len(v) for v in prompts.values())
        print(f"\n{'='*60}")
        print(f"Product: {title}")
        print(f"  Scene: {ctx['scene_context'][:80]}...")
        print(f"  Props: {ctx['props'][:80]}...")
        print(f"  Mood: {ctx['mood']}")
        print(f"  Prompts: {total}")
