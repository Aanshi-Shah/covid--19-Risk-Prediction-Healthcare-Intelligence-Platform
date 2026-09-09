-- =====================================================================
-- COVID-19 PANDEMIC INTELLIGENCE PLATFORM - MYSQL SCHEMA & INSIGHTS
-- =====================================================================
-- This SQL file provides:
-- 1. Database & Table Schema Creation
-- 2. Bulk Load Setup reference
-- 3. High-Value Clinical and Business Insight Queries
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. DATABASE & SCHEMA SETUP
-- ---------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS covid_analytics;
USE covid_analytics;

-- Create Patients Table
CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    temperature_f DECIMAL(5,2) NOT NULL,
    oxygen_level INT NOT NULL,
    minor_cough VARCHAR(3) NOT NULL,
    cold VARCHAR(3) NOT NULL,
    dry_cough VARCHAR(3) NOT NULL,
    loss_of_smell VARCHAR(3) NOT NULL,
    loss_of_taste VARCHAR(3) NOT NULL,
    headache VARCHAR(3) NOT NULL,
    heart_disease VARCHAR(3) NOT NULL,
    diabetes VARCHAR(3) NOT NULL,
    breathing_difficulty VARCHAR(3) NOT NULL,
    covid_result VARCHAR(3) NOT NULL,
    gender_encoded INT NOT NULL,
    cough VARCHAR(3) NOT NULL,
    cough_encoded INT NOT NULL,
    breathing_difficulty_encoded INT NOT NULL,
    heart_disease_encoded INT NOT NULL,
    diabetes_encoded INT NOT NULL,
    target_encoded INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optimize queries by adding indices on key analytical dimensions
CREATE INDEX idx_covid_result ON patients(covid_result);
CREATE INDEX idx_age_gender ON patients(age, gender);
CREATE INDEX idx_vitals ON patients(oxygen_level, temperature_f);
CREATE INDEX idx_comorbidities ON patients(heart_disease, diabetes);

-- ---------------------------------------------------------------------
-- 2. DATA IMPORT REFERENCE (LOCAL DATA LOAD EXAMPLE)
-- ---------------------------------------------------------------------
-- If importing via MySQL Command Line Client:
--
-- LOAD DATA LOCAL INFILE '/path/to/cleaned_covid_data.csv'
-- INTO TABLE patients
-- FIELDS TERMINATED BY ',' 
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES
-- (patient_id, patient_name, age, gender, temperature_f, oxygen_level, 
--  minor_cough, cold, dry_cough, loss_of_smell, loss_of_taste, headache, 
--  heart_disease, diabetes, breathing_difficulty, covid_result, gender_encoded, 
--  cough, cough_encoded, breathing_difficulty_encoded, heart_disease_encoded, 
--  diabetes_encoded, target_encoded);


-- =====================================================================
-- 3. CLINICAL & BUSINESS INSIGHT QUERIES
-- =====================================================================

-- QUERY 1: Triage Priority List (Critical Vitals Audit)
-- Insights: Identify patients with critical vitals who require immediate clinical triage
-- (Hypoxia SpO2 < 90% or Severe Fever >= 102.5°F) sorted by severity.
SELECT 
    patient_id,
    patient_name,
    age,
    gender,
    oxygen_level,
    temperature_f,
    breathing_difficulty,
    covid_result,
    CASE 
        WHEN oxygen_level < 90 AND temperature_f >= 102.5 THEN 'CRITICAL (Priority 1)'
        WHEN oxygen_level < 90 THEN 'HYPOXIA (Priority 2)'
        WHEN temperature_f >= 102.5 THEN 'HIGH FEVER (Priority 3)'
        ELSE 'STABLE'
    END AS triage_status
FROM patients
WHERE oxygen_level < 90 OR temperature_f >= 102.5
ORDER BY oxygen_level ASC, temperature_f DESC
LIMIT 50;


-- QUERY 2: Demographics COVID-19 Positive Rates
-- Insights: Analyze COVID-19 positive ratios by age groups and gender to identify vulnerable population cohorts.
SELECT 
    CASE 
        WHEN age < 18 THEN 'Pediatric (<18)'
        WHEN age BETWEEN 18 AND 35 THEN 'Young Adult (18-35)'
        WHEN age BETWEEN 36 AND 60 THEN 'Middle Aged (36-60)'
        ELSE 'Senior (60+)'
    END AS age_cohort,
    gender,
    COUNT(*) AS total_screened,
    SUM(target_encoded) AS total_positive,
    ROUND((SUM(target_encoded) / COUNT(*)) * 100, 2) AS positive_rate_pct
