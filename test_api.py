"""
Test script for Sleep Disorder Prediction API
Run this to verify your API is working correctly
"""

import requests
import json
from typing import Dict, Any

# Change this to your API URL
# For local testing: "http://localhost:8000"
# For deployed API: "https://your-app.onrender.com"
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint...")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("model_loaded"):
                print("✅ Health check passed - Model is loaded")
                return True
            else:
                print("⚠️  Warning: API is running but model is not loaded")
                return False
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_options():
    """Test the get options endpoint"""
    print("\n" + "="*60)
    print("Testing Get Options Endpoint...")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/options")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nAvailable Options:")
            print(f"  Genders: {data.get('gender', [])}")
            print(f"  Occupations: {len(data.get('occupation', []))} options")
            print(f"  BMI Categories: {data.get('bmi_category', [])}")
            print(f"  Sleep Disorders: {data.get('sleep_disorders', [])}")
            print("✅ Options endpoint working")
            return True, data
        else:
            print("❌ Options endpoint failed")
            return False, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_prediction(sample_data: Dict[str, Any]):
    """Test the prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Prediction Endpoint...")
    print("="*60)
    
    print("\nInput Data:")
    print(json.dumps(sample_data, indent=2))
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/predict",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\nPrediction Result:")
            print(f"  Prediction: {result.get('prediction')}")
            print(f"  Confidence: {result.get('confidence')}%")
            print(f"  Message: {result.get('message')}")
            print("✅ Prediction endpoint working")
            return True
        else:
            print(f"❌ Prediction failed")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("SLEEP DISORDER PREDICTION API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {API_BASE_URL}")
    
    # Test 1: Health Check
    health_ok = test_health_check()
    
    if not health_ok:
        print("\n❌ API is not responding or model is not loaded.")
        print("Make sure to:")
        print("  1. Run 'python app.py' to generate the model file")
        print("  2. Run 'python api.py' to start the API server")
        return
    
    # Test 2: Get Options
    options_ok, options = test_get_options()
    
    # Test 3: Prediction with sample data
    sample_data = {
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
    
    prediction_ok = test_prediction(sample_data)
    
    # Test 4: Another prediction with different parameters
    print("\n" + "="*60)
    print("Testing with High Risk Parameters...")
    print("="*60)
    
    high_risk_data = {
        "gender": "Female",
        "age": 45,
        "occupation": "Nurse",
        "sleep_duration": 5.0,
        "quality_of_sleep": 4,
        "physical_activity_level": 3,
        "stress_level": 9,
        "bmi_category": "Overweight",
        "heart_rate": 90,
        "daily_steps": 3000,
        "systolic_bp": 140,
        "diastolic_bp": 95
    }
    
    test_prediction(high_risk_data)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Health Check: {'✅ PASSED' if health_ok else '❌ FAILED'}")
    print(f"Get Options: {'✅ PASSED' if options_ok else '❌ FAILED'}")
    print(f"Prediction: {'✅ PASSED' if prediction_ok else '❌ FAILED'}")
    
    if health_ok and options_ok and prediction_ok:
        print("\n🎉 All tests passed! Your API is ready to use.")
        print("\nNext steps:")
        print("  1. Deploy to Render (see QUICKSTART.md)")
        print("  2. Update Android app with API URL")
        print("  3. Test from Android app")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    # You can change the API_BASE_URL at the top of this file
    # or pass it as a command line argument
    import sys
    if len(sys.argv) > 1:
        API_BASE_URL = sys.argv[1]
    
    run_all_tests()
