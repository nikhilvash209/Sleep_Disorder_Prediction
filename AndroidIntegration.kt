// Android Integration Example for Sleep Disorder Prediction API
// Complete Android implementation with Retrofit

// ============================================================================
// 1. build.gradle (Module: app) - Add Dependencies
// ============================================================================

/*
dependencies {
    // Retrofit for networking
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    
    // OkHttp for logging
    implementation 'com.squareup.okhttp3:logging-interceptor:4.10.0'
    
    // Coroutines for async operations
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1'
    
    // ViewModel and LiveData
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2'
    implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.6.2'
    
    // Activity KTX for viewModels()
    implementation 'androidx.activity:activity-ktx:1.8.0'
}
*/

// ============================================================================
// 2. AndroidManifest.xml - Add Internet Permission
// ============================================================================

/*
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        ...
        android:usesCleartextTraffic="true"> <!-- For HTTP testing only, use HTTPS in production -->
        ...
    </application>
</manifest>
*/

// ============================================================================
// 3. Data Models
// ============================================================================

package com.example.sleepapp.data.model

import com.google.gson.annotations.SerializedName

data class PredictionRequest(
    @SerializedName("gender")
    val gender: String,
    
    @SerializedName("age")
    val age: Int,
    
    @SerializedName("occupation")
    val occupation: String,
    
    @SerializedName("sleep_duration")
    val sleepDuration: Double,
    
    @SerializedName("quality_of_sleep")
    val qualityOfSleep: Int,
    
    @SerializedName("physical_activity_level")
    val physicalActivityLevel: Int,
    
    @SerializedName("stress_level")
    val stressLevel: Int,
    
    @SerializedName("bmi_category")
    val bmiCategory: String,
    
    @SerializedName("heart_rate")
    val heartRate: Int,
    
    @SerializedName("daily_steps")
    val dailySteps: Int,
    
    @SerializedName("systolic_bp")
    val systolicBp: Int,
    
    @SerializedName("diastolic_bp")
    val diastolicBp: Int
)

data class PredictionResponse(
    @SerializedName("prediction")
    val prediction: String,
    
    @SerializedName("confidence")
    val confidence: Double?,
    
    @SerializedName("message")
    val message: String
)

data class HealthCheckResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("message")
    val message: String,
    
    @SerializedName("version")
    val version: String,
    
    @SerializedName("model_loaded")
    val modelLoaded: Boolean
)

data class OptionsResponse(
    @SerializedName("gender")
    val gender: List<String>,
    
    @SerializedName("occupation")
    val occupation: List<String>,
    
    @SerializedName("bmi_category")
    val bmiCategory: List<String>,
    
    @SerializedName("sleep_disorders")
    val sleepDisorders: List<String>
)

// ============================================================================
// 4. API Interface
// ============================================================================

package com.example.sleepapp.data.api

import com.example.sleepapp.data.model.*
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface SleepDisorderAPI {
    
    @GET("/")
    suspend fun healthCheck(): Response<HealthCheckResponse>
    
    @GET("/api/options")
    suspend fun getOptions(): Response<OptionsResponse>
    
    @POST("/api/predict")
    suspend fun predict(@Body request: PredictionRequest): Response<PredictionResponse>
}

// ============================================================================
// 5. Retrofit Client
// ============================================================================

package com.example.sleepapp.data.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    
    // TODO: Replace with your deployed API URL
    private const val BASE_URL = "https://your-api-url.onrender.com/"
    
    // For local testing: "http://10.0.2.2:8000/" (Android Emulator)
    // For local testing: "http://192.168.x.x:8000/" (Physical Device)
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val api: SleepDisorderAPI by lazy {
        retrofit.create(SleepDisorderAPI::class.java)
    }
}

// ============================================================================
// 6. Repository
// ============================================================================

package com.example.sleepapp.data.repository

import com.example.sleepapp.data.api.RetrofitClient
import com.example.sleepapp.data.model.*
import retrofit2.Response

class SleepDisorderRepository {
    
    private val api = RetrofitClient.api
    
    suspend fun checkHealth(): Response<HealthCheckResponse> {
        return api.healthCheck()
    }
    
