
import mysql.connector
import pandas as pd

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aachal@156",
    database="healthcare_db"
)

# Query to generate health condition reports
query = """
    SELECT description, COUNT(*) AS occurrences 
    FROM conditions 
    GROUP BY description 
    ORDER BY occurrences DESC;
"""

df = pd.read_sql(query, conn)

# Export the report to CSV
output_path = '../data/common_conditions_report.csv'
df.to_csv(output_path, index=False)
print(f"Report exported to {output_path}")


# query to generate most common allergies
allergies_query = """
    SELECT description, COUNT(*) AS count
    FROM allergies
    GROUP BY description
    ORDER BY count DESC;
"""
df_allergies = pd.read_sql(allergies_query, conn)
df_allergies.to_csv('../data/common_allergies_report.csv', index=False)

# query to analyse medication usage
medications_query = """
    SELECT description, COUNT(*) AS count
    FROM medications
    GROUP BY description
    ORDER BY count DESC;
"""
df_medications = pd.read_sql(medications_query, conn)
df_medications.to_csv('../data/medications_report.csv', index=False)

#query to analyse immunization data
immunizations_query = """
    SELECT patient, COUNT(*) AS immunization_count
    FROM immunizations
    GROUP BY patient
    ORDER BY immunization_count DESC;
"""
df_immunizations = pd.read_sql(immunizations_query, conn)
df_immunizations.to_csv('../data/immunizations_report.csv', index=False)

#query for device usage
devices_query = """
    SELECT description, COUNT(*) AS count
    FROM devices
    GROUP BY description
    ORDER BY count DESC;
"""
df_devices = pd.read_sql(devices_query, conn)
df_devices.to_csv('../data/devices_report.csv', index=False)















conn.close()
