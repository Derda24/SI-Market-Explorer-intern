# Supabase CSV Export Guide

This guide explains how to export your scraped product data from Supabase as CSV files for upload to the GitHub repository.

## Method 1: Using Supabase Dashboard (Recommended)

### Step 1: Access Your Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign in to your account
3. Select your project

### Step 2: Navigate to Table Editor
1. In the left sidebar, click on "Table Editor"
2. Select the `products` table

### Step 3: Export Data
1. Click on the "Export" button (usually at the top of the table)
2. Select "CSV" as the export format
3. Choose your export options:
   - **All columns**: Export all product data
   - **Filtered data**: If you want specific date ranges or filters
4. Click "Download" to save the CSV file

### Step 4: Rename the File
Rename the downloaded file to follow the naming convention:
```
products_YYYY_MM_DD.csv
```
Example: `products_2025_01_15.csv`

## Method 2: Using SQL Query (Advanced)

### Step 1: Open SQL Editor
1. In Supabase dashboard, click on "SQL Editor" in the left sidebar
2. Create a new query

### Step 2: Write Export Query
```sql
-- Export all products
SELECT 
    name,
    price,
    category,
    store_id,
    quantity,
    image_url,
    nutriscore,
    nova_group,
    energy_kcal,
    sugars_100g,
    salt_100g,
    saturated_fat_100g,
    city,
    created_at
FROM products
WHERE created_at >= '2025-01-01'  -- Filter by date if needed
ORDER BY created_at DESC;
```

### Step 3: Run and Export
1. Click "Run" to execute the query
2. In the results, click the "Export" button
3. Select "CSV" format and download

## Method 3: Using Python Script (For Automation)

If you want to automate the export process, you can use this Python script:

```python
import os
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# Supabase configuration
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"

def export_products_to_csv():
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Fetch all products
    response = supabase.table('products').select('*').execute()
    
    # Convert to DataFrame
    df = pd.DataFrame(response.data)
    
    # Generate filename with current date
    timestamp = datetime.now().strftime("%Y_%m_%d")
    filename = f"products_{timestamp}.csv"
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Exported {len(df)} products to {filename}")
    
    return filename

if __name__ == "__main__":
    export_products_to_csv()
```

## Important Notes

### CSV Column Requirements
Make sure your CSV includes all these columns (in any order):
- `name` - Product name
- `price` - Product price (numeric)
- `category` - Product category
- `store_id` - Store identifier
- `quantity` - Product quantity/size
- `image_url` - Product image URL
- `nutriscore` - Nutritional score (A-E)
- `nova_group` - NOVA food group (1-4)
- `energy_kcal` - Energy in kcal per 100g
- `sugars_100g` - Sugars per 100g
- `salt_100g` - Salt per 100g
- `saturated_fat_100g` - Saturated fat per 100g
- `city` - City where product was found
- `created_at` - Timestamp when data was created

### Data Quality Tips
1. **Check for duplicates**: Remove duplicate products before export
2. **Validate prices**: Ensure prices are numeric and reasonable
3. **Check dates**: Verify created_at timestamps are correct
4. **Image URLs**: Ensure image URLs are accessible
5. **Nutritional data**: Fill in nutritional information where possible

### File Naming Convention
Always use this format for your CSV files:
```
products_YYYY_MM_DD.csv
```

Examples:
- `products_2025_01_15.csv`
- `products_2025_01_22.csv`
- `products_2025_02_01.csv`

## Troubleshooting

### Common Issues

**Q: My CSV export is empty**
- Check if you have data in your products table
- Verify your date filters are correct
- Ensure you're looking at the right project

**Q: Missing columns in CSV**
- Make sure all required columns exist in your table
- Check for typos in column names
- Verify your SQL query includes all needed fields

**Q: File too large**
- Consider filtering by date range
- Export in smaller batches
- Check for duplicate data

### Getting Help
If you encounter issues:
1. Check the Supabase documentation
2. Review your scraper logs
3. Contact the admin for assistance

## Next Steps

After exporting your CSV:
1. Upload it to your intern folder: `interns/your_name_country/`
2. Commit and push to GitHub
3. Notify the admin that new data is available
4. Update your progress in the intern tracking system
