# 🚀 Deploy MLOps Image Classification to Render

## Overview
Render is a modern cloud platform that makes deployment extremely easy. It handles Docker automatically and gives you a free tier to start.

**Render Benefits:**
- ✅ Free tier available
- ✅ Auto-deploys from GitHub
- ✅ SSL certificate included
- ✅ Auto-scaling available
- ✅ Easy rollbacks
- ✅ No credit card needed for free tier

---

## Step 1: Prepare GitHub Repository

### 1.1 Ensure Your Code is on GitHub

```bash
# Navigate to your project
cd c:\Users\ngami\MLOps_Image_Classification

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "MLOps Image Classification - Ready for Render deployment

- Complete ML pipeline with CIFAR-10
- Flask API with 12 endpoints
- Docker containerization
- Load testing with Locust
- Comprehensive documentation"

# Create repository on GitHub
# Go to https://github.com/new
# Repository name: MLOps_Image_Classification
# Make it PUBLIC

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/MLOps_Image_Classification.git
git branch -M main
git push -u origin main
```

**Verify**: Your code is now on GitHub (public repository)

---

## Step 2: Create Render Account

1. **Go to Render**: https://render.com
2. **Click "Sign up"**
3. **Choose "GitHub" as sign-up method**
4. **Authorize Render to access your GitHub**
5. **Complete profile setup**

**Result**: You now have a Render account connected to GitHub

---

## Step 3: Deploy Flask App to Render

### 3.1 Create New Web Service

1. **Dashboard** → Click **"New +"** → Select **"Web Service"**
2. **Connect GitHub Repository**
   - Click **"Connect Account"** (if needed)
   - Search for **"MLOps_Image_Classification"**
   - Click **"Connect"**

3. **Configure Service**
   - **Name**: `ml-image-classifier` (no spaces, lowercase)
   - **Environment**: `Docker` (Render auto-detects from Dockerfile)
   - **Branch**: `main`
   - **Build Command**: Leave empty (Render uses Dockerfile)
   - **Start Command**: Leave empty (Render uses Dockerfile CMD)

4. **Plan**: Select **"Free"** tier
   - Auto-scales to zero after 15 minutes of inactivity
   - Wakes up on first request (takes 30 seconds)
   - Free for development/testing

5. **Click "Create Web Service"**

**Render will now:**
- ✅ Clone your repository
- ✅ Read the Dockerfile
- ✅ Build the Docker image
- ✅ Deploy the container
- ✅ Assign a public URL

### 3.2 Monitor Deployment

- **Logs**: Watch real-time build and deployment logs
- **Status**: Wait for "Live" status (takes 5-10 minutes)
- **URL**: Copy the public URL (format: `https://ml-image-classifier-xxxx.onrender.com`)

---

## Step 4: Set Environment Variables (Important!)

⚠️ **SEE: RENDER_ENV_QUICK_REFERENCE.md for complete list of variables to add**

### 4.1 Add Secrets in Render Dashboard

1. **Service Dashboard** → Scroll to **"Environment"**
2. **Click "Add Environment Variable"** for each variable

3. **Add MINIMUM required variables:**

```
FLASK_ENV=production
FLASK_SECRET_KEY=<generate-a-random-string>
FLASK_DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
```

4. **Generate FLASK_SECRET_KEY:**
   
   See **RENDER_ENV_QUICK_REFERENCE.md** for ways to generate:
   - PowerShell command
   - Online: https://randomkeygen.com/
   - Python script

5. **For complete list of optional variables, see RENDER_ENV_QUICK_REFERENCE.md**

6. **Click "Save"** → Render will restart the service

---

## Step 5: Verify Deployment

### 5.1 Test API Endpoints

```bash
# Get your Render URL from dashboard (e.g., https://ml-image-classifier-xxxx.onrender.com)

# Health check
curl https://ml-image-classifier-xxxx.onrender.com/api/health

# Model info
curl https://ml-image-classifier-xxxx.onrender.com/api/model/info

# Get uptime
curl https://ml-image-classifier-xxxx.onrender.com/api/model/uptime
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime_seconds": 125.5,
  "timestamp": "2025-11-26T12:34:56.789Z"
}
```

