#!/usr/bin/env python3
"""
Intern Management Dashboard
===========================

Streamlit dashboard for monitoring intern progress and downloading CSV files.
This dashboard provides an overview of all intern activities and allows
administrators to download and review scraped data.

Usage:
    streamlit run dashboard.py

Author: Software Intelligence Team
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import glob
from pathlib import Path
import zipfile
import io
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Intern Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class InternDashboard:
    """Main dashboard class for intern management"""
    
    def __init__(self):
        # Get the correct path to interns directory - FIXED PATH
        current_dir = Path(__file__).parent  # This is admin/
        self.interns_dir = current_dir.parent / "interns"  # This should be SI-Market-Explorer/interns/
        
        # Debug: Print the actual path being used
        st.info(f"Looking for interns directory at: {self.interns_dir.absolute()}")
        st.info(f"Directory exists: {self.interns_dir.exists()}")
        
        # If still not found, create it or use absolute path
        if not self.interns_dir.exists():
            # Try absolute path
            absolute_path = Path("C:/Users/turlu/SI-Market-Explorer/interns")
            st.warning(f"Trying absolute path: {absolute_path}")
            if absolute_path.exists():
                self.interns_dir = absolute_path
                st.success("Found interns directory using absolute path!")
            else:
                st.error("Interns directory not found anywhere!")
        self.csv_columns = [
            'name', 'price', 'category', 'store_id', 'quantity', 'image_url',
            'nutriscore', 'nova_group', 'energy_kcal', 'sugars_100g', 
            'salt_100g', 'saturated_fat_100g', 'city', 'created_at'
        ]
    
    def get_intern_directories(self) -> List[str]:
        """Get list of all intern directories"""
        if not self.interns_dir.exists():
            st.error(f"Interns directory not found at: {self.interns_dir}")
            return []
        
        intern_dirs = [d.name for d in self.interns_dir.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
        
        # Debug info
        st.info(f"Found {len(intern_dirs)} intern directories: {intern_dirs}")
        return sorted(intern_dirs)
    
    def get_csv_files(self, intern_dir: str) -> List[Tuple[str, str]]:
        """Get all CSV files for a specific intern"""
        intern_path = self.interns_dir / intern_dir
        if not intern_path.exists():
            return []
        
        csv_files = []
        for csv_file in intern_path.glob("products_*.csv"):
            file_path = str(csv_file)
            file_date = self._extract_date_from_filename(csv_file.name)
            csv_files.append((file_path, file_date))
        
        return sorted(csv_files, key=lambda x: x[1], reverse=True)
    
    def _extract_date_from_filename(self, filename: str) -> str:
        """Extract date from filename like products_2025_01_15.csv"""
        try:
            date_part = filename.replace('products_', '').replace('.csv', '')
            return date_part
        except:
            return "unknown"
    
    def get_csv_summary(self, csv_file: str) -> Dict:
        """Get summary statistics for a CSV file"""
        try:
            df = pd.read_csv(csv_file)
            return {
                'total_products': len(df),
                'unique_categories': df['category'].nunique() if 'category' in df.columns else 0,
                'avg_price': df['price'].mean() if 'price' in df.columns else 0,
                'file_size': os.path.getsize(csv_file),
                'last_modified': datetime.fromtimestamp(os.path.getmtime(csv_file))
            }
        except Exception as e:
            logger.error(f"Error reading CSV {csv_file}: {str(e)}")
            return {
                'total_products': 0,
                'unique_categories': 0,
                'avg_price': 0,
                'file_size': 0,
                'last_modified': datetime.now()
            }
    
    def load_all_data(self) -> pd.DataFrame:
        """Load and merge all CSV data from all interns"""
        all_data = []
        
        for intern_dir in self.get_intern_directories():
            csv_files = self.get_csv_files(intern_dir)
            
            for csv_file, date in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    df['intern'] = intern_dir
                    df['upload_date'] = date
                    all_data.append(df)
                except Exception as e:
                    logger.error(f"Error loading {csv_file}: {str(e)}")
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def display_overview_metrics(self):
        """Display key metrics overview"""
        st.header("📊 Overview Metrics")
        
        intern_dirs = self.get_intern_directories()
        total_interns = len(intern_dirs)
        
        # Calculate total metrics
        total_csv_files = 0
        total_products = 0
        total_size = 0
        
        for intern_dir in intern_dirs:
            csv_files = self.get_csv_files(intern_dir)
            total_csv_files += len(csv_files)
            
            for csv_file, _ in csv_files:
                summary = self.get_csv_summary(csv_file)
                total_products += summary['total_products']
                total_size += summary['file_size']
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Interns", total_interns)
        
        with col2:
            st.metric("Total CSV Files", total_csv_files)
        
        with col3:
            st.metric("Total Products", f"{total_products:,}")
        
        with col4:
            st.metric("Total Data Size", f"{total_size / (1024*1024):.1f} MB")
    
    def display_intern_progress(self):
        """Display individual intern progress"""
        st.header("👥 Intern Progress")
        
        intern_dirs = self.get_intern_directories()
        
        if not intern_dirs:
            st.warning("No intern directories found. Make sure interns have uploaded their CSV files.")
            return
        
        # Create progress data
        progress_data = []
        
        for intern_dir in intern_dirs:
            csv_files = self.get_csv_files(intern_dir)
            
            total_products = 0
            latest_upload = None
            total_size = 0
            
            for csv_file, date in csv_files:
                summary = self.get_csv_summary(csv_file)
                total_products += summary['total_products']
                total_size += summary['file_size']
                
                if not latest_upload or date > latest_upload:
                    latest_upload = date
            
            # Parse country from directory name (assuming format: name_country)
            parts = intern_dir.split('_')
            country = parts[-1] if len(parts) > 1 else "Unknown"
            name = '_'.join(parts[:-1]) if len(parts) > 1 else intern_dir
            
            progress_data.append({
                'Intern': name,
                'Country': country,
                'CSV Files': len(csv_files),
                'Total Products': total_products,
                'Latest Upload': latest_upload or "No uploads",
                'Data Size (MB)': round(total_size / (1024*1024), 2)
            })
        
        # Display progress table
        progress_df = pd.DataFrame(progress_data)
        st.dataframe(progress_df, use_container_width=True)
        
        # Progress charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                progress_df, 
                x='Intern', 
                y='Total Products',
                title='Products by Intern',
                color='Country'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                progress_df, 
                values='Total Products', 
                names='Country',
                title='Products by Country'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def display_csv_downloads(self):
        """Display CSV download interface"""
        st.header("📥 Download CSV Files")
        
        intern_dirs = self.get_intern_directories()
        
        if not intern_dirs:
            st.warning("No intern directories found.")
            return
        
        # Intern selection
        selected_intern = st.selectbox(
            "Select Intern:",
            intern_dirs,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if selected_intern:
            csv_files = self.get_csv_files(selected_intern)
            
            if not csv_files:
                st.warning(f"No CSV files found for {selected_intern}")
                return
            
            st.subheader(f"CSV Files for {selected_intern.replace('_', ' ').title()}")
            
            # Display CSV files with download options
            for csv_file, date in csv_files:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    summary = self.get_csv_summary(csv_file)
                    st.write(f"**{os.path.basename(csv_file)}**")
                    st.caption(f"Products: {summary['total_products']} | "
                             f"Size: {summary['file_size']/1024:.1f} KB | "
                             f"Date: {date}")
                
                with col2:
                    with open(csv_file, 'rb') as f:
                        st.download_button(
                            "📄 Download",
                            f.read(),
                            file_name=os.path.basename(csv_file),
                            mime="text/csv",
                            key=f"download_{csv_file}"
                        )
                
                with col3:
                    if st.button("📊 Preview", key=f"preview_{csv_file}"):
                        try:
                            df = pd.read_csv(csv_file)
                            st.subheader(f"Preview: {os.path.basename(csv_file)}")
                            st.dataframe(df.head(10), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error reading file: {str(e)}")
    
    def display_bulk_download(self):
        """Display bulk download options"""
        st.header("📦 Bulk Download")
        
        # Download all data as single CSV
        if st.button("📊 Download All Data as Single CSV"):
            all_data = self.load_all_data()
            
            if all_data.empty:
                st.warning("No data available for download.")
                return
            
            csv_buffer = io.StringIO()
            all_data.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            filename = f"all_intern_data_{timestamp}.csv"
            
            st.download_button(
                "📥 Download All Data",
                csv_data,
                file_name=filename,
                mime="text/csv"
            )
        
        # Download all files as ZIP
        if st.button("📁 Download All Files as ZIP"):
            intern_dirs = self.get_intern_directories()
            
            if not intern_dirs:
                st.warning("No intern directories found.")
                return
            
            # Create ZIP file in memory
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for intern_dir in intern_dirs:
                    csv_files = self.get_csv_files(intern_dir)
                    
                    for csv_file, date in csv_files:
                        arcname = f"{intern_dir}/{os.path.basename(csv_file)}"
                        zip_file.write(csv_file, arcname)
            
            zip_buffer.seek(0)
            
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            filename = f"all_intern_files_{timestamp}.zip"
            
            st.download_button(
                "📥 Download ZIP Archive",
                zip_buffer.getvalue(),
                file_name=filename,
                mime="application/zip"
            )
    
    def run(self):
        """Run the main dashboard"""
        st.title("🎯 Software Intelligence - Intern Management Dashboard")
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Select Page:",
            ["Overview", "Intern Progress", "CSV Downloads", "Bulk Download"]
        )
        
        # Display selected page
        if page == "Overview":
            self.display_overview_metrics()
            
            # Recent activity
            st.header("📈 Recent Activity")
            all_data = self.load_all_data()
            
            if not all_data.empty:
                # Timeline chart
                timeline_data = all_data.groupby('upload_date').size().reset_index(name='products')
                fig = px.line(
                    timeline_data, 
                    x='upload_date', 
                    y='products',
                    title='Products Uploaded Over Time'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for timeline.")
        
        elif page == "Intern Progress":
            self.display_intern_progress()
        
        elif page == "CSV Downloads":
            self.display_csv_downloads()
        
        elif page == "Bulk Download":
            self.display_bulk_download()
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Software Intelligence**")
        st.sidebar.markdown("Intern Management System")
        st.sidebar.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

def main():
    """Main function"""
    dashboard = InternDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
