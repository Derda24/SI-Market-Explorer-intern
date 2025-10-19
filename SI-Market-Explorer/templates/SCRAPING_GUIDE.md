# 🕷️ Complete Market Scraping Guide for Interns

## 🎯 Overview

This comprehensive guide will teach you how to scrape product data from supermarkets and markets in different countries. You'll learn specific techniques for each market type, common challenges, and best practices.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Country-Specific Guides](#country-specific-guides)
3. [Market-Specific Strategies](#market-specific-strategies)
4. [Technical Implementation](#technical-implementation)
5. [Common Challenges & Solutions](#common-challenges--solutions)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### Prerequisites
- Basic Python knowledge
- Understanding of HTML/CSS
- Familiarity with web browsers' developer tools
- Patience and persistence! 🎯

### Tools You'll Need
- **Python 3.8+** with these libraries:
  - `requests` - for HTTP requests
  - `beautifulsoup4` - for HTML parsing
  - `selenium` - for JavaScript-heavy sites
  - `pandas` - for data manipulation
  - `lxml` - for faster XML parsing

### Installation
```bash
pip install requests beautifulsoup4 selenium pandas lxml python-dotenv
```

---

## 🌍 Country-Specific Guides

### 🇫🇷 France

#### Major Supermarket Chains
- **Carrefour** - Largest chain, good for beginners
- **Leclerc** - Cooperative chain, varies by region
- **Monoprix** - Urban focus, premium products
- **Auchan** - Hypermarket format
- **Intermarché** - Independent retailers
- **Lidl** - Discount chain
- **Casino** - Various formats

#### Carrefour Scraping Example
```python
import requests
from bs4 import BeautifulSoup
import time
import random

class CarrefourScraper:
    def __init__(self, city="Paris"):
        self.base_url = "https://www.carrefour.fr"
        self.city = city
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8'
        })
    
    def get_categories(self):
        """Get product categories from Carrefour"""
        categories = [
            "alimentation/epicerie-salee",
            "alimentation/epicerie-sucree", 
            "alimentation/boissons",
            "alimentation/frais",
            "alimentation/surgeles"
        ]
        return categories
    
    def scrape_category(self, category):
        """Scrape products from a specific category"""
        products = []
        page = 1
        
        while True:
            url = f"{self.base_url}/c/{category}?page={page}"
            response = self.session.get(url)
            
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product containers
            product_containers = soup.find_all('div', class_='product-card')
            
            if not product_containers:
                break
                
            for container in product_containers:
                product = self.extract_product_data(container)
                if product:
                    products.append(product)
            
            page += 1
            time.sleep(random.uniform(1, 3))  # Rate limiting
            
        return products
    
    def extract_product_data(self, container):
        """Extract product data from HTML container"""
        try:
            name_elem = container.find('h3', class_='product-title')
            price_elem = container.find('span', class_='price')
            image_elem = container.find('img', class_='product-image')
            
            if not name_elem or not price_elem:
                return None
                
            return {
                'name': name_elem.get_text(strip=True),
                'price': self.parse_price(price_elem.get_text(strip=True)),
                'category': self.get_category_from_url(),
                'store_id': f'carrefour_{self.city}',
                'image_url': image_elem.get('src') if image_elem else None,
                'city': self.city
            }
        except Exception as e:
            print(f"Error extracting product: {e}")
            return None
    
    def parse_price(self, price_text):
        """Parse French price format (e.g., '2,50 €')"""
        try:
            # Remove currency symbol and replace comma with dot
            price_clean = price_text.replace('€', '').replace(',', '.').strip()
            return float(price_clean)
        except:
            return None
```

#### Leclerc Scraping Strategy
```python
class LeclercScraper:
    def __init__(self, city="Paris"):
        self.base_url = "https://www.e.leclerc"
        self.city = city
        # Leclerc uses different URLs per region
        self.region_urls = {
            "Paris": "https://www.e.leclerc/paris",
            "Lyon": "https://www.e.leclerc/lyon",
            "Marseille": "https://www.e.leclerc/marseille"
        }
    
    def get_region_url(self):
        """Get the correct Leclerc URL for the city"""
        return self.region_urls.get(self.city, self.region_urls["Paris"])
```

### 🇪🇸 Spain

#### Major Supermarket Chains
- **Mercadona** - Largest chain, private label focus
- **Carrefour** - International chain
- **El Corte Inglés** - Department store with supermarket
- **Dia** - Discount chain
- **Lidl** - German discount chain
- **Eroski** - Cooperative chain

#### Mercadona Scraping Example
```python
class MercadonaScraper:
    def __init__(self, city="Madrid"):
        self.base_url = "https://www.mercadona.es"
        self.city = city
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
        })
    
    def scrape_products(self):
        """Mercadona has a specific API structure"""
        products = []
        
        # Mercadona categories
        categories = [
            "carnes-y-aves",
            "pescados-y-mariscos", 
            "frutas-y-verduras",
            "lacteos-y-huevos",
            "panaderia-y-pasteleria"
        ]
        
        for category in categories:
            category_products = self.scrape_category(category)
            products.extend(category_products)
            
        return products
    
    def scrape_category(self, category):
        """Scrape Mercadona category"""
        url = f"{self.base_url}/categorias/{category}"
        response = self.session.get(url)
        
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Mercadona uses specific CSS classes
        product_containers = soup.find_all('div', class_='product-item')
        
        for container in product_containers:
            product = self.extract_mercadona_product(container)
            if product:
                products.append(product)
                
        return products
    
    def extract_mercadona_product(self, container):
        """Extract product data from Mercadona container"""
        try:
            name_elem = container.find('h4', class_='product-name')
            price_elem = container.find('span', class_='price')
            
            return {
                'name': name_elem.get_text(strip=True) if name_elem else None,
                'price': self.parse_spanish_price(price_elem.get_text(strip=True)) if price_elem else None,
                'category': self.get_category_name(),
                'store_id': f'mercadona_{self.city}',
                'city': self.city
            }
        except Exception as e:
            print(f"Error extracting Mercadona product: {e}")
            return None
    
    def parse_spanish_price(self, price_text):
        """Parse Spanish price format (e.g., '2,50 €')"""
        try:
            price_clean = price_text.replace('€', '').replace(',', '.').strip()
            return float(price_clean)
        except:
            return None
```

### 🇵🇱 Poland

#### Major Supermarket Chains
- **Biedronka** - Largest discount chain
- **Lidl** - German discount chain
- **Tesco** - British chain
- **Carrefour** - International chain
- **Żabka** - Convenience stores
- **Kaufland** - German hypermarket

#### Biedronka Scraping Example
```python
class BiedronkaScraper:
    def __init__(self, city="Warsaw"):
        self.base_url = "https://www.biedronka.pl"
        self.city = city
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'pl-PL,pl;q=0.9,en;q=0.8'
        })
    
    def scrape_products(self):
        """Biedronka has a simple structure"""
        products = []
        
        # Biedronka main categories
        categories = [
            "spozywcze",
            "chemia-domowa",
            "kosmetyki",
            "akcesoria"
        ]
        
        for category in categories:
            category_products = self.scrape_biedronka_category(category)
            products.extend(category_products)
            
        return products
    
    def scrape_biedronka_category(self, category):
        """Scrape Biedronka category"""
        url = f"{self.base_url}/pl/kategoria/{category}"
        response = self.session.get(url)
        
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Biedronka product containers
        product_containers = soup.find_all('div', class_='product-tile')
        
        for container in product_containers:
            product = self.extract_biedronka_product(container)
            if product:
                products.append(product)
                
        return products
    
    def extract_biedronka_product(self, container):
        """Extract product data from Biedronka container"""
        try:
            name_elem = container.find('h3', class_='product-name')
            price_elem = container.find('span', class_='price-value')
            
            return {
                'name': name_elem.get_text(strip=True) if name_elem else None,
                'price': self.parse_polish_price(price_elem.get_text(strip=True)) if price_elem else None,
                'category': self.get_category_name(),
                'store_id': f'biedronka_{self.city}',
                'city': self.city
            }
        except Exception as e:
            print(f"Error extracting Biedronka product: {e}")
            return None
    
    def parse_polish_price(self, price_text):
        """Parse Polish price format (e.g., '2,50 zł')"""
        try:
            price_clean = price_text.replace('zł', '').replace(',', '.').strip()
            return float(price_clean)
        except:
            return None
```

### 🇩🇪 Germany

#### Major Supermarket Chains
- **Lidl** - Discount chain
- **Aldi** - Discount chain (Nord/Süd)
- **Rewe** - Cooperative chain
- **Edeka** - Cooperative chain
- **Kaufland** - Hypermarket

### 🇬🇧 United Kingdom

#### Major Supermarket Chains
- **Tesco** - Largest chain
- **Sainsbury's** - Premium chain
- **Asda** - Walmart-owned
- **Morrisons** - Regional chain
- **Lidl** - German discount
- **Aldi** - German discount

### 🇮🇹 Italy

#### Major Supermarket Chains
- **Coop** - Cooperative chain
- **Conad** - Cooperative chain
- **Esselunga** - Private chain
- **Carrefour** - International
- **Lidl** - German discount

---

## 🏪 Market-Specific Strategies

### 1. Static HTML Sites (Easiest)
**Best for**: Simple websites without JavaScript
**Tools**: `requests` + `BeautifulSoup`

```python
def scrape_static_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find product containers
    products = soup.find_all('div', class_='product')
    
    for product in products:
        name = product.find('h3').text
        price = product.find('span', class_='price').text
        # Extract other data...
```

### 2. JavaScript-Heavy Sites
**Best for**: Modern e-commerce sites
**Tools**: `selenium` + `webdriver`

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_js_site(url):
    driver = webdriver.Chrome()  # or Firefox()
    driver.get(url)
    
    # Wait for content to load
    wait = WebDriverWait(driver, 10)
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product")))
    
    for product in products:
        name = product.find_element(By.CLASS_NAME, "product-name").text
        price = product.find_element(By.CLASS_NAME, "price").text
        # Extract other data...
    
    driver.quit()
```

### 3. API-Based Sites
**Best for**: Sites that load data via AJAX
**Tools**: `requests` + API endpoints

```python
def scrape_api_site():
    # Find API endpoints using browser dev tools
    api_url = "https://site.com/api/products"
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
    }
    
    response = requests.get(api_url, headers=headers)
    data = response.json()
    
    for product in data['products']:
        # Extract product data from JSON
        pass
```

### 4. Pagination Handling
```python
def scrape_with_pagination(base_url):
    page = 1
    all_products = []
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        products = extract_products_from_page(soup)
        
        if not products:
            break
            
        all_products.extend(products)
        page += 1
        time.sleep(1)  # Rate limiting
        
    return all_products
```

---

## 🔧 Technical Implementation

### 1. Rate Limiting & Respect
```python
import time
import random

def respectful_scraping():
    # Always add delays between requests
    time.sleep(random.uniform(1, 3))
    
    # Use session for connection pooling
    session = requests.Session()
    
    # Rotate user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ]
    
    session.headers.update({
        'User-Agent': random.choice(user_agents)
    })
```

### 2. Error Handling
```python
def robust_scraping(url):
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print(f"Failed to scrape {url} after {max_retries} attempts")
                return None
```

### 3. Data Validation
```python
def validate_product_data(product):
    """Validate scraped product data"""
    required_fields = ['name', 'price', 'category']
    
    for field in required_fields:
        if not product.get(field):
            return False
    
    # Validate price is numeric
    try:
        float(product['price'])
    except (ValueError, TypeError):
        return False
    
    return True
```

### 4. Image URL Handling
```python
def process_image_url(image_url, base_url):
    """Handle relative and absolute image URLs"""
    if not image_url:
        return None
        
    if image_url.startswith('http'):
        return image_url
    elif image_url.startswith('/'):
        return base_url + image_url
    else:
        return base_url + '/' + image_url
```

---

## ⚠️ Common Challenges & Solutions

### 1. Anti-Bot Protection
**Problem**: Site blocks your requests
**Solutions**:
- Use realistic user agents
- Add random delays
- Use proxy rotation (advanced)
- Respect robots.txt

### 2. Dynamic Content Loading
**Problem**: Content loads via JavaScript
**Solutions**:
- Use Selenium WebDriver
- Find API endpoints
- Wait for elements to load

### 3. CAPTCHA Challenges
**Problem**: Site shows CAPTCHA
**Solutions**:
- Reduce request frequency
- Use residential proxies
- Consider manual intervention

### 4. Inconsistent HTML Structure
**Problem**: Site structure changes
**Solutions**:
- Use multiple CSS selectors
- Implement fallback parsing
- Regular monitoring and updates

### 5. Rate Limiting
**Problem**: Too many requests too fast
**Solutions**:
- Implement exponential backoff
- Use session pooling
- Distribute requests over time

---

## 🎯 Best Practices

### 1. Research First
- Study the website structure
- Check robots.txt
- Identify the best scraping approach
- Test with small samples

### 2. Be Respectful
- Add delays between requests
- Don't overload servers
- Follow terms of service
- Use appropriate user agents

### 3. Handle Errors Gracefully
- Implement retry logic
- Log errors for debugging
- Continue scraping despite failures
- Validate data quality

### 4. Monitor and Maintain
- Check for site changes regularly
- Update selectors when needed
- Monitor scraping success rates
- Keep backups of working code

### 5. Data Quality
- Validate scraped data
- Handle missing fields
- Clean and normalize data
- Remove duplicates

---

## 🛠️ Troubleshooting

### Common Error Messages

#### "Connection refused"
```python
# Solution: Check URL and add timeout
response = requests.get(url, timeout=10)
```

#### "Element not found"
```python
# Solution: Use try-except and multiple selectors
try:
    name = soup.find('h1', class_='product-name').text
except AttributeError:
    name = soup.find('h2', class_='title').text
```

#### "JSON decode error"
```python
# Solution: Check response content type
if response.headers.get('content-type') == 'application/json':
    data = response.json()
else:
    print("Response is not JSON")
```

### Debugging Tips

1. **Print intermediate results**
```python
print(f"Scraping URL: {url}")
print(f"Found {len(products)} products")
```

2. **Save HTML for inspection**
```python
with open('debug.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
```

3. **Use browser dev tools**
- Inspect element structure
- Check network requests
- Find API endpoints

4. **Test with small samples**
```python
# Test with first 5 products only
for product in products[:5]:
    # Your scraping logic here
```

---

## 📊 Data Quality Checklist

Before uploading your CSV, ensure:

- [ ] All required fields are present
- [ ] Prices are numeric (no currency symbols)
- [ ] Product names are clean (no extra whitespace)
- [ ] Image URLs are valid
- [ ] No duplicate products
- [ ] Categories are consistent
- [ ] Store IDs follow naming convention
- [ ] City names are standardized

---

## 🚀 Advanced Techniques

### 1. Parallel Scraping
```python
import concurrent.futures
import threading

def scrape_parallel(urls, max_workers=3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scrape_single_url, url) for url in urls]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results
```

### 2. Database Integration
```python
import sqlite3

def save_to_database(products):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    for product in products:
        cursor.execute("""
            INSERT INTO products (name, price, category, store_id, city)
            VALUES (?, ?, ?, ?, ?)
        """, (product['name'], product['price'], product['category'], 
              product['store_id'], product['city']))
    
    conn.commit()
    conn.close()
```

### 3. Progress Tracking
```python
from tqdm import tqdm

def scrape_with_progress(urls):
    products = []
    
    for url in tqdm(urls, desc="Scraping products"):
        product = scrape_single_url(url)
        if product:
            products.append(product)
    
    return products
```

---

## 📞 Getting Help

### When You're Stuck

1. **Check the website structure** - Use browser dev tools
2. **Test with small samples** - Don't scrape everything at once
3. **Look for API endpoints** - Often easier than HTML scraping
4. **Check for existing scrapers** - GitHub, Stack Overflow
5. **Ask for help** - Contact your supervisor

### Useful Resources

- **BeautifulSoup Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Selenium Documentation**: https://selenium-python.readthedocs.io/
- **Requests Documentation**: https://docs.python-requests.org/
- **CSS Selectors Guide**: https://www.w3schools.com/cssref/css_selectors.asp

---

## 🎉 Success Tips

1. **Start Simple**: Begin with static sites before tackling JavaScript-heavy ones
2. **Be Patient**: Good scraping takes time to develop
3. **Test Frequently**: Check your results regularly
4. **Document Everything**: Keep notes on what works and what doesn't
5. **Stay Updated**: Websites change, so your scrapers need updates too

---

**Remember**: The goal is to collect high-quality, accurate data while being respectful to the websites you're scraping. Take your time, test thoroughly, and don't hesitate to ask for help when you need it! 🚀

---

*This guide will be updated regularly as we discover new techniques and encounter new challenges. Check back for updates and additional country-specific examples.*