### 5.2 Test Dashboard

1. **Open browser**: `https://ml-image-classifier-xxxx.onrender.com`
2. **You should see**: 
   - Dashboard title
   - Model uptime
   - Visualizations
   - Prediction form
   - Upload section

---

## Step 6: Update README with Live URL

Edit your `README.md`:

```markdown
### 🌐 Live Deployment
**URL:** https://ml-image-classifier-xxxx.onrender.com

### 📱 How to Access

1. **Dashboard**: https://ml-image-classifier-xxxx.onrender.com
   - View model uptime
   - See visualizations
   - Upload and predict

2. **API Endpoints**:
   - Health: https://ml-image-classifier-xxxx.onrender.com/api/health
   - Predict: https://ml-image-classifier-xxxx.onrender.com/api/predict
   - Model Info: https://ml-image-classifier-xxxx.onrender.com/api/model/info

### Note on Render Free Tier
The service may take 30 seconds to wake up after inactivity (spins down after 15 minutes of no use).
For production, upgrade to a paid plan.
```

---

## Step 7: Deploy Updates (Auto-Deploy from GitHub)

Render automatically deploys when you push to GitHub:

```bash
# Make changes to your code
echo "Updated" > README.md

# Commit and push
git add .
git commit -m "Update documentation"
git push origin main

# Render will:
# 1. Detect changes
# 2. Build new Docker image
# 3. Deploy new version
# 4. Restart service

# Check deployment in Render dashboard
# Logs will show build progress
```

---

## Troubleshooting

### Issue: Deployment Failed
**Check logs in Render dashboard:**
```
Render Dashboard → Your Service → Logs (top right)
```

**Common causes:**
- ❌ Dependencies missing → Add to `requirements.txt`
- ❌ Port issue → Make sure app uses port 5000 (Render provides PORT env var)
- ❌ Model files missing → Ensure models/ directory is committed
- ❌ Out of memory → Upgrade to paid plan

**Fix:**
```bash
# Fix issue locally
# Commit and push
git add .
git commit -m "Fix: [describe fix]"
git push origin main

# Render auto-redeploys
```

### Issue: App Takes 30 Seconds to Load
**This is normal on free tier** - service spins down after 15 minutes of inactivity.
**Solution**: Upgrade to paid plan or keep service active with periodic requests.

### Issue: Model Not Loading
**Check logs:**
```
# Error: Model file not found
# Solution: Ensure models/ directory is in git
git add models/
git commit -m "Add model files"
git push origin main
```

### Issue: Disk Space
**Free tier has limited storage.** If you hit limit:
- Delete old prediction logs
- Use cloud storage for model artifacts
- Upgrade to paid plan

---

## Step 8: Make It Production-Ready (Optional)

### 8.1 Add Custom Domain (Paid Plan)
1. **Render Dashboard** → Service Settings
2. **Custom Domain** → Add your domain
3. **Follow DNS setup instructions**

### 8.2 Enable Auto-Scaling (Paid Plan)
1. **Render Dashboard** → Service Settings
2. **Scaling** → Enable auto-scaling
3. **Set max instances**: 3-5 for load balancing

### 8.3 Set Up Monitoring
1. **Render Dashboard** → Alerts
2. **Create alert for uptime** (get notified if service goes down)

### 8.4 Upgrade to Paid Plan
```
Free Tier Limitations:
- Spins down after 15 min inactivity
- Limited CPU/RAM
- No guaranteed uptime

Starter Plan (~$7/month):
- Always running
- More resources
- Better performance
- Suitable for production testing
```

---

## Complete Deployment Checklist

