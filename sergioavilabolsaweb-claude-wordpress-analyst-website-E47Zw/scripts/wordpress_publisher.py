"""
WordPress REST API client.
Supports Yoast SEO, Rank Math and All-in-One SEO meta injection.
Requires WordPress 5.6+ and an Application Password.
"""

import os
import base64
import mimetypes
from pathlib import Path

import requests


class WordPressPublisher:
    def __init__(self):
        self.base_url  = os.environ['WP_URL'].rstrip('/')
        self.api_base  = f'{self.base_url}/wp-json/wp/v2'
        self.seo_plugin = os.environ.get('WP_SEO_PLUGIN', 'yoast').lower()

        username = os.environ['WP_USERNAME']
        password = os.environ['WP_APP_PASSWORD'].replace(' ', '')
        token = base64.b64encode(f'{username}:{password}'.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {token}',
            'Accept':        'application/json',
        }

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def upload_image(self, file_path: str, title: str, alt_text: str = '') -> int:
        """Upload an image to the WordPress Media Library. Returns media ID."""
        path = Path(file_path)
        mime_type = mimetypes.guess_type(str(path))[0] or 'image/png'

        with open(path, 'rb') as fh:
            resp = requests.post(
                f'{self.api_base}/media',
                headers={
                    **self.headers,
                    'Content-Disposition': f'attachment; filename="{path.name}"',
                    'Content-Type': mime_type,
                },
                data=fh,
                timeout=60,
            )

        resp.raise_for_status()
        media_id = resp.json()['id']

        # Set alt text and title
        requests.post(
            f'{self.api_base}/media/{media_id}',
            headers={**self.headers, 'Content-Type': 'application/json'},
            json={'title': title, 'alt_text': alt_text or title},
            timeout=30,
        )

        return media_id

    # ------------------------------------------------------------------
    # Categories / Tags
    # ------------------------------------------------------------------

    def get_or_create_category(self, name: str) -> int:
        """Return the ID of an existing category, or create it."""
        resp = requests.get(
            f'{self.api_base}/categories',
            headers=self.headers,
            params={'search': name, 'per_page': 5},
            timeout=30,
        )
        resp.raise_for_status()
        for cat in resp.json():
            if cat['name'].lower() == name.lower():
                return cat['id']

        # Create
        resp = requests.post(
            f'{self.api_base}/categories',
            headers={**self.headers, 'Content-Type': 'application/json'},
            json={'name': name},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()['id']

    def get_or_create_tag(self, name: str) -> int:
        resp = requests.get(
            f'{self.api_base}/tags',
            headers=self.headers,
            params={'search': name, 'per_page': 5},
            timeout=30,
        )
        resp.raise_for_status()
        for tag in resp.json():
            if tag['name'].lower() == name.lower():
                return tag['id']

        resp = requests.post(
            f'{self.api_base}/tags',
            headers={**self.headers, 'Content-Type': 'application/json'},
            json={'name': name},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()['id']

    # ------------------------------------------------------------------
    # SEO meta
    # ------------------------------------------------------------------

    def _build_seo_meta(self, meta_title: str, meta_desc: str, keywords: str) -> dict:
        if self.seo_plugin == 'yoast':
            return {
                '_yoast_wpseo_title':    meta_title,
                '_yoast_wpseo_metadesc': meta_desc,
                '_yoast_wpseo_focuskw':  keywords.split(',')[0].strip() if keywords else '',
            }
        if self.seo_plugin == 'rankmath':
            return {
                'rank_math_title':         meta_title,
                'rank_math_description':   meta_desc,
                'rank_math_focus_keyword': keywords.split(',')[0].strip() if keywords else '',
            }
        # All-in-One SEO
        return {
            '_aioseop_title':       meta_title,
            '_aioseop_description': meta_desc,
            '_aioseop_keywords':    keywords,
        }

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    def create_post(
        self,
        title:            str,
        content:          str,
        featured_image_id: int,
        meta_title:       str,
        meta_desc:        str,
        keywords:         str,
        category_name:    str,
        tag_names:        list[str] | None = None,
        status:           str = 'publish',
    ) -> int:
        """Create and publish a WordPress post. Returns the new post ID."""
        category_id = self.get_or_create_category(category_name)

        tag_ids = []
        for tag in (tag_names or []):
            tag_ids.append(self.get_or_create_tag(tag))

        seo_meta = self._build_seo_meta(meta_title, meta_desc, keywords)

        payload = {
            'title':          title,
            'content':        content,
            'status':         status,
            'featured_media': featured_image_id,
            'categories':     [category_id],
            'tags':           tag_ids,
            'meta':           seo_meta,
        }

        resp = requests.post(
            f'{self.api_base}/posts',
            headers={**self.headers, 'Content-Type': 'application/json'},
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        post = resp.json()
        print(f"[WP] Post published: id={post['id']}  url={post['link']}")
        return post['id']
