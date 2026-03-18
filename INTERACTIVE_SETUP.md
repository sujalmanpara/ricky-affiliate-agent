# Ricky - Interactive First-Time Setup

## 🎯 THE SETUP EXPERIENCE

When user runs Ricky for the first time, it asks for all credentials interactively!

---

## 💬 INTERACTIVE SETUP FLOW

### First Run:

```bash
$ openclaw run ricky-affiliate-agent
```

**Ricky responds:**

```
🤖 Welcome to Ricky - AI Affiliate Marketing Automation!

I noticed this is your first time running Ricky.
Let me help you set up everything! ✨

This will take about 10 minutes.
I'll ask for a few API keys and credentials.

Ready to start? (yes/no): _
```

---

### Step 1: Amazon Associates

```
════════════════════════════════════════════════════════════
📦 STEP 1/4: Amazon Associates Setup
════════════════════════════════════════════════════════════

To earn money from affiliate marketing, you need an Amazon Associates account.

Do you have an Amazon Associates account? (yes/no): yes

Great! I need your affiliate tag and API credentials.

Your Affiliate Tag (e.g., yourname-21): counitinguniq-21
✅ Saved affiliate tag: counitinguniq-21

Now I need your Amazon Product Advertising API credentials.
These let me find trending products automatically.

Don't have API access yet? 
→ Visit: https://webservices.amazon.in/
→ Request access (usually approved instantly)

Amazon API Access Key: AKIAXXXXXXXXXX_
Amazon API Secret Key: ********************_

🔄 Validating credentials...
✅ Amazon Product API connected!
✅ Can search products: Yes
✅ Daily limit: 8,640 requests

Press Enter to continue...
```

---

### Step 2: Social Media

```
════════════════════════════════════════════════════════════
📱 STEP 2/4: Social Media Accounts
════════════════════════════════════════════════════════════

Ricky will post to your social media accounts to promote products.

How would you like to connect your social media?

1) Easy way - Use Postiz (recommended)
   → Connect all accounts in one place
   → Cost: $19/month
   → Setup time: 5 minutes

2) Advanced - Direct API setup (free)
   → Setup each platform separately
   → Cost: Free
   → Setup time: 30 minutes

Your choice (1/2): 1

Great! Let's use Postiz.

Step 1: Sign up at https://postiz.com/
Step 2: Connect your Twitter, Instagram, Pinterest accounts
Step 3: Get your API key from Settings → API

Have you completed these steps? (yes/no): yes

Your Postiz API Key: sk_postiz_xxxxxxxxxxxxxxxxx_
Your Postiz Workspace ID: workspace-xxxxx_

🔄 Validating Postiz connection...
✅ Postiz connected!

Connected accounts:
  ✅ Twitter: @yourhandle (5,234 followers)
  ✅ Instagram: @yourhandle (3,891 followers)
  ✅ Pinterest: @yourhandle (1,456 followers)

Total reach: 10,581 people ✨

Press Enter to continue...
```

---

### Step 3: Image Generation

```
════════════════════════════════════════════════════════════
🎨 STEP 3/4: AI Image Generation (Fal.ai)
════════════════════════════════════════════════════════════

Ricky generates professional marketing images using AI.
This requires a Fal.ai account.

Cost: ~$0.10 per image
→ 3 images per product = $0.30
→ 3 products per day = $0.90/day
→ ~$27/month

But you'll earn ₹25,000-35,000/month, so it's worth it! 💰

Step 1: Sign up at https://fal.ai/
Step 2: Add $10 credit (enough for 100 images)
Step 3: Get your API key from Dashboard → API Keys

Have you completed these steps? (yes/no): yes

Your Fal.ai API Key: 9b753dc2-xxxx-xxxx-xxxx-xxxxxxxxxxxx_

🔄 Validating Fal.ai connection...
✅ Fal.ai connected!
✅ Account balance: $10.00
✅ Seedream 5.0 model available

Estimated credits: ~100 images (33 products)

Press Enter to continue...
```

---

### Step 4: Preferences

