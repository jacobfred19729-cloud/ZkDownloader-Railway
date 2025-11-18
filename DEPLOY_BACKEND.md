# ☁️ Backend Cloud Deployment Guide

## Backend ko Cloud pe Deploy Karein (Free)

Yeh guide aapko dikhayega kaise backend ko **Railway** ya **Render** pe deploy karein - **completely free!**

---

## 🚀 Railway Deployment (Recommended)

### **Step 1: Railway Account Banao**

1. https://railway.app pe jao
2. **GitHub** se sign up karein
3. Free tier me unlimited projects!

### **Step 2: Project Setup**

1. **New Project** click karein
2. **Deploy from GitHub repo** select karein
3. Apna repo select karein

### **Step 3: Configuration**

Railway automatically detect karega Python project. Agar nahi, to:

**`railway.json`** file banao:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python backend.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Environment Variables** (agar chahiye):
- `PORT` - Railway automatically set karega

### **Step 4: Backend Code Update**

`backend.py` me port update karein:

```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### **Step 5: Deploy**

1. **Deploy** button click karein
2. Railway automatically build aur deploy karega
3. **Domain** mil jayega (example: `zkdownloader.railway.app`)

### **Step 6: App me Backend URL Update**

`app.js` me backend URL update karein:

```javascript
const BACKEND_URL = 'https://zkdownloader.railway.app';
```

---

## 🌐 Render Deployment (Alternative)

### **Step 1: Render Account**

1. https://render.com pe jao
2. **GitHub** se sign up

### **Step 2: New Web Service**

1. **New** → **Web Service**
2. GitHub repo connect karein
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend.py`
   - **Environment**: Python 3

### **Step 3: Deploy**

Render automatically deploy karega. Free domain mil jayega!

---

## 📱 App me Use Karein

Backend URL ko app me hardcode karein:

```javascript
// app.js
const BACKEND_URL = 'https://your-backend.railway.app';
```

Ya environment variable use karein (production me).

---

## ✅ Benefits

- ✅ **Free hosting** - unlimited projects
- ✅ **Auto-deploy** - GitHub push = auto deploy
- ✅ **HTTPS** - secure connection
- ✅ **Always online** - 24/7 available
- ✅ **No server management** - fully managed

---

## 🎉 Done!

Ab backend cloud pe hai - app me sirf URL update karein aur APK build karein! 🚀




