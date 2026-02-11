# Intern Setup Guide

## 🎯 Welcome to Software Intelligence Market Explorer!

This guide will walk you through setting up your market data collection system. By the end of this guide, you'll be able to scrape product data from your local market and upload it to our centralized system.

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Access to the private GitHub repository
- [ ] Basic Python knowledge
- [ ] Internet connection

## 🚀 Step 1: Repository Setup

### 1.1 Clone the Repository
```bash
git clone https://github.com/Derda24/SI-Market-Explorer.git
cd SI-Market-Explorer
```

### 1.2 Create Your Personal Folder
Create a folder with your name and country:
```bash
mkdir interns/your_firstname_lastname_country
```

**Example:**
```bash
mkdir interns/marta_kovacevic_france
mkdir interns/carlos_rodriguez_spain
mkdir interns/anna_nowak_poland
```

### 1.3 Navigate to Your Folder
```bash
cd interns/your_firstname_lastname_country
```

## 🗄️ Step 2: Database Setup

### 2.1 Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Sign up for a free account
3. Create a new project
4. Choose a region close to your location

### 2.2 Set Up Database Schema
Run this SQL in your Supabase SQL editor:

```sql
-- Create products table
CREATE TABLE public.products (
  name text NULL,
  price numeric NULL,
  category text NULL,
  store_id text NULL,
  quantity text NULL,
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at timestamp without time zone NULL DEFAULT now(),
  image_url text NULL,
  nutriscore text NULL,
  nova_group integer NULL,
  energy_kcal numeric NULL,
  sugars_100g numeric NULL,
  salt_100g numeric NULL,
  saturated_fat_100g numeric NULL,
  city text NULL,
  CONSTRAINT products_pkey PRIMARY KEY (id),
  CONSTRAINT unique_name_store UNIQUE (name, store_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_category ON public.products USING btree (category);
CREATE INDEX IF NOT EXISTS idx_products_name ON public.products USING btree (name);
CREATE INDEX IF NOT EXISTS idx_products_store_id ON public.products USING btree (store_id);
```

