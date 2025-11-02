"""
Web Scraper for Mental Health Knowledge Sources
Fetches content from trusted mental health websites and saves to knowledge base
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from urllib.parse import urljoin, urlparse
import hashlib

class MentalHealthWebScraper:
    """Scrape mental health content from trusted sources."""
    
    def __init__(self, output_dir="data/knowledge/web_sources"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Mental Health AI Knowledge Bot)'
        })
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    # Trusted sources with scraping configurations
    TRUSTED_SOURCES = {
        'imh': {
            'name': 'Institute of Mental Health Singapore',
            'base_url': 'https://www.imh.com.sg',
            'pages': [
                '/About-Us/Newsroom/Pages/default.aspx',
                '/Pages/default.aspx',
            ],
            'selectors': {'content': 'div.content, article, main, body'}
        },
        'healthhub': {
            'name': 'HealthHub Singapore',
            'base_url': 'https://www.healthhub.sg',
            'pages': [
                '/live-healthy/mental-wellbeing',
            ],
            'selectors': {'content': 'article, .content-body, main'}
        },
        'samh': {
            'name': 'Singapore Association for Mental Health',
            'base_url': 'https://www.samhealth.org.sg',
            'pages': [
                '/mental-health',
            ],
            'selectors': {'content': 'article, .content, main'}
        },
        'who': {
            'name': 'World Health Organization',
            'base_url': 'https://www.who.int',
            'pages': [
                '/news-room/fact-sheets/detail/mental-health-strengthening-our-response',
            ],
            'selectors': {'content': 'article, .sf-content-block'}
        }
    }
    
    def fetch_page(self, url, timeout=10):
        """Fetch a webpage with error handling."""
        try:
            print(f"  Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"  ❌ Error fetching {url}: {e}")
            return None
    
    def extract_text(self, html, selectors):
        """Extract clean text from HTML using CSS selectors."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Try each selector
            content = None
            for selector in selectors['content'].split(','):
                content_elem = soup.select_one(selector.strip())
                if content_elem:
                    content = content_elem
                    break
            
            if not content:
                # Fallback to body
                content = soup.find('body')
            
            if content:
                # Get text and clean it
                text = content.get_text(separator='\n', strip=True)
                # Remove excessive whitespace
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                return '\n\n'.join(lines)
            
            return None
            
        except Exception as e:
            print(f"  ❌ Error parsing HTML: {e}")
            return None
    
    def save_content(self, source_key, content, url):
        """Save scraped content to a text file."""
        try:
            # Create source-specific directory
            source_dir = os.path.join(self.output_dir, source_key)
            os.makedirs(source_dir, exist_ok=True)
            
            # Generate filename from URL
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"{source_key}_{url_hash}.txt"
            filepath = os.path.join(source_dir, filename)
            
            # Add metadata header
            metadata = f"""Source: {self.TRUSTED_SOURCES[source_key]['name']}
URL: {url}
Scraped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

"""
            
            # Write content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(metadata + content)
            
            print(f"  ✅ Saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"  ❌ Error saving content: {e}")
            return None
    
    def scrape_source(self, source_key):
        """Scrape all pages from a specific source."""
        if source_key not in self.TRUSTED_SOURCES:
            print(f"❌ Unknown source: {source_key}")
            return []
        
        source = self.TRUSTED_SOURCES[source_key]
        print(f"\n📡 Scraping: {source['name']}")
        print(f"   Base URL: {source['base_url']}")
        
        scraped_files = []
        
        for page in source['pages']:
            url = urljoin(source['base_url'], page)
            
            # Fetch page
            html = self.fetch_page(url)
            if not html:
                continue
            
            # Extract text
            content = self.extract_text(html, source['selectors'])
            if not content:
                print(f"  ⚠️  No content extracted from {url}")
                continue
            
            # Verify minimum content length
            if len(content) < 200:
                print(f"  ⚠️  Content too short ({len(content)} chars), skipping")
                continue
            
            # Save to file
            filepath = self.save_content(source_key, content, url)
            if filepath:
                scraped_files.append(filepath)
            
            # Be respectful - wait between requests
            time.sleep(2)
        
        return scraped_files
    
    def scrape_all(self, sources=None):
        """Scrape content from all or specific trusted sources."""
        if sources is None:
            sources = list(self.TRUSTED_SOURCES.keys())
        elif isinstance(sources, str):
            sources = [sources]
        
        print(f"\n{'='*60}")
        print(f"🌐 Mental Health Web Scraper")
        print(f"{'='*60}")
        print(f"Output directory: {self.output_dir}")
        print(f"Sources to scrape: {', '.join(sources)}")
        
        all_files = []
        
        for source_key in sources:
            try:
                files = self.scrape_source(source_key)
                all_files.extend(files)
            except Exception as e:
                print(f"❌ Error scraping {source_key}: {e}")
        
        print(f"\n{'='*60}")
        print(f"✅ Scraping complete!")
        print(f"   Total files saved: {len(all_files)}")
        print(f"   Location: {self.output_dir}")
        print(f"{'='*60}\n")
        
        return all_files


def main():
    """Run the web scraper."""
    scraper = MentalHealthWebScraper()
    
    # Scrape all trusted sources
    # Note: Some websites may block scraping or require special handling
    # This is a basic implementation for educational purposes
    
    print("""
⚠️  IMPORTANT NOTES:
- Respect robots.txt and terms of service
- Some sites may block automated access
- Use scraped content ethically and with attribution
- Consider using official APIs where available
- Review content before adding to knowledge base
""")
    
    # Scrape specific sources (comment out sources that block scraping)
    scraper.scrape_all(['who'])  # Start with WHO as it's usually accessible
    
    # To scrape all:
    # scraper.scrape_all()
    
    # To scrape specific sources:
    # scraper.scrape_all(['imh', 'healthhub'])


if __name__ == "__main__":
    main()
