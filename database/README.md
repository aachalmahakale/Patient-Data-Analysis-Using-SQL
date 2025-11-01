# Database Setup Instructions

This document provides step-by-step instructions to set up the healthcare database.

## Prerequisites

- MySQL Server 8.0 or higher installed
- MySQL client or MySQL Workbench
- Admin/root access to MySQL

## Setup Steps

### 1. Start MySQL Server

**Windows:**
```bash
# Check if MySQL is running
net start MySQL80

# Or start from Services
services.msc
```

**Linux/Mac:**
```bash
sudo systemctl start mysql
# or
sudo service mysql start
```

### 2. Login to MySQL

```bash
mysql -u root -p
```
Enter your root password when prompted.

### 3. Create the Database and Tables

Run the schema file:
```bash
mysql -u root -p < database/schema.sql
```

Or from within MySQL:
```sql
source database/schema.sql;
```

### 4. Verify Database Creation

```sql
USE healthcare_db;
SHOW TABLES;
DESCRIBE patients;
```

You should see the following tables:
- patients
- conditions
- allergies
- medications
- immunizations
- devices
- encounters
- observations
- providers

## Database Schema Overview

### Main Tables

1. **patients** - Patient demographic information
   - Primary Key: `id` (VARCHAR(36))
   - Important fields: birthdate, gender, first, last, address, city, state

2. **conditions** - Medical conditions/diagnoses
   - Links to: patients
   - Key fields: description, start, stop

3. **allergies** - Patient allergies
   - Links to: patients
   - Key fields: description, start, stop

4. **medications** - Prescribed medications
   - Links to: patients
   - Key fields: description, start, stop, base_cost

5. **immunizations** - Vaccination records
   - Links to: patients
   - Key fields: description, date

6. **devices** - Medical devices assigned to patients
   - Links to: patients
   - Key fields: description, start, stop, udi

7. **encounters** - Healthcare visits/encounters
   - Links to: patients, providers
   - Key fields: start, stop, encounterclass, description

8. **observations** - Clinical observations/measurements
   - Links to: patients
   - Key fields: description, value, units, date

9. **providers** - Healthcare providers
   - Primary Key: `id` (VARCHAR(36))
   - Key fields: name, speciality, organization

## Loading Sample Data

### Option 1: Using CSV Files (Recommended)

If you have CSV data files from Synthea or similar sources:

```sql
USE healthcare_db;

-- Load patients
LOAD DATA LOCAL INFILE '/path/to/patients.csv'
INTO TABLE patients
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Repeat for other tables...
```

### Option 2: Using Python Script

Create a data loader script:

```python
import pandas as pd
from db_config import get_db_connection

conn = get_db_connection()

# Load from CSV
patients_df = pd.read_csv('data/patients.csv')
patients_df.to_sql('patients', conn, if_exists='append', index=False)

# Repeat for other tables...
```

### Option 3: Using Synthea Data Generator

1. Download Synthea: https://github.com/synthetichealth/synthea
2. Generate synthetic data:
   ```bash
   ./run_synthea -p 1000 Massachusetts
   ```
3. Import the generated CSV files into the database

## Configuration

### Update Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your database credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_actual_password
   DB_NAME=healthcare_db
   DB_PORT=3306
   ```

### Test Connection

Run the connection test:
```bash
python healthcare_data_project/src/db_config.py
```

You should see: `Successfully connected to MySQL Server version X.X.XX`

## Common Issues & Troubleshooting

### Issue 1: Access Denied
**Error:** `Access denied for user 'root'@'localhost'`

**Solution:**
```sql
-- Reset root password
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Issue 2: Database Already Exists
**Error:** `Can't create database 'healthcare_db'; database exists`

**Solution:** Either drop the existing database or use it:
```sql
DROP DATABASE IF EXISTS healthcare_db;
```

### Issue 3: LOCAL INFILE Disabled
**Error:** `The used command is not allowed with this MySQL version`

**Solution:**
```sql
SET GLOBAL local_infile = 1;
```

Or add to `my.cnf`:
```ini
[mysqld]
local-infile=1

[mysql]
local-infile=1
```

### Issue 4: Connection Timeout

**Solution:**
- Check if MySQL service is running
- Verify port 3306 is not blocked by firewall
- Check MySQL configuration file for bind-address

## Data Privacy & Security

⚠️ **IMPORTANT:**
- This database may contain sensitive healthcare data
- Never commit database credentials to version control
- Use strong passwords for database users
- Implement proper access controls in production
- Ensure HIPAA compliance for real patient data
- The included sample data should be synthetic/anonymized

## Additional Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Synthea Documentation](https://github.com/synthetichealth/synthea/wiki)
- [HIPAA Compliance Guidelines](https://www.hhs.gov/hipaa/index.html)

## Next Steps

After setting up the database:
1. ✅ Test the connection using `db_config.py`
2. ✅ Generate reports using `generate_reports.py`
3. ✅ View visualizations using `data_visualization.py`
4. ✅ Launch the dashboard using `streamlit run dashboard.py`

For any issues, please check the troubleshooting section or open an issue on GitHub.
