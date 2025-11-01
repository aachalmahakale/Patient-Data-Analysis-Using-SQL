# 🚀 Quick Feature Guide

> See [CHANGELOG.md](CHANGELOG.md) for complete version history

## 🎯 Quick Start

```bash
# Run the dashboard
cd healthcare_data_project/src
streamlit run dashboard.py

# Or start the API
python api.py
```

---

## 📊 Main Features

### 1. **Multi-Page Dashboard** (`dashboard.py`)
5 interactive pages with ML analytics:
- 🏠 Overview - Executive KPIs
- � Analytics - Demographics, encounters, devices
- 🔮 Predictive Insights - Risk scoring & readmission predictions  
- 💰 Cost Analysis - Financial trends
- 📈 Trends - Seasonal patterns

### 2. **REST API** (`api.py`)
12+ endpoints with auto-generated docs at `/docs`

### 3. **ML Analytics** (`advanced_analytics.py`)
```python
from advanced_analytics import HealthcareAnalytics

analytics = HealthcareAnalytics()
risk_df = analytics.patient_risk_score()
readmission_df = analytics.readmission_prediction()
cost_df = analytics.cost_trend_analysis()
```

### 4. **Excel Export** (`export_utils.py`)
Professional reports with formatting
- ✅ **Individual Patient Reports** - Detailed patient history
- ✅ **Professional Formatting** - Styled headers, colors, auto-sizing
- ✅ **Multi-sheet Workbooks** - Organized data tabs

**Example Usage:**
```python
from export_utils import HealthcareExporter

exporter = HealthcareExporter()

# Export comprehensive report
exporter.export_comprehensive_report()

# Export executive summary
exporter.export_executive_summary()

# Export individual patient
exporter.export_patient_report(patient_id='abc-123')
```

**Run It:**
```bash
python export_utils.py
# Check exports/ folder
```

---

## � Key Algorithms

### Risk Scoring
```python
risk_score = (condition_count * 15) + (medication_count * 10) + 
             (allergy_count * 5) + (age * 0.5)
```
Categories: Low (0-30), Medium (31-60), High (61-100)

### Readmission Risk
Based on emergency visits, inpatient count, and length of stay

---

## 🔄 Upgrade from v1.0

```bash
pip install -r requirements.txt --upgrade
```

All original scripts still work. `dashboard.py` now includes all advanced features.

---

See [README.md](README.md) for full documentation.
