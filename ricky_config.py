"""
RICKY CONFIG — Secure credential storage and interactive setup wizard.

Config file: ~/.ricky/config.yaml (chmod 600)
First-time setup: python3 ricky_config.py setup
"""

import os
import sys
import yaml
import stat

CONFIG_DIR = os.path.expanduser("~/.ricky")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")

DEFAULT_CONFIG = {
    'version': 1,
    'amazon': {
        'affiliate_tag': '',
        'marketplace': 'amazon.in',
    },
    'fal_ai': {
        'api_key': '',
        'model': 'nano-banana-pro',
        'strength': 0.7,
    },
    'postiz': {
        'api_key': '',
        'base_url': 'https://api.postiz.com/public/v1',
        'integrations': {
            'twitter': '',
            'instagram': '',
            'pinterest': '',
        },
    },
    'posting': {
        'frequency': '1-2/day',
        'schedule_times_ist': ['10:00', '19:00'],
        'auto_post': False,
        'include_ad_disclosure': True,
    },
    'output': {
        'directory': '~/ricky-output',
        'organize_by_asin': True,
    },
}


def ensure_config_dir():
    """Create config directory with secure permissions."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.chmod(CONFIG_DIR, stat.S_IRWXU)  # 700


def load_config() -> dict:
    """Load config from file, return defaults if not found."""
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    # Merge with defaults for any missing keys
    merged = DEFAULT_CONFIG.copy()
    _deep_merge(merged, config)
    return merged


def save_config(config: dict):
    """Save config to file with secure permissions."""
    ensure_config_dir()
    
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 600
    print(f"✅ Config saved to {CONFIG_FILE} (permissions: 600)")


def _deep_merge(base: dict, override: dict):
    """Deep merge override into base."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def is_configured() -> bool:
    """Check if minimum required config exists."""
    config = load_config()
    return bool(
        config.get('fal_ai', {}).get('api_key') and
        config.get('amazon', {}).get('affiliate_tag')
    )


def get_postiz_integrations(api_key: str, base_url: str = None) -> list:
    """Fetch connected social accounts from Postiz."""
    import requests
    
    if not base_url:
        base_url = 'https://api.postiz.com/public/v1'
    
    try:
        r = requests.get(
            f"{base_url}/integrations",
            headers={"Authorization": api_key},
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
        return []
    except Exception:
        return []


# ─── INTERACTIVE SETUP WIZARD ────────────────────────────────

def setup_wizard():
    """Interactive first-time setup."""
    print("="*60)
    print("🚀 RICKY — First Time Setup")
    print("="*60)
    print("\nI'll walk you through setting up Ricky.")
    print("Your credentials are stored locally at ~/.ricky/config.yaml")
    print("with chmod 600 (only you can read them).\n")
    
    config = load_config()
    
    # ── Amazon ──
    print("━"*40)
    print("📦 AMAZON AFFILIATE")
    print("━"*40)
    
    tag = input(f"Affiliate tag [{config['amazon']['affiliate_tag'] or 'e.g. mytag-21'}]: ").strip()
    if tag:
        config['amazon']['affiliate_tag'] = tag
    
    marketplace = input(f"Marketplace [{config['amazon']['marketplace']}]: ").strip()
    if marketplace:
        config['amazon']['marketplace'] = marketplace
    
    # ── Fal.ai ──
    print("\n" + "━"*40)
    print("🎨 FAL.AI (Image Generation)")
    print("━"*40)
    print("Get your API key from: https://fal.ai/dashboard/keys")
    
    fal_key = input(f"API key [{config['fal_ai']['api_key'][:10] + '...' if config['fal_ai']['api_key'] else 'required'}]: ").strip()
    if fal_key:
        config['fal_ai']['api_key'] = fal_key
    
    model = input(f"Model [{config['fal_ai']['model']}] (nano-banana-pro/seedream-v5-lite): ").strip()
    if model:
        config['fal_ai']['model'] = model
    
    # ── Postiz ──
    print("\n" + "━"*40)
    print("📡 POSTIZ (Social Media Posting)")
    print("━"*40)
    print("Get your API key from: Postiz Settings > Developers > Public API")
    print("(Skip if you don't want auto-posting yet)")
    
    postiz_key = input(f"API key [{config['postiz']['api_key'][:10] + '...' if config['postiz']['api_key'] else 'optional'}]: ").strip()
    if postiz_key:
        config['postiz']['api_key'] = postiz_key
        
        # Auto-detect integrations
        print("\n🔍 Detecting connected accounts...")
        integrations = get_postiz_integrations(postiz_key, config['postiz']['base_url'])
        
        if integrations:
            print(f"   Found {len(integrations)} connected accounts:")
            for i, intg in enumerate(integrations):
                print(f"   [{i+1}] {intg['name']} ({intg['identifier']}) — @{intg.get('profile', '?')}")
            
            # Auto-assign platforms
            for intg in integrations:
                ident = intg['identifier']
                if ident == 'x' and not config['postiz']['integrations']['twitter']:
                    config['postiz']['integrations']['twitter'] = intg['id']
                    print(f"   → Twitter: {intg['name']}")
                elif 'instagram' in ident and not config['postiz']['integrations']['instagram']:
                    config['postiz']['integrations']['instagram'] = intg['id']
                    print(f"   → Instagram: {intg['name']}")
                elif ident == 'pinterest' and not config['postiz']['integrations']['pinterest']:
                    config['postiz']['integrations']['pinterest'] = intg['id']
                    print(f"   → Pinterest: {intg['name']}")
        else:
            print("   No accounts found. Connect accounts in Postiz first.")
    
    # ── Posting Schedule ──
    print("\n" + "━"*40)
    print("⏰ POSTING SCHEDULE")
    print("━"*40)
    
    auto = input(f"Enable auto-posting? (y/n) [{('y' if config['posting']['auto_post'] else 'n')}]: ").strip().lower()
    if auto == 'y':
        config['posting']['auto_post'] = True
    elif auto == 'n':
        config['posting']['auto_post'] = False
    
    # ── Save ──
    print("\n" + "━"*40)
    save_config(config)
    
    print(f"\n🎉 Setup complete! Run: python3 ricky_pipeline.py <amazon_url>")
    print(f"   Config: {CONFIG_FILE}")
    
    return config


# ─── CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup_wizard()
    elif len(sys.argv) > 1 and sys.argv[1] == 'show':
        config = load_config()
        # Mask secrets
        display = config.copy()
        if display.get('fal_ai', {}).get('api_key'):
            display['fal_ai']['api_key'] = display['fal_ai']['api_key'][:10] + '...'
        if display.get('postiz', {}).get('api_key'):
            display['postiz']['api_key'] = display['postiz']['api_key'][:10] + '...'
        print(yaml.dump(display, default_flow_style=False))
    else:
        print("Usage:")
        print("  python3 ricky_config.py setup  — Interactive setup wizard")
        print("  python3 ricky_config.py show   — Show current config")
