# ✅ ANSWER: What Environment Variables to Put in Render

## Your Question:
> "What do I put in environment variables when creating web service?"

---

## ✅ Direct Answer

When you click **"Create Web Service"** on Render and see the **Environment** section, add these:

### MINIMUM (5 Required)

```
FLASK_ENV = production
FLASK_SECRET_KEY = <random-string-you-generate>
FLASK_DEBUG = False
LOG_LEVEL = INFO
RATE_LIMIT_ENABLED = True
```

### OPTIONAL (Add these too if you want)

```
API_VERSION = v1
HOST = 0.0.0.0
PORT = 5000
MODEL_DIR = models
UPLOAD_FOLDER = uploads
MAX_CONTENT_LENGTH = 16777216
ALLOWED_EXTENSIONS = png,jpg,jpeg
RATE_LIMIT_STORAGE_URL = memory://
RATE_LIMIT_DEFAULT = 200 per day, 50 per hour
LOG_FILE = logs/app.log
LOG_FORMAT = %(asctime)s - %(name)s - %(levelname)s - %(message)s
DEFAULT_EPOCHS = 50
DEFAULT_BATCH_SIZE = 64
RETRAINING_EPOCHS = 20
RETRAINING_BATCH_SIZE = 64
ENABLE_METRICS = True
METRICS_PORT = 9090
```

---

## 🔑 How to Generate FLASK_SECRET_KEY

### Method 1: PowerShell (Windows) - RECOMMENDED
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Copy the output (something like: `a7f3c9e2b1d8f4g6h5j9k2l4m8n1p3q7`)

### Method 2: Online
Go to: https://randomkeygen.com/
Copy any long key (32+ characters)

### Method 3: Python
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📍 Where Exactly in Render Dashboard

1. **Go to**: https://render.com/dashboard
2. **Click**: Your Web Service (ml-image-classifier)
3. **Look for**: "Environment" section (scroll down)
4. **Click**: "Add Environment Variable"
5. **Enter**:
   - KEY: `FLASK_ENV`
   - VALUE: `production`
6. **Click**: "Add"
7. **Repeat** for each variable
8. **Click**: "Save"

---

## 📋 The 5 You Must Have

| Key | Value | Why |
|-----|-------|-----|
| FLASK_ENV | production | Tells Flask to run in production mode |
| FLASK_SECRET_KEY | random-string | Encrypts sensitive data (SESSION, CSRF tokens) |
| FLASK_DEBUG | False | Disables debug mode (security) |
| LOG_LEVEL | INFO | Sets logging level (INFO is good for production) |
| RATE_LIMIT_ENABLED | True | Protects from being spammed with requests |

---

## ⚠️ Critical Security Notes

- ✅ FLASK_SECRET_KEY must be RANDOM (not hardcoded)
- ✅ FLASK_DEBUG must ALWAYS be False in production
- ✅ FLASK_ENV must be "production" (not "development")
- ❌ Never commit `.env` file to GitHub
- ❌ Never share your FLASK_SECRET_KEY
- ❌ Generate a NEW key for each environment

---

## ✅ How to Verify It Works

After adding environment variables:

1. **Click "Save"** → Service will restart
2. **Wait for "Live" status**
3. **Test this endpoint**:
   ```bash
   curl https://ml-image-classifier-xxxx.onrender.com/api/health
   ```

4. **Should return** (if working):
   ```json
   {
     "status": "healthy",
     "model_loaded": true,
     "uptime_seconds": 120
   }
   ```

---

## 🎯 Quick Checklist

- [ ] Generate FLASK_SECRET_KEY with PowerShell command
- [ ] Go to Render Dashboard
- [ ] Open your Web Service (ml-image-classifier)
- [ ] Scroll to "Environment" section
- [ ] Add FLASK_ENV = production
- [ ] Add FLASK_SECRET_KEY = <your-generated-key>
- [ ] Add FLASK_DEBUG = False
- [ ] Add LOG_LEVEL = INFO
- [ ] Add RATE_LIMIT_ENABLED = True
- [ ] (Optional) Add other variables from optional list
- [ ] Click "Save"
- [ ] Wait for "Live" status
- [ ] Test `/api/health` endpoint
- [ ] Success! ✅

---

## 🆘 If Something Goes Wrong

**Error in Render logs?**
→ Check: [ENVIRONMENT_VARIABLES_GUIDE.md](ENVIRONMENT_VARIABLES_GUIDE.md) troubleshooting

**Not sure about a variable?**
→ Check: [ENVIRONMENT_VARIABLES_GUIDE.md](ENVIRONMENT_VARIABLES_GUIDE.md) detailed explanations

**Want more details?**
→ Read: [RENDER_EXACT_ENV_VALUES.md](RENDER_EXACT_ENV_VALUES.md)

---

## 🔗 All Environment Guides

| Document | Purpose |
|----------|---------|
| [ENVIRONMENT_VARIABLES_INDEX.md](ENVIRONMENT_VARIABLES_INDEX.md) | Navigation hub |
| [RENDER_EXACT_ENV_VALUES.md](RENDER_EXACT_ENV_VALUES.md) | Exact values to use |
| [RENDER_ENV_QUICK_REFERENCE.md](RENDER_ENV_QUICK_REFERENCE.md) | Quick copy-paste |
| [RENDER_ENV_SETUP_VISUAL.md](RENDER_ENV_SETUP_VISUAL.md) | Visual step-by-step |
| [ENVIRONMENT_VARIABLES_GUIDE.md](ENVIRONMENT_VARIABLES_GUIDE.md) | Full detailed guide |

---

## TL;DR

**Add these 5 to Render Environment:**

```
FLASK_ENV=production
FLASK_SECRET_KEY=<run-powershell-command-above>
FLASK_DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
```

**Generate key:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Test it works:**
```bash
curl https://your-render-url.onrender.com/api/health
```

**Done!** ✅

---

*Answer Generated: 2025-11-26*
*For Your Question: "What environment variables when creating web service?"*
