"""
RICKY POSTIZ POSTER — Upload images + create posts on social media.

Supports:
  - Twitter/X (4 images + caption)
  - Instagram (carousel up to 10 images + caption)  
  - Pinterest (pin with image, title, description, link)

Usage:
  poster = PostizPoster(api_key='...')
  result = poster.post_product(
      platform='twitter',
      integration_id='...',
      images=['/path/to/img1.png', ...],
      caption='...',
      schedule_minutes=5,
  )
"""

import os
import requests
import json
from datetime import datetime, timedelta, timezone


class PostizPoster:
    
    def __init__(self, api_key: str, base_url: str = 'https://api.postiz.com/public/v1'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": api_key}
    
    # ─── UPLOAD ──────────────────────────────────────────
    
    def upload_image(self, file_path: str) -> dict:
        """Upload a single image. Returns {id, path} or None on failure."""
        if not os.path.exists(file_path):
            print(f"   ❌ File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'rb') as f:
                r = requests.post(
                    f"{self.base_url}/upload",
                    headers=self.headers,
                    files={"file": (os.path.basename(file_path), f, "image/png")},
                    timeout=30
                )
            
            if r.status_code == 200:
                data = r.json()
                return {"id": data['id'], "path": data['path']}
            else:
                print(f"   ❌ Upload failed ({r.status_code}): {r.text[:100]}")
                return None
                
        except Exception as e:
            print(f"   ❌ Upload error: {str(e)[:60]}")
            return None
    
    def upload_images(self, file_paths: list) -> list:
        """Upload multiple images. Returns list of {id, path}."""
        uploaded = []
        for i, fp in enumerate(file_paths):
            print(f"   📤 Uploading {i+1}/{len(file_paths)}: {os.path.basename(fp)}...", end=" ")
            result = self.upload_image(fp)
            if result:
                print(f"✅")
                uploaded.append(result)
            else:
                print(f"❌")
        return uploaded
    
    # ─── POST CREATION ───────────────────────────────────
    
    def create_post(self, integration_id: str, platform_type: str,
                    caption: str, images: list, schedule_dt: datetime = None,
                    extra_settings: dict = None) -> dict:
        """
        Create a post on any platform.
        
        Args:
            integration_id: Postiz integration ID
            platform_type: 'x', 'instagram-standalone', 'pinterest', etc.
            caption: Post text
            images: List of {id, path} from upload_images
            schedule_dt: When to post (UTC datetime). None = now + 5 min
            extra_settings: Platform-specific settings
        
        Returns:
            {success: bool, post_id: str, error: str}
        """
        if schedule_dt is None:
            schedule_dt = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        date_str = schedule_dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        # Build settings
        settings = {"__type": platform_type}
        
        if platform_type == 'x':
            settings["who_can_reply_post"] = "everyone"
        elif platform_type in ('instagram', 'instagram-standalone'):
            settings["post_type"] = "post"
            settings["is_trial_reel"] = False
            settings["collaborators"] = []
        elif platform_type == 'pinterest':
            if extra_settings and extra_settings.get('board'):
                settings["board"] = extra_settings['board']
            if extra_settings and extra_settings.get('title'):
                settings["title"] = extra_settings['title']
            if extra_settings and extra_settings.get('link'):
                settings["link"] = extra_settings['link']
        
        if extra_settings:
            settings.update(extra_settings)
        
        payload = {
            "type": "schedule",
            "date": date_str,
            "shortLink": False,
            "tags": [],
            "posts": [
                {
                    "integration": {"id": integration_id},
                    "value": [
                        {
                            "content": caption,
                            "image": images
                        }
                    ],
                    "settings": settings
                }
            ]
        }
        
        try:
            r = requests.post(
                f"{self.base_url}/posts",
                headers={**self.headers, "Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if r.status_code == 200 or r.status_code == 201:
                data = r.json()
                if isinstance(data, list) and len(data) > 0:
                    return {"success": True, "post_id": data[0].get('postId', '?')}
                return {"success": True, "post_id": str(data)}
            else:
                return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)[:100]}
    
    def delete_post(self, post_id: str) -> bool:
        """Delete a scheduled post."""
        try:
            r = requests.delete(
                f"{self.base_url}/posts/{post_id}",
                headers=self.headers,
                timeout=10
            )
            return r.status_code in (200, 204)
        except:
            return False
    
    # ─── CONVENIENCE METHODS ─────────────────────────────
    
    def post_to_twitter(self, integration_id: str, caption: str,
                        image_files: list, schedule_dt: datetime = None) -> dict:
        """Post to Twitter/X with up to 4 images."""
        print(f"\n🐦 Posting to Twitter/X...")
        images = self.upload_images(image_files[:4])
        if not images:
            return {"success": False, "error": "No images uploaded"}
        
        result = self.create_post(integration_id, 'x', caption, images, schedule_dt)
        if result['success']:
            print(f"   ✅ Post created: {result['post_id']}")
        else:
            print(f"   ❌ Failed: {result['error']}")
        return result
    
    def post_to_instagram(self, integration_id: str, caption: str,
                          image_files: list, schedule_dt: datetime = None) -> dict:
        """Post Instagram carousel with up to 10 images."""
        print(f"\n📸 Posting to Instagram...")
        images = self.upload_images(image_files[:10])
        if not images:
            return {"success": False, "error": "No images uploaded"}
        
        result = self.create_post(integration_id, 'instagram-standalone', caption, images, schedule_dt)
        if result['success']:
            print(f"   ✅ Post created: {result['post_id']}")
        else:
            print(f"   ❌ Failed: {result['error']}")
        return result
    
    def post_to_pinterest(self, integration_id: str, description: str,
                          image_file: str, title: str = '', link: str = '',
                          board: str = '', schedule_dt: datetime = None) -> dict:
        """Post a Pinterest pin."""
        print(f"\n📌 Posting to Pinterest...")
        images = self.upload_images([image_file])
        if not images:
            return {"success": False, "error": "No image uploaded"}
        
        extra = {}
        if board:
            extra['board'] = board
        if title:
            extra['title'] = title
        if link:
            extra['link'] = link
        
        result = self.create_post(integration_id, 'pinterest', description, images, schedule_dt, extra)
        if result['success']:
            print(f"   ✅ Pin created: {result['post_id']}")
        else:
            print(f"   ❌ Failed: {result['error']}")
        return result
    
    def post_product_all_platforms(self, captions: dict, files: dict,
                                   integrations: dict, product: dict,
                                   schedule_dt: datetime = None) -> dict:
        """
        Post a product to all configured platforms.
        
        Args:
            captions: {twitter: str, instagram: str, pinterest_title: str, pinterest_description: str}
            files: {twitter: [paths], instagram: [paths], pinterest: [paths]}
            integrations: {twitter: id, instagram: id, pinterest: id}
            product: Product dict with asin, affiliate_tag
            schedule_dt: Base schedule time (staggered per platform)
        """
        results = {}
        
        if schedule_dt is None:
            schedule_dt = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        asin = product.get('asin', '')
        tag = product.get('affiliate_tag', 'counitinguniq-21')
        link = f"https://www.amazon.in/dp/{asin}?tag={tag}" if asin else ''
        
        # Twitter
        if integrations.get('twitter') and files.get('twitter'):
            results['twitter'] = self.post_to_twitter(
                integrations['twitter'],
                captions['twitter'],
                files['twitter'],
                schedule_dt
            )
        
        # Instagram (stagger +2 min)
        if integrations.get('instagram') and files.get('instagram'):
            ig_time = schedule_dt + timedelta(minutes=2)
            results['instagram'] = self.post_to_instagram(
                integrations['instagram'],
                captions['instagram'],
                files['instagram'],
                ig_time
            )
        
        # Pinterest (stagger +4 min)
        if integrations.get('pinterest') and files.get('pinterest'):
            pin_time = schedule_dt + timedelta(minutes=4)
            results['pinterest'] = self.post_to_pinterest(
                integrations['pinterest'],
                captions['pinterest_description'],
                files['pinterest'][0],
                title=captions.get('pinterest_title', ''),
                link=link,
                schedule_dt=pin_time
            )
        
        return results
    
    # ─── LIST / MANAGE ───────────────────────────────────
    
    def list_integrations(self) -> list:
        """List all connected social accounts."""
        try:
            r = requests.get(
                f"{self.base_url}/integrations",
                headers=self.headers,
                timeout=10
            )
            return r.json() if r.status_code == 200 else []
        except:
            return []
    
    def list_posts(self, days_back: int = 7) -> list:
        """List recent posts."""
        start = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end = (datetime.now(timezone.utc) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        try:
            r = requests.get(
                f"{self.base_url}/posts",
                headers=self.headers,
                params={"startDate": start, "endDate": end},
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                return data if isinstance(data, list) else data.get('posts', [])
            return []
        except:
            return []
