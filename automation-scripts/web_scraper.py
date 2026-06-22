"""
Web Scraper Script
Automatically extracts data from websites
"""

import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_website(url, selector=None):
    """
    Scrape data from a website

    Args:
        url: Target URL
        selector: CSS selector for target elements (optional)

    Returns:
        Dictionary with scraped data
    """
    print(f"🔍 Scraping: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        result = {
            'url': url,
            'title': soup.title.string if soup.title else 'No title',
            'status_code': response.status_code,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Extract text content
        if selector:
            elements = soup.select(selector)
            result['data'] = [elem.get_text(strip=True) for elem in elements]
        else:
            # Extract all paragraphs
            result['paragraphs'] = [p.get_text(strip=True) for p in soup.find_all('p')[:10]]

        print(f"✅ Success! Found {len(result.get('data', result.get('paragraphs', [])))} items")
        return result

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return {'error': str(e)}

def save_to_json(data, filename='scraped_data.json'):
    """Save scraped data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to: {filename}")

# Example usage
if __name__ == "__main__":
    # Example: Scrape a website
    url = input("Enter URL to scrape: ")
    selector = input("Enter CSS selector (or press Enter to skip): ")

    data = scrape_website(url, selector if selector else None)

    if 'error' not in data:
        save_to_json(data)
        print("\n📊 Scraped Data:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
