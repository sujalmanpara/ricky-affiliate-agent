"""
Professional Image Generator for Ricky Affiliate Agent
Implements research-backed design principles for scroll-stopping marketing banners
"""

import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import json
from typing import Dict, Tuple, List
from dataclasses import dataclass

@dataclass
class ProductData:
    """Product information for banner generation"""
    title: str
    price: str
    original_price: str = None
    discount_pct: int = 0
    rating: float = 0.0
    review_count: int = 0
    category: str = "general"
    top_feature: str = ""
    image_url: str = ""
    
class ProfessionalImageGenerator:
    """
    Generates scroll-stopping affiliate marketing banners
    Based on research-backed design principles and Skechers-level quality
    """
    
    # Color palettes by category
    COLOR_PALETTES = {
        'tech': {
            'bg': '#1a1a1a',
            'text': '#ffffff',
            'accent': '#2C5F8D',
            'price_bg': '#FF6B35'
        },
        'home': {
            'bg': '#f5f5f5',
            'text': '#333333',
            'accent': '#4CAF50',
            'price_bg': '#4CAF50'
        },
        'fashion': {
            'bg': '#000000',
            'text': '#ffffff',
            'accent': '#FFD700',
            'price_bg': '#FF6B9D'
        },
        'fitness': {
            'bg': '#0d1b2a',
            'text': '#ffffff',
            'accent': '#00b4d8',
            'price_bg': '#FF6B35'
        },
        'budget': {
            'bg': '#ffffff',
            'text': '#000000',
            'accent': '#FF0000',
            'price_bg': '#FF6B35'
        }
    }
    
    # Headline formulas
    HEADLINE_FORMULAS = {
        'problem_solve': [
            "Never {pain_point} Again",
            "Stop {pain_point}",
            "End {pain_point} Forever"
        ],
        'aspiration': [
            "Get the {benefit} You Deserve",
            "Feel {emotion}",
            "Be {desired_state}"
        ],
        'comparison': [
            "{good}. Not {bad}.",
            "Smart {category}. Not {negative}."
        ],
        'command': [
            "Upgrade Your {area}",
            "Transform Your {space}"
        ]
    }
    
    def __init__(self, font_path="/usr/share/fonts/truetype/dejavu"):
        self.font_path = font_path
        try:
            self.font_bold_lg = ImageFont.truetype(f"{font_path}/DejaVuSans-Bold.ttf", 60)
            self.font_bold_md = ImageFont.truetype(f"{font_path}/DejaVuSans-Bold.ttf", 48)
            self.font_bold_sm = ImageFont.truetype(f"{font_path}/DejaVuSans-Bold.ttf", 36)
            self.font_regular = ImageFont.truetype(f"{font_path}/DejaVuSans.ttf", 28)
        except:
            # Fallback to default
            self.font_bold_lg = self.font_bold_md = self.font_bold_sm = self.font_regular = ImageFont.load_default()
    
    def generate_headline(self, product: ProductData) -> str:
        """Generate emotional headline based on product category"""
        
        # Category-specific headline generation
        category_headlines = {
            'tech': "Never Die Mid-Day Again" if "power" in product.title.lower() or "battery" in product.title.lower()
                   else "Cut the Cable Chaos" if "wireless" in product.title.lower() or "bluetooth" in product.title.lower()
                   else "Upgrade Your Tech Game",
            
            'home': "Fresh Food. Happy Family." if "refrigerator" in product.title.lower() or "fridge" in product.title.lower()
                   else "Cook Smarter. Live Better." if "kitchen" in product.title.lower()
                   else "Transform Your Home",
            
            'fashion': "Look Good. Feel Great." if "shoes" in product.title.lower() or "clothing" in product.title.lower()
                      else "Style That Speaks",
            
            'fitness': "Feel Stronger. Run Faster." if "shoe" in product.title.lower() or "fitness" in product.title.lower()
                      else "Push Your Limits",
            
            'budget': f"{product.discount_pct}% OFF Today Only!" if product.discount_pct > 20
                     else "Best Deal of the Month"
        }
        
        return category_headlines.get(product.category, "Get It Now. Save Big.")
    
    def get_category_palette(self, category: str) -> Dict[str, str]:
        """Get color palette for product category"""
        return self.COLOR_PALETTES.get(category, self.COLOR_PALETTES['budget'])
    
    def download_image(self, url: str) -> Image.Image:
        """Download and prepare product image"""
        response = requests.get(url, timeout=15)
        img = Image.open(io.BytesIO(response.content))
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        return img
    
    def add_drop_shadow(self, draw: ImageDraw, position: Tuple[int, int], 
                       text: str, font: ImageFont, 
                       text_color: str, shadow_color: str = '#000000', 
                       offset: int = 2):
        """Add drop shadow to text for depth"""
        x, y = position
        
        # Draw shadow first (offset)
        draw.text((x + offset, y + offset), text, fill=shadow_color, font=font)
        
        # Draw main text
        draw.text((x, y), text, fill=text_color, font=font)
    
    def create_gradient_background(self, size: Tuple[int, int], 
                                   color1: str, color2: str) -> Image.Image:
        """Create gradient background"""
        # Simple horizontal gradient
        base = Image.new('RGB', size, color1)
        # In production, use PIL gradient library or implement proper gradient
        return base
    
    def create_twitter_banner(self, product: ProductData) -> Image.Image:
        """
        Generate Twitter/X banner (16:9 - 1200×675px)
        Design: Bold headline top-left, product center, price bottom-left, discount top-right
        """
        size = (1200, 675)
        palette = self.get_category_palette(product.category)
        
        # Download and prepare product image
        product_img = self.download_image(product.image_url)
        product_img.thumbnail((700, 500), Image.Resampling.LANCZOS)
        
        # Create base canvas
        canvas = Image.new('RGB', size, palette['bg'])
        
        # Paste product (centered)
        x_offset = (size[0] - product_img.width) // 2
        y_offset = (size[1] - product_img.height) // 2
        canvas.paste(product_img, (x_offset, y_offset))
        
        # Add dark overlay for text contrast (if light background)
        if palette['bg'].startswith('#f') or palette['bg'].startswith('#e'):
            overlay = Image.new('RGBA', size, (0, 0, 0, 80))
            canvas = Image.alpha_composite(canvas.convert('RGBA'), overlay).convert('RGB')
        
        draw = ImageDraw.Draw(canvas)
        
        # 1. HEADLINE (top-left, bold, emotional)
        headline = self.generate_headline(product)
        self.add_drop_shadow(draw, (40, 40), headline, 
                           self.font_bold_lg, palette['text'])
        
        # 2. PRICE BADGE (bottom-left, prominent)
        price_badge_width = 260
        price_badge_height = 90
        draw.rectangle([
            (20, size[1] - price_badge_height - 20),
            (20 + price_badge_width, size[1] - 20)
        ], fill=palette['price_bg'])
        
        draw.text((35, size[1] - price_badge_height + 15), 
                 f"₹{product.price}", 
                 fill='#ffffff', font=self.font_bold_lg)
        
        # 3. DISCOUNT BADGE (top-right, circular burst)
        if product.discount_pct > 0:
            badge_center = (size[0] - 80, 80)
            badge_radius = 60
            
            # Draw circle
            draw.ellipse([
                (badge_center[0] - badge_radius, badge_center[1] - badge_radius),
                (badge_center[0] + badge_radius, badge_center[1] + badge_radius)
            ], fill='#FF0000')
            
            # Draw text (centered in circle)
            disc_text = f"{product.discount_pct}%\nOFF"
            draw.text((badge_center[0] - 30, badge_center[1] - 20), 
                     disc_text, fill='#ffffff', font=self.font_bold_sm, align='center')
        
        return canvas
    
    def create_instagram_banner(self, product: ProductData) -> Image.Image:
        """
        Generate Instagram banner (1:1 - 1080×1080px)
        Design: Clean, centered product, minimal text, aspirational
        """
        size = (1080, 1080)
        palette = self.get_category_palette(product.category)
        
        # Use white or very light background for Instagram (clean aesthetic)
        bg_color = '#ffffff' if palette['bg'].startswith('#') and int(palette['bg'][1:3], 16) < 200 else palette['bg']
        
        # Download and prepare product image
        product_img = self.download_image(product.image_url)
        product_img.thumbnail((600, 600), Image.Resampling.LANCZOS)
        
        # Create canvas
        canvas = Image.new('RGB', size, bg_color)
        
        # Paste product (centered)
        x_offset = (size[0] - product_img.width) // 2
        y_offset = (size[1] - product_img.height) // 2
        canvas.paste(product_img, (x_offset, y_offset))
        
        draw = ImageDraw.Draw(canvas)
        
        # MINIMAL TEXT - just price badge (bottom-right, small)
        badge_width = 200
        badge_height = 70
        badge_x = size[0] - badge_width - 30
        badge_y = size[1] - badge_height - 30
        
        draw.rectangle([
            (badge_x, badge_y),
            (badge_x + badge_width, badge_y + badge_height)
        ], fill=palette['price_bg'])
        
        draw.text((badge_x + 15, badge_y + 15), 
                 f"₹{product.price}", 
                 fill='#ffffff', font=self.font_bold_sm)
        
        return canvas
    
    def create_pinterest_banner(self, product: ProductData) -> Image.Image:
        """
        Generate Pinterest banner (2:3 - 1000×1500px)
        Design: Info-rich, title banner top, product center, features bottom
        """
        size = (1000, 1500)
        palette = self.get_category_palette(product.category)
        
        # Download and prepare product image
        product_img = self.download_image(product.image_url)
        product_img.thumbnail((600, 900), Image.Resampling.LANCZOS)
        
        # Create canvas
        canvas = Image.new('RGB', size, '#ffffff')
        
        draw = ImageDraw.Draw(canvas)
        
        # 1. TOP BANNER (100px, category color, title)
        banner_height = 120
        draw.rectangle([(0, 0), (size[0], banner_height)], fill=palette['accent'])
        
        # Title text (truncated if needed)
        title = product.title[:40] + "..." if len(product.title) > 40 else product.title
        draw.text((20, 30), title, fill='#ffffff', font=self.font_bold_md)
        
        # 2. PRODUCT (center area)
        y_start_product = banner_height + 50
        product_area_height = 900
        
        x_offset = (size[0] - product_img.width) // 2
        y_offset = y_start_product + (product_area_height - product_img.height) // 2
        canvas.paste(product_img, (x_offset, y_offset))
        
        # 3. BOTTOM INFO SECTION (250px, dark bg, features)
        footer_height = 280
        footer_y = size[1] - footer_height
        draw.rectangle([(0, footer_y), (size[0], size[1])], fill='#333333')
        
        # Price (large)
        draw.text((40, footer_y + 25), f"₹{product.price}", 
                 fill='#ffffff', font=self.font_bold_lg)
        
        # Features (if available)
        features_y = footer_y + 110
        if product.top_feature:
            draw.text((40, features_y), f"✓ {product.top_feature[:50]}", 
                     fill='#ffffff', font=self.font_regular)
        
        # Star rating (if available)
        if product.rating > 0:
            stars = "★" * int(product.rating) + "☆" * (5 - int(product.rating))
            rating_text = f"{stars} ({product.review_count:,} reviews)"
            draw.text((40, features_y + 45), rating_text, 
                     fill='#FFD700', font=self.font_regular)
        
        return canvas
    
    def generate_all_platforms(self, product: ProductData) -> Dict[str, Image.Image]:
        """Generate banners for all 3 platforms"""
        return {
            'twitter': self.create_twitter_banner(product),
            'instagram': self.create_instagram_banner(product),
            'pinterest': self.create_pinterest_banner(product)
        }
    
    def save_banners(self, images: Dict[str, Image.Image], prefix: str = "banner"):
        """Save all generated banners"""
        for platform, img in images.items():
            filename = f"{prefix}_{platform}.jpg"
            img.save(filename, 'JPEG', quality=95)
            print(f"✅ Saved: {filename}")

# Example usage
if __name__ == "__main__":
    # Test with Samsung refrigerator
    product = ProductData(
        title="Samsung 183 L, 5 Star, Digital Inverter, Direct-Cool Single Door Refrigerator",
        price="16990",
        original_price="22990",
        discount_pct=26,
        rating=3.5,
        review_count=1247,
        category="home",
        top_feature="Stabilizer-free operation saves power bills",
        image_url="https://m.media-amazon.com/images/I/61ChcsEZsrL._SY879_.jpg"
    )
    
    generator = ProfessionalImageGenerator()
    images = generator.generate_all_platforms(product)
    generator.save_banners(images, prefix="pro_samsung")
    
    print("\n🎉 All professional banners generated!")
