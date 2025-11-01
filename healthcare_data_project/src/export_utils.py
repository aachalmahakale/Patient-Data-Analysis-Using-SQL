"""
Export Utilities
Export healthcare data and reports to various formats (Excel, CSV, PDF)
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
from db_config import get_db_connection
from mysql.connector import Error
import os


class HealthcareExporter:
    """Export healthcare data to various formats"""
    
    def __init__(self, output_dir='../exports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.conn = None
    
    def get_connection(self):
        """Get database connection"""
        if not self.conn or not self.conn.is_connected():
            self.conn = get_db_connection()
        return self.conn
    
    def export_to_excel(self, dataframes_dict, filename=None):
        """
        Export multiple dataframes to a single Excel file with multiple sheets
        
        Args:
            dataframes_dict (dict): Dictionary of {sheet_name: dataframe}
            filename (str): Output filename (optional)
        
        Returns:
            str: Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"healthcare_report_{timestamp}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in dataframes_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get the worksheet
                worksheet = writer.sheets[sheet_name]
                
                # Style the header
                for cell in worksheet[1]:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center")
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"✅ Excel report exported to: {filepath}")
        return filepath
    
    def export_comprehensive_report(self):
        """Export comprehensive healthcare report with all major analyses"""
        try:
            conn = self.get_connection()
            
            # 1. Patient Demographics
            patients_query = """
                SELECT 
                    CONCAT(first, ' ', last) AS patient_name,
                    birthdate,
                    YEAR(CURDATE()) - YEAR(birthdate) AS age,
                    gender,
                    city,
                    state,
                    healthcare_expenses,
                    healthcare_coverage
                FROM patients
                LIMIT 1000;
            """
            df_patients = pd.read_sql(patients_query, conn)
            
            # 2. Top Conditions
            conditions_query = """
                SELECT 
                    description AS condition,
                    COUNT(*) AS total_cases,
                    COUNT(DISTINCT patient) AS unique_patients,
                    ROUND(AVG(DATEDIFF(COALESCE(stop, CURDATE()), start))) AS avg_duration_days
                FROM conditions
                GROUP BY description
                ORDER BY total_cases DESC
                LIMIT 50;
            """
            df_conditions = pd.read_sql(conditions_query, conn)
            
            # 3. Medication Analysis
            medications_query = """
                SELECT 
                    description AS medication,
                    COUNT(*) AS prescriptions,
                    COUNT(DISTINCT patient) AS unique_patients,
                    ROUND(AVG(base_cost), 2) AS avg_cost,
                    ROUND(SUM(base_cost), 2) AS total_cost
                FROM medications
                GROUP BY description
                ORDER BY prescriptions DESC
                LIMIT 50;
            """
            df_medications = pd.read_sql(medications_query, conn)
            
            # 4. Cost Analysis
            cost_query = """
                SELECT 
                    CONCAT(p.first, ' ', p.last) AS patient_name,
                    p.healthcare_expenses,
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
            df_costs = pd.read_sql(cost_query, conn)
            
            # 5. Encounter Summary
            encounters_query = """
                SELECT 
                    encounterclass AS encounter_type,
                    COUNT(*) AS total_encounters,
                    ROUND(AVG(base_encounter_cost), 2) AS avg_cost,
                    ROUND(SUM(base_encounter_cost), 2) AS total_cost
                FROM encounters
                GROUP BY encounterclass
                ORDER BY total_encounters DESC;
            """
            df_encounters = pd.read_sql(encounters_query, conn)
            
            # Create comprehensive report
            dataframes_dict = {
                'Patients': df_patients,
                'Top_Conditions': df_conditions,
                'Medications': df_medications,
                'Cost_Analysis': df_costs,
                'Encounters': df_encounters
            }
            
            return self.export_to_excel(dataframes_dict, 'comprehensive_healthcare_report.xlsx')
            
        except Error as e:
            print(f"❌ Error generating comprehensive report: {e}")
            return None
    
    def export_executive_summary(self):
        """Export executive summary report"""
        try:
            conn = self.get_connection()
            
            # Key Metrics
            summary_data = {
                'Metric': [
                    'Total Patients',
                    'Total Conditions Recorded',
                    'Total Medications Prescribed',
                    'Total Encounters',
                    'Total Healthcare Costs',
                    'Average Patient Age',
                    'Active Conditions',
                    'Unique Conditions'
                ],
                'Value': []
            }
            
            # Get metrics
            metrics = [
                "SELECT COUNT(*) FROM patients",
                "SELECT COUNT(*) FROM conditions",
                "SELECT COUNT(*) FROM medications",
                "SELECT COUNT(*) FROM encounters",
                "SELECT ROUND(SUM(healthcare_expenses), 2) FROM patients",
                "SELECT ROUND(AVG(YEAR(CURDATE()) - YEAR(birthdate)), 1) FROM patients",
                "SELECT COUNT(*) FROM conditions WHERE stop IS NULL",
                "SELECT COUNT(DISTINCT description) FROM conditions"
            ]
            
            for metric_query in metrics:
                result = pd.read_sql(metric_query, conn)
                summary_data['Value'].append(result.iloc[0, 0])
            
            df_summary = pd.DataFrame(summary_data)
            
            # Gender Distribution
            gender_query = """
                SELECT 
                    gender,
                    COUNT(*) AS count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patients), 2) AS percentage
                FROM patients
                GROUP BY gender;
            """
            df_gender = pd.read_sql(gender_query, conn)
            
            # Top 10 Conditions
            top_conditions_query = """
                SELECT 
                    description,
                    COUNT(*) AS cases
                FROM conditions
                GROUP BY description
                ORDER BY cases DESC
                LIMIT 10;
            """
            df_top_conditions = pd.read_sql(top_conditions_query, conn)
            
            dataframes_dict = {
                'Executive_Summary': df_summary,
                'Gender_Distribution': df_gender,
                'Top_10_Conditions': df_top_conditions
            }
            
            return self.export_to_excel(dataframes_dict, 'executive_summary.xlsx')
            
        except Error as e:
            print(f"❌ Error generating executive summary: {e}")
            return None
    
    def export_patient_report(self, patient_id):
        """Export individual patient report"""
        try:
            conn = self.get_connection()
            
            # Patient Info
            patient_query = f"""
                SELECT * FROM patients WHERE id = '{patient_id}';
            """
            df_patient = pd.read_sql(patient_query, conn)
            
            if df_patient.empty:
                print(f"❌ Patient {patient_id} not found")
                return None
            
            # Patient Conditions
            conditions_query = f"""
                SELECT description, start, stop
                FROM conditions
                WHERE patient = '{patient_id}'
                ORDER BY start DESC;
            """
            df_conditions = pd.read_sql(conditions_query, conn)
            
            # Patient Medications
            medications_query = f"""
                SELECT description, start, stop, base_cost
                FROM medications
                WHERE patient = '{patient_id}'
                ORDER BY start DESC;
            """
            df_medications = pd.read_sql(medications_query, conn)
            
            # Patient Encounters
            encounters_query = f"""
                SELECT encounterclass, start, stop, description, base_encounter_cost
                FROM encounters
                WHERE patient = '{patient_id}'
                ORDER BY start DESC;
            """
            df_encounters = pd.read_sql(encounters_query, conn)
            
            patient_name = f"{df_patient.iloc[0]['first']}_{df_patient.iloc[0]['last']}"
            filename = f"patient_report_{patient_name}_{patient_id[:8]}.xlsx"
            
            dataframes_dict = {
                'Patient_Info': df_patient,
                'Conditions': df_conditions,
                'Medications': df_medications,
                'Encounters': df_encounters
            }
            
            return self.export_to_excel(dataframes_dict, filename)
            
        except Error as e:
            print(f"❌ Error generating patient report: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn and self.conn.is_connected():
            self.conn.close()


if __name__ == "__main__":
    exporter = HealthcareExporter()
    
    print("=== Generating Healthcare Reports ===\n")
    
    # Export comprehensive report
    print("1. Generating Comprehensive Report...")
    exporter.export_comprehensive_report()
    
    # Export executive summary
    print("\n2. Generating Executive Summary...")
    exporter.export_executive_summary()
    
    print("\n✨ All reports generated successfully!")
    print(f"📁 Reports saved to: {exporter.output_dir}")
    
    exporter.close()
