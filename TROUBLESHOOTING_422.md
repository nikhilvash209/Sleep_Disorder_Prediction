# 🔍 Troubleshooting 422 Validation Errors

## What's Happening?

You're seeing `422 Unprocessable Entity` errors, which means the request data doesn't match the expected format.

## Quick Fix Steps

### Step 1: Check What Values Are Valid

Run this command in your terminal:

```bash
cd "c:\Users\Tanya Vashishtha\OneDrive\Desktop\coding\Clg Minor project\Sleep_Disorder_Prediction - Copy (2)"
python debug_model.py
```

This will show you:
- Valid gender options
- Valid occupation options (MUST match exactly!)
- Valid BMI category options (MUST match exactly!)
- Correct request format

### Step 2: Test in Swagger UI

1. Go to http://localhost:8000/docs
2. Click on `GET /api/options` 
3. Click "Try it out" → "Execute"
4. Copy the valid values shown in the response

### Step 3: Use Correct Test Data

The most common issues are:

#### ❌ Wrong Occupation
```json
{
  "occupation": "Software Engineer"  // Might not exist in training data
}
```

#### ✅ Check Valid Occupations
Visit http://localhost:8000/api/options to see the exact list.

Common valid occupations might be:
- Accountant
- Doctor
- Engineer (NOT "Software Engineer")
- Lawyer
- Manager
- Nurse
- Sales Representative
- Salesperson
- Scientist
- Software Engineer (if in your data)
- Teacher

#### ❌ Wrong BMI Category
```json
{
  "bmi_category": "normal"  // lowercase won't work
}
```

#### ✅ Correct BMI Category
```json
{
  "bmi_category": "Normal"  // Must match exactly
}
```

Valid options:
- Normal
- Normal Weight
- Overweight
- Obese

### Step 4: Test with This Guaranteed Working Request

1. First, run: `python debug_model.py` to see valid values
2. Then use this template in `/docs`:

```json
{
  "gender": "Male",
  "age": 30,
  "occupation": "Engineer",
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

**Important:** Replace "Engineer" with an actual occupation from your model (check with `/api/options`)

### Step 5: Common Mistakes Checklist

- [ ] Occupation must EXACTLY match one from the training data
- [ ] BMI Category must be title case: "Normal" not "normal"
- [ ] Gender is case-insensitive (now fixed)
- [ ] All numbers must be actual numbers, not strings
  - ✅ `"age": 30`
  - ❌ `"age": "30"`
- [ ] sleep_duration should be a decimal number
  - ✅ `"sleep_duration": 7.5`
  - ❌ `"sleep_duration": "7.5"`

## Testing Commands

### Get Valid Options
```bash
curl http://localhost:8000/api/options
```

### Test Prediction (Windows CMD)
```bash
curl -X POST http://localhost:8000/api/predict -H "Content-Type: application/json" -d "{\"gender\":\"Male\",\"age\":30,\"occupation\":\"Engineer\",\"sleep_duration\":7.5,\"quality_of_sleep\":8,\"physical_activity_level\":6,\"stress_level\":5,\"bmi_category\":\"Normal\",\"heart_rate\":75,\"daily_steps\":8000,\"systolic_bp\":120,\"diastolic_bp\":80}"
```

### Test Prediction (PowerShell)
```powershell
$body = @{
    gender = "Male"
    age = 30
    occupation = "Engineer"
    sleep_duration = 7.5
    quality_of_sleep = 8
    physical_activity_level = 6
    stress_level = 5
    bmi_category = "Normal"
    heart_rate = 75
    daily_steps = 8000
    systolic_bp = 120
    diastolic_bp = 80
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/predict" -Method POST -Body $body -ContentType "application/json"
```

## What I Fixed

1. **Better Error Messages**: Now shows exactly which field failed and why
2. **Case-Insensitive Gender**: "male", "Male", "MALE" all work now
3. **Case-Insensitive BMI**: "normal", "Normal" both work now
4. **Helpful Error Response**: Includes tip to check `/api/options`

## Still Having Issues?

Run the debug script to see exactly what your model expects:

```bash
python debug_model.py
```

Then copy the exact values it shows into your test request!

## Quick Test Workflow

```bash
# 1. Check valid values
python debug_model.py

# 2. Get options via API
curl http://localhost:8000/api/options

# 3. Test prediction in browser
# Go to http://localhost:8000/docs
# Use /api/predict endpoint
# Copy values from step 1 or 2

# 4. Check for detailed error messages
# The API now shows which field caused the error
```

## Example Error Message (Before)

```
422 Unprocessable Entity
```

## Example Error Message (After)

```json
{
  "detail": "Validation Error",
  "errors": [
    "body -> occupation: Invalid value for Occupation. Valid values are: Accountant, Doctor, Engineer, ..."
  ],
  "tip": "Check the /api/options endpoint to see valid values for categorical fields"
}
```

Much better! 🎉
