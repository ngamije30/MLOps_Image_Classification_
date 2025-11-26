# 📖 Environment Variables Documentation Index

## Quick Navigation

Choose the guide that matches your need:

---

## 🎯 **"I just want the exact values to paste"**
→ **[RENDER_EXACT_ENV_VALUES.md](RENDER_EXACT_ENV_VALUES.md)** ⭐ START HERE

Shows exactly what to put in Render dashboard with copy-paste examples.

---

## 📋 **"I want a quick reference"**
→ **[RENDER_ENV_QUICK_REFERENCE.md](RENDER_ENV_QUICK_REFERENCE.md)**

Fast reference card with minimum required variables and how to generate FLASK_SECRET_KEY.

---

## 🖼️ **"I'm a visual learner"**
→ **[RENDER_ENV_SETUP_VISUAL.md](RENDER_ENV_SETUP_VISUAL.md)**

Visual guide showing step-by-step where to add variables in Render dashboard.

---

## 📚 **"I need detailed explanations"**
→ **[ENVIRONMENT_VARIABLES_GUIDE.md](ENVIRONMENT_VARIABLES_GUIDE.md)**

Comprehensive guide with:
- Explanation of each variable
- Security best practices
- Troubleshooting
- Examples for different environments

---

## 🚀 **"I want to deploy to Render"**
→ **[RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)**

Complete step-by-step deployment guide that references the environment variables guides.

---

## 🔗 **"I need to configure locally"**

Create a `.env` file in your project root:

```bash
# Copy the template
cp .env.example .env

# Edit .env with your local values
```

See **[.env.example](.env.example)** for template.

---

## 📊 At a Glance

| Need | File | Time |
|------|------|------|
| Just the values | RENDER_EXACT_ENV_VALUES.md | 2 min |
| Quick copy-paste | RENDER_ENV_QUICK_REFERENCE.md | 3 min |
| Visual guide | RENDER_ENV_SETUP_VISUAL.md | 5 min |
| Learn everything | ENVIRONMENT_VARIABLES_GUIDE.md | 15 min |
| Full deployment | RENDER_DEPLOYMENT_GUIDE.md | 30 min |

---

## 🚦 Recommended Path

1. **First time deploying?**
   1. Read: RENDER_EXACT_ENV_VALUES.md
   2. Paste values into Render
   3. Test: `curl /api/health`
   4. Done! ✅

2. **Want to understand more?**
   1. Read: RENDER_ENV_QUICK_REFERENCE.md
   2. Read: ENVIRONMENT_VARIABLES_GUIDE.md
   3. Deploy with confidence

3. **Having issues?**
   1. Check: ENVIRONMENT_VARIABLES_GUIDE.md troubleshooting section
   2. Verify in Render logs

---

## 🎯 Most Important Variables

The 5 you MUST set:

```
FLASK_ENV=production
FLASK_SECRET_KEY=<random-string>
FLASK_DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
```

Everything else is optional.

---

## 🔐 Generating FLASK_SECRET_KEY

PowerShell command (run in terminal):
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Or use: https://randomkeygen.com/

---

## ✅ Checklist Before Deploying

- [ ] Read: RENDER_EXACT_ENV_VALUES.md
- [ ] Generated FLASK_SECRET_KEY
- [ ] Added all 5 required variables to Render
- [ ] Clicked "Save" in Render dashboard
- [ ] Service is running ("Live" status)
- [ ] Tested `/api/health` endpoint
- [ ] Dashboard loads in browser

---

## 🆘 Quick Help

**Q: Where do I add environment variables in Render?**
A: Dashboard → Web Service → Environment section

**Q: What's FLASK_SECRET_KEY?**
A: Random string that encrypts your sessions. Must be unique and random.

**Q: Can I use the same SECRET_KEY in dev and production?**
A: No. Generate a new random one for each environment.

**Q: Are the optional variables really optional?**
A: Yes. The app has good defaults. Only required 5 are needed to start.

**Q: How do I test if it's working?**
A: `curl https://your-render-url.onrender.com/api/health`

---

## 🔗 Related Guides

- [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) - Full deployment steps
- [README.md](README.md) - Project overview
- [config.py](config.py) - How your app reads these variables
- [.env.example](.env.example) - Environment template

---

## 📞 Support

- Check troubleshooting in: ENVIRONMENT_VARIABLES_GUIDE.md
- Review Render logs: Dashboard → Logs tab
- Test endpoint: `curl https://your-app.onrender.com/api/health`

---

*Last Updated: 2025-11-26*
*Start with: RENDER_EXACT_ENV_VALUES.md 👉*
