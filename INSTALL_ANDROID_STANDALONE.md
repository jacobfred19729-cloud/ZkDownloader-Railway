# 📱 Android Standalone App Setup (No PC Required)

## ZKDownloader ko Phone pe Standalone Install Karein

Yeh guide aapko dikhayega kaise app ko phone pe completely standalone install karein - **PC ki zaroorat nahi hogi!**

---

## 🎯 Requirements

1. **Android Phone** (Android 7+)
2. **Termux App** (Free, Play Store se install karein)
3. **Internet Connection**

---

## 🚀 Step-by-Step Installation

### **Step 1: Termux Install Karein**

1. **F-Droid** se Termux download karein (recommended):
   - F-Droid: https://f-droid.org/packages/com.termux/
   - Ya **Play Store** se "Termux" search karein

2. Termux open karein aur permissions dein

### **Step 2: Python aur Dependencies Install Karein**

**Option 1: Quick Setup Script (Recommended)**

App files me `setup_android.sh` file hai. Usse run karein:

```bash
# Files ko phone me copy karein (USB/Cloud se)
# Phir Termux me:
cd /path/to/web_app
bash setup_android.sh
```

**Option 2: Manual Setup**

Termux me ye commands run karein:

```bash
# Update packages
pkg update && pkg upgrade -y

# Python aur pip install
pkg install python -y
pkg install git -y

# yt-dlp install
pip install yt-dlp flask
```

### **Step 3: App Files Download Karein**

```bash
# Home directory me jao
cd ~

# App folder banao
mkdir ZKDownloader
cd ZKDownloader

# Files manually copy karein ya git se clone karein
# (Agar git repo hai to)
# git clone YOUR_REPO_URL .

# Ya manually files transfer karein:
# - backend.py
# - index.html
# - app.js
# - style.css
# - manifest.json
# - requirements.txt
# - assets/ folder
```

**Files Transfer Kaise Karein:**
- **Option 1**: USB cable se phone connect karke files copy karein
- **Option 2**: Cloud storage (Google Drive/Dropbox) use karein
- **Option 3**: Termux me `termux-setup-storage` run karein, phir files `/sdcard/` se copy karein

### **Step 4: Backend Start Karein**

**Quick Start:**
```bash
# start_backend.sh file use karein
cd ~/ZKDownloader/web_app
bash start_backend.sh
```

**Ya Manual:**
```bash
cd ~/ZKDownloader/web_app
python backend.py
```

Backend `http://localhost:5000` pe chalega.

### **Step 5: Browser me App Open Karein**

1. Phone ke browser me jao: `http://localhost:5000`
2. App open ho jayegi ✅

### **Step 6: PWA Install Karein (Home Screen pe)**

1. Browser me **Menu (⋮)** → **"Add to Home Screen"**
2. App name edit karein (optional)
3. **"Add"** click karein
4. Ab app home screen pe icon dikhega! 🎉

---

## 🔄 Auto-Start Backend (Optional)

Agar aap chahte hain ki Termux start hote hi backend automatically chal jaye:

### **Method 1: Termux Boot Script**

```bash
# Termux:Boot app install karein (F-Droid se)
# Phir ~/.termux/boot/ folder me script banao:

mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-backend.sh
```

Script me ye add karein:
```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/ZKDownloader/web_app
python backend.py &
```

```bash
# Script ko executable banao
chmod +x ~/.termux/boot/start-backend.sh
```

### **Method 2: Manual Start Script**

```bash
# Quick start script banao
nano ~/start-downloader.sh
```

Add karein:
```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/ZKDownloader/web_app
python backend.py
```

```bash
chmod +x ~/start-downloader.sh
```

Ab sirf `~/start-downloader.sh` run karein!

---

## 📱 Daily Use

1. **Termux open karein**
2. **Backend start karein**: `cd ~/ZKDownloader/web_app && python backend.py`
3. **Home screen se app icon click karein**
4. **Videos download karein!** 🎬

---

## ⚠️ Important Notes

- **Termux background me chalega** - app use karte waqt Termux ko close mat karein
- **Battery optimization** off karein Termux ke liye (Settings → Apps → Termux → Battery → Unrestricted)
- **Internet connection** zaroori hai video download ke liye
- **Storage space** check karte rahein (videos kaafi space leti hain)

---

## 🐛 Troubleshooting

**Problem**: Backend start nahi ho raha
- **Solution**: `pip install --upgrade flask yt-dlp` run karein

**Problem**: Port already in use
- **Solution**: `pkill -f "python backend.py"` run karein, phir dobara start karein

**Problem**: Files nahi mil rahi
- **Solution**: `pwd` se current directory check karein, `ls` se files list dekhein

**Problem**: App browser me open nahi ho rahi
- **Solution**: Backend check karein - `http://localhost:5000` pe kuch dikhna chahiye

---

## 🎉 Success!

Ab aapka app completely standalone hai! PC ki zaroorat nahi - sab kuch phone pe hi chalega! 📱✨

