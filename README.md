# COVID-19 Risk Prediction & Pandemic Intelligence Platform

An end-to-end healthcare analytics and machine learning platform designed to pre-process patient metrics, train high-accuracy clinical risk models, run an interactive web application for patient risk assessment, and prepare enriched population data for Power BI dashboards.

---

## 1. Project Overview & Problem Statement
During a pandemic, emergency departments and medical staff face severe resource constraints. Quickly assessing whether a symptomatic patient is at high risk of severe COVID-19 or hospitalization is critical. 

This platform addresses this by:
* **Cleaning & Pre-processing** raw patient records to standard clinical features.
* **Predicting Risk**: Training machine learning classifiers on patient demographics, symptoms, and vitals to output the probability of COVID-19 infection.
* **Risk Categorization**: Segmenting patient severity into Low, Medium, and High Risk categories with safety clinical overrides (e.g., automatically classifying patient as High Risk if oxygen levels drop below $90\%$).
* **Empowering Intelligence**: Generating Power BI-ready datasets with geospatial, monthly, and patient outcome (recovery vs deceased) simulations for epidemiological insights.

---

## 2. Dataset & Column Mapping

The raw dataset `COVID19_Healthcare_Analytics_Dataset_4000.csv` consists of 4,000 patient records. Below is the mapping of raw columns to model inputs and fallbacks:

| Requested ML Input | Dataset Raw Column | Cleaning & Mapping Fallback Rules |
| :--- | :--- | :--- |
| **Age** | `Age` | Formatted as integer, missing values imputed with training set mean. |
| **Gender** | `Gender` | String stripped & standardized. Encoded: `Male` = 1, `Female` = 0. |
| **Fever Temperature** | `Temperature_F` | Coerced to float, missing values imputed with mean. |
| **Oxygen Level** | `Oxygen_Level` | Coerced to integer, missing values imputed with mean. |
| **Cough** | `Minor_Cough` / `Dry_Cough` | **Fallback:** Combined. If either `Minor_Cough` or `Dry_Cough` is "Yes", `Cough` is mapped to "Yes" (1), otherwise "No" (0). |
| **Breathing Difficulty** | `Breathing_Difficulty` | Normalized case and stripped. Encoded: "Yes" = 1, "No" = 0. |
| **Heart Disease** | `Heart_Disease` | Normalized case and stripped. Encoded: "Yes" = 1, "No" = 0. |
| **Diabetes** | `Diabetes` | Normalized case and stripped. Encoded: "Yes" = 1, "No" = 0. |
| **Target Column** | `COVID_Result` | Automatically detected. Standardized and mapped: "Yes" / "Positive" = 1, "No" / "Negative" = 0. |

---

## 3. Folder Structure

```
covid-risk-platform/
│
├── data/
│   ├── raw_covid_data.csv                  # Copy of the original dataset
│   ├── cleaned_covid_data.csv              # Fully preprocessed dataset used for modeling
│   └── powerbi_covid_dashboard_data.csv    # Enriched dataset ready for Power BI dashboards
│
├── notebooks/
│   └── covid_risk_prediction.ipynb         # Step-by-step Jupyter Notebook containing the workflow
│
├── models/
│   ├── covid_risk_model.pkl                # Serialized best model (Gradient Boosting)
│   └── preprocessing_pipeline.pkl          # Serialized standard scaler and feature mappings
│
├── app/
│   └── streamlit_app.py                    # Streamlit web application dashboard code
│
├── requirements.txt                        # Dependency listing
├── README.md                               # Project documentation
└── .gitignore                              # Git tracking ignore file
```

---

## 4. Machine Learning Modeling & Performance

We trained and evaluated three candidate classifiers: **Logistic Regression**, **Random Forest**, and **Gradient Boosting**, split into an 80% training set and a 20% test set. 

### Metrics Comparison (Sorted by F1-Score)
* **Gradient Boosting (Selected Best Model)**:
  * **F1-Score**: `0.7553` (Accuracy: `76.75%` | Precision: `77.36%` | Recall: `73.78%` | ROC-AUC: `0.8690`)
* **XGBoost**:
  * **F1-Score**: `0.7483` (Accuracy: `76.88%` | Precision: `79.48%` | Recall: `70.69%` | ROC-AUC: `0.8691`)
* **Logistic Regression**:
  * **F1-Score**: `0.7477` (Accuracy: `75.88%` | Precision: `76.06%` | Recall: `73.52%` | ROC-AUC: `0.8535`)
* **Random Forest**:
  * **F1-Score**: `0.7431` (Accuracy: `76.75%` | Precision: `80.30%` | Recall: `69.15%` | ROC-AUC: `0.8717`)

*Note: Models are serialized to the `models/` directory using `joblib`.*

### Feature Importances (Gradient Boosting)
1. **Temperature** ($29.27\%$) — Primary symptom metric.
2. **Oxygen Level (SpO₂)** ($27.07\%$) — Crucial indicator of lung function/hypoxia.
3. **Breathing Difficulty** ($17.97\%$) — Major clinical severity indicator.
4. **Cough** ($11.58\%$) — Respiratory marker.
5. **Age** ($6.38\%$) — Major driver for high-risk complications.
6. **Diabetes** ($3.89\%$) and **Heart Disease** ($3.38\%$) — Comorbidities.
7. **Gender** ($0.46\%$) — Minimal predictive impact.

