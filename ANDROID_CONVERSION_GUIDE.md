# 📱 Converting Your Streamlit App to Android APK

This guide explains how to convert your Sleep Disorder Prediction web app into an Android application.

## Method 1: Progressive Web App (PWA) - Recommended ⭐

PWAs work on all devices and don't require app store approval.

### Steps:

1. **Deploy your app** (if not already deployed):
   - Push to GitHub
   - Deploy on Streamlit Cloud: https://share.streamlit.io

2. **Add to Android Home Screen**:
   - Open your deployed app in Chrome on Android
   - Tap the **⋮** menu → **Add to Home screen**
   - The app will work like a native app with an icon

### Advantages:
- ✅ No APK building required
- ✅ Works on iOS and Android
- ✅ Instant updates (no app store review)
- ✅ Automatic authentication persistence

---

## Method 2: Web2APK / WebView APK Builder

Convert your web app into a standalone APK file.

### Option A: Using Website 2 APK Builder (Free)

**Tool:** https://website2apk.online or https://appsgeyser.com

**Steps:**

1. **Deploy your Streamlit app** and get the URL:
   ```
   https://your-app-name.streamlit.app
   ```

2. **Go to Website2APK Builder**:
   - Visit https://website2apk.online
   - Or use AppsGeyser: https://appsgeyser.com

3. **Enter your app details**:
   - **Website URL**: Your Streamlit app URL
   - **App Name**: Sleep Disorder Predictor
   - **App Icon**: Upload a 512x512 PNG icon
   - **Package Name**: com.yourname.sleepdisorder

4. **Generate APK**:
   - Click "Create APK"
   - Wait for generation (2-5 minutes)
   - Download the APK file

5. **Test the APK**:
   - Enable "Install from Unknown Sources" on Android
   - Install and test the app

### Option B: Using Android Studio (Advanced)

**Prerequisites:**
- Install Android Studio
- Basic knowledge of Android development

**Steps:**

1. **Create new Android Project**:
   ```
   File → New → New Project → Empty Activity
   ```

2. **Add WebView to layout** (`activity_main.xml`):
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <WebView
       xmlns:android="http://schemas.android.com/apk/res/android"
       android:id="@+id/webview"
       android:layout_width="match_parent"
       android:layout_height="match_parent" />
   ```

3. **Configure MainActivity** (`MainActivity.java`):
   ```java
   import android.webkit.WebView;
   import android.webkit.WebViewClient;
   import android.webkit.WebSettings;

   public class MainActivity extends AppCompatActivity {
       private WebView webView;

       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_main);

           webView = findViewById(R.id.webview);
           webView.setWebViewClient(new WebViewClient());
           
           WebSettings webSettings = webView.getSettings();
           webSettings.setJavaScriptEnabled(true);
           webSettings.setDomStorageEnabled(true);
           
           // Load your Streamlit app
           webView.loadUrl("https://your-app.streamlit.app");
       }

       @Override
       public void onBackPressed() {
           if (webView.canGoBack()) {
               webView.goBack();
           } else {
               super.onBackPressed();
           }
       }
   }
   ```

4. **Add Internet Permission** (`AndroidManifest.xml`):
   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
   ```

5. **Build APK**:
   ```
   Build → Build Bundle(s) / APK(s) → Build APK(s)
   ```

---

## Method 3: Using Capacitor (Professional)

Convert your web app to a native mobile app with full device API access.

### Steps:

1. **Install Capacitor**:
   ```bash
   npm install -g @capacitor/cli @capacitor/core
   ```

2. **Initialize Capacitor**:
   ```bash
   npx cap init
   ```

3. **Add Android platform**:
   ```bash
   npx cap add android
   ```

4. **Configure `capacitor.config.json`**:
   ```json
   {
     "appId": "com.yourname.sleepdisorder",
     "appName": "Sleep Disorder Predictor",
     "webDir": "www",
     "server": {
       "url": "https://your-app.streamlit.app",
       "cleartext": true
     }
   }
   ```

