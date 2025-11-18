from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator, ValidationError
import joblib
import pandas as pd
import numpy as np
from typing import Optional
import os
import json

# Initialize FastAPI app
app = FastAPI(
    title="Sleep Disorder Prediction API",
    description="API for predicting sleep disorders based on health and lifestyle data",
    version="1.0.0"
)

# Enable CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Android app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        error_type = error["type"]
        
        # Make error messages more user-friendly
        if "value_error" in error_type:
            errors.append(f"{field}: {message}")
        else:
            errors.append(f"{field}: {message} (type: {error_type})")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation Error",
            "errors": errors,
            "tip": "Check the /api/options endpoint to see valid values for categorical fields"
        }
    )

# Global variable to store model data
model_data = None

# Load model on startup
@app.on_event("startup")
async def load_model():
    global model_data
    try:
        model_path = 'sleepdisordermodel.pkl'
        if os.path.exists(model_path):
            model_data = joblib.load(model_path)
            print("✅ Model loaded successfully!")
        else:
            print("⚠️ Warning: Model file not found. Please train and save the model first.")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")

# Request model for prediction
class PredictionRequest(BaseModel):
    gender: str = Field(..., description="Gender: Male or Female")
    age: int = Field(..., ge=10, le=100, description="Age between 10 and 100")
    occupation: str = Field(..., description="Occupation type")
    sleep_duration: float = Field(..., ge=0, le=12, description="Sleep duration in hours")
    quality_of_sleep: int = Field(..., ge=1, le=10, description="Quality of sleep rating (1-10)")
    physical_activity_level: int = Field(..., ge=1, le=10, description="Physical activity level (1-10)")
    stress_level: int = Field(..., ge=1, le=10, description="Stress level (1-10)")
    bmi_category: str = Field(..., description="BMI Category: Normal, Overweight, Obese, etc.")
    heart_rate: int = Field(..., ge=40, le=150, description="Heart rate in bpm")
    daily_steps: int = Field(..., ge=0, le=50000, description="Daily steps count")
    systolic_bp: int = Field(..., ge=90, le=200, description="Systolic blood pressure")
    diastolic_bp: int = Field(..., ge=60, le=130, description="Diastolic blood pressure")

    @validator('gender')
    def validate_gender(cls, v):
        # Accept case-insensitive and handle common variations
        if v.lower() not in ['male', 'female', 'm', 'f']:
            raise ValueError('Gender must be either Male or Female')
        # Normalize to title case
        return 'Male' if v.lower() in ['male', 'm'] else 'Female'

    @validator('bmi_category')
    def validate_bmi_category(cls, v):
        # Accept case-insensitive and handle variations
        valid_map = {
            'normal': 'Normal',
            'normal weight': 'Normal Weight',
            'overweight': 'Overweight',
            'obese': 'Obese'
        }
        v_lower = v.lower()
        if v_lower not in valid_map:
            raise ValueError(f'BMI Category must be one of: Normal, Normal Weight, Overweight, or Obese')
        return valid_map[v_lower]

    class Config:
        schema_extra = {
            "example": {
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
        }

# Response model
class PredictionResponse(BaseModel):
    prediction: str
    confidence: Optional[float] = None
    message: str

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Sleep Disorder Prediction API is running",
        "version": "1.0.0",
        "model_loaded": model_data is not None
    }

# Get available options endpoint
@app.get("/api/options", tags=["Info"])
async def get_options():
    """Get available options for categorical fields"""
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    label_encoders = model_data['label_encoders']
    
    return {
        "gender": label_encoders['Gender'].classes_.tolist(),
        "occupation": label_encoders['Occupation'].classes_.tolist(),
        "bmi_category": label_encoders['BMI Category'].classes_.tolist(),
        "sleep_disorders": label_encoders['Sleep Disorder'].classes_.tolist()
    }

# Get example request endpoint
@app.get("/api/example", tags=["Info"])
async def get_example_request():
    """Get an example request with valid data from the model"""
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    label_encoders = model_data['label_encoders']
    
    # Create example with actual valid values from the model
    example = {
        "gender": label_encoders['Gender'].classes_[0],
        "age": 30,
        "occupation": label_encoders['Occupation'].classes_[0],
        "sleep_duration": 7.5,
        "quality_of_sleep": 8,
        "physical_activity_level": 6,
        "stress_level": 5,
        "bmi_category": label_encoders['BMI Category'].classes_[0],
        "heart_rate": 75,
        "daily_steps": 8000,
        "systolic_bp": 120,
        "diastolic_bp": 80
    }
    
    return {
        "message": "Copy this example request to test the API",
        "example_request": example,
        "curl_command": f'curl -X POST http://localhost:8000/api/predict -H "Content-Type: application/json" -d \'{json.dumps(example)}\''
    }

# Prediction endpoint
@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_sleep_disorder(request: PredictionRequest):
    """
    Predict sleep disorder based on health and lifestyle data
    
    Returns the predicted sleep disorder category
    """
    if model_data is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the model file exists."
        )
    
    try:
        # Get model components
        model = model_data['model']
        label_encoders = model_data['label_encoders']
        feature_names = model_data['feature_names']
        
        # Prepare input data
        input_data = {
            "Gender": request.gender,
            "Age": request.age,
            "Occupation": request.occupation,
            "Sleep Duration": request.sleep_duration,
            "Quality of Sleep": request.quality_of_sleep,
            "Physical Activity Level": request.physical_activity_level,
            "Stress Level": request.stress_level,
            "BMI Category": request.bmi_category,
            "Heart Rate": request.heart_rate,
            "Daily Steps": request.daily_steps,
            "SystolicBP": request.systolic_bp,
            "DiastolicBP": request.diastolic_bp
        }
        
        # Encode categorical variables
        encoded_data = input_data.copy()
        for col, le in label_encoders.items():
            if col in encoded_data and col != 'Sleep Disorder':
                try:
                    encoded_data[col] = le.transform([encoded_data[col]])[0]
                except ValueError:
                    # Handle unknown categories
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid value for {col}. Valid values are: {', '.join(le.classes_)}"
                    )
        
        # Create DataFrame for prediction
        input_df = pd.DataFrame([encoded_data], columns=feature_names)
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Decode prediction
        predicted_disorder = label_encoders['Sleep Disorder'].inverse_transform([prediction])[0]
        confidence = float(max(prediction_proba)) * 100
        
        # Generate response message
        if predicted_disorder == "None":
            message = "No sleep disorder detected. Maintain healthy lifestyle habits!"
        else:
            message = f"Potential sleep disorder detected: {predicted_disorder}. Consider consulting a healthcare professional."
        
        return PredictionResponse(
            prediction=predicted_disorder,
            confidence=round(confidence, 2),
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

# Batch prediction endpoint (optional - useful for testing)
@app.post("/api/predict/batch", tags=["Prediction"])
async def predict_batch(requests: list[PredictionRequest]):
    """
    Predict sleep disorders for multiple inputs at once
    """
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for idx, request in enumerate(requests):
        try:
            result = await predict_sleep_disorder(request)
            results.append({"index": idx, "success": True, "result": result})
        except Exception as e:
            results.append({"index": idx, "success": False, "error": str(e)})
    
    return {"predictions": results, "total": len(requests)}

if __name__ == "__main__":
    import uvicorn
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
