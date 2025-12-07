# Deployment Guide - Render Hosting

This guide will help you deploy your Web Scraping Chatbot to Render with both backend and frontend hosted together.

## 🚀 Quick Deployment Steps

### Option 1: Deploy Backend + Frontend Together (Recommended)

This option hosts everything on a single Render Web Service.

#### Step 1: Prepare Your Code

1. **Create a GitHub Repository** (if you haven't already)
   ```bash
   cd c:\Users\Hirthick\Downloads\website-to-chatbot-main
   git init
   git add .
   git commit -m "Initial commit - Web Scraping Chatbot"
   ```

2. **Push to GitHub**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

#### Step 2: Deploy to Render

1. **Go to Render Dashboard**
   - Visit: https://render.com
   - Sign up or log in

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your chatbot repository

3. **Configure the Service**
   
   **Basic Settings:**
   - **Name**: `web-scraping-chatbot` (or your preferred name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   
   **Build & Deploy:**
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     python app.py
     ```

4. **Environment Variables**
   
   Add these in the "Environment" section:
   - `PORT` = `10000` (Render uses this)
   - `FLASK_ENV` = `production`

5. **Advanced Settings**
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: Yes (recommended)

6. **Click "Create Web Service"**

#### Step 3: Wait for Deployment

- Render will build and deploy your app (takes 2-5 minutes)
- You'll get a URL like: `https://web-scraping-chatbot.onrender.com`

#### Step 4: Test Your Deployment

1. Visit your Render URL
2. You should see the dark green chatbot interface
3. Test scraping a website
4. Test the chat functionality

---

## 🔧 Alternative: Separate Backend and Frontend

If you want to host them separately:

### Backend on Render

Follow steps above for backend only.

### Frontend on Netlify

1. **Create `netlify.toml`** in your project:
   ```toml
   [build]
     publish = "."
   
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. **Update `script.js`**:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.onrender.com';
   ```

3. **Deploy to Netlify**:
   - Drag and drop `index.html`, `style.css`, `script.js` to Netlify
   - Or connect GitHub repository

---

## 📋 Pre-Deployment Checklist

- [x] All files created and saved
- [x] `requirements.txt` has all dependencies
- [x] `app.py` serves static files
- [x] `script.js` uses dynamic API URL
- [x] Code committed to Git
- [x] GitHub repository created
- [x] Render account created

---

## 🐛 Troubleshooting

### Issue: "Application failed to start"
**Solution**: Check Render logs for errors. Usually missing dependencies.

### Issue: "Cannot connect to backend"
**Solution**: Verify the API_BASE_URL in `script.js` matches your Render URL.

### Issue: "Scraping fails on Render"
**Solution**: Some websites block cloud IPs. Try different websites or add more realistic headers.

### Issue: "Static files not loading"
**Solution**: Ensure `send_from_directory` routes are in `app.py`.

---

## 💰 Pricing

**Render Free Tier:**
- ✅ 750 hours/month free
- ✅ Automatic SSL
- ✅ Custom domains
- ⚠️ Spins down after 15 min of inactivity (cold starts)

**Paid Plans:**
- Start at $7/month for always-on service

---

## 🔒 Security Notes

For production deployment, consider:

1. **Rate Limiting**: Add Flask-Limiter to prevent abuse
2. **API Keys**: Implement authentication for API endpoints
3. **Database**: Replace in-memory storage with PostgreSQL
4. **Logging**: Add proper logging for monitoring
5. **Error Handling**: Enhance error messages (don't expose internals)

---

## 🎯 Post-Deployment

After successful deployment:

1. **Test all features** on the live URL
2. **Share your chatbot** with others
3. **Monitor usage** in Render dashboard
4. **Set up custom domain** (optional)
5. **Enable auto-deploy** for easy updates

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Flask Docs**: https://flask.palletsprojects.com

---

**Your chatbot is ready to go live! 🚀**
