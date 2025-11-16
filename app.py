import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# --- Initialize Supabase Client ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in .env file")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Data Load ---
df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
print("Dataset shape:", df.shape)
print(df.head())

# --- Data Preprocessing ---
# Fill missing Sleep Disorder values with None
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')

# Drop Person ID
df = df.drop('Person ID', axis=1)

# Split Blood Pressure into SystolicBP and DiastolicBP
bp_split = df['Blood Pressure'].str.split('/', expand=True).astype(int)
df['SystolicBP'], df['DiastolicBP'] = bp_split[0], bp_split[1]
df = df.drop('Blood Pressure', axis=1)

print(df.info())

# --- Encode Categorical Variables ---
categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"{col} classes: {le.classes_}")

print(df.head())

# --- Train-Test Split ---
X = df.drop('Sleep Disorder', axis=1)
y = df['Sleep Disorder']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("Training set size:", X_train.shape)
print("Test set size:", X_test.shape)

# --- Train Decision Tree Model ---
model = DecisionTreeClassifier(max_depth=5, min_samples_split=2, min_samples_leaf=2, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully!")

# --- Model Evaluation ---
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoders['Sleep Disorder'].classes_))

# --- Save model and encoders ---
model_data = {
    'model': model,
    'label_encoders': label_encoders,
    'feature_names': list(X.columns)
}
joblib.dump(model_data, 'sleepdisordermodel.pkl')
print("Model saved successfully as sleepdisordermodel.pkl")

# --- Streamlit App ---