```
════════════════════════════════════════════════════════════
⚙️ STEP 4/4: Your Preferences
════════════════════════════════════════════════════════════

Now let's configure what products you want to promote!

Which product categories interest you?
(Choose 1-5, separated by commas)

1. Electronics (keyboards, headphones, gadgets)
2. Home & Kitchen (appliances, cookware)
3. Fashion (clothing, accessories)
4. Beauty & Personal Care
5. Sports & Outdoors
6. Books
7. Toys & Games
8. Office Products

Your choices (e.g., 1,2,3): 1,2,3

Great! Selected:
  ✅ Electronics
  ✅ Home & Kitchen
  ✅ Fashion

What's your preferred price range for products?

Minimum price (₹): 500
Maximum price (₹): 5000

Perfect! I'll find products between ₹500-₹5,000.

How many products should I promote per day?

Products per day (1-5): 3

✅ I'll promote 3 products per day
✅ Across 3 platforms = 9 posts per day
✅ Total: 90 products per month

When should I post? (Times in IST)

Morning time (e.g., 10:00): 10:00
Afternoon time (e.g., 14:00): 14:00
Evening time (e.g., 18:00): 18:00

Perfect! Daily schedule:
  🌅 10:00 AM - Product 1
  ☀️ 02:00 PM - Product 2
  🌆 06:00 PM - Product 3

Press Enter to finalize setup...
```

---

### Final Confirmation

```
════════════════════════════════════════════════════════════
✅ SETUP COMPLETE!
════════════════════════════════════════════════════════════

Here's your configuration:

📦 AMAZON ASSOCIATES
   Tag: counitinguniq-21
   API: Connected ✅

📱 SOCIAL MEDIA (via Postiz)
   Twitter: @yourhandle ✅
   Instagram: @yourhandle ✅
   Pinterest: @yourhandle ✅
   Total reach: 10,581 followers

🎨 IMAGE GENERATION (Fal.ai)
   Credits: $10.00 (100 images)
   Model: Seedream 5.0

⚙️ AUTOMATION
   Products/day: 3
   Posts/day: 9
   Categories: Electronics, Home & Kitchen, Fashion
   Price range: ₹500-₹5,000
   Schedule: 10:00 AM, 2:00 PM, 6:00 PM

💰 ESTIMATED EARNINGS
   Month 1: ₹5,000-₹10,000
   Month 2: ₹15,000-₹25,000
   Month 3+: ₹30,000-₹50,000

════════════════════════════════════════════════════════════

Configuration saved to: ~/.ricky/config.yaml

Want to start the automation now? (yes/no): yes

🚀 Starting Ricky Automation...

✅ First product search scheduled for 10:00 AM today
✅ Cron job added: daily at 9:00 AM
✅ Dashboard available at: http://localhost:8080

All set! I'll handle everything from here. 

You can:
→ Check progress: openclaw logs ricky
→ Update settings: openclaw config ricky
→ View earnings: Login to affiliate.amazon.in

Sit back and watch the money roll in! 💰✨

Press Enter to exit setup...
```

---

## 🔧 TECHNICAL IMPLEMENTATION

### Interactive Setup Script

