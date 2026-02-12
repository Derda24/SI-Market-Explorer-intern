"""
Vercel Serverless Function: File Management API
Handles file listing, downloading, and admin operations
"""

import json
import os
from urllib.parse import urlparse, parse_qs, quote
from http.server import BaseHTTPRequestHandler
import urllib.request

class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler for file operations"""
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            action = query_params.get('action', ['list'])[0]
            
            if action == 'list':
                # List all files from Vercel Blob Storage
                try:
                    # Use REST API directly (more reliable)
                    blob_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
                    if not blob_token:
                        raise Exception("BLOB_READ_WRITE_TOKEN not found")
                    
                    list_url = 'https://blob.vercel-storage.com/list?prefix=interns/'
                    headers = {'Authorization': f'Bearer {blob_token}'}
                    req = urllib.request.Request(list_url, headers=headers)
                    with urllib.request.urlopen(req) as response:
                        response_text = response.read().decode('utf-8')
                        result = json.loads(response_text)
                        
                        # Debug: log the response structure
                        print(f"Blob Storage list response: {json.dumps(result, indent=2)}")
                        
                        # Handle different possible response formats
                        all_blobs = []
                        if isinstance(result, dict):
                            all_blobs = result.get('blobs', result.get('files', []))
                        elif isinstance(result, list):
                            all_blobs = result
                    
                    # Organize blobs by intern name
                    interns_dict = {}
                    total_files = 0
                    
                    for blob in all_blobs:
                        # Try different possible field names for pathname
                        pathname = blob.get('pathname') or blob.get('path') or blob.get('key') or ''
                        
                        # Debug: log blob structure
                        if not pathname:
                            print(f"Blob missing pathname: {json.dumps(blob)}")
                        
                        # Path format: interns/{intern_name}/products_YYYY_MM_DD.csv
                        if pathname and pathname.startswith('interns/') and pathname.endswith('.csv'):
                            parts = pathname.split('/')
                            if len(parts) >= 3:
                                intern_name = parts[1]
                                filename = parts[2]
                                
                                if filename.startswith('products_') and filename.endswith('.csv'):
                                    if intern_name not in interns_dict:
                                        interns_dict[intern_name] = []
                                    
                                    interns_dict[intern_name].append({
                                        'filename': filename,
                                        'date': filename.replace('products_', '').replace('.csv', ''),
                                        'path': pathname,
                                        'url': blob.get('url') or blob.get('downloadUrl'),
                                        'downloadUrl': blob.get('downloadUrl') or blob.get('url')
                                    })
                                    total_files += 1
                    
                    # Convert to list format
                    interns = []
                    for intern_name, files in interns_dict.items():
                        interns.append({
                            'name': intern_name,
                            'files': files,
                            'file_count': len(files)
                        })
                    
                    # Sort interns by name
                    interns.sort(key=lambda x: x['name'])
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'interns': interns,
                        'total_files': total_files,
                        'total_products': 0
                    }).encode('utf-8'))
                    
                except Exception as e:
                    # Log detailed error for debugging
                    import traceback
                    error_details = {
                        'error': str(e),
                        'traceback': traceback.format_exc()
                    }
                    print(f"Error listing blobs: {json.dumps(error_details)}")
                    
                    # Return 200 with error info so frontend can display it
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'interns': [],
                        'total_files': 0,
                        'total_products': 0,
                        'error': str(e),
                        'debug': 'Check Vercel function logs for details'
                    }).encode('utf-8'))
            
            elif action == 'download':
                # Download specific file from Vercel Blob Storage
                file_path = query_params.get('path', [None])[0]
                if not file_path:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing file path'}).encode('utf-8'))
                    return
                
                try:
                    # Use REST API directly
                    blob_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
                    if not blob_token:
                        raise Exception("BLOB_READ_WRITE_TOKEN not found")
                    
                    filename = os.path.basename(file_path)
                    
                    # Get blob info
                    head_url = f'https://blob.vercel-storage.com/head?pathname={quote(file_path)}'
                    headers = {'Authorization': f'Bearer {blob_token}'}
                    req = urllib.request.Request(head_url, headers=headers)
                    with urllib.request.urlopen(req) as response:
                        blob_info = json.loads(response.read().decode('utf-8'))
                        download_url = blob_info.get('downloadUrl') or blob_info.get('url')
                        if download_url:
                            with urllib.request.urlopen(download_url) as download_response:
                                content = download_response.read().decode('utf-8')
                    
                    if content:
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/csv')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                        self.end_headers()
                        self.wfile.write(content.encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': 'File not found'}).encode('utf-8'))
                        
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': f'Download failed: {str(e)}'}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
