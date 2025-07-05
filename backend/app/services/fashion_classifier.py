import re
from typing import Dict, List
from bs4 import BeautifulSoup
import requests

class FashionClassifier:
    """Classify if a website sells women's fashion"""
    
    def __init__(self):
        # Keywords for women's fashion
        self.womens_fashion_keywords = [
            # Clothing types
            'dress', 'dresses', 'skirt', 'skirts', 'blouse', 'blouses',
            'pants', 'jeans', 'shirt', 'shirts', 'sweater', 'sweaters',
            'jacket', 'jackets', 'coat', 'coats', 'suit', 'suits',
            't-shirt', 'tshirt', 'tank top', 'tank tops', 'cardigan',
            'hoodie', 'hoodies', 'leggings', 'shorts', 'jumpsuit',
            
            # Women-specific terms
            'women', 'womens', 'woman', 'ladies', 'lady', 'girls',
            'feminine', 'female', 'her', 'she', 'miss', 'mrs',
            
            # Fashion categories
            'fashion', 'clothing', 'apparel', 'wear', 'outfit',
            'style', 'trendy', 'trend', 'boutique', 'designer',
            
            # Specific women's fashion terms
            'maxi dress', 'mini dress', 'cocktail dress', 'evening dress',
            'wedding dress', 'bridesmaid', 'maternity', 'plus size',
            'petite', 'tall', 'curve', 'juniors', 'misses',
            
            # Accessories
            'handbag', 'handbags', 'purse', 'purses', 'wallet',
            'jewelry', 'necklace', 'earrings', 'bracelet', 'ring',
            'scarf', 'scarves', 'belt', 'belts', 'sunglasses',
            'shoes', 'boots', 'heels', 'flats', 'sandals',
            
            # Beauty
            'makeup', 'cosmetics', 'beauty', 'skincare', 'perfume',
            'fragrance', 'nail polish', 'lipstick', 'mascara'
        ]
        
        # Keywords that suggest it's NOT women's fashion
        self.exclusion_keywords = [
            'men', 'mens', 'man', 'male', 'boys', 'boy', 'guy', 'guys',
            'children', 'kids', 'baby', 'babies', 'toddler',
            'electronics', 'gadgets', 'computers', 'phones',
            'furniture', 'home', 'kitchen', 'garden',
            'sports', 'fitness', 'gym', 'athletic',
            'automotive', 'cars', 'motorcycle',
            'books', 'music', 'movies', 'games'
        ]
    
    def classify_fashion(self, domain: str, html_content: str = None) -> Dict[str, any]:
        """
        Classify if a website sells women's fashion
        
        Args:
            domain: Website domain
            html_content: HTML content if already fetched
            
        Returns:
            Dict with classification results
        """
        if not html_content:
            html_content = self._fetch_content(domain)
        
        if not html_content:
            return {
                'is_womens_fashion': False,
                'confidence': 0.0,
                'error': 'Could not fetch content'
            }
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content
        text_content = self._extract_text(soup)
        
        # Analyze content
        analysis = self._analyze_content(text_content, soup)
        
        # Calculate confidence
        confidence = self._calculate_confidence(analysis)
        is_womens_fashion = confidence > 0.6
        
        return {
            'is_womens_fashion': is_womens_fashion,
            'confidence': confidence,
            'analysis': analysis,
            'keywords_found': analysis['keywords_found'],
            'exclusion_keywords_found': analysis['exclusion_keywords_found']
        }
    
    def _fetch_content(self, domain: str) -> str:
        """Fetch HTML content from domain"""
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(domain, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except:
            return None
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract relevant text content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text from title and meta description
        title = soup.find('title')
        title_text = title.get_text() if title else ""
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_text = meta_desc.get('content', '') if meta_desc else ""
        
        # Get text from main content areas
        main_content = ""
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div']):
            if tag.get_text().strip():
                main_content += " " + tag.get_text().strip()
        
        return f"{title_text} {meta_text} {main_content}".lower()
    
    def _analyze_content(self, text_content: str, soup: BeautifulSoup) -> Dict:
        """Analyze content for fashion indicators"""
        # Find fashion keywords
        keywords_found = []
        for keyword in self.womens_fashion_keywords:
            if keyword.lower() in text_content:
                keywords_found.append(keyword)
        
        # Find exclusion keywords
        exclusion_keywords_found = []
        for keyword in self.exclusion_keywords:
            if keyword.lower() in text_content:
                exclusion_keywords_found.append(keyword)
        
        # Check for product links
        product_links = self._check_product_links(soup)
        
        # Check for price patterns
        price_patterns = self._check_price_patterns(text_content)
        
        return {
            'keywords_found': keywords_found,
            'exclusion_keywords_found': exclusion_keywords_found,
            'product_links': product_links,
            'price_patterns': price_patterns,
            'total_keywords': len(keywords_found),
            'total_exclusions': len(exclusion_keywords_found)
        }
    
    def _check_product_links(self, soup: BeautifulSoup) -> int:
        """Check for product-related links"""
        product_indicators = ['/product', '/products', '/item', '/items', '/buy', '/shop']
        links = soup.find_all('a', href=True)
        
        product_links = 0
        for link in links:
            href = link.get('href', '').lower()
            if any(indicator in href for indicator in product_indicators):
                product_links += 1
        
        return product_links
    
    def _check_price_patterns(self, text_content: str) -> int:
        """Check for price patterns in text"""
        price_patterns = [
            r'\$\d+',  # $100
            r'\d+\s*dollars',  # 100 dollars
            r'\d+\s*usd',  # 100 USD
            r'price:\s*\$\d+',  # Price: $100
            r'from\s*\$\d+',  # From $100
        ]
        
        price_count = 0
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            price_count += len(matches)
        
        return price_count
    
    def _calculate_confidence(self, analysis: Dict) -> float:
        """Calculate confidence score for women's fashion classification"""
        base_score = 0.0
        
        # Positive indicators
        if analysis['total_keywords'] > 0:
            base_score += min(analysis['total_keywords'] * 0.1, 0.5)
        
        if analysis['product_links'] > 0:
            base_score += min(analysis['product_links'] * 0.05, 0.2)
        
        if analysis['price_patterns'] > 0:
            base_score += min(analysis['price_patterns'] * 0.02, 0.1)
        
        # Negative indicators
        if analysis['total_exclusions'] > 0:
            base_score -= min(analysis['total_exclusions'] * 0.15, 0.4)
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, base_score)) 