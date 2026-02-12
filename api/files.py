"""
Vercel Serverless Function: File Management API
Handles file listing, downloading, and admin operations
"""

import json
import os
from urllib.parse import urlparse, parse_qs, quote
from http.server import BaseHTTPRequestHandler

# Use vercel_blob package for Blob Storage operations
try:
    import vercel_blob
    VERCEL_BLOB_AVAILABLE = True
except ImportError:
    VERCEL_BLOB_AVAILABLE = False
    import urllib.request
    import urllib.error

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
                    blob_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
                    if not blob_token:
                        raise Exception("BLOB_READ_WRITE_TOKEN not found")
                    
                    # Use vercel_blob package if available, otherwise fallback to REST API
                    if VERCEL_BLOB_AVAILABLE:
                        # Use the vercel_blob package
                        print("Using vercel_blob package for listing")
                        result = vercel_blob.list({'prefix': 'interns/'})
                        print(f"Full list result: {json.dumps(result, indent=2, default=str)}")
                        all_blobs = result.get('blobs', [])
                        print(f"Blob Storage list response (via package): {len(all_blobs)} blobs found")
                        if len(all_blobs) > 0:
                            print(f"First blob sample: {json.dumps(all_blobs[0], indent=2, default=str)}")
                    else:
                        print("vercel_blob package NOT available, using REST API fallback")
                        # Fallback: Try REST API with GET first
                        try:
                            list_url = 'https://blob.vercel-storage.com/list?prefix=interns/'
                            headers = {'Authorization': f'Bearer {blob_token}'}
                            req = urllib.request.Request(list_url, headers=headers)
                            with urllib.request.urlopen(req) as response:
                                response_text = response.read().decode('utf-8')
                                result = json.loads(response_text)
                                print(f"Blob Storage list response (REST GET): {json.dumps(result, indent=2)}")
                                all_blobs = result.get('blobs', result.get('files', []))
                        except urllib.error.HTTPError as e:
                            # If GET fails with 404, try POST
                            if e.code == 404:
                                list_url = 'https://blob.vercel-storage.com/list'
                                headers = {
                                    'Authorization': f'Bearer {blob_token}',
                                    'Content-Type': 'application/json'
                                }
                                data = json.dumps({'prefix': 'interns/'}).encode('utf-8')
                                req = urllib.request.Request(list_url, data=data, headers=headers, method='POST')
                                with urllib.request.urlopen(req) as response:
                                    response_text = response.read().decode('utf-8')
                                    result = json.loads(response_text)
                                    print(f"Blob Storage list response (REST POST): {json.dumps(result, indent=2)}")
                                    all_blobs = result.get('blobs', result.get('files', []))
                            else:
                                raise
                    
                    # Debug: log total blobs found
                    print(f"Total blobs retrieved: {len(all_blobs)}")
                    
                    # Organize blobs by intern name
                    interns_dict = {}
                    total_files = 0
                    
                    for idx, blob in enumerate(all_blobs):
                        if idx < 3:  # Log first 3 blobs for debugging
                            print(f"Processing blob {idx}: {json.dumps(blob, indent=2, default=str)}")
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
                    
                    # Debug: log final result
                    print(f"Final result: {len(interns)} interns, {total_files} total files")
                    if len(interns) > 0:
                        print(f"Interns: {[i['name'] for i in interns]}")
                    
                    # Include debug info in response (remove in production)
                    debug_info = {
                        'blobs_found': len(all_blobs),
                        'using_package': VERCEL_BLOB_AVAILABLE,
                        'sample_blobs': all_blobs[:3] if len(all_blobs) > 0 else []
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'interns': interns,
                        'total_files': total_files,
                        'total_products': 0,
                        'debug': debug_info
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
                    blob_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
                    if not blob_token:
                        raise Exception("BLOB_READ_WRITE_TOKEN not found")
                    
                    filename = os.path.basename(file_path)
                    
                    # Use vercel_blob package if available
                    if VERCEL_BLOB_AVAILABLE:
                        blob_info = vercel_blob.head(file_path)
                        download_url = blob_info.get('downloadUrl') or blob_info.get('url')
                        if download_url:
                            import urllib.request
                            with urllib.request.urlopen(download_url) as download_response:
                                content = download_response.read().decode('utf-8')
                    else:
                        # Fallback: Use REST API
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
