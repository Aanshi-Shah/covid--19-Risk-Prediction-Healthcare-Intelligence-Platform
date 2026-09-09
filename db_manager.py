import os
import sys
import csv
import mysql.connector
from mysql.connector import Error

def get_connection(host, user, password, database=None):
    """Establishes connection to MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database_and_tables(host, user, password):
    """Creates the database and schema for patients records."""
    conn = get_connection(host, user, password)
    if not conn:
        print("Failed to connect to MySQL to create database.")
        return False
        
    try:
        cursor = conn.cursor()
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS covid_analytics;")
        print("Database 'covid_analytics' created or verified.")
        
        # Switch to database
        cursor.execute("USE covid_analytics;")
        
        # Drop table if exists to reload cleanly
        cursor.execute("DROP TABLE IF EXISTS patients;")
        
        # Create Table
        create_table_query = """
        CREATE TABLE patients (
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
        """
        cursor.execute(create_table_query)
        print("Table 'patients' created successfully.")
        
        # Add index optimizations
        cursor.execute("CREATE INDEX idx_covid_result ON patients(covid_result);")
        cursor.execute("CREATE INDEX idx_age_gender ON patients(age, gender);")
        cursor.execute("CREATE INDEX idx_vitals ON patients(oxygen_level, temperature_f);")
        
        conn.commit()
        return True
    except Error as e:
        print(f"Error during schema creation: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def import_csv_to_mysql(host, user, password, csv_path):
    """Imports rows from CSV into MySQL database."""
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return False
        
    print(f"Reading dataset from: {csv_path}")
    
    conn = get_connection(host, user, password, database="covid_analytics")
    if not conn:
        print("Failed to connect to MySQL to import data.")
        return False
        
    try:
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO patients (
            patient_id, patient_name, age, gender, temperature_f, oxygen_level,
            minor_cough, cold, dry_cough, loss_of_smell, loss_of_taste, headache,
            heart_disease, diabetes, breathing_difficulty, covid_result, gender_encoded,
            cough, cough_encoded, breathing_difficulty_encoded, heart_disease_encoded,
            diabetes_encoded, target_encoded
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Load CSV lines
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header row
            
            rows = []
            for row in reader:
                if not row:
                    continue
                # Map raw values and perform type conversions
                row_tuple = (
                    row[0],  # patient_id
                    row[1],  # patient_name
                    int(row[2]), # age
                    row[3],  # gender
                    float(row[4]), # temp_f
                    int(row[5]), # oxygen_level
                    row[6],  # minor_cough
                    row[7],  # cold
                    row[8],  # dry_cough
                    row[9],  # loss_of_smell
                    row[10], # loss_of_taste
                    row[11], # headache
                    row[12], # heart_disease
                    row[13], # diabetes
                    row[14], # breathing_difficulty
                    row[15], # covid_result
                    int(row[16]), # gender_encoded
                    row[17], # cough
                    int(row[18]), # cough_encoded
                    int(row[19]), # breathing_diff_encoded
                    int(row[20]), # heart_disease_encoded
                    int(row[21]), # diabetes_encoded
                    int(row[22])  # target_encoded
                )
                rows.append(row_tuple)
                
        # Batch insert for high performance
        cursor.executemany(insert_query, rows)
        conn.commit()
        print(f"Successfully imported {len(rows)} records into MySQL database table 'patients'.")
        return True
    except Error as e:
        print(f"Error during CSV import: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def run_business_queries(host, user, password):
    """Executes the business insights queries and prints formatted results to the terminal."""
    conn = get_connection(host, user, password, database="covid_analytics")
    if not conn:
        print("Failed to connect to MySQL to run queries.")
        return
        
    try:
        cursor = conn.cursor()
        
        # Query 1: Critical Vitals Triage Priority
        print("\n" + "="*80)
        print(" CLINICAL TRIAGE REPORT: PATIENTS WITH CRITICAL VITALS")
        print("="*80)
        triage_query = """
        SELECT 
            patient_id, patient_name, age, gender, oxygen_level, temperature_f, covid_result,
            CASE 
                WHEN oxygen_level < 90 AND temperature_f >= 102.5 THEN 'CRITICAL (Priority 1)'
                WHEN oxygen_level < 90 THEN 'HYPOXIA (Priority 2)'
                WHEN temperature_f >= 102.5 THEN 'HIGH FEVER (Priority 3)'
                ELSE 'STABLE'
            END AS triage_status
        FROM patients
        WHERE oxygen_level < 90 OR temperature_f >= 102.5
        ORDER BY oxygen_level ASC, temperature_f DESC
        LIMIT 10;
        """
        cursor.execute(triage_query)
        headers = ["ID", "Name", "Age", "Gender", "SpO2 %", "Temp (°F)", "COVID", "Triage Status"]
        print(f"{headers[0]:<12} {headers[1]:<12} {headers[2]:<5} {headers[3]:<8} {headers[4]:<8} {headers[5]:<10} {headers[6]:<6} {headers[7]}")
        print("-"*80)
        for row in cursor.fetchall():
            print(f"{row[0]:<12} {row[1]:<12} {row[2]:<5} {row[3]:<8} {row[4]:<8} {row[5]:<10.1f} {row[6]:<6} {row[7]}")
            
        # Query 2: Demographics Infection Rates
        print("\n" + "="*80)
        print(" POPULATION DEMOGRAPHIC ANALYSIS & INFECTION RATES")
        print("="*80)
        demo_query = """
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
        """
        cursor.execute(demo_query)
        print(f"{'Age Cohort':<25} {'Gender':<10} {'Screened':<10} {'Positive':<10} {'Infection Rate (%)'}")
        print("-"*80)
        for row in cursor.fetchall():
            print(f"{row[0]:<25} {row[1]:<10} {row[2]:<10} {row[3]:<10} {row[4]:.2f}%")

        # Query 3: Comorbidity Multi-Risk Matrix
        print("\n" + "="*80)
        print(" COMORBIDITY RISK MATRIX & OUTCOMES")
        print("="*80)
        comorbid_query = """
        SELECT 
            heart_disease,
            diabetes,
            COUNT(*) AS patient_count,
            SUM(target_encoded) AS covid_positive_count,
            ROUND((SUM(target_encoded) / COUNT(*)) * 100, 2) AS positive_rate_pct,
            ROUND(AVG(oxygen_level), 1) AS avg_oxygen_saturation
        FROM patients
        GROUP BY heart_disease, diabetes
        ORDER BY positive_rate_pct DESC;
        """
        cursor.execute(comorbid_query)
        print(f"{'Heart Disease':<15} {'Diabetes':<15} {'Total Patients':<15} {'COVID Positive':<15} {'Infection Rate':<15} {'Avg SpO2'}")
        print("-"*80)
        for row in cursor.fetchall():
            print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15} {row[3]:<15} {row[4]:.1f}%          {row[5]:.1f}%")

    except Error as e:
        print(f"Error executing analytics queries: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="COVID Analytics Platform MySQL Schema Creator & Loader")
    parser.add_argument("--host", default="localhost", help="MySQL Database Host (default: localhost)")
    parser.add_argument("--user", default="root", help="MySQL User (default: root)")
    parser.add_argument("--password", default="", help="MySQL Password (default: empty)")
    parser.add_argument("--csv", default="data/cleaned_covid_data.csv", help="Path to Cleaned CSV file")
    parser.add_argument("--setup", action="store_true", help="Setup Database schema & tables")
    parser.add_argument("--import-data", action="store_true", help="Import CSV data into MySQL")
    parser.add_argument("--queries", action="store_true", help="Run analytical business queries")
    
    args = parser.parse_args()
    
    if not (args.setup or args.import_data or args.queries):
        parser.print_help()
        print("\nExample usage:")
        print("  python db_manager.py --setup --import-data --queries --password YOUR_PASSWORD")
        sys.exit(0)
        
    if args.setup:
        print("Setting up database and table schema...")
        success = create_database_and_tables(args.host, args.user, args.password)
        if not success:
            sys.exit(1)
            
    if args.import_data:
        print("Importing CSV data...")
        success = import_csv_to_mysql(args.host, args.user, args.password, args.csv)
        if not success:
            sys.exit(1)
            
    if args.queries:
        print("Running SQL Analytical Queries...")
        run_business_queries(args.host, args.user, args.password)
