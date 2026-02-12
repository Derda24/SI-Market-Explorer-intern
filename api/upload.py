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

import urllib.request

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

def _validate_csv_df(df: pd.DataFrame) -> Dict[str, any]:
    """Validate CSV structure from an already-parsed DataFrame."""
    errors = []
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    if df.empty:
        errors.append("CSV file is empty")
    if 'name' in df.columns and df['name'].isna().all():
        errors.append("All product names are missing")
    if 'price' in df.columns:
        try:
            pd.to_numeric(df['price'], errors='coerce')
        except Exception:
            errors.append("Price column contains invalid numeric values")
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'row_count': int(len(df)),
        'columns': [str(col) for col in df.columns]
    }


def _summary_from_df(df: pd.DataFrame) -> Dict:
    """Build upload summary from an already-parsed DataFrame."""
    summary = {
        'total_products': int(len(df)),
        'columns': [str(col) for col in df.columns],
        'required_columns_present': bool(all(col in df.columns for col in REQUIRED_COLUMNS)),
        'optional_columns_present': [str(col) for col in OPTIONAL_COLUMNS if col in df.columns]
    }
    if 'category' in df.columns:
        summary['unique_categories'] = int(df['category'].nunique())
    if 'price' in df.columns:
        try:
            prices = pd.to_numeric(df['price'], errors='coerce')
            mean_val = prices.mean()
            min_val = prices.min()
            max_val = prices.max()
            # Handle NaN values
            if pd.notna(mean_val):
                summary['avg_price'] = float(mean_val)
            if pd.notna(min_val):
                summary['min_price'] = float(min_val)
            if pd.notna(max_val):
                summary['max_price'] = float(max_val)
        except Exception:
            pass
    if 'city' in df.columns:
        # Convert numpy array to list and ensure all values are strings
        cities = df['city'].unique().tolist()
        summary['cities'] = [str(c) for c in cities if pd.notna(c)]
    return summary

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
            # Read request body with error handling
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'error': 'Request body is empty'
                    }).encode('utf-8'))
                    return
                body = self.rfile.read(content_length)
                body_data = json.loads(body.decode('utf-8'))
            except (ValueError, json.JSONDecodeError) as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': f'Invalid request format: {str(e)}'
                }).encode('utf-8'))
                return
            
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
            
            # Parse CSV once (saves memory and time for large files)
            try:
                df = pd.read_csv(StringIO(csv_content))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'errors': [f'Invalid CSV format: {str(e)}']
                }).encode('utf-8'))
                return

            # Validate CSV structure (reuses same DataFrame)
            csv_validation = _validate_csv_df(df)
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

            # Get summary from same DataFrame (no second parse)
            summary = _summary_from_df(df)
            
            # Save file to Vercel Blob Storage
            blob_url = None
            save_error_message = None
            try:
                # Extract date from filename to ensure consistent naming
                match = re.search(r'products_(\d{4})_(\d{2})_(\d{2})\.csv$', filename, re.IGNORECASE)
                if match:
                    # Use the standard format: products_YYYY_MM_DD.csv
                    standard_filename = f"products_{match.group(1)}_{match.group(2)}_{match.group(3)}.csv"
                else:
                    # Fallback to original filename if pattern doesn't match
                    standard_filename = filename
                
                # Blob path: interns/{intern_name}/products_YYYY_MM_DD.csv
                blob_path = f"interns/{intern_name}/{standard_filename}"
                
                print(f"Attempting to save file to Blob Storage: {blob_path}")
                
                blob_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
                if not blob_token:
                    raise Exception("BLOB_READ_WRITE_TOKEN environment variable not set. Make sure Vercel Blob is enabled in your project.")
                
                print(f"BLOB_READ_WRITE_TOKEN found: {blob_token[:20] if blob_token else 'None'}...")
                
                # Try using vercel_blob package first (more reliable)
                try:
                    import vercel_blob
                    print("Using vercel_blob package for upload")
                    result = vercel_blob.put(blob_path, csv_content.encode('utf-8'), {
                        'contentType': 'text/csv',
                        'addRandomSuffix': False
                    })
                    print(f"vercel_blob.put result: {json.dumps(result, indent=2, default=str)}")
                    blob_url = result.get('url')
                    if blob_url:
                        print(f"Successfully saved to Blob Storage via package: {blob_path} -> {blob_url}")
                except ImportError:
                    print("vercel_blob package not available, using REST API")
                    # Fallback to REST API with PUT method
                    upload_url = 'https://blob.vercel-storage.com/put'
                    headers = {
                        'Authorization': f'Bearer {blob_token}',
                        'Content-Type': 'application/json'
                    }
                    upload_data = {
                        'pathname': blob_path,
                        'content': csv_content,
                        'contentType': 'text/csv',
                        'addRandomSuffix': False
                    }
                    print(f"Upload data size: {len(csv_content)} bytes")
                    print(f"Upload URL: {upload_url}")
                    print(f"Upload pathname: {blob_path}")
                    
                    data = json.dumps(upload_data).encode('utf-8')
                    
                    print("Making PUT request to Blob Storage API...")
                    req = urllib.request.Request(upload_url, data=data, headers=headers, method='PUT')
                    with urllib.request.urlopen(req) as response:
                        result = json.loads(response.read().decode('utf-8'))
                        print(f"Blob Storage upload response: {json.dumps(result, indent=2)}")
                        blob_url = result.get('url')
                        if not blob_url:
                            raise Exception(f"Upload failed: {result}")
                        print(f"Successfully saved to Blob Storage via REST API: {blob_path} -> {blob_url}")
                
            except Exception as save_error:
                # Log error but continue - file is validated
                import traceback
                save_error_message = str(save_error)
                print(f"ERROR: Failed to save file to Blob Storage: {save_error_message}")
                print(f"Traceback: {traceback.format_exc()}")
                # Continue anyway - validation passed
            
            # Prepare response data
            response_data = {
                'success': True,
                'message': f'File {filename} validated successfully',
                'summary': summary,
                'validation': csv_validation
            }
            
            # Include blob storage status in response for debugging
            if save_error_message:
                response_data['blob_storage_error'] = save_error_message
                response_data['blob_storage_warning'] = 'File validated but not saved to Blob Storage'
            elif blob_url:
                response_data['blob_storage_success'] = True
                response_data['blob_url'] = blob_url
            
            # Ensure all values are JSON-serializable
            try:
                response_json = json.dumps(response_data, default=str)
            except (TypeError, ValueError) as json_error:
                # If JSON serialization fails, return a simpler response
                response_data = {
                    'success': True,
                    'message': f'File {filename} validated successfully',
                    'row_count': csv_validation.get('row_count', 0),
                    'columns': csv_validation.get('columns', [])
                }
                response_json = json.dumps(response_data, default=str)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))
            
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
