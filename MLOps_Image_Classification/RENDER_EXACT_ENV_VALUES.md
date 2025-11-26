# 🎯 EXACTLY What To Put in Render Environment Variables

## Answer: When Creating Web Service on Render

In the **"Environment"** section of Render dashboard, add these as **separate environment variables**:

---

## ✅ MINIMUM REQUIRED (Must Have These 5)

```
KEY: FLASK_ENV
VALUE: production

KEY: FLASK_SECRET_KEY
VALUE: <generate-a-random-string>

KEY: FLASK_DEBUG
VALUE: False

KEY: LOG_LEVEL
VALUE: INFO

KEY: RATE_LIMIT_ENABLED
VALUE: True
```

---

## 🎁 COMPLETE SET (Recommended - 27 Variables)

Add each as a separate "Add Environment Variable":

### Section 1: Flask Configuration
```
FLASK_ENV = production
FLASK_SECRET_KEY = <random-string-here>
FLASK_DEBUG = False
```

### Section 2: API Configuration
```
API_VERSION = v1
HOST = 0.0.0.0
PORT = 5000
```

### Section 3: File Handling
```
MODEL_DIR = models
UPLOAD_FOLDER = uploads
MAX_CONTENT_LENGTH = 16777216
ALLOWED_EXTENSIONS = png,jpg,jpeg
```

### Section 4: Rate Limiting
```
RATE_LIMIT_ENABLED = True
RATE_LIMIT_STORAGE_URL = memory://
RATE_LIMIT_DEFAULT = 200 per day, 50 per hour
```

### Section 5: Logging
```
LOG_LEVEL = INFO
LOG_FILE = logs/app.log
LOG_FORMAT = %(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Section 6: Training
```
DEFAULT_EPOCHS = 50
DEFAULT_BATCH_SIZE = 64
RETRAINING_EPOCHS = 20
RETRAINING_BATCH_SIZE = 64
```

### Section 7: Monitoring
```
ENABLE_METRICS = True
METRICS_PORT = 9090
```

---

## 🔐 How to Generate FLASK_SECRET_KEY

You MUST replace `<random-string-here>` with an actual random string.

### Option 1: PowerShell (Windows) - EASIEST
Open PowerShell and run:
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Example output:
```
a7f3c9e2b1d8f4g6h5j9k2l4m8n1p3q7r9s2t4u6v8w1x3y5z7a9b1c3d5
```

Use that as your FLASK_SECRET_KEY value.

### Option 2: Online Generator - FASTEST
1. Go to: https://randomkeygen.com/
2. Copy any of the generated keys (pick the longest one)
3. Use it as FLASK_SECRET_KEY

### Option 3: Python Script
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📍 Step-by-Step in Render Dashboard

### When creating Web Service:

1. **Search for GitHub repo**: MLOps_Image_Classification
2. **Configure settings** (leave defaults)
3. **Scroll down** to "Environment" section
4. **Click** "Add Environment Variable"

For each variable:
```
┌─────────────────────────────────────────┐
│ Environment Variables                    │
├─────────────────────────────────────────┤
│                                          │
│  KEY:    FLASK_ENV                      │
│  VALUE:  production                     │
│                                          │
│  [Add]  [Remove]                        │
│                                          │
└─────────────────────────────────────────┘
```

5. Click **"Add"** button
6. Repeat for each variable
7. Click **"Create Web Service"** or **"Save"**

---

## 📊 Complete Reference Table

| KEY | VALUE | Required? |
|-----|-------|-----------|
| FLASK_ENV | production | ✅ YES |
| FLASK_SECRET_KEY | random-string | ✅ YES |
| FLASK_DEBUG | False | ✅ YES |
| LOG_LEVEL | INFO | ✅ YES |
| RATE_LIMIT_ENABLED | True | ✅ YES |
| API_VERSION | v1 | ⭕ Optional |
| HOST | 0.0.0.0 | ⭕ Optional |
| PORT | 5000 | ⭕ Optional |
| MODEL_DIR | models | ⭕ Optional |
| UPLOAD_FOLDER | uploads | ⭕ Optional |
| MAX_CONTENT_LENGTH | 16777216 | ⭕ Optional |
| ALLOWED_EXTENSIONS | png,jpg,jpeg | ⭕ Optional |
| RATE_LIMIT_STORAGE_URL | memory:// | ⭕ Optional |
| RATE_LIMIT_DEFAULT | 200 per day, 50 per hour | ⭕ Optional |
| LOG_FILE | logs/app.log | ⭕ Optional |
| LOG_FORMAT | %(asctime)s - %(name)s - %(levelname)s - %(message)s | ⭕ Optional |
| DEFAULT_EPOCHS | 50 | ⭕ Optional |
| DEFAULT_BATCH_SIZE | 64 | ⭕ Optional |
| RETRAINING_EPOCHS | 20 | ⭕ Optional |
| RETRAINING_BATCH_SIZE | 64 | ⭕ Optional |
| ENABLE_METRICS | True | ⭕ Optional |
| METRICS_PORT | 9090 | ⭕ Optional |

---

## 🚨 Important Notes

1. ✅ Always use **FLASK_ENV=production** on Render
2. ✅ Always use **FLASK_DEBUG=False** on Render
3. ✅ **Generate a random FLASK_SECRET_KEY** (don't hardcode)
4. ✅ Each variable is separate (not comma-separated)
5. ✅ After adding, click **"Save"** to restart service
6. ❌ Don't use spaces around `=` in Render (KEY and VALUE are separate fields)

---

## ✅ Verify It Works

After setting environment variables, test:

```bash
curl https://your-render-url.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime_seconds": 45,
  "timestamp": "2025-11-26T12:34:56.789Z",
  "version": "v1"
}
```

---

## 🆘 Troubleshooting

### Error: "SECRET_KEY NOT SET"
→ Make sure FLASK_SECRET_KEY is added and has a value

### Error: "Port already in use"
→ Port is usually auto-configured by Render, shouldn't happen

### App won't start
→ Check Render logs (Logs tab in dashboard)
→ Make sure all required variables are set

### 500 Internal Server Error
→ Check model loads: `/api/model/info`
→ Check logs for specific error message

---

## 📚 Additional Resources

- **RENDER_ENV_QUICK_REFERENCE.md** - Quick copy-paste
- **ENVIRONMENT_VARIABLES_GUIDE.md** - Detailed explanations
- **RENDER_DEPLOYMENT_GUIDE.md** - Complete deployment steps
- **config.py** - How your app reads these variables

---

## TL;DR

Copy these 5 lines to Render environment variables:

```
FLASK_ENV=production
FLASK_SECRET_KEY=<generate-random-string-with-powershell>
FLASK_DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
```

Generate key with:
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Done! ✅

---

*Last Updated: 2025-11-26*
*Created for: MLOps Image Classification Render Deployment*