### 2.3 Get Your Credentials
1. In Supabase dashboard, go to Settings → API
2. Copy your Project URL and API Key
3. Keep these credentials secure (don't share them)

## 🕷️ Step 3: Scraper Setup

### 3.1 Copy the Template
```bash
cp ../../templates/scraper_template.py scraper.py
```

### 3.2 Read the Complete Scraping Guide
**IMPORTANT**: Before customizing your scraper, read the comprehensive scraping guide:
```bash
# Open the detailed scraping guide
cat ../../templates/SCRAPING_GUIDE.md
```

This guide contains:
- Country-specific examples (France, Spain, Poland, Germany, UK, Italy)
- Market-specific strategies for different supermarket chains
- Technical implementation details
- Common challenges and solutions
- Best practices and troubleshooting

### 3.3 Customize Your Scraper
Edit `scraper.py` and update these variables:

```python
# TODO: Replace with your actual market details
MARKET_NAME = "Carrefour"        # Your target market
COUNTRY = "France"               # Your country
CITY = "Paris"                   # Your city
```

### 3.3 Set Up Environment Variables
Create a `.env` file in your folder:
```bash
# .env file (keep this private!)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

### 3.4 Install Dependencies
```bash
pip install requests pandas python-dotenv supabase
```

## 🏪 Step 4: Market Research

### 4.1 Choose Your Target Market
Select a major supermarket chain in your area:
- **France**: Carrefour, Leclerc, Monoprix, Auchan
- **Spain**: Mercadona, Carrefour, El Corte Inglés, Dia
- **Poland**: Biedronka, Lidl, Tesco, Carrefour
- **Other countries**: Research local major chains

### 4.2 Analyze the Website
1. Visit the market's website
2. Find the product catalog/section
3. Note the URL structure
4. Check if they use JavaScript (affects scraping method)
5. Identify product detail pages

### 4.3 Plan Your Scraping Strategy
- **Product categories**: Focus on food products initially
- **Geographic scope**: Choose 1-2 cities to start
- **Data fields**: Prioritize name, price, category, image
- **Rate limiting**: Be respectful (1-3 seconds between requests)

## 🔧 Step 5: Implement Your Scraper

### 5.1 Basic Scraper Structure
Your scraper should:
1. Connect to Supabase
2. Scrape product listings
3. Extract product details
4. Save to database
5. Handle errors gracefully

### 5.2 Example Implementation
Here's a simplified example for a static website:

```python
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_products():
    products = []
    base_url = "https://your-market-website.com"
    
    # Get product listing page
    response = requests.get(f"{base_url}/products")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find product links
    product_links = soup.find_all('a', class_='product-link')
    
    for link in product_links:
        product_url = base_url + link['href']
        product_data = scrape_single_product(product_url)
        
        if product_data:
            products.append(product_data)
        
        # Rate limiting
        time.sleep(random.uniform(1, 3))
    
    return products

def scrape_single_product(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'name': soup.find('h1').text.strip(),
            'price': extract_price(soup),
            'category': soup.find('.category').text.strip(),
            # ... other fields
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
```

### 5.3 Test Your Scraper
```bash
python scraper.py
```

Check your Supabase dashboard to verify data is being saved.

## 📊 Step 6: Export and Upload Data

### 6.1 Export CSV from Supabase
1. Go to Supabase Table Editor
2. Select your `products` table
3. Click "Export" → "CSV"
4. Save the file

### 6.2 Rename Your CSV
Use this naming convention:
```
products_YYYY_MM_DD.csv
```

Example: `products_2025_01_15.csv`

### 6.3 Upload to GitHub
```bash
# Add your CSV file
git add products_2025_01_15.csv

# Commit with descriptive message
git commit -m "Add initial product data for Carrefour Paris - 150 products"

# Push to repository
git push origin main
```

## 📈 Step 7: Monitor Your Progress

### 7.1 Check Admin Dashboard
The admin can track your progress using the dashboard:
- Total products scraped
- Number of CSV uploads
- Latest upload date
- Data quality metrics

### 7.2 Regular Updates
Upload new CSV files weekly:
- Run your scraper regularly
- Export fresh data from Supabase
- Upload with date stamps
- Notify admin of updates

## 🛠️ Troubleshooting

### Common Issues

**Q: My scraper isn't working**
- Check your internet connection
- Verify the website hasn't changed structure
- Look at error logs in your console
- Test with a small subset first

**Q: Supabase connection failed**
- Verify your URL and API key
- Check if your project is active
- Ensure you have the correct permissions

**Q: CSV export is empty**
- Check if data exists in your Supabase table
- Verify your table has the correct columns
- Try exporting from SQL editor instead

**Q: Git push failed**
- Make sure you have the latest changes: `git pull`
- Check if you're in the correct branch
- Verify your GitHub permissions

### Getting Help
1. **Check Documentation**: Review templates and guides
2. **Read Scraping Guide**: See `templates/SCRAPING_GUIDE.md` for detailed scraping instructions
3. **Test Incrementally**: Start small and build up
4. **Contact Admin**: For technical or access issues
5. **Review Logs**: Check error messages for clues

## 📅 Weekly Routine

### Monday: Planning
- [ ] Review previous week's data
- [ ] Plan new categories to scrape
- [ ] Check for website changes

### Tuesday-Thursday: Scraping
- [ ] Run scraper for new products
- [ ] Monitor data quality
- [ ] Handle any errors

### Friday: Upload
- [ ] Export fresh CSV from Supabase
- [ ] Upload to GitHub
- [ ] Update admin on progress

## 🎯 Success Metrics

Track these metrics to measure your progress:
- **Products per week**: Aim for 100-500 products
- **Data quality**: 90%+ complete records
- **Consistency**: Regular weekly uploads
- **Coverage**: Multiple product categories

## 📞 Support Contacts

- **Technical Issues**: Contact the repository admin
- **Database Problems**: Check Supabase documentation
- **Scraping Challenges**: Review template examples
- **GitHub Issues**: Check repository issues section

## 🏆 Best Practices

1. **Be Respectful**: Don't overload websites with requests
2. **Stay Consistent**: Regular uploads are better than large batches
3. **Quality First**: Better to have fewer high-quality records
4. **Document Changes**: Note any website structure changes
5. **Backup Data**: Keep local copies of important CSVs

---

**Good luck with your market data collection! 🚀**

*Remember: If you encounter any issues, don't hesitate to ask for help. The admin is here to support your success.*
