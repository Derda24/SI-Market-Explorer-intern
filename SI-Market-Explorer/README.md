# Software Intelligence - Market Explorer

## 🎯 Project Overview

This repository serves as a centralized platform for managing intern market data collection across multiple countries. Interns scrape product data from local markets, store it in their individual Supabase databases, and upload CSV exports to this repository for centralized monitoring and analysis.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Intern A      │    │   Intern B       │    │   Intern C      │
│   (France)      │    │   (Spain)        │    │   (Poland)      │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ Local Scraper   │    │ Local Scraper    │    │ Local Scraper   │
│ ↓               │    │ ↓                │    │ ↓               │
│ Supabase DB     │    │ Supabase DB      │    │ Supabase DB     │
│ ↓               │    │ ↓                │    │ ↓               │
│ CSV Export      │    │ CSV Export       │    │ CSV Export      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ GitHub Repo     │
                    │ (This Repo)     │
                    │ ↓               │
                    │ Admin Dashboard │
                    └─────────────────┘
```

## 📁 Repository Structure

```
SI-Market-Explorer/
├── interns/                    # Individual intern folders
│   ├── marta_kovacevic_france/
│   ├── carlos_rodriguez_spain/
│   └── anna_nowak_poland/
├── admin/                      # Admin tools and dashboard
│   ├── dashboard.py           # Streamlit dashboard
│   ├── requirements.txt       # Dashboard dependencies
│   └── README.md              # Admin instructions
├── templates/                  # Templates for interns
│   ├── scraper_template.py    # Scraper code template
│   ├── csv_template.csv       # CSV format example
│   └── supabase_export_guide.md
├── .gitignore                 # Security and cleanup
├── README.md                  # This file
└── INTERN_SETUP_GUIDE.md     # Detailed intern onboarding
```

## 🚀 Quick Start

### For Interns
1. **Clone the repository**: `git clone [repo-url]`
2. **Create your folder**: `interns/your_name_country/`
3. **Learn scraping**: Read `templates/SCRAPING_GUIDE.md` for comprehensive instructions
4. **Quick reference**: Use `templates/SCRAPING_QUICK_REFERENCE.md` while coding
5. **Set up your scraper**: Use `templates/scraper_template.py`
6. **Export data**: Follow `templates/supabase_export_guide.md`
7. **Upload CSV**: Commit and push your CSV files

### For Admins
1. **Install dependencies**: `pip install -r admin/requirements.txt`
2. **Run dashboard**: `streamlit run admin/dashboard.py`
3. **Monitor progress**: View intern activity and download data

## 📊 Key Features

### For Interns
- **Easy Setup**: Pre-built templates and clear instructions
- **Comprehensive Guides**: Detailed scraping instructions for all countries
- **Flexible Scraping**: Customize scrapers for any market worldwide
- **Quick Reference**: Handy reference cards for common tasks
- **Secure Storage**: Individual Supabase databases
- **Simple Upload**: CSV export and GitHub upload

### For Admins
- **Real-time Monitoring**: Track all intern progress
- **Data Visualization**: Charts and graphs of collected data
- **Bulk Downloads**: Download all data or individual files
- **Progress Tracking**: See who's active and when

## 🔒 Security & Privacy

- **Private Repository**: Only authorized users can access
- **Individual Databases**: Each intern has their own Supabase instance
- **Local Processing**: All scraping happens locally on intern machines
- **Controlled Access**: Admin approval required for data integration

## 📈 Data Schema

All CSV files must follow this standardized schema:

| Column | Type | Description |
|--------|------|-------------|
| `name` | text | Product name |
| `price` | numeric | Product price |
| `category` | text | Product category |
| `store_id` | text | Store identifier |
| `quantity` | text | Product quantity/size |
| `image_url` | text | Product image URL |
| `nutriscore` | text | Nutritional score (A-E) |
| `nova_group` | integer | NOVA food group (1-4) |
| `energy_kcal` | numeric | Energy in kcal per 100g |
| `sugars_100g` | numeric | Sugars per 100g |
| `salt_100g` | numeric | Salt per 100g |
| `saturated_fat_100g` | numeric | Saturated fat per 100g |
| `city` | text | City where product was found |
| `created_at` | timestamp | Data creation timestamp |

## 🛠️ Technology Stack

- **Python**: Core scraping and processing
- **Supabase**: Individual database storage
- **Streamlit**: Admin dashboard interface
- **GitHub**: Version control and collaboration
- **CSV**: Data exchange format

## 📞 Support & Contact

### For Technical Issues
- Check the documentation in `/templates/` folder
- Review the `INTERN_SETUP_GUIDE.md` for detailed instructions
- Contact the admin for repository access issues

### For Data Questions
- Use the admin dashboard for data analysis
- Contact individual interns for specific market questions
- Review CSV templates for data format requirements

## 📋 Getting Started Checklist

### Intern Onboarding
- [ ] Clone repository
- [ ] Create personal folder (`interns/your_name_country/`)
- [ ] Set up Supabase database
- [ ] Customize scraper template
- [ ] Test scraper with sample data
- [ ] Export first CSV file
- [ ] Upload CSV to GitHub
- [ ] Notify admin of first upload

### Admin Setup
- [ ] Install Streamlit dependencies
- [ ] Test dashboard functionality
- [ ] Set up monitoring schedule
- [ ] Configure data backup procedures
- [ ] Train team on dashboard usage

## 🎯 Project Goals

1. **Centralized Data Collection**: Gather market data from multiple countries
2. **Quality Control**: Ensure data consistency and accuracy
3. **Progress Monitoring**: Track intern activity and productivity
4. **Scalable Architecture**: Support growing team and new markets
5. **Data Security**: Protect sensitive information and maintain privacy

## 📝 License

This project is proprietary to Software Intelligence. All rights reserved.

---

**Software Intelligence Team**  
*Market Data Collection & Analysis Platform*
