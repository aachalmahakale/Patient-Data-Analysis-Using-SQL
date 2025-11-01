"""
RESTful API for Healthcare Data
FastAPI-based REST API for programmatic access to healthcare data
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from db_config import get_db_connection
from mysql.connector import Error
from advanced_analytics import HealthcareAnalytics
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Analytics API",
    description="RESTful API for healthcare data analysis and insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Patient(BaseModel):
    id: str
    first: str
    last: str
    birthdate: str
    gender: str

class Condition(BaseModel):
    description: str
    occurrences: int

class ExecutiveSummary(BaseModel):
    total_patients: int
    patients_with_active_conditions: int
    total_encounters: int
    total_healthcare_costs: float
    average_patient_age: float

# Helper function
def get_conn():
    try:
        return get_db_connection()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """API Root - Welcome message"""
    return {
        "message": "Welcome to Healthcare Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "summary": "/api/summary",
            "patients": "/api/patients",
            "conditions": "/api/conditions",
            "medications": "/api/medications",
            "risk_scores": "/api/analytics/risk-scores",
            "readmission_risk": "/api/analytics/readmission-risk",
            "costs": "/api/analytics/costs"
        }
    }

@app.get("/api/summary", response_model=ExecutiveSummary)
def get_executive_summary():
    """Get executive summary with key metrics"""
    try:
        analytics = HealthcareAnalytics()
        summary = analytics.generate_executive_summary()
        analytics.close()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patients")
def get_patients(limit: int = Query(100, ge=1, le=1000)):
    """Get list of patients"""
    try:
        conn = get_conn()
        query = f"""
            SELECT id, first, last, birthdate, gender, city, state
            FROM patients
            LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conditions", response_model=List[Condition])
def get_conditions(limit: int = Query(20, ge=1, le=100)):
    """Get most common medical conditions"""
    try:
        conn = get_conn()
        query = f"""
            SELECT description, COUNT(*) AS occurrences
            FROM conditions
            GROUP BY description
            ORDER BY occurrences DESC
            LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/medications")
def get_medications(limit: int = Query(20, ge=1, le=100)):
    """Get most prescribed medications"""
    try:
        conn = get_conn()
        query = f"""
            SELECT description, COUNT(*) AS prescriptions,
                   AVG(base_cost) AS avg_cost
            FROM medications
            GROUP BY description
            ORDER BY prescriptions DESC
            LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/allergies")
def get_allergies(limit: int = Query(20, ge=1, le=100)):
    """Get most common allergies"""
    try:
        conn = get_conn()
        query = f"""
            SELECT description, COUNT(*) AS occurrences
            FROM allergies
            GROUP BY description
            ORDER BY occurrences DESC
            LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/risk-scores")
def get_risk_scores():
    """Get patient risk scores"""
    try:
        analytics = HealthcareAnalytics()
        risk_df = analytics.patient_risk_score()
        analytics.close()
        
        if risk_df.empty:
            return {"message": "No risk data available"}
        
        return {
            "total_patients_analyzed": len(risk_df),
            "high_risk_count": len(risk_df[risk_df['risk_category'] == 'High']),
            "medium_risk_count": len(risk_df[risk_df['risk_category'] == 'Medium']),
            "low_risk_count": len(risk_df[risk_df['risk_category'] == 'Low']),
            "top_high_risk_patients": risk_df[risk_df['risk_category'] == 'High'].head(10).to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/readmission-risk")
def get_readmission_risk():
    """Get readmission risk predictions"""
    try:
        analytics = HealthcareAnalytics()
        readmission_df = analytics.readmission_prediction()
        analytics.close()
        
        if readmission_df.empty:
            return {"message": "Insufficient data for readmission prediction"}
        
        return {
            "total_patients_analyzed": len(readmission_df),
            "high_risk_patients": readmission_df.head(10).to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/costs")
def get_cost_analysis():
    """Get cost trend analysis"""
    try:
        analytics = HealthcareAnalytics()
        cost_df = analytics.cost_trend_analysis()
        analytics.close()
        
        if cost_df.empty:
            return {"message": "No cost data available"}
        
        return {
            "total_patients_analyzed": len(cost_df),
            "total_healthcare_expenses": float(cost_df['healthcare_expenses'].sum()),
            "average_cost_per_patient": float(cost_df['healthcare_expenses'].mean()),
            "highest_cost_patients": cost_df.head(10).to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/demographics/age-distribution")
def get_age_distribution():
    """Get patient age distribution"""
    try:
        conn = get_conn()
        query = """
            SELECT 
                CASE 
                    WHEN age < 18 THEN '0-17'
                    WHEN age BETWEEN 18 AND 30 THEN '18-30'
                    WHEN age BETWEEN 31 AND 45 THEN '31-45'
                    WHEN age BETWEEN 46 AND 60 THEN '46-60'
                    WHEN age BETWEEN 61 AND 75 THEN '61-75'
                    ELSE '75+'
                END AS age_group,
                COUNT(*) AS count
            FROM (
                SELECT YEAR(CURDATE()) - YEAR(birthdate) AS age
                FROM patients
            ) AS age_data
            GROUP BY age_group
            ORDER BY 
                CASE age_group
                    WHEN '0-17' THEN 1
                    WHEN '18-30' THEN 2
                    WHEN '31-45' THEN 3
                    WHEN '46-60' THEN 4
                    WHEN '61-75' THEN 5
                    ELSE 6
                END;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        conn = get_conn()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Run the API
if __name__ == "__main__":
    print("🚀 Starting Healthcare Analytics API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Interactive API: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
