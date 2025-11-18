# 🔧 Git Install Karne ka Guide (Windows)

Aapke system pe Git install nahi hai. Pehle Git install karein, phir GitHub pe code push kar sakte hain.

---

## 📥 Step 1: Git Download Karein

1. Browser me jao: **https://git-scm.com/download/win**
2. Download automatically start ho jayega
3. Ya manually **"Click here to download"** pe click karein

---

## 💿 Step 2: Git Install Karein

1. Downloaded file (`Git-2.x.x-64-bit.exe`) pe double-click karein
2. Installation wizard open hoga

### **Installation Options (Default theek hain):**

1. **Select Components:**
   - ✅ Git Bash Here
   - ✅ Git GUI Here
   - ✅ Associate .git* files
   - ✅ Associate .sh files
   - ✅ Check daily for updates

2. **Default Editor:**
   - Default: **Nano** (theek hai)
   - Ya **VS Code** select kar sakte hain agar use karte hain

3. **PATH Environment:**
   - ✅ **"Git from the command line and also from 3rd-party software"** (Recommended)
   - Yeh option select karein taaki PowerShell me `git` command kaam kare

4. **HTTPS Transport:**
   - ✅ **"Use the OpenSSL library"** (Default)

5. **Line Ending Conversions:**
   - ✅ **"Checkout Windows-style, commit Unix-style line endings"** (Default)

6. **Terminal Emulator:**
   - ✅ **"Use Windows' default console window"** (Default)

7. **Default Behavior:**
   - ✅ **"Default (fast-forward or merge)"**
   - ✅ **"Git Credential Manager"**

8. **Extra Options:**
   - ✅ **"Enable file system caching"**

9. **Experimental Options:**
   - Kuch bhi select karne ki zarurat nahi

10. **"Install"** button click karein

11. Installation complete hone tak wait karein (2-3 minutes)

12. **"Finish"** click karein

---

## ✅ Step 3: Git Verify Karein

### **Option A: PowerShell me Check Karein**

1. **New PowerShell window** kholo (purani close karke nayi kholo - important!)
2. Type karein:
   ```powershell
   git --version
   ```
3. Agar version number dikhe (jaise `git version 2.42.0`), to Git successfully install ho gaya! ✅

### **Option B: Git Bash me Check Karein**

1. **Start Menu** me **"Git Bash"** search karein
2. Open karein
3. Type karein:
   ```bash
   git --version
   ```

---

## 🔄 Step 4: PowerShell Restart Karein

**Important:** Agar PowerShell already open hai, to:
1. **Close karein** current PowerShell window
2. **Nayi PowerShell window** kholo
3. Ab `git` command kaam karega!

---

## 🎯 Step 5: Git Configure Karein (Pehli Baar)

Git install hone ke baad, apna naam aur email set karein:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Example:**
```powershell
git config --global user.name "Modern Tech"
git config --global user.email "your-email@gmail.com"
```

---

## 🚀 Step 6: Ab GitHub Setup Continue Karein

Git install ho gaya! Ab `GITHUB_SETUP.md` follow karein:

1. `cd web_app` folder me jao
2. `git init` run karein
3. Files add karein
4. GitHub pe push karein

---

## ❌ Agar Abhi Bhi Error Aaye

### **Problem: "git is not recognized"**

**Solutions:**

1. **PowerShell restart karein** (close aur nayi kholo)
2. **System restart** karein (agar zarurat ho)
3. **PATH check karein:**
   - `C:\Program Files\Git\cmd` PATH me hona chahiye
   - Usually Git installer automatically add kar deta hai

4. **Manual PATH add karein (agar zarurat ho):**
   - Windows Search me **"Environment Variables"** search karein
   - **"Edit the system environment variables"** open karein
   - **"Environment Variables"** button click karein
   - **"Path"** select karein → **"Edit"**
   - **"New"** click karein
   - Add karein: `C:\Program Files\Git\cmd`
   - **"OK"** sab jagah
   - PowerShell restart karein

---

## 🎉 Success!

Ab Git install ho gaya hai! Ab aap GitHub pe code push kar sakte hain! 🚀

**Next:** `GITHUB_SETUP.md` follow karein!

