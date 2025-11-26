# 🔐 Environment Variables Configuration Guide

This guide explains what environment variables to set when deploying to **Render**, **Docker**, or **production**.

---

## Overview

Environment variables are configuration settings that change per environment:
- **Local Development** (your computer)
- **Docker/Staging** (testing)
- **Production/Render** (live deployment)

They are **NOT** hardcoded in your code, making your app **secure** and **flexible**.

---

## Quick Copy-Paste for Render

When creating a Web Service on Render, go to **Environment** and add these variables:

```
FLASK_ENV=production
FLASK_SECRET_KEY=CHANGE_THIS_TO_A_RANDOM_STRING
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

## Detailed Variable Breakdown

### 🔧 Flask Configuration (Required)

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `FLASK_ENV` | `production` | Environment type | `production` (for live) |
| `FLASK_SECRET_KEY` | **Random string** | Secret key for sessions | See below ⬇️ |
| `FLASK_DEBUG` | `False` | Debug mode (NEVER True in production) | `False` |

**How to generate FLASK_SECRET_KEY:**

Option 1 - PowerShell:
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Option 2 - Online: https://randomkeygen.com/

Option 3 - Python:
```python
import secrets
secrets.token_hex(32)
```

**✅ Example:**
```
FLASK_SECRET_KEY=a7f3c9e2b1d8f4g6h5j9k2l4m8n1p3q7
```

---

### 🌐 API Configuration

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `API_VERSION` | `v1` | API version | `v1` |
| `HOST` | `0.0.0.0` | Listen on all interfaces | `0.0.0.0` |
| `PORT` | `5000` | Port number | `5000` |

**Note:** On Render, PORT is automatically set. You can leave it as `5000`.

---

### 📁 File & Model Configuration

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `MODEL_DIR` | `models` | Where models are stored | `models` |
| `UPLOAD_FOLDER` | `uploads` | Where uploaded files go | `uploads` |
| `MAX_CONTENT_LENGTH` | `16777216` | Max file size (16MB in bytes) | `16777216` |
| `ALLOWED_EXTENSIONS` | `png,jpg,jpeg` | Allowed image formats | `png,jpg,jpeg` |

**Size Reference:**
- 1 MB = 1,048,576 bytes
- 16 MB = 16,777,216 bytes
- 50 MB = 52,428,800 bytes

---

### ⚡ Rate Limiting

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `RATE_LIMIT_ENABLED` | `True` | Enable rate limiting | `True` |
| `RATE_LIMIT_STORAGE_URL` | `memory://` | Where to store limits | `memory://` |
| `RATE_LIMIT_DEFAULT` | `200 per day, 50 per hour` | Global rate limit | `200 per day, 50 per hour` |

**What this means:**
- Each IP can make max 200 requests per day
- Max 50 requests per hour
- Individual endpoints have stricter limits (30/min for predictions)

---

### 📊 Logging Configuration

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `LOG_LEVEL` | `INFO` | Logging verbosity | `INFO`, `DEBUG`, `WARNING`, `ERROR` |
| `LOG_FILE` | `logs/app.log` | Where logs are saved | `logs/app.log` |
| `LOG_FORMAT` | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` | Log message format | See below |

**Log Level Options:**
- `DEBUG` - Most verbose (local development only)
- `INFO` - Standard (recommended for production)
- `WARNING` - Only warnings/errors
- `ERROR` - Only errors

---

### 🧠 Model Training Configuration

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `DEFAULT_EPOCHS` | `50` | Training epochs | `50` |
| `DEFAULT_BATCH_SIZE` | `64` | Training batch size | `64` |
| `RETRAINING_EPOCHS` | `20` | Retraining epochs | `20` |
| `RETRAINING_BATCH_SIZE` | `64` | Retraining batch size | `64` |

**Tuning Tips:**
- Fewer epochs for quick testing
- Larger batch size = faster but less accurate
- Smaller batch size = slower but more accurate

---

### 📈 Monitoring Configuration

| Variable | Value | Description | Example |
|----------|-------|-------------|---------|
| `ENABLE_METRICS` | `True` | Enable metrics collection | `True` |
| `METRICS_PORT` | `9090` | Prometheus metrics port | `9090` |

---

## 📍 How to Set Variables in Render

### Step-by-Step:

1. **Go to Render Dashboard**
2. **Select Your Web Service**
3. **Scroll to "Environment" section**
4. **Click "Add Environment Variable"**

   For each variable:
   ```
   KEY: FLASK_ENV
   VALUE: production
   ```
   Then click "Add"

5. **Repeat for all variables above**

6. **Click "Save"** → Service restarts automatically

### Alternative: Use Environment File

1. **Click "Add Secret File"**
2. **Filename**: `.env`
3. **Content**: (paste all variables)
4. **Click "Save"**

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use `FLASK_ENV=production` on Render
- ✅ Use `FLASK_DEBUG=False` always
- ✅ Generate a random `FLASK_SECRET_KEY`
- ✅ Keep `RATE_LIMIT_ENABLED=True`
- ✅ Use `LOG_LEVEL=INFO` (not DEBUG)
- ✅ Never commit `.env` to GitHub

### ❌ DON'T:
- ❌ Hardcode secrets in code
- ❌ Use `FLASK_DEBUG=True` in production
- ❌ Use simple secrets like "password123"
- ❌ Commit `.env` file to Git
- ❌ Reuse the same secret across environments
- ❌ Share your SECRET_KEY

---

## 📝 Local Development Setup

Create a `.env` file in your project root (same folder as `app.py`):

```bash
# Copy the example
cp .env.example .env

