# Power BI Dashboard Visual Layout Plan

This blueprint outlines the page sizing, color styles, visual alignments, and design grid for the COVID-19 Pandemic Intelligence Dashboard in Power BI Desktop.

---

## 🎨 Style Guide & Visual Theme

### 1. Sizing
* **Page Dimensions**: Widescreen (16:9) ratio — `1280px x 720px` (or standard Power BI Canvas size).
* **Grid Layout**: 12-column dynamic modular grid with `15px` gutters.

### 2. Color Palette
To match modern UI trends (Sleek Dark/Light hybrid):
* **Background Canvas**: Ice Grey (`#F4F6F9`)
* **Visual Card Background**: Pure White (`#FFFFFF`) with rounded borders (`8pt`) and subtle shadows.
* **Primary / Text Color**: Dark Indigo Slate (`#1A202C`)
* **Clinical Accents**:
  * **Positive / Selected**: Primary Blue (`#0F62FE`)
  * **Low Risk / Recovery**: Forest Green (`#2F855A`)
  * **Medium Risk / Symptomatic**: Safety Amber (`#DD6B20`)
  * **High Risk / Critical Outcome**: Emergency Crimson (`#E53E3E`)

---

## 📐 Page-by-Page Visual Grid Blueprint

### Page 1: Executive Overview
*Focuses on high-level pandemic indicators and demographics.*

```
+------------------------------------------------------------------------------------------+
|  [Logo]  COVID-19 Pandemic Executive Intelligence Dashboard                  [Filters]   |
+------------------------------------------------------------------------------------------+
|  [KPI Card: Patients]  [KPI Card: Positives]  [KPI: Recovery Rate]  [KPI: Critical Rate] |
+------------------------------------------------------------------------------------------+
|  [Monthly Cases Trend (Line)]              |  [COVID Pos vs Neg (Clustered Column)]      |
|  X-Axis: Registration_Date (Month)         |  X-Axis: COVID_Positive_Flag (Yes/No)       |
|  Y-Axis: Total_Cases                       |  Y-Axis: Count of Patients                  |
|                                            |                                             |
+--------------------------------------------+---------------------------------------------+
|  [Age Analysis (Stacked Bar)]              |  [Gender Analysis (Donut Chart)]            |
|  Y-Axis: Age (Grouped Bin or Slider)       |  Slices: Gender (Male / Female)             |
|  X-Axis: Total_COVID_Positive              |  Values: Total_COVID_Positive               |
+------------------------------------------------------------------------------------------+
```

---

### Page 2: Geographic Analysis
*Focuses on regional metrics across simulated locations. Map visual uses simulated data.*

```
+------------------------------------------------------------------------------------------+
|  🏥 Pandemic Regional Spread Dashboard                                       [State Slicer] |
+------------------------------------------------------------------------------------------+
|  [Filled/Bubble Map Visual]                |  [Top 5 States by Positives (Bar Chart)]    |
|  Location: State                           |  Y-Axis: State                              |
|  Bubble Size: Positive Cases               |  X-Axis: Positive Cases                     |
|  Color Saturation: Critical Outcome Rate   |                                             |
+--------------------------------------------+---------------------------------------------+
|  [State Outcome Metrics Table]                                                           |
|  Columns: State | Total Cases | Positive Cases | Recovery Rate | Critical Outcome Rate    |
|                                                                                          |
+------------------------------------------------------------------------------------------+
|  [State-wise Patient Risk Mix (Stacked Column Chart)]                                    |
|  X-Axis: State                                                                           |
|  Y-Axis: Total Patients                                                                  |
|  Legend: Risk_Category (Low, Medium, High)                                               |
+------------------------------------------------------------------------------------------+
```

---

### Page 3: Risk Intelligence
*Focuses on clinical factors, correlations, and patient vulnerability metrics.*

```
+------------------------------------------------------------------------------------------+
|  🧬 Clinical Risk Factor & Comorbidity Analysis                                           |
+------------------------------------------------------------------------------------------+
|  [Oxygen Saturation Distribution (Area)]   |  [Body Temperature Distribution (Area)]      |
|  X-Axis: Oxygen_Level                      |  X-Axis: Body_Temperature_F                 |
|  Y-Axis: Count of Positive Cases           |  Y-Axis: Count of Positive Cases           |
|                                            |                                             |
+--------------------------------------------+---------------------------------------------+
|  [Diabetes Impact (Clustered Column)]      |  [Heart Disease Impact (Clustered Column)]   |
|  X-Axis: Diabetes (Yes/No)                 |  X-Axis: Heart_Disease (Yes/No)             |
|  Legend: COVID_Positive_Flag               |  Legend: COVID_Positive_Flag               |
+--------------------------------------------+---------------------------------------------+
|  [Breathing Difficulty (Donut)]            |  [Vulnerability Matrix (Heatmap Table)]     |
|  Slices: Breathing_Difficulty (Yes/No)     |  Rows: Age Groups (Binned: <30, 30-60, 60+)  |
|  Values: Positive Cases                    |  Columns: Diabetes | Heart_Disease           |
|                                            |  Values: High Risk Patient %                |
+------------------------------------------------------------------------------------------+
```

---

## 📌 Formatting and UX Standards
1. **Title Alignment**: Keep titles left-aligned in all visual containers with a semi-bold `11pt` font size.
2. **Number Display**: Force short numbers (e.g. `1.2K` instead of `1231`) on chart data labels, but show full integers on KPI cards.
3. **Rates & Percentages**: Display all rates (`Recovery Rate`, `Critical Outcome Rate`, etc.) rounded to `1` decimal point with the `%` symbol.
4. **Data Warnings**: Add a footnote text block on **Pages 1 & 2** stating:
   > ⚠️ *Notice: Registration Date, States, Recoveries, and Critical Outcomes are simulated demo values generated by the data cleaning pipeline for modeling and Power BI display purposes.*
