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

conn.close()