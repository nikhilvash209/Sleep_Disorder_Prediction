# 🚀 Quick Reference Card

## 📋 Before You Start
- [ ] Model file exists: `sleepdisordermodel.pkl` ✅ (Already exists)
- [ ] Python 3.11+ installed
- [ ] pip installed

## 🔧 Local Testing (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run API
python api.py

# 3. Test API (in another terminal)
python test_api.py

# 4. Open browser
# http://localhost:8000/docs
```

## ☁️ Deploy to Render (5 minutes)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Add FastAPI backend"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

Then on https://render.com:
1. New Web Service
2. Connect GitHub repo  
3. Name: `sleep-disorder-api`
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn api:app --host 0.0.0.0 --port $PORT`
6. Deploy ✓

Your API: `https://sleep-disorder-api.onrender.com`

## 📱 Android Setup (10 minutes)

### 1. Add to `build.gradle`:
```gradle
implementation 'com.squareup.retrofit2:retrofit:2.9.0'
implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
implementation 'com.squareup.okhttp3:logging-interceptor:4.10.0'
implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1'
implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2'
```

### 2. Add to `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### 3. Copy code from:
- `AndroidIntegration.kt` → Your project
- Update `BASE_URL` with your API URL

### 4. Copy layout from:
- `android_layout_example.xml` → `res/layout/activity_main.xml`

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/api/options` | GET | Get dropdown values |
| `/api/predict` | POST | Make prediction |

## 🧪 Test with curl

```bash
# Health check
curl https://your-api.onrender.com/

# Get options
curl https://your-api.onrender.com/api/options

# Predict
curl -X POST https://your-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"gender":"Male","age":30,"occupation":"Software Engineer","sleep_duration":7.5,"quality_of_sleep":8,"physical_activity_level":6,"stress_level":5,"bmi_category":"Normal","heart_rate":75,"daily_steps":8000,"systolic_bp":120,"diastolic_bp":80}'
```

## 📊 Model Input Parameters

| Parameter | Type | Range | Example |
|-----------|------|-------|---------|
| gender | string | Male/Female | "Male" |
| age | int | 10-100 | 30 |
| occupation | string | Various | "Software Engineer" |
| sleep_duration | float | 0-12 | 7.5 |
| quality_of_sleep | int | 1-10 | 8 |
| physical_activity_level | int | 1-10 | 6 |
| stress_level | int | 1-10 | 5 |
| bmi_category | string | Normal/Overweight/Obese | "Normal" |
| heart_rate | int | 40-150 | 75 |
| daily_steps | int | 0-50000 | 8000 |
| systolic_bp | int | 90-200 | 120 |
| diastolic_bp | int | 60-130 | 80 |

## 🆘 Common Issues

### "Model not loaded"
```bash
python app.py  # Regenerate model file
```

### Android can't connect
- Local testing: Use `http://10.0.2.2:8000/` for emulator
- Local testing: Use `http://YOUR_IP:8000/` for physical device
- Production: Use `https://your-api.onrender.com/`

### Render deployment fails
- Check model file is committed to git
- Verify requirements.txt is complete
- Check build logs on Render dashboard

## 📚 Documentation

- `README.md` - Project overview
- `API_README.md` - Complete API documentation
- `QUICKSTART.md` - Detailed deployment guide
- `SETUP_SUMMARY.md` - Setup checklist
- `AndroidIntegration.kt` - Android code
- `android_layout_example.xml` - Android UI

## 🎯 Your URLs

Once deployed, save these:
- API Base: `https://your-api.onrender.com`
- API Docs: `https://your-api.onrender.com/docs`
- Health: `https://your-api.onrender.com/`
- Predict: `https://your-api.onrender.com/api/predict`

## ✅ Checklist

- [ ] Model trained (`sleepdisordermodel.pkl` exists) ✅
- [ ] API runs locally
- [ ] Test script passes
- [ ] Code pushed to GitHub
- [ ] API deployed to Render
- [ ] Android dependencies added
- [ ] Android code copied
- [ ] BASE_URL updated in Android
- [ ] App tested with API

## 💡 Pro Tips

1. **Free Tier Sleep**: Render free tier sleeps after 15 min → first request slow
2. **Testing**: Use `/docs` endpoint for interactive API testing
3. **Monitoring**: Check Render dashboard for logs and metrics
4. **Security**: Add authentication before going to production
5. **Backup**: Save your API URL and keep documentation handy

---

**Need Help?** Check the detailed documentation files or run `python test_api.py` to diagnose issues.
