# 🚀 Scraping Quick Reference Card

## 📋 Before You Start

1. **Read the full guide**: `templates/SCRAPING_GUIDE.md`
2. **Choose your market**: Pick a major supermarket chain in your country
3. **Study the website**: Use browser dev tools to understand the structure
4. **Start small**: Test with 5-10 products first

## 🌍 Country Quick Start

### 🇫🇷 France
- **Best for beginners**: Carrefour
- **URL**: https://www.carrefour.fr
- **Key selectors**: `.product-card`, `.product-title`, `.price`

### 🇪🇸 Spain  
- **Best for beginners**: Mercadona
- **URL**: https://www.mercadona.es
- **Key selectors**: `.product-item`, `.product-name`, `.price`

### 🇵🇱 Poland
- **Best for beginners**: Biedronka
- **URL**: https://www.biedronka.pl
- **Key selectors**: `.product-tile`, `.product-name`, `.price-value`

### 🇩🇪 Germany
- **Best for beginners**: Lidl
- **URL**: https://www.lidl.de
- **Key selectors**: `.product`, `.product-title`, `.price`

### 🇬🇧 United Kingdom
- **Best for beginners**: Tesco
- **URL**: https://www.tesco.com
- **Key selectors**: `.product-tile`, `.product-title`, `.price`

## 🔧 Essential Code Snippets

### Basic Scraper Structure
```python
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_products():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    url = "YOUR_MARKET_URL"
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    product_containers = soup.find_all('div', class_='PRODUCT_CONTAINER_CLASS')
    
    for container in product_containers:
        product = extract_product(container)
        if product:
            products.append(product)
        time.sleep(random.uniform(1, 3))  # Rate limiting
    
    return products

def extract_product(container):
    try:
        name = container.find('h3', class_='PRODUCT_NAME_CLASS').text.strip()
        price = container.find('span', class_='PRICE_CLASS').text.strip()
        
        return {
            'name': name,
            'price': parse_price(price),
            'category': 'YOUR_CATEGORY',
            'store_id': 'YOUR_STORE_ID',
            'city': 'YOUR_CITY'
        }
    except Exception as e:
        print(f"Error: {e}")
        return None
```

### Price Parsing by Country
```python
def parse_price(price_text, country):
    if country == "France":
        return float(price_text.replace('€', '').replace(',', '.').strip())
    elif country == "Spain":
        return float(price_text.replace('€', '').replace(',', '.').strip())
    elif country == "Poland":
        return float(price_text.replace('zł', '').replace(',', '.').strip())
    elif country == "Germany":
        return float(price_text.replace('€', '').replace(',', '.').strip())
    elif country == "UK":
        return float(price_text.replace('£', '').strip())
    else:
        # Generic parsing
        import re
        numbers = re.findall(r'\d+\.?\d*', price_text)
        return float(numbers[0]) if numbers else None
```

## 🎯 Common CSS Selectors

### Product Containers
- `.product`
- `.product-item`
- `.product-card`
- `.product-tile`
- `.item`
- `[data-testid="product"]`

### Product Names
- `.product-name`
- `.product-title`
- `h3`
- `h4`
- `.title`

### Prices
- `.price`
- `.price-value`
- `.cost`
- `[data-testid="price"]`
- `.amount`

### Images
- `img.product-image`
- `img[alt*="product"]`
- `.product-photo img`

## ⚠️ Common Issues & Quick Fixes

### "Connection refused"
```python
# Add timeout and retry
response = requests.get(url, timeout=10)
```

### "Element not found"
```python
# Use try-except with fallback selectors
try:
    name = container.find('h3', class_='product-name').text
except AttributeError:
    name = container.find('h2', class_='title').text
```

### "No products found"
```python
# Debug: print the HTML structure
print(soup.prettify()[:1000])  # First 1000 characters
```

### "Rate limited"
```python
# Increase delays
time.sleep(random.uniform(3, 6))  # 3-6 seconds between requests
```

## 🔍 Debugging Checklist

- [ ] Check if URL is correct
- [ ] Verify CSS selectors in browser dev tools
- [ ] Print HTML structure to see what's available
- [ ] Test with small sample (5 products)
- [ ] Check for JavaScript loading (use Selenium if needed)
- [ ] Verify price parsing works
- [ ] Ensure all required fields are extracted

## 📊 Data Validation

```python
def validate_product(product):
    required_fields = ['name', 'price', 'category', 'store_id', 'city']
    
    for field in required_fields:
        if not product.get(field):
            return False
    
    # Check if price is numeric
    try:
        float(product['price'])
    except (ValueError, TypeError):
        return False
    
    return True
```

## 🚀 Testing Your Scraper

```python
def test_scraper():
    products = scrape_products()
    
    print(f"Found {len(products)} products")
    
    # Test first product
    if products:
        first_product = products[0]
        print("First product:", first_product)
        
        # Validate
        if validate_product(first_product):
            print("✅ Product validation passed")
        else:
            print("❌ Product validation failed")
    
    return products
```

## 📝 Final Checklist

Before uploading your CSV:

- [ ] Scraper runs without errors
- [ ] At least 50 products scraped
- [ ] All required fields present
- [ ] Prices are numeric (no currency symbols)
- [ ] Product names are clean
- [ ] No duplicate products
- [ ] CSV file named correctly (products_YYYY_MM_DD.csv)

## 🆘 Need Help?

1. **Check the full guide**: `templates/SCRAPING_GUIDE.md`
2. **Test with browser dev tools**: Right-click → Inspect Element
3. **Start with a simple site**: Choose the easiest market first
4. **Ask for help**: Contact your supervisor with specific error messages

---

**Remember**: Start simple, test frequently, and don't be afraid to ask for help! 🎯
