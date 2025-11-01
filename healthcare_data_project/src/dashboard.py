"""
Advanced Healthcare Data Insights Dashboard
Multi-page interactive dashboard with ML-powered analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mysql.connector import Error
from db_config import get_db_connection
from advanced_analytics import HealthcareAnalytics

# Page configuration
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize analytics
@st.cache_resource
def init_analytics():
    """Initialize analytics module"""
    return HealthcareAnalytics()

# Database connection
@st.cache_resource
def get_connection():
    """Get database connection"""
    try:
        conn = get_db_connection()
        return conn
    except Error as e:
        st.error(f"❌ Database Connection Failed: {e}")
        st.stop()
        return None

# Sidebar navigation
st.sidebar.title("🏥 Healthcare Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["📊 Overview", "🔍 Analytics", "🔮 Predictive Insights", "📈 Trends", "🏥 Patient Insights", "📋 Reports"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use the tabs and filters to explore different aspects of the data")

# Initialize connection and analytics
conn = get_connection()
analytics = init_analytics()

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "📊 Overview":
    st.title("🏥 Healthcare Data Overview")
    st.markdown("### Executive Dashboard - Key Performance Indicators")
    
    # Get executive summary
    try:
        summary = analytics.executive_summary()
        
        # Display KPIs in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👥 Total Patients",
                value=f"{summary['total_patients']:,}",
                delta="Active in system"
            )
        
        with col2:
            st.metric(
                label="🏥 Total Encounters",
                value=f"{summary['total_encounters']:,}",
                delta=f"Avg: {summary['avg_encounters_per_patient']:.1f}/patient"
            )
        
        with col3:
            st.metric(
                label="💊 Medications",
                value=f"{summary['total_medications']:,}",
                delta=f"Avg: {summary['avg_medications_per_patient']:.1f}/patient"
            )
        
        with col4:
            st.metric(
                label="🦠 Conditions",
                value=f"{summary['total_conditions']:,}",
                delta=f"Avg: {summary['avg_conditions_per_patient']:.1f}/patient"
            )
        
        st.markdown("---")
        
        # Two column layout for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Top Conditions")
            query_conditions = """
                SELECT description, COUNT(*) AS occurrences 
                FROM conditions 
                GROUP BY description 
                ORDER BY occurrences DESC 
                LIMIT 10;
            """
            df_conditions = pd.read_sql(query_conditions, conn)
            if not df_conditions.empty:
                fig = px.bar(
                    df_conditions, 
                    x='occurrences', 
                    y='description',
                    orientation='h',
                    color='occurrences',
                    color_continuous_scale='Reds',
                    title="Most Common Medical Conditions"
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💊 Top Medications")
            query_meds = """
                SELECT description, COUNT(*) AS occurrences 
                FROM medications 
                GROUP BY description 
                ORDER BY occurrences DESC 
                LIMIT 10;
            """
            df_meds = pd.read_sql(query_meds, conn)
            if not df_meds.empty:
                fig = px.bar(
                    df_meds, 
                    x='occurrences', 
                    y='description',
                    orientation='h',
                    color='occurrences',
                    color_continuous_scale='Blues',
                    title="Most Prescribed Medications"
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Additional metrics row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤧 Allergy Distribution")
            query_allergies = """
                SELECT description, COUNT(*) AS count 
                FROM allergies 
                GROUP BY description 
                ORDER BY count DESC 
                LIMIT 8;
            """
            df_allergies = pd.read_sql(query_allergies, conn)
            if not df_allergies.empty:
                fig = px.pie(
                    df_allergies, 
                    values='count', 
                    names='description',
                    title="Common Allergies Distribution",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💉 Immunization Coverage")
            query_immunizations = """
                SELECT description, COUNT(*) AS count 
                FROM immunizations 
                GROUP BY description 
                ORDER BY count DESC 
                LIMIT 8;
            """
            df_immunizations = pd.read_sql(query_immunizations, conn)
            if not df_immunizations.empty:
                fig = px.pie(
                    df_immunizations, 
                    values='count', 
                    names='description',
                    title="Immunization Distribution",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading overview: {e}")

# ============================================================================
# PAGE 2: ANALYTICS
# ============================================================================
elif page == "🔍 Analytics":
    st.title("🔍 Deep Dive Analytics")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Demographics", "🏥 Encounters", "🔧 Devices", "👨‍⚕️ Providers"])
    
    with tab1:
        st.subheader("Patient Demographics Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution
            query_gender = """
                SELECT gender, COUNT(*) as count 
                FROM patients 
                GROUP BY gender;
            """
            df_gender = pd.read_sql(query_gender, conn)
            if not df_gender.empty:
                fig = px.pie(
                    df_gender, 
                    values='count', 
                    names='gender',
                    title="Gender Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age distribution
            query_age = """
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) < 18 THEN '0-17'
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 18 AND 30 THEN '18-30'
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 31 AND 50 THEN '31-50'
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 51 AND 70 THEN '51-70'
                        ELSE '71+'
                    END as age_group,
                    COUNT(*) as count
                FROM patients
                GROUP BY age_group
                ORDER BY age_group;
            """
            df_age = pd.read_sql(query_age, conn)
            if not df_age.empty:
                fig = px.bar(
                    df_age, 
                    x='age_group', 
                    y='count',
                    title="Age Group Distribution",
                    color='count',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Encounter Analysis")
        
        # Encounter types
        query_encounters = """
            SELECT encounterclass, COUNT(*) as count 
            FROM encounters 
            GROUP BY encounterclass 
            ORDER BY count DESC;
        """
        df_encounters = pd.read_sql(query_encounters, conn)
        if not df_encounters.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    df_encounters, 
                    x='encounterclass', 
                    y='count',
                    title="Encounters by Type",
                    color='count',
                    color_continuous_scale='Teal'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.treemap(
                    df_encounters,
                    path=['encounterclass'],
                    values='count',
                    title="Encounter Type Hierarchy"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Medical Devices Usage")
        
        query_devices = """
            SELECT description, COUNT(*) as count 
            FROM devices 
            GROUP BY description 
            ORDER BY count DESC 
            LIMIT 15;
        """
        df_devices = pd.read_sql(query_devices, conn)
        if not df_devices.empty:
            fig = px.bar(
                df_devices, 
                x='count', 
                y='description',
                orientation='h',
                title="Most Used Medical Devices",
                color='count',
                color_continuous_scale='Sunset'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Provider Analysis")
        
        # Provider workload
        query_providers = """
            SELECT p.name, p.speciality, COUNT(e.id) as encounter_count
            FROM providers p
            LEFT JOIN encounters e ON p.id = e.provider
            GROUP BY p.id, p.name, p.speciality
            ORDER BY encounter_count DESC
            LIMIT 15;
        """
        df_providers = pd.read_sql(query_providers, conn)
        if not df_providers.empty:
            fig = px.bar(
                df_providers, 
                x='encounter_count', 
                y='name',
                orientation='h',
                color='speciality',
                title="Provider Workload Analysis",
                hover_data=['speciality']
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 3: PREDICTIVE INSIGHTS
# ============================================================================
elif page == "🔮 Predictive Insights":
    st.title("🔮 Predictive Analytics & Risk Assessment")
    st.markdown("### ML-Powered Patient Risk Analysis")
    
    try:
        # Patient Risk Scores
        st.subheader("📊 Patient Risk Score Distribution")
        risk_df = analytics.patient_risk_score()
        
        if not risk_df.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                low_risk = len(risk_df[risk_df['risk_category'] == 'Low'])
                st.metric("🟢 Low Risk Patients", low_risk)
            
            with col2:
                medium_risk = len(risk_df[risk_df['risk_category'] == 'Medium'])
                st.metric("🟡 Medium Risk Patients", medium_risk)
            
            with col3:
                high_risk = len(risk_df[risk_df['risk_category'] == 'High'])
                st.metric("🔴 High Risk Patients", high_risk)
            
            # Risk distribution visualization
            col1, col2 = st.columns(2)
            
            with col1:
                risk_counts = risk_df['risk_category'].value_counts()
                fig = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Risk Category Distribution",
                    color=risk_counts.index,
                    color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(
                    risk_df,
                    x='risk_score',
                    nbins=20,
                    title="Risk Score Distribution",
                    color='risk_category',
                    color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # High-risk patients table
            st.subheader("🚨 High Risk Patients (Requires Attention)")
            high_risk_df = risk_df[risk_df['risk_category'] == 'High'].head(10)
            if not high_risk_df.empty:
                st.dataframe(
                    high_risk_df[['patient_id', 'risk_score', 'condition_count', 
                                  'medication_count', 'allergy_count']],
                    use_container_width=True
                )
        
        st.markdown("---")
        
        # Readmission Prediction
        st.subheader("🏥 Readmission Risk Prediction")
        readmission_df = analytics.readmission_prediction()
        
        if not readmission_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                high_readmit = len(readmission_df[readmission_df['risk_level'] == 'High'])
                st.metric("⚠️ High Readmission Risk", high_readmit)
            
            with col2:
                avg_score = readmission_df['readmission_score'].mean()
                st.metric("📊 Average Readmission Score", f"{avg_score:.1f}")
            
            # Readmission visualization
            fig = px.scatter(
                readmission_df.head(100),
                x='emergency_visits',
                y='readmission_score',
                color='risk_level',
                size='inpatient_visits',
                hover_data=['patient_id'],
                title="Readmission Risk vs Emergency Visits",
                color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # High readmission risk table
            st.subheader("🔔 Patients at High Readmission Risk")
            high_readmit_df = readmission_df[readmission_df['risk_level'] == 'High'].head(10)
            if not high_readmit_df.empty:
                st.dataframe(
                    high_readmit_df[['patient_id', 'readmission_score', 'emergency_visits', 
                                     'inpatient_visits', 'risk_level']],
                    use_container_width=True
                )
    
    except Exception as e:
        st.error(f"Error loading predictive insights: {e}")

# ============================================================================
# ============================================================================
# PAGE 4: TRENDS
# ============================================================================
elif page == "📈 Trends":
    st.title("📈 Data Trends & Patterns")
    st.markdown("### Historical Analysis & Growth Insights")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top conditions trend
            st.subheader("📊 Top Conditions Distribution")
            query_conditions = """
                SELECT description, COUNT(*) as count 
                FROM conditions 
                GROUP BY description 
                ORDER BY count DESC 
                LIMIT 10;
            """
            df_conditions_trend = pd.read_sql(query_conditions, conn)
            
            if not df_conditions_trend.empty:
                fig = px.bar(
                    df_conditions_trend,
                    x='count',
                    y='description',
                    orientation='h',
                    title="Most Common Conditions",
                    color='count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top medications trend
            st.subheader("💊 Top Medications Distribution")
            query_meds = """
                SELECT description, COUNT(*) as count 
                FROM medications 
                GROUP BY description 
                ORDER BY count DESC 
                LIMIT 10;
            """
            df_meds_trend = pd.read_sql(query_meds, conn)
            
            if not df_meds_trend.empty:
                fig = px.bar(
                    df_meds_trend,
                    x='count',
                    y='description',
                    orientation='h',
                    title="Most Prescribed Medications",
                    color='count',
                    color_continuous_scale='Greens'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Encounter class distribution
        st.subheader("🏥 Encounter Types Distribution")
        query_encounters = """
            SELECT encounterclass, COUNT(*) as count 
            FROM encounters 
            GROUP BY encounterclass 
            ORDER BY count DESC;
        """
        df_encounters = pd.read_sql(query_encounters, conn)
        
        if not df_encounters.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    df_encounters,
                    values='count',
                    names='encounterclass',
                    title="Encounter Type Distribution",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_encounters,
                    x='encounterclass',
                    y='count',
                    title="Encounter Volume by Type",
                    color='count',
                    color_continuous_scale='Oranges'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Patient demographics trends
        st.subheader("👥 Patient Demographics Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            query_age = """
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) < 18 THEN '0-17'
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 18 AND 30 THEN '18-30'
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 31 AND 50 THEN '31-50'
                        WHEN TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) BETWEEN 51 AND 70 THEN '51-70'
                        ELSE '71+'
                    END as age_group,
                    COUNT(*) as count
                FROM patients
                GROUP BY age_group
                ORDER BY age_group;
            """
            df_age_trend = pd.read_sql(query_age, conn)
            
            if not df_age_trend.empty:
                fig = px.funnel(
                    df_age_trend,
                    x='count',
                    y='age_group',
                    title="Patient Age Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gender distribution
            query_gender = """
                SELECT gender, COUNT(*) as count 
                FROM patients 
                GROUP BY gender;
            """
            df_gender_trend = pd.read_sql(query_gender, conn)
            
            if not df_gender_trend.empty:
                fig = px.pie(
                    df_gender_trend,
                    values='count',
                    names='gender',
                    title="Gender Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading trends: {e}")
        import traceback
        st.code(traceback.format_exc())

# ============================================================================
# PAGE 5: PATIENT INSIGHTS
# ============================================================================
elif page == "🏥 Patient Insights":
    st.title("🏥 Patient Deep Dive")
    st.markdown("### Individual Patient Analysis & Search")
    
    try:
        # Patient search and selection
        st.subheader("🔍 Search Patient")
        
        # Get all patients
        query_patients = """
            SELECT 
                id,
                CONCAT(first, ' ', last) as name,
                gender,
                YEAR(CURDATE()) - YEAR(birthdate) as age,
                city,
                state
            FROM patients
            ORDER BY last, first
            LIMIT 100;
        """
        df_all_patients = pd.read_sql(query_patients, conn)
        
        if not df_all_patients.empty:
            # Create a searchable dropdown
            patient_options = df_all_patients.apply(
                lambda x: f"{x['name']} (Age: {x['age']}, {x['gender']}, {x['city']}, {x['state']})", 
                axis=1
            ).tolist()
            
            selected_patient_display = st.selectbox(
                "Select a patient to view details:",
                options=patient_options,
                index=0
            )
            
            # Get the selected patient ID
            selected_idx = patient_options.index(selected_patient_display)
            selected_patient_id = df_all_patients.iloc[selected_idx]['id']
            selected_patient_name = df_all_patients.iloc[selected_idx]['name']
            
            st.markdown("---")
            st.subheader(f"📋 Patient Profile: {selected_patient_name}")
            
            # Patient summary stats
            col1, col2, col3, col4 = st.columns(4)
            
            # Get patient stats
            query_patient_conditions = f"""
                SELECT COUNT(*) as count FROM conditions WHERE patient = '{selected_patient_id}'
            """
            conditions_count = pd.read_sql(query_patient_conditions, conn)['count'].iloc[0]
            
            query_patient_meds = f"""
                SELECT COUNT(*) as count FROM medications WHERE patient = '{selected_patient_id}'
            """
            meds_count = pd.read_sql(query_patient_meds, conn)['count'].iloc[0]
            
            query_patient_encounters = f"""
                SELECT COUNT(*) as count FROM encounters WHERE patient = '{selected_patient_id}'
            """
            encounters_count = pd.read_sql(query_patient_encounters, conn)['count'].iloc[0]
            
            query_patient_allergies = f"""
                SELECT COUNT(*) as count FROM allergies WHERE patient = '{selected_patient_id}'
            """
            allergies_count = pd.read_sql(query_patient_allergies, conn)['count'].iloc[0]
            
            with col1:
                st.metric("🦠 Conditions", conditions_count)
            with col2:
                st.metric("💊 Medications", meds_count)
            with col3:
                st.metric("🏥 Encounters", encounters_count)
            with col4:
                st.metric("🤧 Allergies", allergies_count)
            
            st.markdown("---")
            
            # Patient details in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🦠 Conditions", "💊 Medications", "🏥 Encounters", "🤧 Allergies"])
            
            with tab1:
                query_conditions = f"""
                    SELECT description, start, stop
                    FROM conditions
                    WHERE patient = '{selected_patient_id}'
                    ORDER BY start DESC;
                """
                df_conditions = pd.read_sql(query_conditions, conn)
                if not df_conditions.empty:
                    st.dataframe(df_conditions, use_container_width=True)
                else:
                    st.info("No conditions recorded")
            
            with tab2:
                query_meds = f"""
                    SELECT description, start, stop, reasondescription
                    FROM medications
                    WHERE patient = '{selected_patient_id}'
                    ORDER BY start DESC;
                """
                df_meds = pd.read_sql(query_meds, conn)
                if not df_meds.empty:
                    st.dataframe(df_meds, use_container_width=True)
                else:
                    st.info("No medications recorded")
            
            with tab3:
                query_encounters = f"""
                    SELECT encounterclass, start, stop, reasondescription
                    FROM encounters
                    WHERE patient = '{selected_patient_id}'
                    ORDER BY start DESC;
                """
                df_encounters = pd.read_sql(query_encounters, conn)
                if not df_encounters.empty:
                    st.dataframe(df_encounters, use_container_width=True)
                else:
                    st.info("No encounters recorded")
            
            with tab4:
                query_allergies = f"""
                    SELECT description, start, stop
                    FROM allergies
                    WHERE patient = '{selected_patient_id}'
                    ORDER BY start DESC;
                """
                df_allergies = pd.read_sql(query_allergies, conn)
                if not df_allergies.empty:
                    st.dataframe(df_allergies, use_container_width=True)
                else:
                    st.info("No allergies recorded")
        
        else:
            st.warning("No patients found in the database")
    
    except Exception as e:
        st.error(f"Error loading patient insights: {e}")
        import traceback
        st.code(traceback.format_exc())

# ============================================================================
# PAGE 6: REPORTS
# ============================================================================
elif page == "📋 Reports":
    st.title("📋 Generate Reports")
    st.markdown("### Export & Download Data Reports")
    
    try:
        st.subheader("📊 Available Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Summary Reports")
            
            if st.button("📄 Generate Conditions Report", use_container_width=True):
                query = """
                    SELECT description, COUNT(*) as occurrences
                    FROM conditions
                    GROUP BY description
                    ORDER BY occurrences DESC;
                """
                df_report = pd.read_sql(query, conn)
                
                st.success("✅ Report generated!")
                st.dataframe(df_report, use_container_width=True)
                
                # Download button
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="conditions_report.csv",
                    mime="text/csv"
                )
            
            if st.button("💊 Generate Medications Report", use_container_width=True):
                query = """
                    SELECT description, COUNT(*) as occurrences
                    FROM medications
                    GROUP BY description
                    ORDER BY occurrences DESC;
                """
                df_report = pd.read_sql(query, conn)
                
                st.success("✅ Report generated!")
                st.dataframe(df_report, use_container_width=True)
                
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="medications_report.csv",
                    mime="text/csv"
                )
            
            if st.button("🤧 Generate Allergies Report", use_container_width=True):
                query = """
                    SELECT description, COUNT(*) as occurrences
                    FROM allergies
                    GROUP BY description
                    ORDER BY occurrences DESC;
                """
                df_report = pd.read_sql(query, conn)
                
                st.success("✅ Report generated!")
                st.dataframe(df_report, use_container_width=True)
                
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="allergies_report.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("### 🎯 Analytics Reports")
            
            if st.button("📊 Generate Patient Summary", use_container_width=True):
                query = """
                    SELECT 
                        COUNT(*) as total_patients,
                        AVG(YEAR(CURDATE()) - YEAR(birthdate)) as avg_age,
                        SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) as male_count,
                        SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as female_count
                    FROM patients;
                """
                df_report = pd.read_sql(query, conn)
                
                st.success("✅ Report generated!")
                st.dataframe(df_report, use_container_width=True)
                
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="patient_summary.csv",
                    mime="text/csv"
                )
            
            if st.button("🏥 Generate Encounter Summary", use_container_width=True):
                query = """
                    SELECT 
                        encounterclass,
                        COUNT(*) as total_encounters,
                        COUNT(DISTINCT patient) as unique_patients
                    FROM encounters
                    GROUP BY encounterclass
                    ORDER BY total_encounters DESC;
                """
                df_report = pd.read_sql(query, conn)
                
                st.success("✅ Report generated!")
                st.dataframe(df_report, use_container_width=True)
                
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="encounter_summary.csv",
                    mime="text/csv"
                )
            
            if st.button("🔮 Generate Risk Report", use_container_width=True):
                with st.spinner("Calculating risk scores..."):
                    risk_df = analytics.patient_risk_score()
                    
                    if not risk_df.empty:
                        st.success("✅ Report generated!")
                        st.dataframe(risk_df.head(50), use_container_width=True)
                        
                        csv = risk_df.to_csv(index=False)
                        st.download_button(
                            label="💾 Download Full Risk Report CSV",
                            data=csv,
                            file_name="patient_risk_scores.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No risk data available")
        
        st.markdown("---")
        st.info("💡 **Tip**: Click any button above to generate and download reports in CSV format")
    
    except Exception as e:
        st.error(f"Error generating reports: {e}")
        import traceback
        st.code(traceback.format_exc())

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Quick Links")
st.sidebar.markdown("- [API Documentation](/api/docs)")
st.sidebar.markdown("- [Export Reports](#)")
st.sidebar.markdown("- [Settings](#)")

st.sidebar.markdown("---")
st.sidebar.caption("**Healthcare Analytics Dashboard** v2.0")
st.sidebar.caption("Built with Streamlit, Plotly & ML")

