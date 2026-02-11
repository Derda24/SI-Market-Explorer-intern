# Interns Directory

## 📁 Folder Structure

Each intern should create their own folder following this naming convention:

```
interns/
├── firstname_lastname_country/
│   ├── scraper.py
│   ├── products_2025_01_15.csv
│   ├── products_2025_01_22.csv
│   └── .env (keep private!)
```

## 🏷️ Naming Convention

**Folder Name Format**: `firstname_lastname_country`

**Examples:**
- `marta_kovacevic_france`
- `carlos_rodriguez_spain`
- `anna_nowak_poland`
- `john_smith_uk`

## 📄 Required Files

### 1. Scraper File
- **Name**: `scraper.py`
- **Purpose**: Your market data scraper
- **Template**: Copy from `../templates/scraper_template.py`

### 2. CSV Files
- **Name**: `products_YYYY_MM_DD.csv`
- **Purpose**: Exported product data from Supabase
- **Frequency**: Weekly uploads recommended

### 3. Environment File (Private)
- **Name**: `.env`
- **Purpose**: Supabase credentials (DO NOT commit to git!)
- **Contents**:
  ```
  SUPABASE_URL=your_url_here
  SUPABASE_KEY=your_key_here
  ```

## 🚀 Getting Started

1. **Create Your Folder**
   ```bash
   mkdir interns/your_name_country
   cd interns/your_name_country
   ```

2. **Copy Template**
   ```bash
   cp ../../templates/scraper_template.py scraper.py
   ```

3. **Customize Scraper**
   - Edit `scraper.py`
   - Update market name, country, city
   - Implement your scraping logic

4. **Set Up Database**
   - Create Supabase account
   - Set up database schema
   - Add credentials to `.env`

5. **Test and Upload**
   - Run your scraper
   - Export CSV from Supabase
   - Upload CSV to GitHub

## 📊 CSV Requirements

Your CSV files must include these columns:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| `name` | ✅ | text | Product name |
| `price` | ✅ | numeric | Product price |
| `category` | ✅ | text | Product category |
| `store_id` | ✅ | text | Store identifier |
| `quantity` | ❌ | text | Product quantity/size |
| `image_url` | ❌ | text | Product image URL |
| `nutriscore` | ❌ | text | Nutritional score (A-E) |
| `nova_group` | ❌ | integer | NOVA food group (1-4) |
| `energy_kcal` | ❌ | numeric | Energy in kcal per 100g |
| `sugars_100g` | ❌ | numeric | Sugars per 100g |
| `salt_100g` | ❌ | numeric | Salt per 100g |
| `saturated_fat_100g` | ❌ | numeric | Saturated fat per 100g |
| `city` | ✅ | text | City where product was found |
| `created_at` | ✅ | timestamp | Data creation timestamp |

## 📅 Upload Schedule

**Recommended Upload Frequency**: Weekly

**File Naming**: Use date format `YYYY_MM_DD`
- `products_2025_01_15.csv`
- `products_2025_01_22.csv`
- `products_2025_01_29.csv`

## 🔒 Security Notes

- **Never commit `.env` files** - they contain sensitive credentials
- **Keep your Supabase credentials private**
- **Don't share your scraper code with other interns**
- **Use rate limiting** to be respectful to target websites

## 📈 Progress Tracking

The admin can monitor your progress through:
- Number of CSV files uploaded
- Total products collected
- Latest upload date
- Data quality metrics

## 🆘 Getting Help

1. **Check Templates**: Review files in `../templates/` folder
2. **Read Guide**: See `../INTERN_SETUP_GUIDE.md` for detailed instructions
3. **Contact Admin**: For technical or access issues
4. **Review Examples**: Look at other intern folders (if any exist)

## ✅ Checklist

Before uploading your first CSV:

- [ ] Folder created with correct naming convention
- [ ] Scraper implemented and tested
- [ ] Supabase database set up
- [ ] First batch of products scraped
- [ ] CSV exported with correct format
- [ ] File named with date stamp
- [ ] Ready to commit and push

## 📞 Contact

For questions about this directory structure or requirements, contact the repository admin.

---

**Good luck with your market data collection! 🚀**