st.set_page_config(
    page_title="Sleep Disorder Predictor", 
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fix scrolling and UI issues with custom CSS
st.markdown("""
<style>
    /* Fix scrolling issues */
    .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        padding-bottom: 2rem;
        overflow-y: auto;
    }
    
    /* Ensure proper scrolling */
    section[data-testid="stAppViewContainer"] {
        overflow-y: auto;
        height: 100vh;
    }
    
    /* Fix header padding */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Better button styling */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Better input styling */
    .stTextInput input, .stSelectbox select {
        border-radius: 8px;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Fix slider labels */
    .stSlider {
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Authentication Functions ---

def init_session_state():
    """Initialize session state variables and check for existing session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'session_checked' not in st.session_state:
        st.session_state.session_checked = False
    if 'verification_success' not in st.session_state:
        st.session_state.verification_success = False
    
    # Check for existing Supabase session on first load
    if not st.session_state.session_checked:
        try:
            session = supabase.auth.get_session()
            if session and session.user:
                st.session_state.authenticated = True
                st.session_state.user = session.user
                # Check if user just verified email
                if session.user.email_confirmed_at and not st.session_state.get('verified_shown', False):
                    st.session_state.verification_success = True
                    st.session_state.verified_shown = True
        except Exception as e:
            pass  # No valid session
        st.session_state.session_checked = True

def sign_up_with_password(email, password):
    """Sign up a new user with email and password"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if response.user:
            return True, "Account created successfully! Please check your email to verify your account."
        return False, "Sign up failed. Please try again."
    except Exception as e:
        return False, f"Error: {str(e)}"

def sign_in_with_password(email, password):
    """Sign in with email and password"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user and response.session:
            st.session_state.authenticated = True
            st.session_state.user = response.user
            # Session is automatically stored by Supabase client
            return True, "Login successful!"
        return False, "Invalid credentials"
    except Exception as e:
        return False, f"Error: {str(e)}"

def sign_out():
    """Sign out the current user"""
    try:
        supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.session_checked = False
        st.rerun()
    except Exception as e:
        st.error(f"Error signing out: {str(e)}")

def authentication_ui():
    """Display authentication UI"""
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("😴 Sleep Disorder Predictor")
        st.markdown("### 🔐 Welcome! Please login to continue")
        
        # Show verification success message if redirected from email
        if st.session_state.verification_success:
            st.success("✅ Email verified successfully! You can now log in.")
            st.session_state.verification_success = False
        
        st.markdown("")  # Spacing
        
        # Create tabs for different auth methods
        tab1, tab2 = st.tabs(["🔑 Login", "✨ Sign Up"])
        
        with tab1:
            st.markdown("#### Login with Email & Password")
            email = st.text_input("📧 Email Address", key="login_email", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")
            
            st.markdown("")  # Spacing
            if st.button("🚀 Login", key="login_btn", use_container_width=True):
                if email and password:
                    with st.spinner("Logging in..."):
                        success, message = sign_in_with_password(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("⚠️ Please enter both email and password")
        
        with tab2:
            st.markdown("#### Create New Account")
            signup_email = st.text_input("📧 Email Address", key="signup_email", placeholder="your.email@example.com")
            signup_password = st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Minimum 6 characters")
            signup_password_confirm = st.text_input("🔒 Confirm Password", type="password", key="signup_password_confirm", placeholder="Re-enter password")
            
            st.markdown("")  # Spacing
            if st.button("✨ Create Account", key="signup_btn", use_container_width=True):
                if signup_email and signup_password and signup_password_confirm:
                    if signup_password != signup_password_confirm:
                        st.error("❌ Passwords do not match!")
                    elif len(signup_password) < 6:
                        st.error("❌ Password must be at least 6 characters long")
                    else:
                        with st.spinner("Creating account..."):
                            success, message = sign_up_with_password(signup_email, signup_password)
                        if success:
                            st.success(message)
                            st.info("📧 Please check your email to verify your account before logging in.")
                        else:
                            st.error(message)
                else:
                    st.warning("⚠️ Please fill in all fields")

def encode_input(inputs, label_encoders):
    # Replace "" with default 'unknown' encoding: here 0 for simplicity
    for col, le in label_encoders.items():
        if col in inputs:
            val = inputs[col]
            if val == "" or val not in le.classes_:
                inputs[col] = 0
            else:
                inputs[col] = le.transform([val])[0]
    return inputs

def sleep_disorder_prediction_ui():
    # Display user info and logout button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("😴 Sleep Disorder Prediction")
        if st.session_state.user:
            st.caption(f"👤 Logged in as: {st.session_state.user.email}")
    with col2:
        st.write("")  # Spacing
        if st.button("🚪 Logout", key="logout_btn"):
            sign_out()
    
    st.markdown("---")
    
    # Organize inputs in sections with columns
    st.subheader("📋 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Select Gender"] + list(label_encoders['Gender'].classes_), index=0)
        age = st.slider("Age", 10, 100, 30)
    with col2:
        occupation = st.selectbox("Occupation", ["Select Occupation"] + list(label_encoders['Occupation'].classes_), index=0)
        bmi_category = st.selectbox("BMI Category", ["Select BMI Category"] + list(label_encoders['BMI Category'].classes_), index=0)
    
    st.markdown("---")
    st.subheader("😴 Sleep & Lifestyle")
    col1, col2 = st.columns(2)
    with col1:
        sleep_duration = st.slider("Sleep Duration (hours)", 0.0, 12.0, 7.0, step=0.1)
        quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 5)
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
    with col2:
        physical_activity_level = st.slider("Physical Activity Level (1-10)", 1, 10, 5)
        daily_steps = st.slider("Daily Steps", 0, 20000, 5000, step=100)
    
    st.markdown("---")
    st.subheader("❤️ Health Metrics")
    col1, col2 = st.columns(2)
    with col1:
        heart_rate = st.slider("Heart Rate (bpm)", 40, 150, 75)
        systolic_bp = st.slider("Systolic Blood Pressure (mmHg)", 90, 180, 120)
    with col2:
        diastolic_bp = st.slider("Diastolic Blood Pressure (mmHg)", 60, 120, 80)

    user_inputs = {
        "Gender": gender,
        "Age": age,
        "Occupation": occupation,
        "Sleep Duration": sleep_duration,
        "Quality of Sleep": quality_of_sleep,
        "Physical Activity Level": physical_activity_level,
        "Stress Level": stress_level,
        "BMI Category": bmi_category,
        "Heart Rate": heart_rate,
        "Daily Steps": daily_steps,
        "SystolicBP": systolic_bp,
        "DiastolicBP": diastolic_bp
    }

    encoded_inputs = encode_input(user_inputs.copy(), label_encoders)

    input_df = pd.DataFrame([encoded_inputs], columns=model_data['feature_names'])

    st.markdown("---")
    
    # Center the predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_btn = st.button("🔮 Predict Sleep Disorder", key="predict_btn", use_container_width=True)
    
    if predict_btn:
        with st.spinner("Analyzing your data..."):
            prediction = model.predict(input_df)[0]
            pred_label = label_encoders['Sleep Disorder'].inverse_transform([prediction])[0]
        
        st.markdown("---")
        st.subheader("📊 Prediction Result")
        
        # Display result with better formatting
        if pred_label == "None":
            st.success(f"✅ **Result:** No sleep disorder detected")
            st.info("💡 Continue maintaining your healthy sleep habits!")
        else:
            st.warning(f"⚠️ **Result:** {pred_label} detected")
            st.info("💡 Consider consulting a healthcare professional for proper diagnosis and treatment.")

if __name__ == "__main__":
    # Initialize session state
    init_session_state()
    
    # Check authentication status
    if not st.session_state.authenticated:
        authentication_ui()
    else:
        sleep_disorder_prediction_ui()
