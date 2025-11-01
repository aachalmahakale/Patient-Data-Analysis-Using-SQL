# 🏥 Patient Data Analysis Using SQL

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange.svg)](https://www.mysql.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A comprehensive healthcare data analysis system that analyzes patient demographics, diagnoses, medications, and treatment patterns using SQL queries and interactive visualizations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Sample Queries](#sample-queries)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project provides a complete solution for healthcare data analysis, featuring:
- **Interactive Dashboard**: Real-time data visualization using Streamlit
- **SQL Analysis**: Complex queries for patient demographics, conditions, medications, and more
- **Report Generation**: Automated CSV report generation for further analysis
- **Data Visualization**: Matplotlib-based charts and graphs
- **Secure Configuration**: Environment-based credential management

Perfect for:
- Healthcare data analysts
- Medical researchers
- Hospital administrators
- Data science students
- Anyone interested in healthcare analytics

## ✨ Features

### 📊 Interactive Dashboard
- Real-time data visualization with Streamlit
- **NEW! Multi-page Dashboard** with advanced navigation
- Configurable display limits (5-20 records)
- **Interactive Plotly Charts** with zoom, pan, and export
- Expandable data tables for detailed analysis
- **Executive KPI Metrics** with real-time updates
- Interactive charts for:
  - Top medical conditions
  - Common allergies
  - Medication usage
  - Immunization coverage
  - Medical device utilization

### 🔮 Predictive Analytics (NEW!)
- **Patient Risk Scoring** - ML-based risk assessment algorithm
- **Readmission Prediction** - Identify high-risk patients
- **Cost Trend Analysis** - Financial forecasting and optimization
- **Seasonal Pattern Detection** - Time-series analysis for resource planning
- **Medication Effectiveness Analysis** - Treatment outcome insights

### 🌐 RESTful API (NEW!)
- **FastAPI-based REST API** for programmatic access
- **Auto-generated Documentation** (Swagger/OpenAPI)
- 12+ API endpoints covering:
  - Patient data
  - Medical conditions
  - Medications and allergies
  - Risk scores and predictions
  - Cost analysis
  - Demographics
- **CORS enabled** for frontend integration
- **Health check endpoint** for monitoring

### 📥 Advanced Export Features (NEW!)
- **Excel Export** with formatted, multi-sheet workbooks
- **Executive Summary Reports** - C-level ready
- **Comprehensive Healthcare Reports** - All analyses in one file
- **Individual Patient Reports** - Detailed patient history
- **Automated Report Generation** - Scheduled exports
- Professional styling with headers, colors, and auto-sizing

### 🔍 Data Analysis
- **Patient Demographics**: Age, gender, geographic distribution
- **Medical Conditions**: Disease prevalence and patterns
- **Medications**: Prescription trends and costs
- **Allergies**: Common allergic reactions
- **Immunizations**: Vaccination coverage rates
- **Devices**: Medical device usage patterns
- **Healthcare Costs**: Financial analysis

### 📈 Visualization Tools
- Age distribution charts
- Condition prevalence graphs
- Medication usage statistics
- Immunization coverage reports
- Device utilization analysis

### 🔒 Security Features
- Environment-based configuration
- No hardcoded credentials
- `.gitignore` for sensitive files
- Secure database connection handling

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Database**: MySQL 8.0+
- **Web Frameworks**: Streamlit, FastAPI
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn, SciPy
- **API**: FastAPI, Uvicorn, Pydantic
- **Database**: mysql-connector-python
- **Export**: OpenpyXL
- **Configuration**: python-dotenv

## 📁 Project Structure

```
Patient-Data-Analysis-Using-SQL/
│
├── database/                          # Database files
│   ├── schema.sql                    # Database schema definition
│   ├── sample_queries.sql            # 25+ sample SQL queries
│   └── README.md                     # Database setup guide
│
├── healthcare_data_project/
│   ├── src/
│   │   ├── dashboard.py             # ⭐ Advanced multi-page dashboard with ML analytics
│   │   ├── advanced_analytics.py    # ⭐ ML & predictive analytics module
│   │   ├── api.py                   # ⭐ RESTful API (FastAPI)
│   │   ├── export_utils.py          # ⭐ Excel/CSV export utilities
│   │   ├── generate_reports.py      # CSV report generator
│   │   ├── data_visualization.py    # Matplotlib visualizations
│   │   └── db_config.py             # Database configuration module
│   │
│   ├── data/                         # Generated CSV reports
│   │   ├── common_conditions_report.csv
│   │   ├── common_allergies_report.csv
│   │   ├── medications_report.csv
│   │   ├── immunizations_report.csv
│   │   └── devices_report.csv
│   │
│   └── docs/                         # Documentation
│
├── data/                             # Additional data files
├── .env.example                      # Example environment configuration
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── RECRUITER_GUIDE.md                # ⭐ NEW! Project showcase for recruiters
└── README.md                         # This file
```

## 🚀 Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **MySQL Server 8.0 or higher**
   ```bash
   mysql --version
   ```

3. **Git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/aachalmahakale/Patient-Data-Analysis-Using-SQL.git
cd Patient-Data-Analysis-Using-SQL
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

1. **Create the database and tables:**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

2. **Load your data** (see [Database Setup Guide](database/README.md))

### Step 5: Configure Environment

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your database credentials:**
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_NAME=healthcare_db
   DB_PORT=3306
   ```

3. **Test the connection:**
   ```bash
   python healthcare_data_project/src/db_config.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DB_HOST=localhost          # Database host
DB_USER=root              # Database username
DB_PASSWORD=your_password # Database password
DB_NAME=healthcare_db     # Database name
DB_PORT=3306              # Database port
```

### Streamlit Configuration (Optional)

Create `.streamlit/config.toml` for custom Streamlit settings:

```toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## 💻 Usage

### 1. Launch the Basic Dashboard

```bash
cd healthcare_data_project/src
streamlit run dashboard.py
```

The advanced dashboard will open in your browser at `http://localhost:8501`

**Features:**
- 🏠 **Overview Page** - Executive KPIs and key metrics
- 📊 **Analytics Page** - Demographics, encounters, devices, providers
- 🔮 **Predictive Insights** - ML-based risk scores & readmission predictions
- 💰 **Cost Analysis** - Financial trends and high-cost patient identification
- 📈 **Trends** - Seasonal patterns and temporal analysis

### 2. Start the REST API (NEW! ⭐)

```bash
cd healthcare_data_project/src
python api.py
```

**API will be available at:**
- Main API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

**Sample API Calls:**
```bash
# Get executive summary
curl http://localhost:8000/api/summary

# Get top conditions
curl http://localhost:8000/api/conditions?limit=10

# Get patient risk scores
curl http://localhost:8000/api/analytics/risk-scores

# Health check
curl http://localhost:8000/health
```

### 3. Generate Advanced Analytics Reports (NEW! ⭐)

```bash
cd healthcare_data_project/src
python advanced_analytics.py
```

**Outputs:**
- Patient risk scores
- Readmission predictions
- Cost trend analysis
- Seasonal insights
- Executive summary

### 4. Export to Excel (NEW! ⭐)

```bash
cd healthcare_data_project/src
python export_utils.py
```

**Generated Files:**
- `comprehensive_healthcare_report.xlsx` - All analyses
- `executive_summary.xlsx` - Key metrics for leadership
- Professional formatting with styled headers

### 5. Generate CSV Reports (Original)

```bash
cd healthcare_data_project/src
python generate_reports.py
```

This creates CSV files in `healthcare_data_project/data/`:
- `common_conditions_report.csv`
- `common_allergies_report.csv`
- `medications_report.csv`
- `immunizations_report.csv`
- `devices_report.csv`

### 6. Create Visualizations (Original)

```bash
cd healthcare_data_project/src
python data_visualization.py
```

Generates matplotlib charts for:
- Patient age distribution
- Common allergies
- Medication usage
- Immunization patterns
- Device utilization

### 7. Run Custom SQL Queries

Use the sample queries in `database/sample_queries.sql` or create your own:

```bash
mysql -u root -p healthcare_db < database/sample_queries.sql
```

## 🗄️ Database Schema

The database includes the following main tables:

| Table | Description | Key Fields |
|-------|-------------|------------|
| **patients** | Patient demographic data | id, birthdate, gender, address |
| **conditions** | Medical conditions/diagnoses | description, patient, start, stop |
| **allergies** | Patient allergies | description, patient, start |
| **medications** | Prescribed medications | description, patient, cost |
| **immunizations** | Vaccination records | description, patient, date |
| **devices** | Medical devices | description, patient, udi |
| **encounters** | Healthcare visits | patient, provider, encounterclass |
| **observations** | Clinical measurements | description, value, units |
| **providers** | Healthcare providers | name, speciality, organization |

For detailed schema information, see [database/schema.sql](database/schema.sql)

## 📊 Sample Queries

The project includes 25+ sample SQL queries for common analyses:

- Patient demographics (age, gender, location)
- Top medical conditions
- Medication usage and costs
- Immunization coverage
- Device utilization
- Healthcare provider analysis
- Cost analysis
- Multi-condition patients
- Emergency department utilization

See [database/sample_queries.sql](database/sample_queries.sql) for all queries.

## 📸 Screenshots

### Interactive Dashboard
*[Add screenshot of your Streamlit dashboard here]*

### Data Visualizations
*[Add screenshots of your matplotlib charts here]*

### Sample Reports
*[Add screenshot of generated CSV reports here]*

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Aachal Mahakale**
- GitHub: [@aachalmahakale](https://github.com/aachalmahakale)

## 🙏 Acknowledgments

- [Synthea](https://github.com/synthetichealth/synthea) - Synthetic patient data generator
- [Streamlit](https://streamlit.io/) - For the amazing dashboard framework
- [MySQL](https://www.mysql.com/) - For robust database management

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

⭐ **Star this repository if you find it helpful!**
