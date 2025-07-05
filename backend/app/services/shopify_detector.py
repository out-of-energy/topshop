import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional
import time
from app.core.config import settings

class ShopifyDetector:
    """Detect if a website is built with Shopify"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def detect_shopify(self, domain: str) -> Dict[str, any]:
        """
        Detect if a domain is a Shopify store
        
        Returns:
            Dict with detection results
        """
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        
        try:
            # Add delay to be respectful
            time.sleep(settings.SCRAPING_DELAY)
            
            response = self.session.get(
                domain, 
                timeout=settings.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check multiple indicators
            indicators = {
                'shopify_js': self._check_shopify_js(soup),
                'shopify_meta': self._check_shopify_meta(soup),
                'shopify_links': self._check_shopify_links(soup),
                'shopify_content': self._check_shopify_content(soup),
                'shopify_api': self._check_shopify_api(domain),
            }
            
            # Calculate confidence score
            confidence = sum(indicators.values()) / len(indicators)
            is_shopify = confidence > 0.5
            
            return {
                'is_shopify': is_shopify,
                'confidence': confidence,
                'indicators': indicators,
                'status_code': response.status_code,
                'final_url': response.url
            }
            
        except requests.RequestException as e:
            return {
                'is_shopify': False,
                'confidence': 0.0,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def _check_shopify_js(self, soup: BeautifulSoup) -> float:
        """Check for Shopify JavaScript files"""
        js_sources = soup.find_all('script', src=True)
        shopify_indicators = [
            'shopify.com',
            'cdn.shopify.com',
            'shopify.assets',
            'shopify.js',
            'shopify.min.js'
        ]
        
        for script in js_sources:
            src = script.get('src', '').lower()
            if any(indicator in src for indicator in shopify_indicators):
                return 1.0
        
        return 0.0
    
    def _check_shopify_meta(self, soup: BeautifulSoup) -> float:
        """Check for Shopify meta tags"""
        meta_tags = soup.find_all('meta')
        shopify_meta_indicators = [
            'shopify',
            'shopify:',
            'shopify-theme'
        ]
        
        for meta in meta_tags:
            content = meta.get('content', '').lower()
            name = meta.get('name', '').lower()
            property_attr = meta.get('property', '').lower()
            
            if any(indicator in content or indicator in name or indicator in property_attr 
                   for indicator in shopify_meta_indicators):
                return 1.0
        
        return 0.0
    
    def _check_shopify_links(self, soup: BeautifulSoup) -> float:
        """Check for Shopify-related links"""
        links = soup.find_all('a', href=True)
        shopify_link_indicators = [
            '/admin',
            '/cart',
            '/products',
            '/collections',
            '/pages',
            '/blogs'
        ]
        
        shopify_links_found = 0
        for link in links:
            href = link.get('href', '').lower()
            if any(indicator in href for indicator in shopify_link_indicators):
                shopify_links_found += 1
        
        # Normalize score based on number of Shopify links found
        return min(shopify_links_found / 3.0, 1.0)
    
    def _check_shopify_content(self, soup: BeautifulSoup) -> float:
        """Check for Shopify-specific content patterns"""
        text_content = soup.get_text().lower()
        shopify_content_indicators = [
            'powered by shopify',
            'shopify theme',
            'shopify store',
            'shopify checkout',
            'shopify cart'
        ]
        
        for indicator in shopify_content_indicators:
            if indicator in text_content:
                return 1.0
        
        return 0.0
    
    def _check_shopify_api(self, domain: str) -> float:
        """Check for Shopify API endpoints"""
        api_endpoints = [
            '/admin',
            '/admin/api',
            '/apps',
            '/cart.js',
            '/products.json',
            '/collections.json'
        ]
        
        for endpoint in api_endpoints:
            try:
                url = f"{domain.rstrip('/')}{endpoint}"
                response = self.session.head(url, timeout=5)
                if response.status_code in [200, 401, 403]:  # These status codes suggest Shopify endpoints
                    return 1.0
            except:
                continue
        
        return 0.0 