# Edit .env with your values (different from production)
# For local: FLASK_ENV=development, FLASK_DEBUG=True
```

Your `.env` file (LOCAL ONLY - NEVER commit):
```dotenv
FLASK_ENV=development
FLASK_SECRET_KEY=dev-key-not-secure-change-me
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

Your `.env.example` (COMMIT to GitHub):
```dotenv
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key-change-this-in-production
FLASK_DEBUG=False
LOG_LEVEL=INFO
```

**Add to `.gitignore`:**
```
.env
.env.local
.env.*.local
```

---

## 🚀 Environment-Specific Configurations

### Local Development
```
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
RATE_LIMIT_ENABLED=False
MODEL_DIR=models
```

### Docker/Staging
```
FLASK_ENV=staging
FLASK_DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
MODEL_DIR=/app/models
```

### Production/Render
```
FLASK_ENV=production
FLASK_DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
MODEL_DIR=models
```

---

## ✅ Verification Checklist

After setting environment variables on Render:

- [ ] Check logs: `tail -f logs/app.log`
- [ ] Test health endpoint: `curl https://your-app.onrender.com/api/health`
- [ ] Verify no errors in Render dashboard logs
- [ ] Confirm rate limiting is working
- [ ] Test predictions work
- [ ] Check model loads correctly

---

## 🐛 Common Issues & Fixes

### Issue: "SECRET KEY NOT SET"
**Cause**: `FLASK_SECRET_KEY` is missing or empty
**Fix**: Generate new key and add to Render environment

### Issue: "Rate Limit Error"
**Cause**: Too many requests too quickly
**Fix**: Adjust `RATE_LIMIT_DEFAULT` or wait before retrying

### Issue: "File Too Large"
**Cause**: Upload exceeds `MAX_CONTENT_LENGTH`
**Fix**: Increase value (in bytes):
- 16 MB = 16777216
- 50 MB = 52428800
- 100 MB = 104857600

### Issue: "Model Not Loading"
**Cause**: `MODEL_DIR` path is wrong
**Fix**: Make sure `MODEL_DIR=models` matches your repo structure

### Issue: "Permission Denied on Logs"
**Cause**: `LOG_FILE` path doesn't exist
**Fix**: Make sure `logs/` directory exists or use relative path

---

## 📚 How Code Reads These Variables

Your `config.py` automatically reads all environment variables:

```python
# From config.py
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(32).hex())
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

Then `app.py` uses them:

```python
# From app.py
app.config.from_object(config_obj)
app.run(
    host=app.config['HOST'],
    port=app.config['PORT'],
    debug=app.config['DEBUG']
)
```

---

## 🔗 Render Environment Variables Docs

Full documentation: https://render.com/docs/environment-variables

---

## Summary Table

**For Render, use these minimum required variables:**

| Variable | Value |
|----------|-------|
| FLASK_ENV | production |
| FLASK_SECRET_KEY | *(generate random string)* |
| FLASK_DEBUG | False |
| LOG_LEVEL | INFO |
| RATE_LIMIT_ENABLED | True |

**Optional but recommended:**

| Variable | Value |
|----------|-------|
| API_VERSION | v1 |
| DEFAULT_EPOCHS | 50 |
| RETRAINING_EPOCHS | 20 |

---

## ✨ Pro Tips

1. **Generate Unique Secret Key for Each Environment**
   ```bash
   # Different key for dev, staging, production
   ```

2. **Use Different Log Levels**
   - Local: `DEBUG`
   - Staging: `INFO`
   - Production: `WARNING`

3. **Monitor Your Logs**
   ```bash
   # Render dashboard → Logs tab
   # Check for errors and warnings
   ```

4. **Test After Changing Variables**
   ```bash
   curl https://your-app.onrender.com/api/health
   ```

5. **Keep `.env.example` Updated**
   - Helps team members set up quickly
   - Don't commit actual `.env`

---

*Last Updated: 2025-11-26*
*For Questions: Check Render docs or review config.py*
