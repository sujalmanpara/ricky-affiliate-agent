#!/bin/bash

# Ricky Affiliate Agent - Setup Script
# Configures APIs and installs dependencies

set -e

echo "🤖 Ricky Setup - Affiliate Content Automation"
echo "=============================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
fi
echo "✅ Python 3 found"

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install it first."
    exit 1
fi
echo "✅ pip3 found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install --quiet --upgrade pip
pip3 install --quiet requests pillow python-dotenv
echo "✅ Dependencies installed"

# Get installation directory
echo ""
read -p "📁 Installation directory [default: ~/ricky-affiliate-agent]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-~/ricky-affiliate-agent}
INSTALL_DIR=$(eval echo $INSTALL_DIR)

cd "$INSTALL_DIR"

# Collect API keys
echo ""
echo "🔑 API Configuration"
echo "===================="
echo ""
echo "You'll need API keys from:"
echo "  1. Amazon Product Advertising API (free for affiliates)"
echo "  2. Postiz API (multi-platform posting)"
echo "  3. Image AI (Fal.ai or Replicate)"
echo ""

# Amazon
echo "📦 Amazon Product Advertising API"
read -p "Access Key: " AMAZON_ACCESS_KEY
read -p "Secret Key: " AMAZON_SECRET_KEY
read -p "Affiliate Tag (yourname-20): " AMAZON_TAG
AMAZON_REGION="us-east-1"

# Postiz
echo ""
echo "📱 Postiz API"
read -p "API Key: " POSTIZ_KEY
read -p "Workspace ID (optional): " POSTIZ_WORKSPACE

# Image AI
echo ""
echo "🎨 Image Generation AI"
echo "Choose provider:"
echo "  1. Fal.ai (recommended - fast, cheap)"
echo "  2. Replicate (flexible, many models)"
echo "  3. Together AI (budget-friendly)"
read -p "Select (1-3): " AI_CHOICE

if [ "$AI_CHOICE" = "1" ]; then
    AI_PROVIDER="fal"
    read -p "Fal.ai API Key: " AI_KEY
    
    echo ""
    echo "Choose model quality:"
    echo "  1. FLUX Pro ($0.03/image, best quality)"
    echo "  2. FLUX Dev ($0.01/image, balanced) ⭐ Recommended"
    echo "  3. FLUX Schnell ($0.003/image, fastest)"
    read -p "Select (1-3): " MODEL_CHOICE
    
    case $MODEL_CHOICE in
        1) AI_MODEL="fal-ai/flux-pro" ;;
        2) AI_MODEL="fal-ai/flux-dev" ;;
        3) AI_MODEL="fal-ai/flux-schnell" ;;
        *) AI_MODEL="fal-ai/flux-dev" ;;
    esac
    
elif [ "$AI_CHOICE" = "2" ]; then
    AI_PROVIDER="replicate"
    AI_MODEL="stability-ai/sdxl"
    read -p "Replicate API Key: " AI_KEY
    
else
    AI_PROVIDER="together"
    AI_MODEL="black-forest-labs/FLUX.1-schnell"
    read -p "Together AI API Key: " AI_KEY
fi

# Niche selection
echo ""
echo "🎯 Niche Selection"
echo "Choose your primary niche:"
echo "  1. Tech & Productivity"
echo "  2. Fitness & Health"
echo "  3. Home & Office"
echo "  4. Other (specify)"
read -p "Select (1-4): " NICHE_CHOICE

case $NICHE_CHOICE in
    1)
        NICHE="Tech & Productivity"
        CATEGORIES='["Electronics", "Computers", "Office Products"]'
        ;;
    2)
        NICHE="Fitness & Health"
        CATEGORIES='["Sports", "Health", "Fitness"]'
        ;;
    3)
        NICHE="Home & Office"
        CATEGORIES='["Home", "Office", "Furniture"]'
        ;;
    4)
        read -p "Enter your niche: " NICHE
        CATEGORIES='["All"]'
        ;;