5. **Build for Android**:
   ```bash
   npx cap sync
   npx cap open android
   ```

6. **Build APK in Android Studio**:
   - The Android Studio will open automatically
   - Click **Build → Build Bundle(s) / APK(s) → Build APK(s)**

---

## 🎨 Creating App Icon

Your app needs a proper icon:

### Online Tools:
- **App Icon Generator**: https://appicon.co
- **Icon Kitchen**: https://icon.kitchen

### Requirements:
- Size: 512x512 px
- Format: PNG with transparent background
- Simple, recognizable design

### Quick Icon Idea:
- 😴 Sleep emoji on colored background
- 🏥 Medical cross with sleep symbol
- 📊 Chart/graph representing predictions

---

## ⚙️ Important Configuration

### 1. Update Supabase Settings

In your Supabase dashboard:
- Go to **Authentication → URL Configuration**
- Add your app's redirect URLs:
  ```
  https://your-app.streamlit.app
  capacitor://localhost (for Capacitor apps)
  ```

### 2. Enable CORS

If you face CORS issues, add allowed origins in Supabase:
- Go to **Settings → API**
- Add your APK's domain to allowed origins

### 3. Session Persistence

The updated `app.py` already includes:
- ✅ Automatic session recovery on page load
- ✅ Persistent login across refreshes
- ✅ Secure token storage via Supabase

---

## 📤 Publishing to Google Play Store (Optional)

### Requirements:
- Google Play Developer Account ($25 one-time fee)
- Signed APK (release build)
- App screenshots
- Privacy policy URL

### Steps:
1. Create signed release APK in Android Studio
2. Create developer account: https://play.google.com/console
3. Upload APK and fill app details
4. Submit for review

### Alternative: Direct APK Distribution
- Share APK file directly with users
- Host on your website for download
- No app store approval needed

---

## 🔒 Security Notes

### For APK Distribution:
- ✅ Your Supabase credentials are safe (stored in Streamlit Cloud secrets)
- ✅ Authentication works the same way
- ✅ SSL/HTTPS is maintained through Streamlit's servers

### Best Practices:
- Always use HTTPS for your Streamlit app
- Keep Supabase keys in cloud secrets, not in APK
- Test authentication flow in APK before distribution
- Consider adding biometric login for mobile users

---

## 🆘 Troubleshooting

### App doesn't load:
- Check if your Streamlit app URL is correct
- Ensure the app is publicly accessible
- Test the URL in a mobile browser first

### Authentication doesn't work:
- Add APK URL to Supabase redirect URLs
- Check internet permissions in AndroidManifest.xml
- Enable DOM storage and JavaScript in WebView

### Session not persisting:
- Ensure cookies are enabled in WebView
- Check Supabase session storage settings
- Verify the updated `app.py` is deployed

---

## 📊 Summary Table

| Method | Difficulty | Time | Cost | Best For |
|--------|-----------|------|------|----------|
| PWA | ⭐ Easy | 5 min | Free | Quick deployment, all platforms |
| Web2APK | ⭐⭐ Medium | 15 min | Free | Simple APK, no coding |
| Android Studio | ⭐⭐⭐ Hard | 2 hours | Free | Custom features, full control |
| Capacitor | ⭐⭐⭐ Hard | 3 hours | Free | Professional apps, native APIs |

---

## 🎯 Recommendation

**For quick deployment:** Use PWA method - it's instant and works everywhere.

**For shareable APK:** Use Website2APK - easiest way to create installable app.

**For professional app:** Use Android Studio or Capacitor for full customization.

---

## 📞 Need Help?

- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Supabase Auth: https://supabase.com/docs/guides/auth
- Android WebView: https://developer.android.com/guide/webapps/webview
- Capacitor: https://capacitorjs.com/docs

Your app is now ready to be converted to Android! 🚀
