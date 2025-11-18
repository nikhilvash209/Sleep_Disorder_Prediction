"""
Debug script to check model expectations and test API validation
"""
import joblib
import json

# Load the model to see what it expects
print("="*60)
print("MODEL EXPECTATIONS")
print("="*60)

model_data = joblib.load('sleepdisordermodel.pkl')

print("\n1. GENDER OPTIONS:")
print(model_data['label_encoders']['Gender'].classes_)

print("\n2. OCCUPATION OPTIONS:")
for i, occ in enumerate(model_data['label_encoders']['Occupation'].classes_):
    print(f"   {i}: {occ}")

print("\n3. BMI CATEGORY OPTIONS:")
print(model_data['label_encoders']['BMI Category'].classes_)

print("\n4. SLEEP DISORDER OPTIONS (Predictions):")
print(model_data['label_encoders']['Sleep Disorder'].classes_)

print("\n5. FEATURE NAMES (in order):")
for i, feat in enumerate(model_data['feature_names']):
    print(f"   {i}: {feat}")

# Create a test request
print("\n" + "="*60)
print("TEST REQUEST")
print("="*60)

test_request = {
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

print("\nTest request (copy this for /docs):")
print(json.dumps(test_request, indent=2))

# Validate occupation
print("\n" + "="*60)
print("VALIDATION CHECK")
print("="*60)

occupation_test = test_request['occupation']
if occupation_test in model_data['label_encoders']['Occupation'].classes_:
    print(f"✅ Occupation '{occupation_test}' is valid")
else:
    print(f"❌ Occupation '{occupation_test}' is NOT valid")
    print(f"Valid occupations are:")
    for occ in model_data['label_encoders']['Occupation'].classes_:
        print(f"   - {occ}")

bmi_test = test_request['bmi_category']
if bmi_test in model_data['label_encoders']['BMI Category'].classes_:
    print(f"✅ BMI Category '{bmi_test}' is valid")
else:
    print(f"❌ BMI Category '{bmi_test}' is NOT valid")
    print(f"Valid BMI categories are:")
    for bmi in model_data['label_encoders']['BMI Category'].classes_:
        print(f"   - {bmi}")

print("\n" + "="*60)
print("COMMON MISTAKES")
print("="*60)
print("1. Make sure occupation exactly matches one from the list above")
print("2. Make sure BMI category exactly matches (case-sensitive)")
print("3. All integer fields should be integers, not strings")
print("4. sleep_duration should be a float (e.g., 7.5 not '7.5')")
print("="*60)