esac

# Generate config.json
echo ""
echo "📝 Generating config.json..."

cat > config.json <<EOF
{
  "amazon": {
    "access_key": "$AMAZON_ACCESS_KEY",
    "secret_key": "$AMAZON_SECRET_KEY",
    "affiliate_tag": "$AMAZON_TAG",
    "region": "$AMAZON_REGION",
    "categories": $CATEGORIES
  },
  "postiz": {
    "api_key": "$POSTIZ_KEY",
    "workspace_id": "$POSTIZ_WORKSPACE",
    "accounts": {
      "instagram": "",
      "twitter": "",
      "pinterest": "",
      "facebook": ""
    }
  },
  "image_ai": {
    "provider": "$AI_PROVIDER",
    "api_key": "$AI_KEY",
    "model": "$AI_MODEL",
    "default_mode": "image-to-image",
    "fallback_mode": "text-to-image"
  },
  "niche": {
    "primary": "$NICHE",
    "categories": $CATEGORIES,
    "price_range": {
      "min": 20,
      "max": 150
    },
    "min_rating": 4.0,
    "min_reviews": 1000,
    "min_commission": 5
  },
  "posting": {
    "frequency": "3_per_day",
    "platforms": ["instagram", "twitter", "pinterest", "facebook"],
    "schedule": {
      "morning": "09:00",
      "afternoon": "14:00",
      "evening": "18:00"
    }
  }
}
EOF

echo "✅ Config file created"

# Update TOOLS.md with niche
echo ""
echo "📝 Updating TOOLS.md..."
sed -i.bak "s/Tech & Productivity/$NICHE/g" TOOLS.md
echo "✅ TOOLS.md updated"

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p images
mkdir -p logs
echo "✅ Directories created"

# Test configuration
echo ""
echo "🧪 Testing configuration..."
echo "⏳ This may take a moment..."

# Simple Python test script
python3 << 'PYEOF'
import json
import sys

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Check required fields
    assert config['amazon']['access_key'], "Amazon Access Key missing"
    assert config['amazon']['affiliate_tag'], "Amazon Affiliate Tag missing"
    assert config['postiz']['api_key'], "Postiz API Key missing"
    assert config['image_ai']['api_key'], "Image AI API Key missing"
    
    print("✅ Configuration valid!")
    sys.exit(0)
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo "✅ Configuration test passed"
else
    echo "⚠️  Configuration has issues. Please check config.json manually."
fi

# Postiz account connection reminder
echo ""
echo "📱 Postiz Account Setup"
echo "======================="
echo "⚠️  Don't forget to connect your social media accounts in Postiz:"
echo "1. Go to: https://postiz.com/integrations"
echo "2. Connect: Instagram, Twitter, Pinterest, Facebook"
echo "3. Copy account IDs and update config.json"

# Final instructions
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Installation directory: $INSTALL_DIR"
echo "Config file: $INSTALL_DIR/config.json"
echo "Niche: $NICHE"
echo ""
echo "Next steps:"
echo "1. Install Ricky in OpenClaw:"
echo "   cp $INSTALL_DIR/SOUL.md ~/.openclaw/workspace/"
echo "   cp $INSTALL_DIR/IDENTITY.md ~/.openclaw/workspace/"
echo "   cp $INSTALL_DIR/TOOLS.md ~/.openclaw/workspace/"
echo "   mkdir -p ~/.openclaw/skills/affiliate-automation"
echo "   cp $INSTALL_DIR/SKILL.md ~/.openclaw/skills/affiliate-automation/"
echo ""
echo "2. Connect social accounts in Postiz (see link above)"
echo ""
echo "3. Test your first product search:"
echo "   In OpenClaw, say:"
echo '   "Ricky, find 3 trending products in my niche"'
echo ""
echo "4. Check back tomorrow for your first automated posts!"
echo ""
echo "📊 Weekly reports will arrive every Monday at 9am."
echo ""
echo "Happy automating! 🚀"
