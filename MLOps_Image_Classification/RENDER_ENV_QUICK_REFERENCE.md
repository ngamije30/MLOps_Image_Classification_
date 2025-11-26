# 🎯 Quick Render Environment Variables Reference

## Copy-Paste for Render Dashboard

When setting up a Web Service on Render, add these environment variables in the **Environment** section.

### Minimum Required (ESSENTIAL)

```
FLASK_ENV=production
FLASK_SECRET_KEY=<GENERATE-A-RANDOM-STRING>
FLASK_DEBUG=False
LOG_LEVEL=INFO
```

### Complete Set (RECOMMENDED)

Add each as a separate environment variable:

```
FLASK_ENV=production
FLASK_SECRET_KEY=generate-random-string-here
FLASK_DEBUG=False
API_VERSION=v1
HOST=0.0.0.0
PORT=5000
MODEL_DIR=models
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg
RATE_LIMIT_ENABLED=True
RATE_LIMIT_STORAGE_URL=memory://
RATE_LIMIT_DEFAULT=200 per day, 50 per hour
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
DEFAULT_EPOCHS=50
DEFAULT_BATCH_SIZE=64
RETRAINING_EPOCHS=20
RETRAINING_BATCH_SIZE=64
ENABLE_METRICS=True
METRICS_PORT=9090
```

---

## 🔐 How to Generate FLASK_SECRET_KEY

### Option 1: PowerShell (Windows)
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### Option 2: Online Generator
Visit: https://randomkeygen.com/

Copy any of the generated keys (pick the longest one - at least 32 characters)

### Option 3: Python
```python
import secrets
print(secrets.token_hex(32))
```

### Example Generated Key
```
a7f3c9e2b1d8f4a6h5j9k2l4m8n1p3q7r9s2t4u6v8w1x3y5z7a9b1c3d5e7f9
```

---

## 📍 Step-by-Step in Render Dashboard

1. **Go to https://render.com/dashboard**
2. **Click on your Web Service** (ml-image-classifier)
3. **Scroll to "Environment" section**
4. **Click "Add Environment Variable"**
5. For each variable:
   - **KEY**: `FLASK_ENV`
   - **VALUE**: `production`
   - Click **"Add"**
6. **Repeat for all variables above**
7. **Click "Save"** → Service restarts automatically

---

## ✅ After Adding Variables

Test your deployment:

```bash
# Health check
curl https://ml-image-classifier-xxxx.onrender.com/api/health

# Expected response:
# {"status": "healthy", "model_loaded": true, ...}
```

---

## 🚨 Important Notes

- ⚠️ **Always** use `FLASK_ENV=production`
- ⚠️ **Never** use `FLASK_DEBUG=True` in production
- ⚠️ **Generate** a unique `FLASK_SECRET_KEY` (not default)
- ⚠️ **Never** hardcode secrets in your code
- ⚠️ **Don't** commit `.env` file to GitHub

---

## 📊 Variable Quick Reference

| Variable | Purpose | Value |
|----------|---------|-------|
| FLASK_ENV | Environment type | `production` |
| FLASK_SECRET_KEY | Session encryption | *random string* |
| FLASK_DEBUG | Debug mode | `False` |
| LOG_LEVEL | Log verbosity | `INFO` |
| RATE_LIMIT_ENABLED | Rate limiting | `True` |
| MAX_CONTENT_LENGTH | Max file size | `16777216` (16MB) |

---

For detailed explanations, see: **ENVIRONMENT_VARIABLES_GUIDE.md**
