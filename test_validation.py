"""
Simple test to see what's going wrong with validation
"""
import requests
import json

API_URL = "http://localhost:8000"

print("="*60)
print("TESTING API VALIDATION")
print("="*60)

# First, get the valid options
print("\n1. Getting valid options from API...")
try:
    response = requests.get(f"{API_URL}/api/options")
    if response.status_code == 200:
        options = response.json()
        print("✅ Options retrieved successfully!")
        print(f"\nValid Genders: {options['gender']}")
        print(f"Valid Occupations: {options['occupation']}")
        print(f"Valid BMI Categories: {options['bmi_category']}")
        
        # Use the FIRST occupation from the list
        first_occupation = options['occupation'][0]
        print(f"\n📌 Will use occupation: '{first_occupation}'")
    else:
        print(f"❌ Failed to get options: {response.status_code}")
        print(response.text)
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test with minimal valid data
print("\n" + "="*60)
print("2. Testing prediction with valid data...")
print("="*60)

test_data = {
    "gender": "Male",
    "age": 30,
    "occupation": first_occupation,  # Use actual occupation from model
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

print("\nRequest data:")
print(json.dumps(test_data, indent=2))

try:
    response = requests.post(
        f"{API_URL}/api/predict",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS!")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Message: {result['message']}")
    else:
        print("\n❌ FAILED!")
        print("Response:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)
            
except Exception as e:
    print(f"❌ Error: {e}")

# Try with different data types to identify the issue
print("\n" + "="*60)
print("3. Testing with edge cases...")
print("="*60)

# Test case 1: All strings (common mistake)
print("\n📋 Test Case 1: All values as strings (wrong)")
bad_data_1 = {
    "gender": "Male",
    "age": "30",  # String instead of int
    "occupation": first_occupation,
    "sleep_duration": "7.5",  # String instead of float
    "quality_of_sleep": "8",  # String instead of int
    "physical_activity_level": "6",
    "stress_level": "5",
    "bmi_category": "Normal",
    "heart_rate": "75",
    "daily_steps": "8000",
    "systolic_bp": "120",
    "diastolic_bp": "80"
}

response = requests.post(f"{API_URL}/api/predict", json=bad_data_1)
print(f"Status: {response.status_code}")
if response.status_code != 200:
    print("Expected to fail - string values where numbers needed")

# Test case 2: Out of range
print("\n📋 Test Case 2: Out of range values")
bad_data_2 = test_data.copy()
bad_data_2["age"] = 200  # Out of range

response = requests.post(f"{API_URL}/api/predict", json=bad_data_2)
print(f"Status: {response.status_code}")
if response.status_code != 200:
    print("Expected to fail - age out of range")

# Test case 3: Wrong occupation
print("\n📋 Test Case 3: Invalid occupation")
bad_data_3 = test_data.copy()
bad_data_3["occupation"] = "Astronaut"  # Not in training data

response = requests.post(f"{API_URL}/api/predict", json=bad_data_3)
print(f"Status: {response.status_code}")
if response.status_code != 200:
    try:
        error = response.json()
        print("Expected to fail:")
        print(error.get('detail', response.text))
    except:
        print(response.text)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("If Test Case 1 (all strings) passes, that's your issue!")
print("If Test Case 2 fails properly, validation is working")
print("If Test Case 3 fails with helpful error, API is good")
print("="*60)
