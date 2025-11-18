# Sleep Disorder Prediction Model

This project implements a machine learning model to predict sleep disorders based on health and lifestyle data. The predictive model is built using a Decision Tree classifier trained on a comprehensive sleep health dataset.

## 🌟 Features

- **Streamlit Web Interface**: User-friendly interface for testing predictions
- **FastAPI REST API**: Production-ready API for mobile/web app integration
- **Android Integration**: Complete example code for native Android apps
- **Robust ML Model**: Decision Tree classifier with comprehensive evaluation
- **Cloud Deployment Ready**: Configuration files for Render, Railway, and Back4App
- **Real-world Data**: Features include age, gender, occupation, sleep duration, physical activity, stress level, BMI category, heart rate, blood pressure, and daily steps

## 📊 Predicted Conditions

- **None** - No sleep disorder detected
- **Sleep Apnea** - Breathing interruptions during sleep
- **Insomnia** - Difficulty falling or staying asleep

## 🚀 Quick Start

### Option 1: Streamlit Web App (Testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

### Option 2: FastAPI REST API (Production)

```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
python api.py

# Test the API
python test_api.py
```

Visit http://localhost:8000/docs for interactive API documentation.

## 📱 Android Integration

This project includes complete Android integration with Retrofit. See:
- `AndroidIntegration.kt` - Complete Android code with Retrofit
- `android_layout_example.xml` - Example UI layout
- `API_README.md` - Detailed API documentation

## 🌐 Deployment

### Deploy to Render (Recommended - Free)

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push -u origin main

# On Render.com:
# 1. New Web Service
# 2. Connect GitHub repo
# 3. Auto-deploy
```

See `QUICKSTART.md` for detailed deployment instructions.

## 📁 Project Structure

```
├── app.py                          # Streamlit web interface
├── api.py                          # FastAPI REST API
├── sleep_prediction.ipynb          # Model training notebook
├── sleepdisordermodel.pkl          # Trained model file
├── Sleep_health_and_lifestyle_dataset.csv  # Training data
├── requirements.txt                # Python dependencies
├── test_api.py                     # API testing script
├── Procfile                        # Render deployment config
├── runtime.txt                     # Python version specification
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── API_README.md                   # Complete API documentation
├── QUICKSTART.md                   # Quick deployment guide
├── SETUP_SUMMARY.md                # Setup summary and checklist
├── AndroidIntegration.kt           # Android code examples
└── android_layout_example.xml      # Android UI layout
```

## 🛠️ Technology Stack

### Machine Learning
- **scikit-learn** - Decision Tree Classifier
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **joblib** - Model serialization

### Backend
- **FastAPI** - Modern API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Streamlit** - Web interface

### Android (Example Code Provided)
- **Retrofit** - HTTP client
- **Kotlin Coroutines** - Async operations
- **ViewModel & LiveData** - Architecture components

## 📖 API Endpoints

### Health Check
```
GET /
```
Returns API status and version

### Get Options
```
GET /api/options
```
Returns valid values for dropdowns (gender, occupation, BMI, etc.)

### Predict Sleep Disorder
```
POST /api/predict
```
Request body:
```json
{
  "gender": "Male",
  "age": 30,
  "occupation": "Software Engineer",
  "sleep_duration": 7.5,
  "quality_of_sleep": 8,
  "physical_activity_level": 6,
  "stress_level": 5,
  "bmi_category": "Normal",
  "heart_rate": 75,
  "daily_steps": 8000,
  "systolic_bp": 120,
  "diastolic_bp": 80
}
```

Response:
```json
{
  "prediction": "None",
  "confidence": 95.67,
  "message": "No sleep disorder detected. Maintain healthy lifestyle habits!"
}
```

## 🧪 Testing

### Test API Locally
```bash
python test_api.py
```

### Test with curl
```bash
curl http://localhost:8000/
curl http://localhost:8000/api/options
curl -X POST http://localhost:8000/api/predict -H "Content-Type: application/json" -d '{"gender":"Male","age":30,...}'
```

### Interactive Testing
Visit http://localhost:8000/docs for Swagger UI

## 📚 Documentation

- **`API_README.md`** - Complete API documentation with Android integration guide
- **`QUICKSTART.md`** - Quick deployment guide for Render, Railway, and Back4App
- **`SETUP_SUMMARY.md`** - Complete setup summary and troubleshooting
- **`AndroidIntegration.kt`** - Full Android implementation example
- **`android_layout_example.xml`** - Android UI layout example

## 🔒 Security Considerations

For production deployment:
- Add authentication (API keys, JWT tokens)
- Enable rate limiting
- Use HTTPS only
- Restrict CORS to specific domains
- Implement input sanitization
- Monitor API usage and errors

## 💡 Use Cases

1. **Mobile Health Apps** - Integrate prediction into fitness/health tracking apps
2. **Clinical Tools** - Screening tool for healthcare professionals
3. **Wellness Platforms** - Add sleep disorder assessment to wellness programs
4. **Research** - Collect and analyze sleep health data

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is for educational purposes.

## 🎓 Acknowledgments

This project uses open-source libraries including:
- scikit-learn for machine learning
- FastAPI for the REST API
- Streamlit for the web interface
- Retrofit for Android integration examples