---

## 5. Power BI Dashboard Dataset & Setup Guide

The pre-processed and enriched dataset `data/powerbi_covid_dashboard_data.csv` is ready. To help you build a professional 3-page interactive report in Power BI Desktop, we have created step-by-step instructions and references inside the `dashboard/` directory:

1. 📘 **Assembly Guide**: [powerbi_dashboard_guide.md](file:///d:/projects/AI-Powered-COVID-Analytics-Dashboard/dashboard/powerbi_dashboard_guide.md) — Walkthrough of data load, settings, and page assemblies.
2. 📐 **Visual Grid Layout**: [dashboard_layout_plan.md](file:///d:/projects/AI-Powered-COVID-Analytics-Dashboard/dashboard/dashboard_layout_plan.md) — Blueprint for visual placement, sizing, and colors.
3. 🧮 **DAX Formulas**: [powerbi_measures_dax.txt](file:///d:/projects/AI-Powered-COVID-Analytics-Dashboard/dashboard/powerbi_measures_dax.txt) — Raw DAX codes for KPI card integrations.

> [!WARNING]
> **SIMULATION NOTICE FOR MEDICAL DATA ETHICS**
> The columns `State`, `Registration_Date`, `Patient_Outcome` (Recovered vs Deceased outcomes), and the resulting mortality rates are **simulated demo fields** generated programmatically during the preprocessing step. They are intended for demonstration, dashboard design, and modeling logic exercises, and should **not** be presented as real-world medical statistics.

### Enriched Columns Description:
1. **Patient Outcome (Deceased / Recovered)**:
   * Patients who tested COVID negative are marked as `Not Applicable`.
   * For COVID positive patients: if they are in a critical state (Oxygen levels $< 88\%$ or Age $> 75$ with comorbidities), they are assigned a $35\%$ probability of death to simulate mortality rates. Non-critical positives have a $99.5\%$ recovery rate.
2. **Registration Date**: Randomly assigned over the last 6 months (Jan 1, 2026 to June 21, 2026) with a seasonal wave peak during March and April to enable **Monthly Timeline Trends** in Power BI.
3. **State/Location**: Randomly assigned US states (`California`, `Texas`, `New York`, etc.) based on population density weights to support **Map-based Geo Visualizations** in Power BI.
4. **KPI columns**: Exposes `Total_Cases`, `Total_COVID_Positive`, `Total_Deceased`, and `Total_Recovered` as integer indicators (0/1) to simplify DAX measures in Power BI.

---

## 6. Streamlit Web App Features

The Streamlit web application `app/streamlit_app.py` features a custom premium health-tech UI:
* **Interactive Form Panel**: Sliders and dropdown selectors to quickly adjust patient vitals and demographics.
* **Risk Gauge**: A visual gauge dial illustrating infection risk percentage.
* **Status Banners**: Dynamic color tags indicating Risk Category (Green for Low Risk, Amber for Medium Risk, Red for High Risk).
* **Clinical Safety Overrides**: Automatically upgrades patient to High Risk if SpO₂ drops below $90\%$ or if temperature exceeds $102.5^\circ\text{F}$ for medical safety.
* **Risk Drivers Breakdown**: Displays a Plotly horizontal bar chart showing exactly which metrics are contributing the most to the patient's risk.
* **Comparative Population Plot**: Renders a scatter plot showing where the current patient stands compared to the rest of the database.

---

## 7. How to Setup and Run the Platform

### Step 1: Install Dependencies
Run the command to install packages:
```bash
pip install -r requirements.txt
```
*(Note: If you are using the virtual environment `env` provided in this workspace, packages are already configured.)*

### Step 2: Run the Streamlit Application (Directly)
Because the pre-trained models and cleaned datasets are already included in the repository, you can run the Streamlit app immediately without any extra setup:
```bash
streamlit run app/streamlit_app.py
```
This starts the local web server, typically accessible at `http://localhost:8501`.

### Step 3: Retraining the Model & Data Regeneration (Optional)
If you want to retrain the machine learning models or regenerate the datasets:
1. Open and run the Jupyter notebook [covid_risk_prediction.ipynb](file:///d:/projects/AI-Powered-COVID-Analytics-Dashboard/notebooks/covid_risk_prediction.ipynb) in your preferred environment.
2. The notebook will automatically output the trained models to the `models/` folder and datasets to the `data/` folder.

---

## 8. Business & Healthcare Insights
* **Clinical Resource Triage**: Patients flagged as High Risk with Low Oxygen Levels should be prioritized for immediate clinical beds and oxygen concentrators.
* **Vitals Over Symptoms**: High body temperatures and low oxygen levels are far stronger predictors of active COVID cases ($56.3\%$ combined impact) than comorbidities like Diabetes ($3.89\%$).
* **Age Aggravation**: Patients above age 60 with underlying heart conditions require preventive teleconsultations even if their immediate symptoms appear mild.

---

## 9. Future Improvements
1. **Integration of Real-Time Health Feeds**: Connect the Streamlit form to IoT-enabled pulse oximeters and smart thermometers.
2. **SHAP Explanations**: Integrate SHAP (SHapley Additive exPlanations) directly into the Streamlit app to explain multi-feature interactions.
3. **Hyperparameter Tuning**: Run grid searches on Gradient Boosting parameters to further push F1-score beyond $76\%$.
