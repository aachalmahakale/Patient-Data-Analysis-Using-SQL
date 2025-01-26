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
query_conditions = """
    SELECT description, COUNT(*) AS occurrences 
    FROM conditions 
    GROUP BY description 
    ORDER BY occurrences DESC 
    LIMIT 10;
"""
df_conditions = pd.read_sql(query_conditions, conn)

# Display condition occurrences bar chart
st.subheader("Top 10 Common Conditions")
st.bar_chart(df_conditions.set_index("description"))

# Query to fetch allergy occurrences
query_allergies = """
    SELECT description, COUNT(*) AS occurrences
    FROM allergies
    GROUP BY description
    ORDER BY occurrences DESC
    LIMIT 10;
"""
df_allergies = pd.read_sql(query_allergies, conn)

# Display allergy occurrences bar chart
st.subheader("Top 10 Common Allergies")
st.bar_chart(df_allergies.set_index("description"))

# Query to fetch medication usage
query_medications = """
    SELECT description, COUNT(*) AS occurrences
    FROM medications
    GROUP BY description
    ORDER BY occurrences DESC
    LIMIT 10;
"""
df_medications = pd.read_sql(query_medications, conn)

# Display medication usage bar chart
st.subheader("Top 10 Common Medications")
st.bar_chart(df_medications.set_index("description"))

# Query to fetch immunization records
query_immunizations = """
    SELECT description, COUNT(*) AS occurrences
    FROM immunizations
    GROUP BY description
    ORDER BY occurrences DESC
    LIMIT 10;
"""
df_immunizations = pd.read_sql(query_immunizations, conn)

# Display immunization records bar chart
st.subheader("Top 10 Immunizations")
st.bar_chart(df_immunizations.set_index("description"))

# Query to fetch device usage
query_devices = """
    SELECT description, COUNT(*) AS occurrences
    FROM devices
    GROUP BY description
    ORDER BY occurrences DESC
    LIMIT 10;
"""
df_devices = pd.read_sql(query_devices, conn)

# Display device usage bar chart
st.subheader("Top 10 Medical Devices")
st.bar_chart(df_devices.set_index("description"))

conn.close()