    suspend fun getOptions(): Response<OptionsResponse> {
        return api.getOptions()
    }
    
    suspend fun predictSleepDisorder(request: PredictionRequest): Response<PredictionResponse> {
        return api.predict(request)
    }
}

// ============================================================================
// 7. ViewModel
// ============================================================================

package com.example.sleepapp.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sleepapp.data.model.*
import com.example.sleepapp.data.repository.SleepDisorderRepository
import kotlinx.coroutines.launch

sealed class UiState<out T> {
    object Idle : UiState<Nothing>()
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

class SleepPredictionViewModel : ViewModel() {
    
    private val repository = SleepDisorderRepository()
    
    private val _healthCheckState = MutableLiveData<UiState<HealthCheckResponse>>()
    val healthCheckState: LiveData<UiState<HealthCheckResponse>> = _healthCheckState
    
    private val _optionsState = MutableLiveData<UiState<OptionsResponse>>()
    val optionsState: LiveData<UiState<OptionsResponse>> = _optionsState
    
    private val _predictionState = MutableLiveData<UiState<PredictionResponse>>()
    val predictionState: LiveData<UiState<PredictionResponse>> = _predictionState
    
    fun checkHealth() {
        viewModelScope.launch {
            _healthCheckState.value = UiState.Loading
            try {
                val response = repository.checkHealth()
                if (response.isSuccessful) {
                    response.body()?.let {
                        _healthCheckState.value = UiState.Success(it)
                    } ?: run {
                        _healthCheckState.value = UiState.Error("Empty response body")
                    }
                } else {
                    _healthCheckState.value = UiState.Error("Error: ${response.code()} - ${response.message()}")
                }
            } catch (e: Exception) {
                _healthCheckState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }
    
    fun loadOptions() {
        viewModelScope.launch {
            _optionsState.value = UiState.Loading
            try {
                val response = repository.getOptions()
                if (response.isSuccessful) {
                    response.body()?.let {
                        _optionsState.value = UiState.Success(it)
                    } ?: run {
                        _optionsState.value = UiState.Error("Empty response body")
                    }
                } else {
                    _optionsState.value = UiState.Error("Error: ${response.code()} - ${response.message()}")
                }
            } catch (e: Exception) {
                _optionsState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }
    
    fun predictSleepDisorder(request: PredictionRequest) {
        viewModelScope.launch {
            _predictionState.value = UiState.Loading
            try {
                val response = repository.predictSleepDisorder(request)
                if (response.isSuccessful) {
                    response.body()?.let {
                        _predictionState.value = UiState.Success(it)
                    } ?: run {
                        _predictionState.value = UiState.Error("Empty response body")
                    }
                } else {
                    _predictionState.value = UiState.Error("Error: ${response.code()} - ${response.message()}")
                }
            } catch (e: Exception) {
                _predictionState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }
    
    fun resetPrediction() {
        _predictionState.value = UiState.Idle
    }
}

// ============================================================================
// 8. MainActivity Example
// ============================================================================

package com.example.sleepapp

import android.os.Bundle
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.example.sleepapp.data.model.PredictionRequest
import com.example.sleepapp.ui.viewmodel.SleepPredictionViewModel
import com.example.sleepapp.ui.viewmodel.UiState

class MainActivity : AppCompatActivity() {
    
    private val viewModel: SleepPredictionViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Check API health on startup
        viewModel.checkHealth()
        
        // Load options for dropdowns
        viewModel.loadOptions()
        
        // Observe health check
        viewModel.healthCheckState.observe(this) { state ->
            when (state) {
                is UiState.Loading -> {
                    // Show loading indicator
                }
                is UiState.Success -> {
                    if (state.data.modelLoaded) {
                        Toast.makeText(this, "API Connected Successfully", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(this, "Warning: Model not loaded", Toast.LENGTH_LONG).show()
                    }
                }
                is UiState.Error -> {
                    Toast.makeText(this, "API Error: ${state.message}", Toast.LENGTH_LONG).show()
                }
                is UiState.Idle -> {}
            }
        }
        
        // Observe options
        viewModel.optionsState.observe(this) { state ->
            when (state) {
                is UiState.Success -> {
                    // Populate spinners with options
                    populateGenderSpinner(state.data.gender)
                    populateOccupationSpinner(state.data.occupation)
                    populateBmiSpinner(state.data.bmiCategory)
                }
                is UiState.Error -> {
                    Toast.makeText(this, "Error loading options: ${state.message}", Toast.LENGTH_SHORT).show()
                }
                else -> {}
            }
        }
        
        // Observe prediction results
        viewModel.predictionState.observe(this) { state ->
            when (state) {
                is UiState.Loading -> {
                    // Show loading dialog
                    showLoading()
                }
                is UiState.Success -> {
                    hideLoading()
                    displayResult(state.data)
                }
                is UiState.Error -> {
                    hideLoading()
                    Toast.makeText(this, "Prediction Error: ${state.message}", Toast.LENGTH_LONG).show()
                }
                is UiState.Idle -> {
                    hideLoading()
                }
            }
        }
        
        // Setup predict button
        setupPredictButton()
    }
    
    private fun setupPredictButton() {
        // Get references to your UI elements
        // btnPredict.setOnClickListener {
        //     val request = createPredictionRequest()
        //     viewModel.predictSleepDisorder(request)
        // }
    }
    
    private fun createPredictionRequest(): PredictionRequest {
        // Collect data from UI elements
        return PredictionRequest(
            gender = "Male", // Get from spinner
            age = 30, // Get from input
            occupation = "Software Engineer", // Get from spinner
            sleepDuration = 7.5, // Get from input
            qualityOfSleep = 8, // Get from slider/input
            physicalActivityLevel = 6, // Get from slider/input
            stressLevel = 5, // Get from slider/input
            bmiCategory = "Normal", // Get from spinner
            heartRate = 75, // Get from input
            dailySteps = 8000, // Get from input
            systolicBp = 120, // Get from input
            diastolicBp = 80 // Get from input
        )
    }
    
    private fun displayResult(result: PredictionResponse) {
        // Display prediction result
        // resultTextView.text = "Prediction: ${result.prediction}"
        // confidenceTextView.text = "Confidence: ${result.confidence}%"
        // messageTextView.text = result.message
    }
    
    private fun populateGenderSpinner(options: List<String>) {
        // Populate gender spinner
    }
    
    private fun populateOccupationSpinner(options: List<String>) {
        // Populate occupation spinner
    }
    
    private fun populateBmiSpinner(options: List<String>) {
        // Populate BMI spinner
    }
    
    private fun showLoading() {
        // Show loading dialog or progress bar
    }
    
    private fun hideLoading() {
        // Hide loading dialog or progress bar
    }
}

// ============================================================================
// 9. Simple Usage Example
// ============================================================================

/*
// In your Activity or Fragment:

class PredictionActivity : AppCompatActivity() {
    
    private val viewModel: SleepPredictionViewModel by viewModels()
    
    fun onPredictButtonClick() {
        val request = PredictionRequest(
            gender = spinnerGender.selectedItem.toString(),
            age = editTextAge.text.toString().toInt(),
            occupation = spinnerOccupation.selectedItem.toString(),
            sleepDuration = editTextSleepDuration.text.toString().toDouble(),
            qualityOfSleep = seekBarSleepQuality.progress,
            physicalActivityLevel = seekBarActivity.progress,
            stressLevel = seekBarStress.progress,
            bmiCategory = spinnerBmi.selectedItem.toString(),
            heartRate = editTextHeartRate.text.toString().toInt(),
            dailySteps = editTextSteps.text.toString().toInt(),
            systolicBp = editTextSystolic.text.toString().toInt(),
            diastolicBp = editTextDiastolic.text.toString().toInt()
        )
        
        viewModel.predictSleepDisorder(request)
    }
}
*/

// ============================================================================
// 10. Testing with Local API
// ============================================================================

/*
To test with local API:

1. Run the API on your computer: python api.py
2. Find your computer's IP address:
   - Windows: ipconfig
   - Mac/Linux: ifconfig
3. Update BASE_URL in RetrofitClient:
   - Emulator: "http://10.0.2.2:8000/"
   - Physical device: "http://YOUR_IP_ADDRESS:8000/"
4. Ensure your phone and computer are on the same WiFi network
*/
