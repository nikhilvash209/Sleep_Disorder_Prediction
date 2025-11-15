Sleep Disorder Prediction Model
This project implements a machine learning model to predict sleep disorders based on health and lifestyle data. The predictive model is built using a Decision Tree classifier trained on a comprehensive sleep health dataset.

Features
User-friendly Streamlit web interface for inputting health and lifestyle parameters.

Uses real-world data with features including age, gender, occupation, sleep duration, physical activity, stress level, BMI category, heart rate, blood pressure, and daily steps.

Preprocessing steps including label encoding of categorical variables.

Robust Decision Tree classifier with model evaluation metrics.

Predicts sleep disorders such as Sleep Apnea and others.

Model and encoders saved for efficient deployment.

Installation
Clone the repository.

Ensure Python 3.8+ is installed.

Install dependencies:

bash
pip install -r requirements.txt
The requirements.txt should include at least:

text
pandas
numpy
scikit-learn
seaborn
matplotlib
joblib
streamlit
Usage
Place the dataset Sleephealthandlifestyledataset.csv in the project directory.

Run the training script to train and save the model (optional if model is already saved):

bash
python sleep_disorder_train.py
Run the Streamlit app to interact with the model via a web UI:

bash
streamlit run app.py
Input your health and lifestyle data on the web interface and click Predict Sleep Disorder to view predictions.

Project Structure
sleep_disorder_train.py: Script to load data, preprocess, train model, and save the model/encoders.

app.py: Streamlit app script to provide a user interface for prediction.

Sleephealthandlifestyledataset.csv: Dataset file (not included in repo).

sleepdisordermodel.pkl: Saved model and LabelEncoders file.

requirements.txt: Python dependencies.

Acknowledgments
This project uses open-source libraries such as scikit-learn and Streamlit for building the machine learning model and web interface.