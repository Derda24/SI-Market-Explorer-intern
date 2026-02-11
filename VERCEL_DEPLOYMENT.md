# 🚀 Vercel Deployment Guide

This guide will help you deploy the Market Explorer CSV sharing platform on Vercel.

## 📋 Prerequisites

- Vercel account (free tier available)
- GitHub account (for connecting repository)
- Python 3.9+ knowledge

## 🎯 Quick Deployment

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Import Project on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Configure Build Settings**
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: (leave empty or use `npm run build` if you add one)
   - Output Directory: `public`

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at `your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Production Deploy**
   ```bash
   vercel --prod
   ```

## 📁 Project Structure for Vercel

```
SI-Market-Explorer-Intern/
├── api/                    # Serverless functions
│   ├── upload.py          # CSV upload handler
│   ├── files.py           # File management handler
│   └── index.py           # Main router
├── public/                # Static files
│   └── index.html         # Frontend application
├── vercel.json            # Vercel configuration
├── requirements-vercel.txt # Python dependencies
└── package.json           # (Optional) for build scripts
```

## ⚙️ Configuration

### vercel.json

The `vercel.json` file configures:
- Python serverless functions for `/api/*` routes
- Static file serving for frontend
- CORS headers for API endpoints

### Environment Variables (Optional)

You can add environment variables in Vercel dashboard:
- `STORAGE_TYPE`: `vercel-blob` or `external` (for file storage)
- `BLOB_READ_WRITE_TOKEN`: If using Vercel Blob Storage

## 🔧 File Storage Options

Vercel serverless functions have a read-only filesystem. For file storage, choose one:

### Option 1: Vercel Blob Storage (Recommended)

1. **Enable Vercel Blob**
   - Go to your project settings
   - Enable "Blob Storage"
   - Get your read/write token

2. **Update API Code**
   ```python
   from vercel_blob import put
   
   # In upload.py handler
   blob = await put(filename, csv_content)
   ```

### Option 2: External Storage (Supabase Storage, AWS S3, etc.)

Update `api/upload.py` to save files to your external storage:

```python
# Example with Supabase Storage
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase.storage.from_('csv-files').upload(
    f'{intern_name}/{filename}',
    csv_content.encode()
)
```

### Option 3: Database Storage

Store CSV content in a database (PostgreSQL, MongoDB, etc.):

```python
# Store CSV content as text/blob in database
# Retrieve when needed for downloads
```

## 📝 API Endpoints

### POST `/api/upload`
Upload a CSV file.

**Request Body:**
```json
{
  "filename": "products_2025_01_15.csv",
  "csv_content": "name,price,category...",
  "intern_name": "marta_kovacevic_france"
}
```

**Response:**
```json
{
  "success": true,
  "message": "File validated successfully",
  "summary": {
    "total_products": 150,
    "columns": ["name", "price", ...]
  }
}
```

### GET `/api/files?action=list`
List all uploaded files.

**Response:**
```json
{
  "interns": [
    {
      "name": "marta_kovacevic_france",
      "files": [...],
      "file_count": 2
    }
  ],
  "total_files": 5
}
```

### GET `/api/files?action=download&path=...`
Download a specific file.

## 🎨 Customization

### Update Frontend

Edit `public/index.html` to customize:
- Colors and styling
- Layout and components
- Additional features

### Update API

Edit files in `api/` directory:
- `upload.py`: Upload validation and processing
- `files.py`: File listing and download logic

## 🔒 Security Considerations

### Add Authentication (Recommended)

1. **Vercel Authentication**
   - Use Vercel's built-in authentication
   - Or integrate Auth0, Clerk, etc.

2. **API Key Protection**
   - Add API key validation in handlers
   - Use Vercel environment variables

### Rate Limiting

Vercel has built-in rate limiting, but you can add custom limits:

```python
# In api/upload.py
# Add rate limiting logic
```

## 🐛 Troubleshooting

### Function Timeout

Vercel free tier: 10s timeout
- Upgrade to Pro for longer timeouts
- Optimize file processing
- Use background jobs for large files

### File Size Limits

- Vercel: 4.5MB request body limit
- For larger files, use chunked uploads or direct storage uploads

### CORS Issues

CORS is configured in `vercel.json` and handlers. If issues persist:
- Check `Access-Control-Allow-Origin` headers
- Verify request methods are allowed

### Python Dependencies

If packages aren't installing:
- Check `requirements-vercel.txt`
- Ensure packages are compatible with Python 3.9
- Some packages may not work in serverless environment

## 📊 Monitoring

### Vercel Dashboard

- View function logs
- Monitor performance
- Check error rates
- View analytics

### Logs

```bash
vercel logs
```

## 🚀 Production Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] File storage solution implemented
- [ ] Frontend tested
- [ ] API endpoints tested
- [ ] CORS configured correctly
- [ ] Error handling implemented
- [ ] Monitoring set up
- [ ] Custom domain configured (optional)

## 🔄 Updates

To update your deployment:

```bash
git add .
git commit -m "Update features"
git push origin main
```

Vercel will automatically redeploy on push to main branch.

## 📞 Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Discord**: Community support
- **GitHub Issues**: Report bugs in repository

## 🎉 Success!

Once deployed, share your Vercel URL with interns:
```
https://your-project.vercel.app
```

Interns can now:
- Upload CSV files directly via web interface
- View their upload history
- Admins can monitor all activity

---

**Happy Deploying! 🚀**
