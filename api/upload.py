"""
Vercel Serverless Function: CSV Upload API
Handles CSV file uploads and validation
"""

import json
import re
import pandas as pd
from datetime import datetime
from io import StringIO
import os
from typing import Dict, List, Optional

# Required CSV columns
REQUIRED_COLUMNS = ['name', 'price', 'category', 'store_id', 'city', 'created_at']
OPTIONAL_COLUMNS = ['quantity', 'image_url', 'nutriscore', 'nova_group', 
                    'energy_kcal', 'sugars_100g', 'salt_100g', 'saturated_fat_100g']

def validate_filename(filename: str) -> Dict[str, any]:
    """Validate CSV filename format. Accepts exact name or name ending with products_YYYY_MM_DD.csv"""
    # Must end with products_YYYY_MM_DD.csv (optional prefix like firstname_lastname_country_)
    match = re.search(r'products_(\d{4})_(\d{2})_(\d{2})\.csv$', filename, re.IGNORECASE)
    if not match:
        return {
            'valid': False,
            'error': 'Filename must end with: products_YYYY_MM_DD.csv (e.g. products_2025_01_15.csv or myname_products_2025_01_15.csv)'
        }
    year, month, day = match.group(1), match.group(2), match.group(3)
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        return {
            'valid': False,
            'error': 'Invalid date in filename'
        }
    return {'valid': True}

def validate_csv_structure(csv_content: str) -> Dict[str, any]:
    """Validate CSV structure and columns"""
    errors = []
    
    try:
        df = pd.read_csv(StringIO(csv_content))
    except Exception as e:
        return {
            'valid': False,
            'errors': [f'Invalid CSV format: {str(e)}']
        }
    
    # Check required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for empty dataframe
    if df.empty:
        errors.append("CSV file is empty")
    
    # Check for required data
    if 'name' in df.columns and df['name'].isna().all():
        errors.append("All product names are missing")
    
    if 'price' in df.columns:
        try:
            pd.to_numeric(df['price'], errors='coerce')
        except:
            errors.append("Price column contains invalid numeric values")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'row_count': len(df),
        'columns': list(df.columns)
    }

def get_upload_summary(csv_content: str) -> Dict:
    """Get summary statistics for uploaded CSV"""
    try:
        df = pd.read_csv(StringIO(csv_content))
        summary = {
            'total_products': len(df),
            'columns': list(df.columns),
            'required_columns_present': all(col in df.columns for col in REQUIRED_COLUMNS),
            'optional_columns_present': [col for col in OPTIONAL_COLUMNS if col in df.columns]
        }
        
        if 'category' in df.columns:
            summary['unique_categories'] = int(df['category'].nunique())
        
        if 'price' in df.columns:
            try:
                prices = pd.to_numeric(df['price'], errors='coerce')
                summary['avg_price'] = float(prices.mean())
                summary['min_price'] = float(prices.min())
                summary['max_price'] = float(prices.max())
            except:
                pass
        
        if 'city' in df.columns:
            summary['cities'] = df['city'].unique().tolist()
        
        return summary
    except Exception as e:
        return {'error': str(e)}

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            body_data = json.loads(body.decode('utf-8'))
            
            # Get file data
            filename = body_data.get('filename')
            csv_content = body_data.get('csv_content')
            intern_name = body_data.get('intern_name')
            
            if not filename or not csv_content or not intern_name:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'Missing required fields: filename, csv_content, intern_name'
                }).encode('utf-8'))
                return
            
            # Validate filename
            filename_validation = validate_filename(filename)
            if not filename_validation['valid']:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': filename_validation['error']
                }).encode('utf-8'))
                return
            
            # Validate CSV structure
            csv_validation = validate_csv_structure(csv_content)
            if not csv_validation['valid']:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'errors': csv_validation['errors']
                }).encode('utf-8'))
                return
            
            # Get summary
            summary = get_upload_summary(csv_content)
            
            # Save file (in production, use Vercel Blob Storage or external storage)
            # For now, return success - actual storage should be implemented
            # based on your storage solution (Vercel Blob, Supabase Storage, etc.)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': f'File {filename} validated successfully',
                'summary': summary,
                'validation': csv_validation
            }).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8'))
    
    def do_GET(self):
        self.send_response(405)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Method not allowed'}).encode('utf-8'))
