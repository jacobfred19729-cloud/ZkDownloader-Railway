# 🐍 PythonAnywhere pe Backend Deploy Karne ka Guide (Free, No Card!)

PythonAnywhere Python apps ke liye perfect hai - **completely free, no card needed!**

---

## 📋 Step 1: PythonAnywhere Account Banao

1. https://www.pythonanywhere.com pe jao
2. **"Beginner"** plan select karein (free hai!)
3. Sign up karein (email se ya GitHub se)
4. **No credit card required!** ✅

---

## 📋 Step 2: Web App Create Karein

1. Login ke baad dashboard me **"Web"** tab click karein
2. **"Add a new web app"** click karein
3. **"Next"** click karein
4. **"Flask"** select karein
5. **"Python 3.10"** (ya latest) select karein
6. **"Next"** click karein
7. **"Next"** click karein (default path theek hai)
8. **"Finish"** click karein

---

## 📋 Step 3: Files Upload Karein

### **Method 1: Files Tab (Easiest)**

1. Dashboard me **"Files"** tab click karein
2. `mysite/` folder me jao (ya jo folder create hua)
3. **"Upload a file"** click karein
4. Upload karein:
   - `backend.py`
   - `requirements.txt`
   - `index.html`
   - `app.js`
   - `style.css`
   - `manifest.json`
   - `assets/` folder (zip karke upload karein)

### **Method 2: Git Clone (Better)**

1. **"Files"** tab me jao
2. **"Bash"** click karein (terminal open hoga)
3. Terminal me:
   ```bash
   cd ~
   git clone https://github.com/jacobfred19729-cloud/zkdownloader-webapp.git
   cd zkdownloader-webapp
   ls
   ```
   
**Note:** Files directly `zkdownloader-webapp` folder me hain, `web_app` subdirectory me nahi!

---

## 📋 Step 4: Dependencies Install Karein

1. **"Tasks"** tab me jao
2. **"Bash"** click karein (terminal open hoga)
3. Run karein:
   ```bash
   pip3.10 install --user flask flask-cors yt-dlp
   ```

**Note:** PythonAnywhere me `pip3.10` use karein (Python version ke according).

---

## 📋 Step 5: Web App Configure Karein

1. **"Web"** tab me jao
2. **"Source code"** me path set karein:
   ```
   /home/jacobfred1/zkdownloader-webapp
   ```
   **Important:** `/web_app` mat add karein - files directly root me hain!
3. **"WSGI configuration file"** click karein
4. File edit karein:

```python
import sys
import os

path = '/home/jacobfred1/zkdownloader-webapp'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['FLASK_APP'] = 'backend'

from backend import app as application
```

5. **"Save"** click karein

---

## 📋 Step 6: Static Files Configure Karein

**"Web"** tab me scroll karke **"Static files"** section me:

1. **URL:** `/static`
2. **Directory:** `/home/jacobfred1/zkdownloader-webapp`

**"Add"** click karein.

**Note:** Path me `/web_app` mat add karein - files directly root me hain!

---

## 📋 Step 7: Reload Web App

**"Web"** tab me **"Reload"** button click karein.

---

## 📋 Step 8: App URL Note Karein

**"Web"** tab me top pe URL dikhega:
```
https://yourusername.pythonanywhere.com
```

**Yeh URL copy karein!** 📋

---

## 📋 Step 9: Frontend me Backend URL Update Karein

`app.js` me line 29 pe backend URL update karein:

```javascript
return 'https://yourusername.pythonanywhere.com'; // Apna PythonAnywhere URL
```

---

## ✅ Benefits

- ✅ **Free tier** - no credit card needed
- ✅ **Python-specific** - perfect for Flask
- ✅ **Easy to use** - web interface
- ✅ **No sleep** - always running
- ✅ **Free SSL**

---

## ⚠️ Free Tier Limits

- ⚠️ **1 web app** only
- ⚠️ **512 MB disk space**
- ⚠️ **100 seconds CPU time per day**
- ⚠️ **Custom domain** nahi (subdomain milta hai)

**Note:** Small apps ke liye perfect hai!

---

## 🔧 Troubleshooting

### **Problem: Module not found**

**Solution:**
- Bash terminal me `pip3.10 install --user module_name` run karein
- Ya **"Tasks"** tab me bash use karein

### **Problem: App not loading**

**Solution:**
- **"Web"** tab me **"Error log"** check karein
- WSGI configuration file sahi hai ya nahi verify karein

---

## 🎉 Success!

Ab backend PythonAnywhere pe hai - **completely free, no card needed!** 🚀

