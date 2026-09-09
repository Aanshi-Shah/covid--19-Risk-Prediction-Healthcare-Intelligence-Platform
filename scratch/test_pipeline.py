import os
import joblib
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)

model_path = os.path.join(root_dir, "models", "covid_risk_model.pkl")
pipeline_path = os.path.join(root_dir, "models", "preprocessing_pipeline.pkl")

print("Checking model path:", model_path)
print("Checking pipeline path:", pipeline_path)

try:
    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)
    print("Success loading model and pipeline!")
    
    # Mock input matching streamlit_app.py logic
    age = 45
    gender = "Male"
    temp_f = 98.6
    oxygen_level = 97
    cough = "No"
    breathing_diff = "No"
    heart_disease = "No"
    diabetes = "No"
    
    encoded_input = {}
    encoded_input['Age'] = age
    encoded_input['Gender_Encoded'] = pipeline['gender_mapping'][gender]
    encoded_input['Temperature_F'] = temp_f
    encoded_input['Oxygen_Level'] = oxygen_level
    encoded_input['Cough_Encoded'] = pipeline['binary_mapping'][cough]
    encoded_input['Breathing_Difficulty_Encoded'] = pipeline['binary_mapping'][breathing_diff]
    encoded_input['Heart_Disease_Encoded'] = pipeline['binary_mapping'][heart_disease]
    encoded_input['Diabetes_Encoded'] = pipeline['binary_mapping'][diabetes]
    
    input_df = pd.DataFrame([encoded_input])
    numeric_names = pipeline['numeric_names']
    input_df[numeric_names] = pipeline['scaler'].transform(input_df[numeric_names])
    
    risk_prob = model.predict_proba(input_df[pipeline['feature_cols']])[:, 1][0]
    print(f"Prediction success! Risk prob: {risk_prob}")
except Exception as e:
    print("Error encountered:", str(e))
    import traceback
    traceback.print_exc()
