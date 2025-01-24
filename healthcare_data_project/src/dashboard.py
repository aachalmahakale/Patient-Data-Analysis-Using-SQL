import streamlit as st
import pandas as pd
import mysql.connector

st.title("Healthcare Data Insights")

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aachal@156",
    database="healthcare_db"
)

# Query to fetch condition occurrences
query = """
    SELECT description, COUNT(*) AS occurrences 
    FROM conditions 
    GROUP BY description 
    ORDER BY occurrences DESC 
    LIMIT 10;
"""
df = pd.read_sql(query, conn)

# Display results
st.bar_chart(df.set_index("description"))

conn.close()