FROM patients
GROUP BY age_cohort, gender
ORDER BY age_cohort, positive_rate_pct DESC;


-- QUERY 3: Comorbidity Multi-Risk Matrix
-- Insights: Show how presence of single or combined comorbidities (Diabetes & Heart Disease) 
-- correlates with positive COVID outcomes.
SELECT 
    heart_disease,
    diabetes,
    COUNT(*) AS patient_count,
    SUM(target_encoded) AS covid_positive_count,
    ROUND((SUM(target_encoded) / COUNT(*)) * 100, 2) AS positive_rate_pct,
    ROUND(AVG(oxygen_level), 1) AS avg_oxygen_saturation,
    ROUND(AVG(temperature_f), 1) AS avg_body_temperature
FROM patients
GROUP BY heart_disease, diabetes
ORDER BY positive_rate_pct DESC;


-- QUERY 4: Symptom Prevalence & COVID Result Correlation
-- Insights: Assess symptom frequencies among COVID-positive cases to identify the strongest predictors.
SELECT 
    symptom_name,
    total_occurrences_in_positive,
    ROUND((total_occurrences_in_positive / total_positive_patients) * 100, 2) AS prevalence_in_positives_pct
FROM (
    SELECT 
        (SELECT COUNT(*) FROM patients WHERE target_encoded = 1) AS total_positive_patients,
        'Breathing Difficulty' AS symptom_name, SUM(CASE WHEN breathing_difficulty = 'Yes' AND target_encoded = 1 THEN 1 ELSE 0 END) AS total_occurrences_in_positive UNION ALL
        'Dry Cough' AS symptom_name, SUM(CASE WHEN dry_cough = 'Yes' AND target_encoded = 1 THEN 1 ELSE 0 END) AS total_occurrences_in_positive UNION ALL
        'Loss of Smell' AS symptom_name, SUM(CASE WHEN loss_of_smell = 'Yes' AND target_encoded = 1 THEN 1 ELSE 0 END) AS total_occurrences_in_positive UNION ALL
        'Loss of Taste' AS symptom_name, SUM(CASE WHEN loss_of_taste = 'Yes' AND target_encoded = 1 THEN 1 ELSE 0 END) AS total_occurrences_in_positive UNION ALL
        'Headache' AS symptom_name, SUM(CASE WHEN headache = 'Yes' AND target_encoded = 1 THEN 1 ELSE 0 END) AS total_occurrences_in_positive UNION ALL
        'Cold' AS symptom_name, SUM(CASE WHEN cold = 'Yes' AND target_encoded = 1 THEN 1 ELSE 0 END) AS total_occurrences_in_positive
    FROM patients
) AS symptom_stats
ORDER BY prevalence_in_positives_pct DESC;


-- QUERY 5: Clinical Safety Override Audit
-- Insights: Audit potential override cases—patients whose general symptoms did not yield positive COVID
-- but presented clinical red-flags (Oxygen levels below 90% SpO2 or body temp >= 102.5 F).
SELECT 
    covid_result,
    COUNT(*) AS total_patients,
    SUM(CASE WHEN oxygen_level < 90 THEN 1 ELSE 0 END) AS hypoxia_cases,
    SUM(CASE WHEN temperature_f >= 102.5 THEN 1 ELSE 0 END) AS high_fever_cases,
    SUM(CASE WHEN oxygen_level < 90 OR temperature_f >= 102.5 THEN 1 ELSE 0 END) AS total_clinical_overrides_needed,
    ROUND((SUM(CASE WHEN oxygen_level < 90 OR temperature_f >= 102.5 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS override_ratio_pct
FROM patients
GROUP BY covid_result;


-- QUERY 6: Monthly Infection Trend & Average Vitals Summary
-- Insights: Track historical patient trends (mocked by Patient ID chronological sequence) to view
-- progress rates and changes in average patient baseline metrics.
SELECT 
    LEFT(patient_id, 8) AS batch_group,
    COUNT(*) AS patients_screened,
    SUM(target_encoded) AS positive_cases,
    ROUND(AVG(oxygen_level), 2) AS batch_avg_spo2,
    ROUND(AVG(temperature_f), 2) AS batch_avg_temp
FROM patients
GROUP BY batch_group
ORDER BY batch_group ASC;
