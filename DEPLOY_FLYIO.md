# 🚀 Fly.io pe Backend Deploy Karne ka Guide (Free, No Card!)

Fly.io free tier me card ki zarurat nahi hai! Perfect alternative hai Render ka.

---

## 📋 Step 1: Fly.io Account Banao

1. https://fly.io pe jao
2. **"Sign Up"** click karein
3. GitHub se sign in karein (free hai!)
4. **No credit card required!** ✅

---

## 📋 Step 2: Fly.io CLI Install Karein

### **Windows:**

1. PowerShell me yeh command run karein:
   ```powershell
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. Ya manually download karein:
   - https://fly.io/docs/hands-on/install-flyctl/
   - Windows installer download karein

3. Install hone ke baad PowerShell restart karein

4. Verify karein:
   ```powershell
   flyctl version
   ```

---

## 📋 Step 3: Fly.io Login Karein

```powershell
flyctl auth login
```

Browser automatically open hoga, GitHub se login karein.

---

## 📋 Step 4: Fly.io App Initialize Karein

Project folder me jao aur initialize karein:

```powershell
cd "C:\Users\Modern Tech\Downloads\KivyDownloaderApp\KivyDownloaderApp\web_app"
flyctl launch
```

**Prompts:**
- App name: `zkdownloader-backend` (ya kuch bhi)
- Region: `iad` (Washington DC) ya apne paas wala
- PostgreSQL: `No` (zarurat nahi)
- Redis: `No` (zarurat nahi)

---

## 📋 Step 5: fly.toml Configure Karein

`fly.toml` file automatically generate hogi. Isko update karein:

```toml
app = "zkdownloader-backend"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[services]]
  http_checks = []
  internal_port = 5000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

    [services.concurrency]
      hard_limit = 25
      soft_limit = 20
      type = "connections"

    [[services.ports]]
      force_https = true
      handlers = ["http"]
      port = 80

    [[services.ports]]
      handlers = ["tls", "http"]
      port = 443

    [[services.tcp_checks]]
      grace_period = "1s"
      interval = "15s"
      restart_limit = 0
      timeout = "2s"
```

**Important:** `internal_port` ko `5000` rakhein (Flask default port).

---

## 📋 Step 6: backend.py Update Karein

`backend.py` me PORT environment variable check karein. Agar nahi hai to add karein:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Note:** Already hai to kuch change karne ki zarurat nahi!

---

## 📋 Step 7: Deploy Karein

```powershell
flyctl deploy
```

Build process start ho jayega. 5-10 minutes wait karein.

---

## 📋 Step 8: App URL Note Karein

Deploy complete hone ke baad:

```powershell
flyctl status
```

Ya dashboard me: https://fly.io/dashboard

URL mil jayega: `https://zkdownloader-backend.fly.dev`

---

## 📋 Step 9: Frontend me Backend URL Update Karein

`app.js` me line 29 pe backend URL update karein:

```javascript
return 'https://zkdownloader-backend.fly.dev'; // Apna Fly.io URL
```

---

## ✅ Benefits

- ✅ **Free tier** - no credit card needed
- ✅ **No sleep** - always running (free tier me bhi!)
- ✅ **Fast deployment**
- ✅ **Global edge network**
- ✅ **Auto HTTPS**

---

## 🔧 Troubleshooting

### **Problem: flyctl command not found**

**Solution:**
- PowerShell restart karein
- Ya PATH me manually add karein

### **Problem: Build fails**

**Solution:**
- `requirements.txt` check karein
- Logs dekhne ke liye: `flyctl logs`

### **Problem: App not starting**

**Solution:**
- `fly.toml` me `internal_port` sahi hai ya nahi check karein
- `backend.py` me `host='0.0.0.0'` hai ya nahi verify karein

---

## 🎉 Success!

Ab backend Fly.io pe hai - **completely free, no card needed!** 🚀

