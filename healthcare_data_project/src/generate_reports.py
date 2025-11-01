"""
Healthcare Data Report Generator
Generates CSV reports from healthcare database
"""

import pandas as pd
from mysql.connector import Error
from db_config import get_db_connection
import os

# Create data directory if it doesn't exist
DATA_DIR = '../data'
os.makedirs(DATA_DIR, exist_ok=True)

def generate_report(query, output_filename, report_name):
    """
    Generic function to generate and export reports
    
    Args:
        query (str): SQL query to execute
        output_filename (str): Name of the output CSV file
        report_name (str): Human-readable name of the report
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        
        output_path = os.path.join(DATA_DIR, output_filename)
        df.to_csv(output_path, index=False)
        print(f"✅ {report_name} exported to {output_path}")
        return True
        
    except Error as e:
        print(f"❌ Error generating {report_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in {report_name}: {e}")
        return False

def main():
    """Generate all healthcare reports"""
    print("Starting report generation...\n")
    
    # Report 1: Health Conditions
    query_conditions = """
        SELECT description, COUNT(*) AS occurrences 
        FROM conditions 
        GROUP BY description 
        ORDER BY occurrences DESC;
    """
    generate_report(query_conditions, 'common_conditions_report.csv', 'Common Conditions Report')
    
    # Report 2: Common Allergies
    query_allergies = """
        SELECT description, COUNT(*) AS count
        FROM allergies
        GROUP BY description
        ORDER BY count DESC;
    """
    generate_report(query_allergies, 'common_allergies_report.csv', 'Common Allergies Report')
    
    # Report 3: Medication Usage
    query_medications = """
        SELECT description, COUNT(*) AS count
        FROM medications
        GROUP BY description
        ORDER BY count DESC;
    """
    generate_report(query_medications, 'medications_report.csv', 'Medications Report')
    
    # Report 4: Immunization Data
    query_immunizations = """
        SELECT patient, COUNT(*) AS immunization_count
        FROM immunizations
        GROUP BY patient
        ORDER BY immunization_count DESC;
    """
    generate_report(query_immunizations, 'immunizations_report.csv', 'Immunizations Report')
    
    # Report 5: Device Usage
    query_devices = """
        SELECT description, COUNT(*) AS count
        FROM devices
        GROUP BY description
        ORDER BY count DESC;
    """
    generate_report(query_devices, 'devices_report.csv', 'Devices Report')
    
    print("\n✨ Report generation completed!")

if __name__ == "__main__":
    main()

