# Admin Dashboard

## 🎯 Overview

This dashboard provides a comprehensive view of all intern activities, progress tracking, and data management capabilities for the Software Intelligence Market Explorer project.

## 🚀 Quick Start

### 1. Installation
```bash
cd admin
pip install -r requirements.txt
```

### 2. Run Dashboard
```bash
streamlit run dashboard.py
```

### 3. Access Dashboard
Open your browser to: `http://localhost:8501`

## 📊 Dashboard Features

### Overview Page
- **Total Metrics**: Interns, CSV files, products, data size
- **Recent Activity**: Timeline of uploads
- **Quick Stats**: At-a-glance project status

### Intern Progress Page
- **Individual Tracking**: Progress per intern
- **Country Analysis**: Products by country
- **Visual Charts**: Bar charts and pie charts
- **Performance Metrics**: Upload frequency, data quality

### CSV Downloads Page
- **Individual Downloads**: Download specific CSV files
- **File Previews**: Quick data previews
- **Intern Selection**: Filter by specific intern
- **Metadata Display**: File size, product count, dates

### Bulk Download Page
- **All Data Export**: Single CSV with all intern data
- **ZIP Archive**: Complete file collection
- **Batch Processing**: Download multiple files at once

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web dashboard framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charts and visualizations
- **Pathlib**: File system operations

### Data Sources
- **CSV Files**: Located in `../interns/` directory
- **File Structure**: `interns/name_country/products_*.csv`
- **Schema**: Standardized product data format

### Performance
- **Real-time Updates**: Dashboard refreshes with new data
- **Efficient Loading**: Optimized for large datasets
- **Memory Management**: Handles multiple large CSV files

## 📁 Directory Structure

```
admin/
├── dashboard.py          # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### File Paths
The dashboard automatically scans for CSV files in:
```
../interns/*/products_*.csv
```

### Expected File Format
CSV files should follow this naming convention:
- `products_YYYY_MM_DD.csv`
- Example: `products_2025_01_15.csv`

### Data Schema
Expected CSV columns:
```
name,price,category,store_id,quantity,image_url,nutriscore,
nova_group,energy_kcal,sugars_100g,salt_100g,saturated_fat_100g,
city,created_at
```

## 📈 Monitoring Features

### Real-time Metrics
- **Total Interns**: Number of active interns
- **Total Files**: CSV files uploaded
- **Total Products**: Combined product count
- **Data Size**: Total storage usage

### Progress Tracking
- **Individual Progress**: Per-intern statistics
- **Upload Frequency**: How often interns upload
- **Data Quality**: Completeness of records
- **Geographic Coverage**: Products by country

### Visual Analytics
- **Timeline Charts**: Upload activity over time
- **Country Distribution**: Products by geography
- **Category Analysis**: Product type breakdown
- **Performance Trends**: Progress visualization

## 📥 Download Capabilities

### Individual Downloads
- **Single CSV**: Download specific intern files
- **File Preview**: Quick data inspection
- **Metadata**: File size, product count, dates
- **Format Validation**: Check CSV structure

### Bulk Operations
- **Merged CSV**: All data in single file
- **ZIP Archive**: Complete file collection
- **Batch Export**: Multiple files at once
- **Filtered Downloads**: By date, intern, or country

## 🔒 Security Features

### Access Control
- **Local Only**: Dashboard runs on local machine
- **No External Access**: Not exposed to internet
- **File Permissions**: Respects system file access
- **Data Privacy**: No data transmitted externally

### Data Protection
- **Read-Only Operations**: No data modification
- **Backup Capabilities**: Export all data
- **Version Control**: Track file changes via Git
- **Audit Trail**: Monitor all downloads

## 🚨 Troubleshooting

### Common Issues

**Dashboard won't start**
- Check Python installation: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Verify Streamlit: `streamlit --version`

**No data displayed**
- Check file paths in `../interns/` directory
- Verify CSV file naming convention
- Ensure CSV files have correct schema

**Download errors**
- Check file permissions
- Verify CSV file integrity
- Ensure sufficient disk space

**Performance issues**
- Close other applications
- Check available RAM
- Consider data filtering options

### Debug Mode
Run with debug information:
```bash
streamlit run dashboard.py --logger.level=debug
```

## 📊 Usage Examples

### Daily Monitoring
1. Open dashboard in morning
2. Check "Overview" for new uploads
3. Review "Intern Progress" for activity
4. Download any new CSV files needed

### Weekly Review
1. Use "Bulk Download" for complete data export
2. Analyze trends in "Intern Progress"
3. Check data quality across all interns
4. Generate reports for stakeholders

### Data Export
1. Select specific intern from "CSV Downloads"
2. Preview data before downloading
3. Use "Bulk Download" for complete dataset
4. Save exports with timestamps

## 🔄 Maintenance

### Regular Tasks
- **Weekly**: Check for new uploads
- **Monthly**: Review data quality trends
- **Quarterly**: Archive old CSV files
- **As Needed**: Update dashboard features

### Data Management
- **Backup**: Regular exports of all data
- **Cleanup**: Remove old/unused files
- **Validation**: Check CSV format compliance
- **Monitoring**: Track intern engagement

## 📞 Support

### Technical Issues
- Check Streamlit documentation
- Review error logs in terminal
- Verify file permissions and paths
- Contact development team

### Feature Requests
- Document requirements clearly
- Provide use case examples
- Consider impact on existing functionality
- Submit through appropriate channels

## 🎯 Best Practices

### Dashboard Usage
- **Regular Monitoring**: Check daily for new uploads
- **Data Validation**: Preview files before downloading
- **Backup Strategy**: Regular exports of important data
- **Performance**: Monitor system resources

### Data Management
- **File Organization**: Maintain clear directory structure
- **Naming Conventions**: Follow established patterns
- **Quality Control**: Validate CSV format and content
- **Documentation**: Keep records of changes and issues

---

**Software Intelligence - Admin Dashboard**  
*Market Data Collection & Management Platform*