- [ ] Code pushed to public GitHub repository
- [ ] GitHub repository URL: `https://github.com/YOUR_USERNAME/MLOps_Image_Classification`
- [ ] Render account created and connected to GitHub
- [ ] Web Service created on Render
- [ ] Environment variables set (SECRET_KEY, etc.)
- [ ] Deployment completed (status = "Live")
- [ ] Health check endpoint works
- [ ] Dashboard loads in browser
- [ ] Render URL obtained: `https://ml-image-classifier-xxxx.onrender.com`
- [ ] README.md updated with live URL
- [ ] Changes pushed to GitHub (auto-redeploy triggered)

---

## Your Deployment URLs

Once deployed, you'll have:

```
🌐 Dashboard:    https://ml-image-classifier-xxxx.onrender.com
🔌 API Root:     https://ml-image-classifier-xxxx.onrender.com/api
📊 Health:       https://ml-image-classifier-xxxx.onrender.com/api/health
🤖 Model Info:   https://ml-image-classifier-xxxx.onrender.com/api/model/info
🔮 Predict:      https://ml-image-classifier-xxxx.onrender.com/api/predict
```

---

## Quick Reference Commands

### Push Code to GitHub (First Time)
```bash
cd c:\Users\ngami\MLOps_Image_Classification
git init
git add .
git commit -m "Initial commit - MLOps ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/MLOps_Image_Classification.git
git branch -M main
git push -u origin main
```

### Update Deployment (Subsequent Times)
```bash
git add .
git commit -m "Update: [describe changes]"
git push origin main
# Render auto-deploys!
```

### View Render Logs
```
Render Dashboard → Your Service → Logs
```

### Get Your Live URL
```
Render Dashboard → Your Service → Copy URL from top
```

---

## Next Steps

1. **Push code to GitHub** (if not already done)
2. **Create Render account** at https://render.com
3. **Create Web Service** and connect GitHub
4. **Wait for deployment** (5-10 minutes)
5. **Test live URL** in browser
6. **Update README.md** with live URL
7. **Push update** to GitHub
8. **Share your live deployment!** 🎉

---

## Example: What Your Live App Looks Like

```
📍 URL: https://ml-image-classifier-abc123.onrender.com

✨ Features:
- ✅ Real-time model uptime display
- ✅ Interactive prediction dashboard
- ✅ 6+ visualizations
- ✅ Batch image upload
- ✅ Retraining trigger
- ✅ API endpoints
- ✅ Load balancing (with 3 containers)

📊 Performance:
- 🚀 ~80-120 requests/second (free tier)
- ⏱️ 500-1000ms average latency
- 🔄 Auto-scales on paid plan

🎓 Perfect for:
- Assignment submission
- Portfolio showcase
- Live demo
- Academic evaluation
```

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **GitHub Integration**: https://render.com/docs/github
- **Docker on Render**: https://render.com/docs/docker
- **Environment Variables**: https://render.com/docs/environment-variables
- **Troubleshooting**: https://render.com/docs/troubleshooting

---

## FAQ

**Q: Is it free?**
A: Yes! Free tier is included. Service spins down after 15 min inactivity. Upgrade to Starter ($7/month) for always-on.

**Q: How long does deployment take?**
A: 5-10 minutes for first deployment. Updates take 2-3 minutes.

**Q: Can I use my own domain?**
A: Yes, on paid plans. Free tier uses `onrender.com` subdomain.

**Q: Will my data be safe?**
A: Yes. Render provides SSL/TLS encryption. All data is secure.

**Q: Can I scale to multiple instances?**
A: Yes, on paid plans. Free tier runs single instance.

**Q: What if my code has bugs?**
A: Easy rollback! Click "Rollback" in Render dashboard.

---

## Success! 🎉

Your MLOps Image Classification app is now **live on the internet**!

**Share your URL:**
```
https://ml-image-classifier-xxxx.onrender.com
```

**You can now:**
- ✅ Access dashboard from anywhere
- ✅ Make predictions online
- ✅ Share live demo with instructors
- ✅ Show portfolio to employers
- ✅ Run load tests on live instance

---

*Deployment Guide Created: 2025-11-26*
*Platform: Render (https://render.com)*
*Status: Ready to Deploy 🚀*
