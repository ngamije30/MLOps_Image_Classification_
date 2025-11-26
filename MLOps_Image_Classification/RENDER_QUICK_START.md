# 🚀 RENDER DEPLOYMENT - QUICK START (5 STEPS)

## ⏱️ Time Required: ~20 minutes total

---

## STEP 1: Push Code to GitHub (5 min)

```bash
cd c:\Users\ngami\MLOps_Image_Classification

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "MLOps Image Classification - Ready for Render deployment"

# Go to https://github.com/new and create repository:
# - Name: MLOps_Image_Classification
# - Make it PUBLIC
# - Do NOT initialize with README

# Connect and push
git remote add origin https://github.com/YOUR_USERNAME/MLOps_Image_Classification.git
git branch -M main
git push -u origin main
```

✅ **Done**: Your code is on GitHub

---

## STEP 2: Create Render Account (3 min)

1. Go to **https://render.com**
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access GitHub
5. Complete profile

✅ **Done**: You have a Render account

---

## STEP 3: Deploy to Render (10 min + 5-10 min build time)

### 3.1 Create New Web Service

1. **Render Dashboard** → Click **"New +"** → Select **"Web Service"**
2. Click **"Connect Account"** → Search **"MLOps_Image_Classification"** → Click **"Connect"**

### 3.2 Configure

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `ml-image-classifier` |
| **Environment** | `Docker` |
| **Branch** | `main` |
| **Build Command** | (leave empty) |
| **Start Command** | (leave empty) |
| **Plan** | `Free` |

3. Click **"Create Web Service"**

### 3.3 Wait for Deployment

- Watch the logs (they auto-update)
- Wait until you see: **"Live ✓"** at the top
- Takes ~5-10 minutes

✅ **Done**: Your app is live! Copy the URL

---

## STEP 4: Set Environment Variables (2 min)

1. In Render dashboard, scroll down to **"Environment"**
2. Click **"Add Secret"** and add:

```
FLASK_ENV=production
FLASK_SECRET_KEY=<generate-random-key>
```

3. To generate random key:
   - Option A: Use https://randomkeygen.com/ (copy Fort Knox password)
   - Option B: PowerShell: `-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})`

4. Click **"Save"** → Service auto-restarts

✅ **Done**: Environment configured

---

## STEP 5: Test Your Live App (3 min)

### 5.1 Get Your URL

- Render Dashboard → Your Service → Copy URL from top
- Format: `https://ml-image-classifier-xxxx.onrender.com`

### 5.2 Test in Browser

```
Open: https://ml-image-classifier-xxxx.onrender.com
You should see the dashboard!
```

### 5.3 Test API

```bash
# Health check (copy-paste your URL)
curl https://ml-image-classifier-xxxx.onrender.com/api/health

# Should return:
# {"status": "healthy", "model_loaded": true, ...}
```

✅ **Done**: Your app is working live!

---

## BONUS: Auto-Deploy on GitHub Push

Every time you push to GitHub, Render automatically:
1. Pulls new code
2. Rebuilds Docker image
3. Deploys new version
4. Service is live in 2-3 minutes

```bash
# Make a change
echo "Updated" >> README.md

# Push to GitHub
git add .
git commit -m "Update documentation"
git push origin main

# Watch Render dashboard → auto-deploys! 🎉
```

---

## YOUR LIVE URLS

Once deployed:

| Endpoint | URL |
|----------|-----|
| 🌐 **Dashboard** | `https://ml-image-classifier-xxxx.onrender.com` |
| 📊 **Health Check** | `https://ml-image-classifier-xxxx.onrender.com/api/health` |
| 🤖 **Model Info** | `https://ml-image-classifier-xxxx.onrender.com/api/model/info` |
| 🔮 **Predict** | `https://ml-image-classifier-xxxx.onrender.com/api/predict` |
| 📈 **Statistics** | `https://ml-image-classifier-xxxx.onrender.com/api/statistics` |

---

## ⚡ IMPORTANT NOTES

### Free Tier Behavior
- ✅ Always deployed
- ✅ Free forever
- ⚠️ Service spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes ~30 seconds
- ℹ️ For production, upgrade to Starter ($7/month for always-on)

### How to Keep Service Awake (Free Tier)
Option 1: Make periodic requests
```bash
# Windows Task Scheduler or cron job
# Every 14 minutes, hit: https://ml-image-classifier-xxxx.onrender.com/api/health
```

Option 2: Use free monitoring service
```
Sign up at https://uptimerobot.com
Monitor your URL every 5 minutes (keeps it awake)
```

---

## 🆘 TROUBLESHOOTING

### "Deployment Failed"
→ Check **Logs** tab in Render dashboard
→ Common: Missing dependencies, port issues
→ Fix locally, push to GitHub, auto-redeploys

### "Takes 30 seconds to load"
→ Normal on free tier (service spinning up)
→ Subsequent requests are fast
→ Upgrade to paid for always-on

### "Model not found"
→ Ensure `models/` folder is committed to GitHub
```bash
git add models/
git commit -m "Add model files"
git push origin main
# Render redeploys
```

### "App won't start"
→ Check environment variables set correctly
→ Check all dependencies in `requirements.txt`
→ View logs: Render Dashboard → Logs

---

## 📋 QUICK CHECKLIST

- [ ] Code pushed to GitHub (public repo)
- [ ] Render account created
- [ ] Web Service connected to GitHub
- [ ] Deployment shows "Live" status
- [ ] Environment variables set
- [ ] Health endpoint works
- [ ] Dashboard loads
- [ ] Live URL obtained
- [ ] README updated with URL
- [ ] Demo video recorded

---

## 🎉 SUCCESS!

Your MLOps Image Classification app is now **LIVE ON THE INTERNET**!

**Share this URL:**
```
https://ml-image-classifier-xxxx.onrender.com
```

**You can now:**
- ✅ Access from anywhere
- ✅ Share with instructors
- ✅ Show portfolio to employers
- ✅ Run live demos
- ✅ Use in presentations

---

## 📚 Next Steps

1. ✅ **Deploy to Render** (follow steps above)
2. 📝 **Update README** with live URL
3. 🎬 **Record demo video** showing live app
4. 📤 **Upload to YouTube**
5. 📊 **Run load tests** (optional)
6. 📤 **Submit assignment**

---

**Deployment Guide**: RENDER_DEPLOYMENT_GUIDE.md (detailed version)
**Status**: 🚀 Ready to Deploy
**Time to Live**: ~20 minutes

