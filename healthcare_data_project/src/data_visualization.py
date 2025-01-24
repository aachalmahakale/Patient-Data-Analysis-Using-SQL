import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector  # For MySQL, use psycopg2 for PostgreSQL

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aachal@156",
    database="healthcare_db"
)

# Query data to analyze age distribution
query1 = """
    SELECT YEAR(CURDATE()) - YEAR(birthdate) AS age, 
           COUNT(*) AS count 
    FROM patients 
    GROUP BY age 
    ORDER BY age;
"""
df = pd.read_sql(query1, conn)

# Visualize patient age distribution
plt.figure(figsize=(10, 6))
plt.bar(df['age'], df['count'], color='skyblue')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.title('Patient Age Distribution')
plt.grid(axis='y')
plt.show()

conn.close()
