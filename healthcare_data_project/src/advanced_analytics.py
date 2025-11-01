"""
Advanced Analytics Module
Provides predictive analytics and statistical insights for healthcare data
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from scipy import stats
from db_config import get_db_connection
from mysql.connector import Error
import warnings
warnings.filterwarnings('ignore')


class HealthcareAnalytics:
    """Advanced analytics for healthcare data"""
    
    def __init__(self):
        self.conn = None
        
    def get_connection(self):
        """Get database connection"""
        if not self.conn or not self.conn.is_connected():
            self.conn = get_db_connection()
        return self.conn
    
    def patient_risk_score(self):
        """
        Calculate patient risk scores based on conditions, medications, and age
        
        Returns:
            DataFrame: Patient risk analysis
        """
        try:
            conn = self.get_connection()
            
            query = """
                SELECT 
                    p.id,
                    CONCAT(p.first, ' ', p.last) AS patient_name,
                    YEAR(CURDATE()) - YEAR(p.birthdate) AS age,
                    p.gender,
                    COUNT(DISTINCT c.description) AS condition_count,
                    COUNT(DISTINCT m.description) AS medication_count,
                    COUNT(DISTINCT a.description) AS allergy_count
                FROM patients p
                LEFT JOIN conditions c ON p.id = c.patient AND c.stop IS NULL
                LEFT JOIN medications m ON p.id = m.patient
                LEFT JOIN allergies a ON p.id = a.patient
                GROUP BY p.id, patient_name, age, p.gender
                HAVING condition_count > 0 OR medication_count > 0
                ORDER BY condition_count DESC, medication_count DESC
                LIMIT 100;
            """
            
            df = pd.read_sql(query, conn)
            
            # Calculate risk score (0-100)
            df['risk_score'] = (
                (df['condition_count'] * 15) + 
                (df['medication_count'] * 10) + 
                (df['allergy_count'] * 5) +
                (df['age'] * 0.5)
            ).clip(0, 100)
            
            # Risk category
            df['risk_category'] = pd.cut(
                df['risk_score'], 
                bins=[0, 30, 60, 100], 
                labels=['Low', 'Medium', 'High']
            )
            
            return df[['patient_name', 'age', 'gender', 'condition_count', 
                      'medication_count', 'risk_score', 'risk_category']]
            
        except Error as e:
            print(f"Error calculating risk scores: {e}")
            return pd.DataFrame()
    
    def readmission_prediction(self):
        """
        Predict patients at risk of readmission based on historical patterns
        
        Returns:
            DataFrame: Readmission risk analysis
        """
        try:
            conn = self.get_connection()
            
            query = """
                SELECT 
                    p.id,
                    CONCAT(p.first, ' ', p.last) AS patient_name,
                    YEAR(CURDATE()) - YEAR(p.birthdate) AS age,
                    COUNT(e.id) AS total_encounters,
                    COUNT(CASE WHEN e.encounterclass = 'emergency' THEN 1 END) AS emergency_visits,
                    COUNT(CASE WHEN e.encounterclass = 'inpatient' THEN 1 END) AS inpatient_visits,
                    AVG(TIMESTAMPDIFF(DAY, e.start, e.stop)) AS avg_length_of_stay
                FROM patients p
                JOIN encounters e ON p.id = e.patient
                WHERE e.start >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                GROUP BY p.id, patient_name, age
                HAVING total_encounters >= 2;
            """
            
            df = pd.read_sql(query, conn)
            
            # Readmission risk score
            df['readmission_risk'] = (
                (df['emergency_visits'] * 20) + 
                (df['inpatient_visits'] * 15) + 
                (df['avg_length_of_stay'] * 2)
            ).clip(0, 100)
            
            df['risk_level'] = pd.cut(
                df['readmission_risk'],
                bins=[0, 30, 60, 100],
                labels=['Low Risk', 'Moderate Risk', 'High Risk']
            )
            
            return df.sort_values('readmission_risk', ascending=False)
            
        except Error as e:
            print(f"Error predicting readmissions: {e}")
            return pd.DataFrame()
    
    def cost_trend_analysis(self):
        """
        Analyze healthcare cost trends and identify high-cost patients
        
        Returns:
            DataFrame: Cost analysis with patient_id, total_cost, encounter_count, cost_category
        """
        try:
            conn = self.get_connection()
            
            query = """
                SELECT 
                    p.id AS patient_id,
                    CONCAT(p.first, ' ', p.last) AS patient_name,
                    p.healthcare_expenses AS total_cost,
                    p.healthcare_coverage,
                    (p.healthcare_expenses - p.healthcare_coverage) AS out_of_pocket,
                    COUNT(DISTINCT m.id) AS medication_count,
                    COUNT(DISTINCT e.id) AS encounter_count
                FROM patients p
                LEFT JOIN medications m ON p.id = m.patient
                LEFT JOIN encounters e ON p.id = e.patient
                WHERE p.healthcare_expenses > 0
                GROUP BY p.id, patient_name, p.healthcare_expenses, p.healthcare_coverage
                ORDER BY p.healthcare_expenses DESC
                LIMIT 100;
            """
            
            df = pd.read_sql(query, conn)
            
            # Add cost category with proper labels (Low, Medium, High)
            if not df.empty:
                df['cost_category'] = pd.cut(
                    df['total_cost'],
                    bins=[0, 10000, 50000, float('inf')],
                    labels=['Low', 'Medium', 'High']
                )
            
            return df
            
        except Error as e:
            print(f"Error analyzing costs: {e}")
            return pd.DataFrame()
    
    def seasonal_trends(self):
        """
        Analyze seasonal trends in conditions and encounters
        
        Returns:
            DataFrame: Seasonal analysis with month, description, count columns
        """
        try:
            conn = self.get_connection()
            
            # Get condition trends by month
            query = """
                SELECT 
                    MONTH(c.start) AS month,
                    c.description,
                    COUNT(*) AS count
                FROM conditions c
                WHERE c.start IS NOT NULL 
                AND c.start >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
                GROUP BY MONTH(c.start), c.description
                ORDER BY month, count DESC;
            """
            
            df = pd.read_sql(query, conn)
            return df
            
        except Error as e:
            print(f"Error analyzing seasonal trends: {e}")
            return pd.DataFrame()
    
    def medication_effectiveness(self):
        """
        Analyze medication patterns and potential effectiveness
        
        Returns:
            DataFrame: Medication analysis
        """
        try:
            conn = self.get_connection()
            
            query = """
                SELECT 
                    m.description AS medication,
                    c.description AS condition_treated,
                    COUNT(DISTINCT m.patient) AS patient_count,
                    AVG(DATEDIFF(COALESCE(m.stop, CURDATE()), m.start)) AS avg_duration_days,
                    AVG(m.base_cost) AS avg_cost
                FROM medications m
                JOIN conditions c ON m.patient = c.patient 
                    AND m.reasoncode = c.code
                WHERE m.reasoncode IS NOT NULL
                GROUP BY m.description, c.description
                HAVING patient_count >= 5
                ORDER BY patient_count DESC
                LIMIT 30;
            """
            
            df = pd.read_sql(query, conn)
            return df
            
        except Error as e:
            print(f"Error analyzing medication effectiveness: {e}")
            return pd.DataFrame()
    
    def demographic_insights(self):
        """
        Advanced demographic analysis with statistical insights
        
        Returns:
            dict: Statistical insights
        """
        try:
            conn = self.get_connection()
            
            query = """
                SELECT 
                    YEAR(CURDATE()) - YEAR(birthdate) AS age,
                    gender,
                    healthcare_expenses,
                    state
                FROM patients
                WHERE healthcare_expenses > 0;
            """
            
            df = pd.read_sql(query, conn)
            
            insights = {
                'age_statistics': {
                    'mean': df['age'].mean(),
                    'median': df['age'].median(),
                    'std_dev': df['age'].std(),
                    'range': (df['age'].min(), df['age'].max())
                },
                'gender_distribution': df['gender'].value_counts().to_dict(),
                'cost_statistics': {
                    'mean': df['healthcare_expenses'].mean(),
                    'median': df['healthcare_expenses'].median(),
                    'total': df['healthcare_expenses'].sum()
                },
                'top_states': df['state'].value_counts().head(5).to_dict()
            }
            
            return insights
            
        except Error as e:
            print(f"Error generating insights: {e}")
            return {}
    
    def executive_summary(self):
        """
        Generate executive summary with key metrics for dashboard
        
        Returns:
            dict: Executive summary with dashboard-compatible fields
        """
        try:
            conn = self.get_connection()
            
            # Total patients
            total_patients = pd.read_sql(
                "SELECT COUNT(*) as count FROM patients", conn
            )['count'].iloc[0]
            
            # Total encounters
            total_encounters = pd.read_sql(
                "SELECT COUNT(*) as count FROM encounters", conn
            )['count'].iloc[0]
            
            # Total medications
            total_medications = pd.read_sql(
                "SELECT COUNT(*) as count FROM medications", conn
            )['count'].iloc[0]
            
            # Total conditions
            total_conditions = pd.read_sql(
                "SELECT COUNT(*) as count FROM conditions", conn
            )['count'].iloc[0]
            
            # Calculate averages
            avg_encounters = total_encounters / total_patients if total_patients > 0 else 0
            avg_medications = total_medications / total_patients if total_patients > 0 else 0
            avg_conditions = total_conditions / total_patients if total_patients > 0 else 0
            
            summary = {
                'total_patients': int(total_patients),
                'total_encounters': int(total_encounters),
                'total_medications': int(total_medications),
                'total_conditions': int(total_conditions),
                'avg_encounters_per_patient': round(avg_encounters, 1),
                'avg_medications_per_patient': round(avg_medications, 1),
                'avg_conditions_per_patient': round(avg_conditions, 1)
            }
            
            return summary
            
        except Error as e:
            print(f"Error generating summary: {e}")
            return {
                'total_patients': 0,
                'total_encounters': 0,
                'total_medications': 0,
                'total_conditions': 0,
                'avg_encounters_per_patient': 0,
                'avg_medications_per_patient': 0,
                'avg_conditions_per_patient': 0
            }
    
    def generate_executive_summary(self):
        """
        Generate detailed executive summary with extended metrics
        (Legacy method for backward compatibility)
        
        Returns:
            dict: Extended executive summary
        """
        try:
            conn = self.get_connection()
            
            # Total patients
            total_patients = pd.read_sql(
                "SELECT COUNT(*) as count FROM patients", conn
            )['count'].iloc[0]
            
            # Active conditions
            active_conditions = pd.read_sql(
                "SELECT COUNT(DISTINCT patient) as count FROM conditions WHERE stop IS NULL", conn
            )['count'].iloc[0]
            
            # Total encounters
            total_encounters = pd.read_sql(
                "SELECT COUNT(*) as count FROM encounters", conn
            )['count'].iloc[0]
            
            # Total healthcare costs
            total_costs = pd.read_sql(
                "SELECT SUM(healthcare_expenses) as total FROM patients", conn
            )['total'].iloc[0]
            
            # Average patient age
            avg_age = pd.read_sql(
                "SELECT AVG(YEAR(CURDATE()) - YEAR(birthdate)) as avg FROM patients", conn
            )['avg'].iloc[0]
            
            summary = {
                'total_patients': int(total_patients),
                'patients_with_active_conditions': int(active_conditions),
                'total_encounters': int(total_encounters),
                'total_healthcare_costs': float(total_costs) if total_costs else 0,
                'average_patient_age': round(float(avg_age), 1) if avg_age else 0,
                'condition_rate': round((active_conditions / total_patients) * 100, 2)
            }
            
            return summary
            
        except Error as e:
            print(f"Error generating summary: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn and self.conn.is_connected():
            self.conn.close()


if __name__ == "__main__":
    analytics = HealthcareAnalytics()
    
    print("=== EXECUTIVE SUMMARY ===")
    summary = analytics.generate_executive_summary()
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value:,}")
    
    print("\n=== TOP 10 HIGH-RISK PATIENTS ===")
    risk_df = analytics.patient_risk_score()
    print(risk_df.head(10).to_string(index=False))
    
    print("\n=== READMISSION RISK ANALYSIS ===")
    readmission_df = analytics.readmission_prediction()
    print(readmission_df.head(10).to_string(index=False))
    
    analytics.close()