```python
# setup.py
import inquirer
import yaml
import os

class RickySetup:
    def __init__(self):
        self.config = {}
        
    def run_interactive_setup(self):
        """Complete interactive setup flow"""
        
        print("🤖 Welcome to Ricky - AI Affiliate Marketing Automation!")
        print()
        
        # Check if already configured
        if os.path.exists('~/.ricky/config.yaml'):
            reconfigure = inquirer.confirm(
                "You already have a configuration. Reconfigure?",
                default=False
            )
            if not reconfigure:
                return
        
        # Step 1: Amazon
        self.setup_amazon()
        
        # Step 2: Social Media
        self.setup_social_media()
        
        # Step 3: Image Generation
        self.setup_image_generation()
        
        # Step 4: Preferences
        self.setup_preferences()
        
        # Save config
        self.save_config()
        
        # Validate
        self.validate_setup()
        
        print("\n✅ Setup complete!")
        
    def setup_amazon(self):
        """Amazon Associates + API setup"""
        questions = [
            inquirer.Text('affiliate_tag', 
                message="Your Amazon affiliate tag (e.g., yourname-21)"),
            inquirer.Text('api_key',
                message="Amazon Product API Access Key"),
            inquirer.Password('api_secret',
                message="Amazon Product API Secret Key")
        ]
        
        answers = inquirer.prompt(questions)
        
        # Validate
        if self.validate_amazon_api(answers):
            self.config['amazon'] = answers
            print("✅ Amazon connected!")
        else:
            print("❌ Invalid credentials. Please try again.")
            self.setup_amazon()
    
    def setup_social_media(self):
        """Social media setup (Postiz or direct)"""
        method = inquirer.list_input(
            "How to connect social media?",
            choices=['Postiz (easy)', 'Direct APIs (advanced)']
        )
        
        if 'Postiz' in method:
            self.setup_postiz()
        else:
            self.setup_direct_apis()
    
    def setup_postiz(self):
        """Postiz integration"""
        questions = [
            inquirer.Text('api_key', message="Postiz API Key"),
            inquirer.Text('workspace', message="Postiz Workspace ID")
        ]
        
        answers = inquirer.prompt(questions)
        
        if self.validate_postiz(answers):
            self.config['postiz'] = answers
            print("✅ Postiz connected!")
        else:
            print("❌ Invalid credentials.")
    
    def setup_image_generation(self):
        """Fal.ai setup"""
        api_key = inquirer.text("Fal.ai API Key")
        
        if self.validate_fal_api(api_key):
            self.config['fal_api'] = api_key
            print("✅ Fal.ai connected!")
        else:
            print("❌ Invalid API key.")
    
    def setup_preferences(self):
        """User preferences"""
        categories = inquirer.checkbox(
            "Select product categories",
            choices=[
                'Electronics',
                'Home & Kitchen',
                'Fashion',
                'Beauty & Personal Care',
                'Sports & Outdoors',
                'Books',
                'Toys & Games',
                'Office Products'
            ]
        )
        
        price_min = inquirer.text("Minimum price (₹)", default="500")
        price_max = inquirer.text("Maximum price (₹)", default="5000")
        
        products_per_day = inquirer.text(
            "Products per day (1-5)",
            default="3",
            validate=lambda _, x: 1 <= int(x) <= 5
        )
        
        self.config['preferences'] = {
            'categories': categories,
            'price_range': {
                'min': int(price_min),
                'max': int(price_max)
            },
            'products_per_day': int(products_per_day)
        }
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.expanduser('~/.ricky'), exist_ok=True)
        
        with open(os.path.expanduser('~/.ricky/config.yaml'), 'w') as f:
            yaml.dump(self.config, f)
        
        # Set permissions (only user can read)
        os.chmod(os.path.expanduser('~/.ricky/config.yaml'), 0o600)
    
    def validate_setup(self):
        """Validate all connections"""
        print("\n🔄 Validating configuration...")
        
        # Test each service
        tests = [
            ('Amazon API', self.test_amazon),
            ('Postiz', self.test_postiz),
            ('Fal.ai', self.test_fal)
        ]
        
        for name, test in tests:
            if test():
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name} - Check credentials")

# Run setup
if __name__ == '__main__':
    setup = RickySetup()
    setup.run_interactive_setup()
```

---

## 📋 STORING CREDENTIALS SECURELY

### Config File Structure

```yaml
# ~/.ricky/config.yaml
# Permissions: 600 (user read/write only)

amazon:
  affiliate_tag: "counitinguniq-21"
  api_key: "AKIAXXXXXXXXXX"
  api_secret: "xxxxxxxxxxxxxxxx"

social_media:
  postiz:
    api_key: "sk_postiz_xxxxxxxxx"
    workspace: "workspace-xxxxx"
    platforms:
      - twitter
      - instagram
      - pinterest

image_generation:
  fal_api_key: "9b753dc2-xxxx-xxxx-xxxx"
  model: "seedream-5-lite"

camoufox:
  enabled: true
  token_file: "/data/browser-server-token"

automation:
  products_per_day: 3
  schedule:
    - "10:00"
    - "14:00"
    - "18:00"

preferences:
  categories:
    - "Electronics"
    - "Home & Kitchen"
    - "Fashion"
  price_range:
    min: 500
    max: 5000

created_at: "2026-03-18T07:10:00Z"
```

---

## ✅ USER EXPERIENCE SUMMARY

### First Time:
1. User runs: `openclaw run ricky`
2. Ricky detects no config
3. Interactive setup starts
4. User answers questions (10 min)
5. Config saved
6. Automation starts!

### Second Time+:
1. User runs: `openclaw run ricky`
2. Ricky loads config
3. Starts working immediately!

**Setup once, run forever!** 🚀

---

**This is how professional agents work - friendly setup, then automation!** ✨
