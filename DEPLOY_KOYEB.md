# ⚡ Koyeb pe Backend Deploy Karne ka Guide (Free, No Card!)

Koyeb ek modern platform hai - **completely free, no card needed, no sleep!**

---

## 📋 Step 1: Koyeb Account Banao

1. https://www.koyeb.com pe jao
2. **"Get Started"** click karein
3. GitHub se sign in karein (free hai!)
4. **No credit card required!** ✅

---

## 📋 Step 2: Create App

1. Dashboard me **"Create App"** click karein
2. **"GitHub"** select karein
3. Repository select karein: `zkdownloader-webapp`

---

## 📋 Step 3: Build Settings

1. **Name:** `zkdownloader-backend`
2. **Region:** `Washington, D.C.` (ya apne paas wala)
3. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Command:**
   ```bash
   python backend.py
   ```
5. **Root Directory:** `web_app` (agar repo root me hai)

---

## 📋 Step 4: Environment Variables

**"Environment Variables"** section me:
- `PORT` - Koyeb automatically set karega (zarurat nahi)

---

## 📋 Step 5: Deploy

1. **"Deploy"** button click karein
2. 5-10 minutes wait karein
3. Deploy complete hone ke baad URL mil jayega

---

## 📋 Step 6: App URL Note Karein

Dashboard me app ke saamne URL dikhega:
```
https://zkdownloader-backend-xyz.koyeb.app
```

**Yeh URL copy karein!** 📋

---

## 📋 Step 7: Frontend me Backend URL Update Karein

`app.js` me line 29 pe backend URL update karein:

```javascript
return 'https://zkdownloader-backend-xyz.koyeb.app'; // Apna Koyeb URL
```

---

## ✅ Benefits

- ✅ **Free tier** - no credit card needed
- ✅ **No sleep** - always running!
- ✅ **Fast deployment**
- ✅ **Global edge network**
- ✅ **Auto HTTPS**

---

## 🔧 Troubleshooting

### **Problem: Build fails**

**Solution:**
- Build logs check karein (Koyeb dashboard)
- `requirements.txt` verify karein

### **Problem: App crashes**

**Solution:**
- Logs check karein
- `backend.py` me `host='0.0.0.0'` hai ya nahi verify karein

---

## 🎉 Success!

Ab backend Koyeb pe hai - **completely free, no card needed, no sleep!** 🚀

