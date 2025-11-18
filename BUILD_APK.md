# Build Android APK for ZKDownloader

## Prerequisites
- **Node.js** (v16+): https://nodejs.org/
- **Java JDK 11+**: https://www.oracle.com/java/technologies/downloads/
- **Android SDK**: Install via Android Studio https://developer.android.com/studio
- **Git** (already have)

## Steps to Build APK

### 1. Install Capacitor CLI
```bash
npm install -g @capacitor/cli
```

### 2. Initialize Capacitor (from web_app folder)
```bash
cd c:\Users\Modern Tech\Downloads\KivyDownloaderApp\KivyDownloaderApp\web_app
npm install
npx cap init zkdownloader com.zkdownloader.app
```

### 3. Add Android Platform
```bash
npx cap add android
```

### 4. Sync Files
```bash
npx cap sync
```

### 5. Open in Android Studio
```bash
npx cap open android
```

### 6. Build APK in Android Studio
- Android Studio opens automatically
- Wait for Gradle sync to complete
- Click **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
- APK will be generated at: `android/app/build/outputs/apk/debug/app-debug.apk`

### 7. Install on Phone
- Enable **Developer Mode** on Android phone (tap Build Number 7 times in Settings)
- Enable **USB Debugging** in Developer Options
- Connect phone via USB
- In Android Studio: **Run** → **Run 'app'** or drag APK to phone

## Alternative: Use APKsigner for Release APK
```bash
npx cap build android --prod
```

## Troubleshooting
- **Gradle error**: Update Android SDK in Android Studio SDK Manager
- **Java error**: Ensure JAVA_HOME environment variable is set
- **Port issues**: Change `server.url` in capacitor.config.json if needed

## Notes
- App will load from your Railway URL: `https://web-production-cfdd5d.up.railway.app`
- Ensure internet connection on phone for downloads to work
- APK size: ~50-80MB depending on dependencies
