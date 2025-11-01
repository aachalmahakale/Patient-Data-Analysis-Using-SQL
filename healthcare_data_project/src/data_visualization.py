"""
Healthcare Data Visualization
Creates matplotlib visualizations from healthcare data
"""

import pandas as pd
import matplotlib.pyplot as plt
from mysql.connector import Error
from db_config import get_db_connection
import os

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')

def visualize_age_distribution():
    """Visualize patient age distribution from database"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT YEAR(CURDATE()) - YEAR(birthdate) AS age, 
                   COUNT(*) AS count 
            FROM patients 
            GROUP BY age 
            ORDER BY age;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        plt.figure(figsize=(12, 6))
        plt.bar(df['age'], df['count'], color='skyblue', edgecolor='navy', alpha=0.7)
        plt.xlabel('Age', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Patients', fontsize=12, fontweight='bold')
        plt.title('Patient Age Distribution', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        print("✅ Age distribution visualization completed")
        
    except Error as e:
        print(f"❌ Database error in age distribution: {e}")
    except Exception as e:
        print(f"❌ Error visualizing age distribution: {e}")

def visualize_from_csv(csv_path, title, xlabel, ylabel, color='lightgreen'):
    """
    Generic function to visualize data from CSV files
    
    Args:
        csv_path (str): Path to CSV file
        title (str): Chart title
        xlabel (str): X-axis label
        ylabel (str): Y-axis label
        color (str): Bar color
    """
    try:
        if not os.path.exists(csv_path):
            print(f"⚠️  File not found: {csv_path}")
            return
            
        df = pd.read_csv(csv_path)
        
        # Take top 15 for better visibility
        df = df.head(15)
        
        plt.figure(figsize=(14, 8))
        plt.bar(df.iloc[:, 0], df.iloc[:, 1], color=color, edgecolor='black', alpha=0.7)
        plt.xlabel(xlabel, fontsize=12, fontweight='bold')
        plt.ylabel(ylabel, fontsize=12, fontweight='bold')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        print(f"✅ {title} visualization completed")
        
    except Exception as e:
        print(f"❌ Error visualizing {title}: {e}")

def main():
    """Generate all visualizations"""
    print("Starting data visualization...\n")
    
    # Visualize from database
    visualize_age_distribution()
    
    # Visualize from CSV reports
    visualize_from_csv(
        '../data/common_allergies_report.csv',
        'Common Allergies',
        'Allergy Description',
        'Number of Patients',
        'lightgreen'
    )
    
    visualize_from_csv(
        '../data/medications_report.csv',
        'Common Medications',
        'Medication Description',
        'Number of Patients',
        'lightcoral'
    )
    
    visualize_from_csv(
        '../data/immunizations_report.csv',
        'Immunization Count by Patient',
        'Patient ID',
        'Number of Immunizations',
        'lightskyblue'
    )
    
    visualize_from_csv(
        '../data/devices_report.csv',
        'Device Usage',
        'Device Description',
        'Number of Patients',
        'lightgoldenrodyellow'
    )
    
    print("\n✨ All visualizations completed!")

if __name__ == "__main__":
    main()

