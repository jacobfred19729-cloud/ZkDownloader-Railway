# 📱 Mobile App Installation Guide

## ZKDownloader ko Phone pe Install Kaise Karein

### Prerequisites
1. Backend server chal raha ho (`python backend.py`)
2. Phone aur computer same WiFi network pe hon

---

## 🚀 Step-by-Step Installation

### **Step 1: Backend Start Karein**

Computer pe terminal me:
```bash
cd web_app
python backend.py
```

Server `http://localhost:5000` pe chalega.

### **Step 2: Phone se Connect Karein**

1. Computer ka **IP address** find karein:
   - **Windows**: `ipconfig` (IPv4 address dekho)
   - **Mac/Linux**: `ifconfig` ya `ip addr`
   
   Example: `192.168.1.100`

2. Phone ke browser me jao:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

### **Step 3: PWA Install Karein**

#### **Android (Chrome/Brave)**
1. Browser me app open karein
2. Address bar me **"Install"** ya **"Add to Home Screen"** option dikhega
3. Ya **Menu (⋮)** → **"Add to Home Screen"** / **"Install App"**
4. **"Install"** button click karein
5. App home screen pe add ho jayegi ✅

#### **iOS (Safari)**
1. Safari me app open karein
2. **Share button (□↑)** click karein
3. **"Add to Home Screen"** select karein
4. App name edit kar sakte hain (optional)
5. **"Add"** button click karein
6. App home screen pe add ho jayegi ✅

---

## 🔧 Alternative: Local Network Setup

Agar phone aur computer same WiFi pe nahi hain:

### Option 1: Hotspot Use Karein
1. Computer se WiFi hotspot create karein
2. Phone ko us hotspot se connect karein
3. Same IP address use karein

### Option 2: ngrok (Internet se Access)
```bash
# ngrok install karein (https://ngrok.com)
ngrok http 5000
```
ngrok ka URL phone me open karein (example: `https://abc123.ngrok.io`)

---

## ✅ Installation Complete!

Ab app home screen pe icon dikhega. Click karke direct open ho jayegi - bilkul native app ki tarah! 🎉

---

## 🐛 Troubleshooting

**Problem**: Install option nahi dikh raha
- **Solution**: HTTPS use karein (ngrok) ya local network pe ensure karein ki backend chal raha hai

**Problem**: App open nahi ho rahi
- **Solution**: Backend server check karein (`python backend.py`)

**Problem**: Network error
- **Solution**: Phone aur computer same WiFi pe hon, firewall check karein

---

## 📝 Notes

- App offline me kaam nahi karegi (backend server chahiye)
- Internet connection zaroori hai video download ke liye
- App data local me store hota hai (downloads, history)

