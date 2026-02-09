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
                    ┌─────────────────────────┐
                    │  Web Upload Platform    │
                    │  (Vercel Deployment)   │
                    │  ↓                      │
                    │  File Storage           │
                    │  (Cloud Storage)        │
                    └─────────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │  Admin Dashboard        │
                    │  (Monitoring & Download)│
                    └─────────────────────────┘
```

## 📁 Repository Structure

```
SI-Market-Explorer-Intern/
├── api/                        # Vercel serverless functions
│   ├── upload.py              # CSV upload API endpoint
│   └── files.py                # File management API endpoint
├── public/                     # Frontend static files
│   └── index.html             # Web interface (upload + dashboard)
├── interns/                    # Individual intern folders
│   ├── marta_kovacevic_france/
│   ├── carlos_rodriguez_spain/
│   └── anna_nowak_poland/
├── admin/                      # Admin documentation
│   └── README.md              # Admin instructions
├── templates/                  # Templates for interns
│   ├── scraper_template.py    # Scraper code template
│   ├── csv_template.csv       # CSV format example
│   └── supabase_export_guide.md
├── vercel.json                 # Vercel configuration
├── requirements-vercel.txt     # Python dependencies for Vercel
├── package.json                # Node.js configuration
├── .gitignore                 # Security and cleanup
├── README.md                  # This file
├── VERCEL_DEPLOYMENT.md       # Vercel deployment guide
├── VERCEL_SETUP_COMPLETE.md    # Setup summary
└── INTERN_SETUP_GUIDE.md      # Detailed intern onboarding
```

## 🚀 Quick Start

### Deploy to Vercel

**Step 1: Push to GitHub**
```bash
git add .
git commit -m "Add Vercel deployment"
git push origin main
```

**Step 2: Deploy on Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Click "Deploy"

**Step 3: Share Your Link**
Once deployed, you'll get a URL like:
```
https://your-project.vercel.app
```

Share this link with interns to upload CSV files!

### For Interns
1. **Visit Upload Portal**: Go to your Vercel URL
2. **Click "Upload CSV" Tab**: Select the upload interface
3. **Enter Your Name**: Use format `firstname_lastname_country` (e.g., `marta_kovacevic_france`)
4. **Select CSV File**: Choose your `products_YYYY_MM_DD.csv` file
5. **Review Preview**: Check file preview and validation
6. **Upload**: Click "Upload CSV File" button

### For Admins
1. **Visit Dashboard**: Go to your Vercel URL
2. **Click "Admin Dashboard" Tab**: View all intern activity
3. **Monitor Progress**: See metrics, file counts, and statistics
4. **Download Files**: Access individual or bulk downloads

See `VERCEL_DEPLOYMENT.md` for detailed deployment instructions.

## 📊 Key Features

### For Interns
- **Easy Setup**: Pre-built templates and clear instructions
- **Comprehensive Guides**: Detailed scraping instructions for all countries
- **Flexible Scraping**: Customize scrapers for any market worldwide
- **Quick Reference**: Handy reference cards for common tasks
- **Secure Storage**: Individual Supabase databases
- **Web Upload Interface**: Simple CSV upload via web browser (no Git required!)
- **File Validation**: Automatic validation of CSV format and structure
- **Upload History**: View your previously uploaded files

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
- **Vercel**: Web hosting and serverless functions
- **HTML/JavaScript**: Frontend interface
- **Pandas**: CSV processing and validation
- **GitHub**: Version control and collaboration
- **CSV**: Data exchange format

## 🌐 Deployment

The application is deployed on **Vercel**:

1. **Push to GitHub**: Commit and push your code
2. **Deploy on Vercel**: Import repository and deploy
3. **Share URL**: Distribute the Vercel URL to interns

**Features:**
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Serverless functions
- ✅ Easy sharing via URL
- ✅ Automatic deployments on git push

See `VERCEL_DEPLOYMENT.md` for detailed deployment instructions.

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
- [ ] Set up Supabase database
- [ ] Customize scraper template
- [ ] Test scraper with sample data
- [ ] Export first CSV file
- [ ] Access upload portal (web interface)
- [ ] Upload CSV via web interface
- [ ] Verify upload in dashboard

### Admin Setup
- [ ] Push code to GitHub
- [ ] Deploy on Vercel (see `VERCEL_DEPLOYMENT.md`)
- [ ] Implement file storage (Vercel Blob or Supabase Storage)
- [ ] Share Vercel URL with interns
- [ ] Test upload and dashboard functionality
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
