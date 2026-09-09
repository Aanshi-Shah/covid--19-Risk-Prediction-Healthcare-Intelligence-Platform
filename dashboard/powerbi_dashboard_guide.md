# Power BI Dashboard Setup Guide

This step-by-step guide explains how to import the preprocessed and enriched dataset `data/powerbi_covid_dashboard_data.csv` into **Power BI Desktop** and build a 3-page interactive intelligence dashboard.

> [!IMPORTANT]
> **SIMULATION NOTICE FOR MEDICAL DATA ETHICS**
> The fields `State`, `Registration_Date`, `Patient_Outcome` (Recovered vs Deceased outcomes), and the resulting mortality rates are **simulated demo fields** generated programmatically during the preprocessing step. They are intended for demonstration, dashboard design, and modeling logic exercises, and should **not** be presented as real-world medical statistics.

---

## 🛠️ Step 1: Data Import and Transformation

1. Launch **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Locate and select the file: `data/powerbi_covid_dashboard_data.csv`.
4. In the preview window, click **Transform Data** to open the **Power Query Editor**.
5. Verify and adjust the following data types:
   * `Patient_ID` $\rightarrow$ Text
   * `Patient_Name` $\rightarrow$ Text
   * `Age` $\rightarrow$ Whole Number
   * `Gender` $\rightarrow$ Text
   * `Body_Temperature_F` $\rightarrow$ Decimal Number
   * `Oxygen_Level` $\rightarrow$ Whole Number
   * `Registration_Date` $\rightarrow$ Date
   * `COVID_Positive_Flag` $\rightarrow$ Whole Number
   * `Total_Cases` $\rightarrow$ Whole Number
   * All symptom and comorbidity columns (`Dry_Cough`, `Diabetes`, `Breathing_Difficulty`, etc.) $\rightarrow$ Text
6. Click **Close & Apply** in the Home ribbon to load the dataset.

---

## 📊 Step 2: Establish DAX Measures

To keep the model clean, create a dedicated table for calculations:
1. In the Home ribbon, click **Enter Data**. Name the table `_Measures` and click Load.
2. Right-click the new `_Measures` table and select **New Measure** to create each metric.
3. Open [powerbi_measures_dax.txt](file:///d:/projects/AI-Powered-COVID-Analytics-Dashboard/dashboard/powerbi_measures_dax.txt) and copy/paste the formulas.
4. Delete the empty column `Column1` in the `_Measures` table to turn it into a calculation table.

---

## 🎨 Step 3: Design Dashboard Pages

### Page 1: Executive Overview
*Provides a baseline analysis of case counts and patient demographics.*

#### 1. Setup KPIs (Card Visuals)
* **Total Patients Card**: Drag `[Total Patients]` measure. Title: "Total Screened".
* **Positive Cases Card**: Drag `[Positive Cases]` measure. Title: "Confirmed Cases".
* **Recovery Rate Card**: Drag `[Recovery Rate]` measure. Format as percentage (`0.0%`). Title: "Recovery Rate".
* **Critical Outcome Rate Card**: Drag `[Critical Outcome Rate]` measure. Format as percentage (`0.0%`). Title: "Critical Rate (Simulated)".

#### 2. Visualizations
* **Monthly Cases Trend (Line Chart)**:
  * **X-Axis**: `Registration_Date` (Grouped by Month/Year)
  * **Y-Axis**: `[Total Patients]` or `[Positive Cases]`
  * **Formatting**: Enable data markers, set color to Clinical Blue.
* **Gender Analysis (Donut Chart)**:
  * **Legend**: `Gender`
  * **Values**: `[Positive Cases]`
  * **Formatting**: Show details label as Category + Percent of Total.
* **Age Distribution (Clustered Column Chart)**:
  * Right-click `Age` in fields, select **New Group** $\rightarrow$ Group type: Bins, Size: 10.
  * **X-Axis**: `Age (bins)`
  * **Y-Axis**: `[Positive Cases]`
* **Diagnosis Split (Clustered Column Chart)**:
  * **X-Axis**: `COVID_Result`
  * **Y-Axis**: `[Total Patients]`
  * **Formatting**: Color Negative cases Green, Positive cases Crimson.

---

### Page 2: Geographic Analysis
*Maps the regional spread and tracks local risk segments using simulated location fields.*

#### 1. Visualizations
* **State-wise Cases Map (Bubble Map)**:
  * **Location**: `State`
  * **Bubble Size**: `[Positive Cases]`
  * **Tooltip**: `[Recovery Rate]`, `[Critical Outcome Rate]`
  * *Note: Go to Options > Security > Enable Map and Filled Map visuals if it does not display.*
* **Top 5 States by Positive Cases (Horizontal Bar Chart)**:
  * **Y-Axis**: `State`
  * **X-Axis**: `[Positive Cases]`
  * **Filters Pane**: Drag `State` into filters, choose **Top N**, N = 5, by value `[Positive Cases]`.
* **State Outcome Metrics Table**:
  * **Columns**: `State`, `[Total Patients]`, `[Positive Cases]`, `[Recovery Rate]`, `[Critical Outcome Rate]`
  * **Formatting**: Enable conditional formatting data bars for `[Positive Cases]`.
* **State-wise Risk Mix (Stacked Column Chart)**:
  * **X-Axis**: `State`
  * **Y-Axis**: `[Total Patients]`
  * **Legend**: `Risk_Category` (High, Medium, Low)
  * **Colors**: High Risk (Crimson), Medium Risk (Amber), Low Risk (Forest Green).

---

### Page 3: Risk Intelligence
*Drills down into medical features, symptom impact, and model-derived high-risk metrics.*

#### 1. Visualizations
* **Comorbidity Impact (Clustered Column Charts)**:
  * **Chart A (Diabetes)**: X-Axis = `Diabetes`, Y-Axis = `[Total Patients]`, Legend = `COVID_Result`
  * **Chart B (Heart Disease)**: X-Axis = `Heart_Disease`, Y-Axis = `[Total Patients]`, Legend = `COVID_Result`
* **Oxygen Level Distribution (Area Chart)**:
  * **X-Axis**: `Oxygen_Level`
  * **Y-Axis**: `[Positive Cases]`
  * **Formatting**: Set line color to Crimson. Notice the spike in cases at low oxygen levels.
* **Temperature Distribution (Area Chart)**:
  * **X-Axis**: `Body_Temperature_F` (Binned or raw value)
  * **Y-Axis**: `[Positive Cases]`
  * **Formatting**: Set line color to Orange.
* **Breathing Difficulty Impact (Donut Chart)**:
  * **Legend**: `Breathing_Difficulty`
  * **Values**: `[Positive Cases]`
* **High Risk Segments Matrix**:
  * **Rows**: `Age (bins)`
  * **Columns**: `Risk_Category`
  * **Values**: `[Total Patients]`
  * **Formatting**: Turn on conditional background color scales (Heatmap).

---

## 🩺 Step 4: Add Filter Panes & Slicers
Add a collapsible filter pane or header slicers to all pages:
* **Date Slicer**: `Registration_Date` (Between slicer)
* **Symptom Slicer**: `Breathing_Difficulty` (Dropdown)
* **Comorbidities**: `Diabetes` / `Heart_Disease` (List checkboxes)
