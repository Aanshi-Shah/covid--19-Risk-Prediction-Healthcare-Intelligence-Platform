import os
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import datetime
import warnings

# Suppress scikit-learn version inconsistency warnings
warnings.filterwarnings("ignore", message="Trying to unpickle estimator")

# Set Page Config
st.set_page_config(
    page_title="Pandemic Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        .main {
            background-color: #0e1117;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #0e1117;
            border-right: 1px solid #1f2937;
            padding-top: 1.5rem;
        }
        
        /* Ensure sidebar text, labels, and headings are light for high contrast on the dark background */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] .stMarkdown p {
            color: #f8fafc !important;
        }
        
        /* Metric Card styling */
        .metric-card {
            background: #11151c;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #2d3748;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
            border-color: #4a5568;
        }
        
        .metric-label {
            color: #94a3b8;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .metric-value {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0.25rem;
        }
        
        /* Title styling */
        .main-title {
            background: linear-gradient(135deg, #0f62fe 0%, #009688 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }
        
        /* Indicator Banner Styles */
        .risk-banner {
            padding: 1.25rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.25rem;
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            border-left: 6px solid;
        }
        
        .risk-high {
            background-color: #fff5f5;
            color: #c53030;
            border-color: #e53e3e;
        }
        
        .risk-medium {
            background-color: #fffaf0;
            color: #dd6b20;
            border-color: #dd6b20;
        }
        
        .risk-low {
            background-color: #f0fff4;
            color: #2f855a;
            border-color: #38a169;
        }
        
        .risk-minor {
            background-color: #ebf8ff;
            color: #2b6cb0;
            border-color: #3182ce;
        }
        
        /* Buttons custom */
        div.stButton > button {
            background: linear-gradient(135deg, #0f62fe 0%, #0840b0 100%);
            color: white;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 6px rgba(15, 98, 254, 0.2);
            transition: all 0.2s ease;
            width: 100%;
        }
        
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(15, 98, 254, 0.3);
            background: linear-gradient(135deg, #116eff 0%, #0947c4 100%);
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to load model and preprocessor safely
@st.cache_resource
def load_assets():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Try dynamic paths
    model_paths = [
        os.path.join(root_dir, "models", "covid_risk_model.pkl"),
        os.path.join(script_dir, "models", "covid_risk_model.pkl"),
        "models/covid_risk_model.pkl"
    ]
    pipeline_paths = [
        os.path.join(root_dir, "models", "preprocessing_pipeline.pkl"),
        os.path.join(script_dir, "models", "preprocessing_pipeline.pkl"),
        "models/preprocessing_pipeline.pkl"
    ]
    
    clf = None
    pipeline = None
    
    for path in model_paths:
        if os.path.exists(path):
            try:
                clf = joblib.load(path)
                break
            except Exception:
                pass
                
    for path in pipeline_paths:
        if os.path.exists(path):
            try:
                pipeline = joblib.load(path)
                break
            except Exception:
                pass
                
    return clf, pipeline

# Paths configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)

# Load model assets
model, pipeline = load_assets()


# Main Title and Headers
st.markdown('<div class="main-title">COVID-19 Risk Prediction & Pandemic Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">An educational screening and analytics tool demonstrating predictive modeling for patient risk metrics.</div>', unsafe_allow_html=True)

# 1. Medical Disclaimer near the top
st.warning("⚠️ **Medical Disclaimer:** This tool is for educational and analytics demonstration only. It is not a medical diagnosis system. Please consult a certified healthcare professional for real medical decisions.")

# Check if assets are loaded
if model is None or pipeline is None:
    st.error("⚠️ Model training artifacts not found. Please run the model training notebooks/scripts first to generate 'models/covid_risk_model.pkl' and 'models/preprocessing_pipeline.pkl'.")
    st.info("You can train the model by executing the Jupyter notebook or the `scratch/train_model.py` script.")
    st.stop()

# Initialize session state for prediction trigger
if 'predicted' not in st.session_state:
    st.session_state.predicted = False

# Sidebar Config
st.sidebar.markdown("### 🏥 Demographics & Vitals")

# Demographics
age = st.sidebar.slider("Age (Years)", min_value=0, max_value=120, value=45, step=1)
gender = st.sidebar.selectbox("Gender", options=["Male", "Female"])

# Vitals
temp_f = st.sidebar.slider("Body Temperature (°F)", min_value=95.0, max_value=106.0, value=98.6, step=0.1)
oxygen_level = st.sidebar.slider("Oxygen Level (SpO2 %)", min_value=50, max_value=100, value=97, step=1)

st.sidebar.markdown("### 🤒 Symptoms & Comorbidities")

# Symptoms & Comorbidities
cough = st.sidebar.selectbox("Active Cough (Dry/Minor)", options=["No", "Yes"])
breathing_diff = st.sidebar.selectbox("Breathing Difficulty", options=["No", "Yes"])
heart_disease = st.sidebar.selectbox("Heart Disease History", options=["No", "Yes"])
diabetes = st.sidebar.selectbox("Diabetes History", options=["No", "Yes"])

st.sidebar.markdown("---")

# 2. Predict COVID Risk Button in the Sidebar
if st.sidebar.button("🔮 Predict COVID Risk", type="primary"):
    st.session_state.predicted = True

# Metrics cards showing current user entries
st.markdown("### 📊 Patient Metrics Entered")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Patient Demographics</div>
            <div class="metric-value">{age} y/o • {gender}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Entered Temperature</div>
            <div class="metric-value">{temp_f:.1f}°F</div>
        </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Oxygen Saturation</div>
            <div class="metric-value" style="color: {'#e53e3e' if oxygen_level < 90 else '#2d3748'}">{oxygen_level}% SpO₂</div>
        </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Symptoms</div>
            <div class="metric-value">
                {sum([1 for x in [cough, breathing_diff] if x == 'Yes'])} / 2
            </div>
        </div>
    """, unsafe_allow_html=True)

# Main Dashboard Content Flow
if not st.session_state.predicted:
    # Guidelines to start
    st.info("👈 Adjust patient demographics, vitals, and symptoms in the sidebar, then click **Predict COVID Risk** to see the analytical predictions.")
else:
    # ------------------ Inference Processing ------------------
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

    try:
        risk_prob = model.predict_proba(input_df[pipeline['feature_cols']])[:, 1][0]
        risk_pct = round(risk_prob * 100, 1)
    except Exception as e:
        st.error(f"Inference pipeline failed: {str(e)}")
        st.stop()

    # Risk level classification based on risk probability
    if risk_pct < 20:
        risk_category = 'Minor Risk'
    elif risk_pct < 50:
        risk_category = 'Low Risk'
    elif risk_pct < 80:
        risk_category = 'Average Risk'
    else:
        risk_category = 'High Risk'

    # Clinical safety overrides - depend on the risk probability
    clinical_overrides = []
    override_triggered = False
    
    # Overrides are only active and override_triggered is only True when risk probability is high (>=80%)
    if risk_pct >= 80:
        override_triggered = True
        if oxygen_level < 90:
            clinical_overrides.append("Low Oxygen Levels (<90% SpO2)")
        if temp_f >= 102.5:
            clinical_overrides.append("High Temperature (≥102.5°F)")
        if breathing_diff == "Yes":
            clinical_overrides.append("Breathing Difficulty Present")

    # 3. Dynamic Result Cards Layout
    st.markdown("### 🩺 Platform Assessment Summary")
    card_col1, card_col2, card_col3, card_col4 = st.columns(4)
    
    with card_col1:
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid #0f62fe;">
                <div class="metric-label">COVID Risk Probability</div>
                <div class="metric-value" style="color: #0f62fe;">{risk_pct}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    with card_col2:
        if risk_category == "High Risk":
            badge_color = "#e53e3e"
        elif risk_category == "Average Risk":
            badge_color = "#dd6b20"
        elif risk_category == "Low Risk":
            badge_color = "#2f855a"
        else: # Minor Risk
            badge_color = "#2b6cb0"
            
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {badge_color};">
                <div class="metric-label">Risk Category</div>
                <div class="metric-value" style="color: {badge_color};">{risk_category}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with card_col3:
        override_txt = "Triggered" if override_triggered else "None"
        override_color = "#e53e3e" if override_triggered else "#718096"
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {override_color};">
                <div class="metric-label">Override Status</div>
                <div class="metric-value" style="color: {override_color};">{override_txt}</div>
            </div>
        """, unsafe_allow_html=True)
        
    # Calculate patient-specific risk factor drivers for visual graph
    drivers = []
    values = []
    
    temp_excess = max(0, temp_f - 98.6)
    drivers.append("Body Temperature")
    values.append(temp_excess * 8.5)
    
    oxygen_deficit = max(0, 95 - oxygen_level)
    drivers.append("Oxygen Deficit")
    values.append(oxygen_deficit * 12.0)
    
    age_risk = max(0, age - 40)
    drivers.append("Age Vulnerability")
    values.append(age_risk * 0.5)
    
    if breathing_diff == "Yes":
        drivers.append("Breathing Difficulty")
        values.append(25.0)
    if cough == "Yes":
        drivers.append("Cough")
        values.append(15.0)
    if diabetes == "Yes":
        drivers.append("Diabetes")
        values.append(10.0)
    if heart_disease == "Yes":
        drivers.append("Heart Disease")
        values.append(12.0)
        
    driver_df = pd.DataFrame({'Driver': drivers, 'Impact': values})
    driver_df = driver_df.sort_values(by='Impact', ascending=True)
    main_driver = driver_df.iloc[-1]['Driver'] if (len(driver_df) > 0 and driver_df['Impact'].sum() > 0) else "None (Baseline)"
        
    with card_col4:
        st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid #319795;">
                <div class="metric-label">Primary Risk Driver</div>
                <div class="metric-value" style="color: #319795; font-size: 1.35rem; line-height: 1.9rem; padding-top: 0.2rem;">{main_driver}</div>
            </div>
        """, unsafe_allow_html=True)



    # Risk Assessment Plots & Guidance Split
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.subheader("🏥 Risk Visualizer")
        
        # Risk gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_pct,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Estimated Infection Probability", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#0f62fe"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 20], 'color': 'rgba(43, 108, 176, 0.15)'},
                    {'range': [20, 50], 'color': 'rgba(76, 175, 80, 0.2)'},
                    {'range': [50, 80], 'color': 'rgba(255, 152, 0, 0.2)'},
                    {'range': [80, 100], 'color': 'rgba(244, 67, 54, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, use_container_width=True)

        # 5. Downloadable Patient Risk Report as CSV
        st.markdown("### 📥 Export Screening Data")
        report_data = {
            "Parameter": [
                "Assessment Timestamp", "Patient Age (Years)", "Patient Gender", 
                "Body Temperature (F)", "Oxygen Saturation (SpO2 %)", "Active Cough Present", 
                "Breathing Difficulty Present", "Pre-existing Heart Disease", "Pre-existing Diabetes", 
                "Analytical COVID Infection Risk (%)", "Vulnerability Level", "Safety Overrides Applied"
            ],
            "Value": [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                age, gender, temp_f, oxygen_level, cough, breathing_diff, heart_disease, diabetes,
                f"{risk_pct}%", risk_category, ", ".join(clinical_overrides) if clinical_overrides else "None"
            ]
        }
        report_df = pd.DataFrame(report_data)
        csv_data = report_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Patient Risk Report (CSV)",
            data=csv_data,
            file_name=f"patient_risk_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with col_right:
        # 4. Renamed Risk Factor Chart Title
        st.subheader("🧬 Clinical Driver Estimates")
        
        if len(driver_df) > 0 and driver_df['Impact'].sum() > 0:
            fig_drivers = go.Figure(go.Bar(
                x=driver_df['Impact'],
                y=driver_df['Driver'],
                orientation='h',
                marker_color='#0f62fe',
                text=driver_df['Impact'].round(1).astype(str) + '%',
                textposition='auto'
            ))
            fig_drivers.update_layout(
                title="Rule-Based Clinical Risk Driver Estimate",
                xaxis_title="Estimated Risk Contribution (%)",
                yaxis_title="Symptom / Metric",
                height=300,
                margin=dict(l=40, r=20, t=50, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_drivers, use_container_width=True)
        else:
            st.info("No active clinical indicators found above standard ranges.")

        # 7. Wording Improvements - "Suggested Risk Guidance"
        if risk_category == 'High Risk':
            st.markdown('<div class="risk-banner risk-high">🔴 HIGH VULNERABILITY PROFILE</div>', unsafe_allow_html=True)
            guidance_title = "📋 Suggested Risk Guidance:"
            guidance = """
            - Consider consulting a certified healthcare professional via telehealth or visit a clinical center for evaluation.
            - Periodically check blood oxygen saturation (SpO₂) every 2 to 4 hours.
            - If breathing issues become severe or SpO₂ remains low, seek medical evaluation.
            - Practice social isolation in a dedicated room to reduce contact risks.
            """
        elif risk_category == 'Average Risk':
            st.markdown('<div class="risk-banner risk-medium">🟡 AVERAGE VULNERABILITY PROFILE</div>', unsafe_allow_html=True)
            guidance_title = "📋 Suggested Risk Guidance:"
            guidance = """
            - Telehealth consultation is recommended to check symptoms.
            - Monitor body temperature and oxygen levels twice daily.
            - Rest, maintain fluid intake, and consult a doctor regarding any symptomatic reliefs.
            - Self-isolate at home and monitor for progressive changes in breathing.
            """
        elif risk_category == 'Low Risk':
            st.markdown('<div class="risk-banner risk-low">🟢 LOW VULNERABILITY PROFILE</div>', unsafe_allow_html=True)
            guidance_title = "📋 Suggested Guidance:"
            guidance = """
            - Continue monitoring temperature and general physical symptoms.
            - Adhere to standard safety precautions: wear masks in dense environments and practice hand hygiene.
            - Re-assess with the tool if coughing, fever, or breathing difficulty begins.
            """
        else: # Minor Risk
            st.markdown('<div class="risk-banner risk-minor">🔵 MINOR VULNERABILITY PROFILE</div>', unsafe_allow_html=True)
            guidance_title = "📋 Suggested Guidance:"
            guidance = """
            - Continue monitoring temperature and general physical symptoms.
            - Adhere to standard safety precautions: wear masks in dense environments and practice hand hygiene.
            - Re-assess with the tool if coughing, fever, or breathing difficulty begins.
            """

        st.markdown(f"""
            <div style="background-color: #11151c; color: #f8fafc; padding: 1.5rem; border-radius: 12px; border: 1px solid #2d3748; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);">
                <div style="font-weight: 700; color: #ffffff; margin-bottom: 0.5rem; font-size: 1.1rem;">{guidance_title}</div>
                <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                    {guidance}
                </div>
            </div>
        """, unsafe_allow_html=True)

        if clinical_overrides:
            st.markdown(f"""
                <div style="margin-top: 1rem; padding: 0.75rem 1rem; background-color: #2c1d11; border-radius: 8px; border-left: 4px solid #dd6b20; font-size: 0.85rem; color: #fbd38d;">
                    ⚠️ **Clinical Override Indicator:** Risk category adjusted to reflect: {', '.join(clinical_overrides)}.
                </div>
            """, unsafe_allow_html=True)

    # Comparative Analysis and Dataset insights
    st.markdown("---")
    st.subheader("📊 Comparative Population Analytics")
    
    cleaned_data_path = os.path.join(root_dir, "data", "cleaned_covid_data.csv")
    if not os.path.exists(cleaned_data_path):
        cleaned_data_path = "data/cleaned_covid_data.csv"
        
    if os.path.exists(cleaned_data_path):
        try:
            # Load dataset for population references
            sum_df = pd.read_csv(cleaned_data_path)
                
            plot_df = sum_df.sample(n=300, random_state=42) if len(sum_df) > 300 else sum_df
            
            # Row 1: Table & Age vs SpO2 Scatter
            col_row1_1, col_row1_2 = st.columns(2)
            
            with col_row1_1:
                # Pre-calculate pill badge styles and labels for clinical metrics check
                if oxygen_level < 90:
                    o2_status_pill = '<span style="background-color: #fff5f5; color: #c53030; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Hypoxia (Critical)</span>'
                    o2_val_style = 'color: #c53030; font-weight: 600;'
                elif oxygen_level <= 94:
                    o2_status_pill = '<span style="background-color: #fffaf0; color: #dd6b20; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Borderline</span>'
                    o2_val_style = 'color: #dd6b20; font-weight: 600;'
                else:
                    o2_status_pill = '<span style="background-color: #f0fff4; color: #2f855a; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Normal</span>'
                    o2_val_style = 'color: #2f855a; font-weight: 600;'

                if temp_f >= 101.5:
                    temp_status_pill = '<span style="background-color: #fff5f5; color: #c53030; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Fever (High)</span>'
                    temp_val_style = 'color: #c53030; font-weight: 600;'
                elif temp_f >= 99.5:
                    temp_status_pill = '<span style="background-color: #fffaf0; color: #dd6b20; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Elevated</span>'
                    temp_val_style = 'color: #dd6b20; font-weight: 600;'
                else:
                    temp_status_pill = '<span style="background-color: #f0fff4; color: #2f855a; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Normal</span>'
                    temp_val_style = 'color: #2f855a; font-weight: 600;'

                comorbid_list = '/'.join([k for k, v in {'Heart': heart_disease, 'Diab': diabetes}.items() if v == 'Yes']) or 'None'
                if heart_disease == 'Yes' or diabetes == 'Yes':
                    comorbid_status_pill = '<span style="background-color: #fff5f5; color: #c53030; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Increased Risk</span>'
                    comorbid_val_style = 'color: #c53030; font-weight: 600;'
                else:
                    comorbid_status_pill = '<span style="background-color: #f0fff4; color: #2f855a; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Low Risk</span>'
                    comorbid_val_style = 'color: #2f855a; font-weight: 600;'

                st.markdown(f"""
                    <div style="background-color: #11151c; color: #f8fafc; padding: 1.5rem; border-radius: 12px; border: 1px solid #2d3748; height: 100%;">
                        <h4 style="margin-top:0; color:#ffffff; font-weight:700;">Clinical Metrics Check</h4>
                        <p style="color:#94a3b8; font-size:0.9rem;">
                            Comparing entered patient values to standard clinical ranges and thresholds.
                        </p>
                        <table style="width:100%; border-collapse: collapse; font-size: 0.95rem; color: #f8fafc;">
                            <tr style="border-bottom: 1px solid #2d3748; padding: 8px 0;">
                                <td style="padding: 10px 0; font-weight: 500;">Parameter</td>
                                <td style="text-align: right; font-weight: 500; padding-right: 10px;">Entered Value</td>
                                <td style="text-align: right; font-weight: 500; padding-right: 10px;">Normal Reference Range</td>
                                <td style="text-align: right; font-weight: 500;">Status Indicator</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #2d3748;">
                                <td style="padding: 12px 0;">Oxygen Saturation (SpO₂)</td>
                                <td style="text-align: right; padding-right: 10px; {o2_val_style}">{oxygen_level}%</td>
                                <td style="text-align: right; padding-right: 10px;">95% - 100%</td>
                                <td style="text-align: right; padding: 6px 0;">{o2_status_pill}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #2d3748;">
                                <td style="padding: 12px 0;">Body Temperature</td>
                                <td style="text-align: right; padding-right: 10px; {temp_val_style}">{temp_f:.1f}°F</td>
                                <td style="text-align: right; padding-right: 10px;">97.0°F - 99.0°F</td>
                                <td style="text-align: right; padding: 6px 0;">{temp_status_pill}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #2d3748;">
                                <td style="padding: 12px 0;">Comorbidities</td>
                                <td style="text-align: right; padding-right: 10px; {comorbid_val_style}">{comorbid_list}</td>
                                <td style="text-align: right; padding-right: 10px;">No History</td>
                                <td style="text-align: right; padding: 6px 0;">{comorbid_status_pill}</td>
                            </tr>
                        </table>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_row1_2:
                fig_compare = go.Figure()
                fig_compare.add_trace(go.Scatter(
                    x=plot_df[plot_df['Target_Encoded'] == 1]['Age'],
                    y=plot_df[plot_df['Target_Encoded'] == 1]['Oxygen_Level'],
                    mode='markers',
                    name='COVID Positive (Database)',
                    marker=dict(color='rgba(244, 67, 54, 0.4)', size=7)
                ))
                fig_compare.add_trace(go.Scatter(
                    x=plot_df[plot_df['Target_Encoded'] == 0]['Age'],
                    y=plot_df[plot_df['Target_Encoded'] == 0]['Oxygen_Level'],
                    mode='markers',
                    name='COVID Negative (Database)',
                    marker=dict(color='rgba(76, 175, 80, 0.4)', size=7)
                ))
                fig_compare.add_trace(go.Scatter(
                    x=[age],
                    y=[oxygen_level],
                    mode='markers',
                    name='Current Patient',
                    marker=dict(color='#0f62fe', size=16, symbol='star', line=dict(color='white', width=2))
                ))
                
                fig_compare.update_layout(
                    title="Current Patient vs Database Metrics (Age vs SpO₂)",
                    xaxis_title="Age (Years)",
                    yaxis_title="Oxygen Saturation (%)",
                    legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
                    height=350,
                    margin=dict(l=40, r=20, t=50, b=80),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_compare, use_container_width=True)
                
            # Row 2: Temperature Distribution & Symptom Prevalence Comparison
            col_row2_1, col_row2_2 = st.columns(2)
            
            with col_row2_1:
                # 1. Body Temperature population distribution comparison
                pos_temp = plot_df[plot_df['Target_Encoded'] == 1]['Temperature_F']
                neg_temp = plot_df[plot_df['Target_Encoded'] == 0]['Temperature_F']
                
                fig_temp_dist = go.Figure()
                fig_temp_dist.add_trace(go.Histogram(
                    x=pos_temp,
                    nbinsx=15,
                    name='COVID Positive (Database)',
                    marker_color='rgba(244, 67, 54, 0.5)',
                    histnorm='probability density'
                ))
                fig_temp_dist.add_trace(go.Histogram(
                    x=neg_temp,
                    nbinsx=15,
                    name='COVID Negative (Database)',
                    marker_color='rgba(76, 175, 80, 0.5)',
                    histnorm='probability density'
                ))
                fig_temp_dist.add_vline(
                    x=temp_f, 
                    line_width=3, 
                    line_dash="dash", 
                    line_color="#0f62fe",
                    annotation_text=f"Current Patient ({temp_f:.1f}°F)", 
                    annotation_position="top right"
                )
                fig_temp_dist.update_layout(
                    title="Temperature Distribution vs. Current Patient",
                    xaxis_title="Temperature (°F)",
                    yaxis_title="Probability Density",
                    barmode='overlay',
                    legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
                    height=350,
                    margin=dict(l=40, r=20, t=50, b=80),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_temp_dist, use_container_width=True)
                
            with col_row2_2:
                # 2. Symptoms and comorbidities comparison chart
                pos_cases = sum_df[sum_df['Target_Encoded'] == 1]
                symptom_labels = ['Breathing Difficulty', 'Cough', 'Diabetes', 'Heart Disease']
                
                # Database positive averages
                db_avg = [
                    (pos_cases['Breathing_Difficulty'] == 'Yes').mean() * 100,
                    (pos_cases['Cough'] == 'Yes').mean() * 100,
                    (pos_cases['Diabetes'] == 'Yes').mean() * 100,
                    (pos_cases['Heart_Disease'] == 'Yes').mean() * 100
                ]
                
                # Current patient values
                patient_vals = [
                    100 if breathing_diff == 'Yes' else 0,
                    100 if cough == 'Yes' else 0,
                    100 if diabetes == 'Yes' else 0,
                    100 if heart_disease == 'Yes' else 0
                ]
                
                fig_symptom_comp = go.Figure()
                fig_symptom_comp.add_trace(go.Bar(
                    x=symptom_labels,
                    y=db_avg,
                    name='COVID-Positive Avg (%)',
                    marker_color='rgba(244, 67, 54, 0.6)'
                ))
                fig_symptom_comp.add_trace(go.Bar(
                    x=symptom_labels,
                    y=patient_vals,
                    name='Current Patient (0 or 100%)',
                    marker_color='#0f62fe'
                ))
                
                fig_symptom_comp.update_layout(
                    title="Patient Symptoms vs. COVID-Positive Database Prevalence",
                    xaxis_title="Clinical Factor",
                    yaxis_title="Prevalence / Patient Value (%)",
                    barmode='group',
                    legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
                    height=350,
                    margin=dict(l=40, r=20, t=50, b=80),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_symptom_comp, use_container_width=True)
                
        except Exception as ex:
            st.info(f"Population analytics visualization is currently unavailable: {str(ex)}")
    else:
        st.info("Cleaned population dataset not found. Population plot unavailable.")
