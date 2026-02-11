"""
Vercel Serverless Function: File Management API
Handles file listing, downloading, and admin operations
"""

import json
import os
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

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
                # List all intern directories and files
                # In production, this would query your storage solution
                interns_dir = os.path.join(os.getcwd(), 'interns')
                
                if not os.path.exists(interns_dir):
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'interns': [],
                        'total_files': 0,
                        'total_products': 0
                    }).encode('utf-8'))
                    return
                
                # Scan directories
                interns = []
                total_files = 0
                total_products = 0
                
                for intern_dir in os.listdir(interns_dir):
                    intern_path = os.path.join(interns_dir, intern_dir)
                    if os.path.isdir(intern_path):
                        files = []
                        for file in os.listdir(intern_path):
                            if file.startswith('products_') and file.endswith('.csv'):
                                file_path = os.path.join(intern_path, file)
                                files.append({
                                    'filename': file,
                                    'date': file.replace('products_', '').replace('.csv', ''),
                                    'path': file_path
                                })
                                total_files += 1
                        
                        interns.append({
                            'name': intern_dir,
                            'files': files,
                            'file_count': len(files)
                        })
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'interns': interns,
                    'total_files': total_files,
                    'total_products': total_products
                }).encode('utf-8'))
            
            elif action == 'download':
                # Download specific file
                file_path = query_params.get('path', [None])[0]
                if not file_path:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing file path'}).encode('utf-8'))
                    return
                
                # In production, read from storage
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/csv')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
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
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
