Sleep Disorder Prediction Model
This project implements a machine learning model to predict sleep disorders based on health and lifestyle data. The predictive model is built using a Decision Tree classifier trained on a comprehensive sleep health dataset.

## 🔐 Authentication

The app now includes **Supabase Authentication** with the following features:
- **Email & Password Login** - Traditional authentication
- **Email & Password Sign Up** - Create new accounts with email verification

Features
🔒 Secure authentication using Supabase

User-friendly Streamlit web interface for inputting health and lifestyle parameters.

Uses real-world data with features including age, gender, occupation, sleep duration, physical activity, stress level, BMI category, heart rate, blood pressure, and daily steps.

Preprocessing steps including label encoding of categorical variables.

Robust Decision Tree classifier with model evaluation metrics.

Predicts sleep disorders such as Sleep Apnea and others.

Model and encoders saved for efficient deployment.

Installation

### 1. Clone the repository

### 2. Ensure Python 3.8+ is installed

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up Supabase Authentication

1. **Create a Supabase project** (if you don't have one):
   - Go to [https://supabase.com](https://supabase.com)
   - Click "Start your project"
   - Create a new project

2. **Get your Supabase credentials**:
   - In your Supabase project dashboard, go to **Settings** → **API**
   - Copy the **Project URL** and **anon/public key**

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your Supabase credentials:
     ```
     SUPABASE_URL=https://your-project-id.supabase.co
     SUPABASE_KEY=your-anon-public-key-here
     ```

4. **Enable Email Authentication in Supabase**:
   - In your Supabase dashboard, go to **Authentication** → **Providers**
   - Ensure **Email** is enabled
   - Configure email templates if desired (optional)

The requirements.txt includes:

```
pandas
numpy
scikit-learn
seaborn
matplotlib
joblib
streamlit
supabase
python-dotenv
```
Usage

### 1. Place the dataset
Ensure `Sleep_health_and_lifestyle_dataset.csv` is in the project directory.

### 2. Run the Streamlit app

```bash
streamlit run app.py
```

### 3. Authenticate

The app will show a login screen with two tabs:
- **Login with Password**: Enter your email and password
- **Sign Up**: Create a new account (verification email will be sent)

### 4. Make Predictions

After successful authentication, you can:
- Input your health and lifestyle data
- Click **Predict Sleep Disorder** to view predictions
- Logout using the button in the top-right corner

## Authentication Methods

### Email & Password Login
- Traditional username/password authentication
- Secure password storage via Supabase
- Email verification on sign up

Project Structure
sleep_disorder_train.py: Script to load data, preprocess, train model, and save the model/encoders.

app.py: Streamlit app script to provide a user interface for prediction.

Sleephealthandlifestyledataset.csv: Dataset file (not included in repo).

sleepdisordermodel.pkl: Saved model and LabelEncoders file.

requirements.txt: Python dependencies.

## 🔒 Session Persistence

The app now includes **automatic session persistence**:
- ✅ Stay logged in after page refresh
- ✅ Secure session management via Supabase
- ✅ No need to login again unless you logout
- ✅ Works across browser tabs

## 📱 Converting to Android App

Want to use this as a mobile app? See the comprehensive guide:
- **[ANDROID_CONVERSION_GUIDE.md](ANDROID_CONVERSION_GUIDE.md)** - Complete instructions for converting to APK

**Quick Options:**
1. **PWA (Easiest)**: Add to home screen from mobile browser
2. **Web2APK**: Generate APK using online tools like https://website2apk.online
3. **Android Studio**: Build native WebView app with full customization

## 🛡️ Security Features

- 🔐 Supabase authentication with email verification
- 🔑 Secure credential management via environment variables
- 🔄 Persistent sessions with automatic recovery
- 🚫 Protected routes (login required for predictions)

## 📁 Project Structure

```
Sleep_Disorder_Prediction/
├── app.py                          # Main Streamlit app with auth
├── requirements.txt                # Python dependencies
├── .env                           # Supabase credentials (not in git)
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore file
├── setup.bat                      # Windows quick setup script
├── README.md                      # This file
├── ANDROID_CONVERSION_GUIDE.md    # Android APK conversion guide
├── sleepdisordermodel.pkl         # Trained ML model
└── Sleep_health_and_lifestyle_dataset.csv
```

## 🚀 Quick Setup

**Windows Users:**
```cmd
setup.bat
```

**Manual Setup:**
```bash
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your Supabase credentials
streamlit run app.py
```

## Acknowledgments
This project uses open-source libraries such as scikit-learn, Streamlit, and Supabase for building the machine learning model, web interface, and authentication system.