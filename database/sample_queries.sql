-- Sample Queries for Healthcare Database Analysis
-- Use these queries to analyze your healthcare data

-- ============================================
-- PATIENT DEMOGRAPHICS
-- ============================================

-- 1. Age Distribution
SELECT 
    YEAR(CURDATE()) - YEAR(birthdate) AS age,
    COUNT(*) AS patient_count
FROM patients
GROUP BY age
ORDER BY age;

-- 2. Gender Distribution
SELECT 
    gender,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patients), 2) AS percentage
FROM patients
GROUP BY gender;

-- 3. Geographic Distribution by State
SELECT 
    state,
    city,
    COUNT(*) AS patient_count
FROM patients
GROUP BY state, city
ORDER BY patient_count DESC
LIMIT 20;

-- ============================================
-- MEDICAL CONDITIONS ANALYSIS
-- ============================================

-- 4. Top 20 Most Common Conditions
SELECT 
    description,
    COUNT(*) AS occurrences,
    COUNT(DISTINCT patient) AS unique_patients
FROM conditions
GROUP BY description
ORDER BY occurrences DESC
LIMIT 20;

-- 5. Conditions by Gender
SELECT 
    c.description,
    p.gender,
    COUNT(*) AS count
FROM conditions c
JOIN patients p ON c.patient = p.id
GROUP BY c.description, p.gender
ORDER BY count DESC
LIMIT 20;

-- 6. Average Age of Patients by Condition
SELECT 
    c.description,
    ROUND(AVG(YEAR(CURDATE()) - YEAR(p.birthdate))) AS avg_age,
    COUNT(*) AS patient_count
FROM conditions c
JOIN patients p ON c.patient = p.id
GROUP BY c.description
HAVING patient_count >= 10
ORDER BY avg_age DESC;

-- ============================================
-- ALLERGIES ANALYSIS
-- ============================================

-- 7. Most Common Allergies
SELECT 
    description,
    COUNT(*) AS count,
    COUNT(DISTINCT patient) AS unique_patients
FROM allergies
GROUP BY description
ORDER BY count DESC
LIMIT 15;

-- 8. Patients with Multiple Allergies
SELECT 
    patient,
    COUNT(*) AS allergy_count
FROM allergies
GROUP BY patient
HAVING allergy_count > 3
ORDER BY allergy_count DESC;

-- ============================================
-- MEDICATION ANALYSIS
-- ============================================

-- 9. Most Prescribed Medications
SELECT 
    description,
    COUNT(*) AS prescription_count,
    COUNT(DISTINCT patient) AS unique_patients,
    ROUND(AVG(base_cost), 2) AS avg_cost
FROM medications
GROUP BY description
ORDER BY prescription_count DESC
LIMIT 20;

-- 10. Total Medication Costs by Patient
SELECT 
    patient,
    COUNT(*) AS medication_count,
    ROUND(SUM(base_cost), 2) AS total_cost
FROM medications
GROUP BY patient
ORDER BY total_cost DESC
LIMIT 20;

-- 11. Medications by Condition
SELECT 
    c.description AS condition_name,
    m.description AS medication,
    COUNT(*) AS usage_count
FROM medications m
JOIN conditions c ON m.patient = c.patient AND m.reasoncode = c.code
GROUP BY c.description, m.description
ORDER BY usage_count DESC
LIMIT 30;

-- ============================================
-- IMMUNIZATION ANALYSIS
-- ============================================

-- 12. Immunization Coverage
SELECT 
    description,
    COUNT(*) AS total_immunizations,
    COUNT(DISTINCT patient) AS unique_patients,
    ROUND(COUNT(DISTINCT patient) * 100.0 / (SELECT COUNT(*) FROM patients), 2) AS coverage_percentage
FROM immunizations
GROUP BY description
ORDER BY total_immunizations DESC;

-- 13. Immunization Timeline
SELECT 
    YEAR(date) AS year,
    COUNT(*) AS immunization_count
FROM immunizations
WHERE date IS NOT NULL
GROUP BY YEAR(date)
ORDER BY year DESC;

-- ============================================
-- DEVICE USAGE ANALYSIS
-- ============================================

-- 14. Most Common Medical Devices
SELECT 
    description,
    COUNT(*) AS usage_count,
    COUNT(DISTINCT patient) AS unique_patients
FROM devices
GROUP BY description
ORDER BY usage_count DESC;

-- 15. Average Device Usage Duration
SELECT 
    description,
    COUNT(*) AS total_devices,
    ROUND(AVG(DATEDIFF(COALESCE(stop, CURDATE()), start))) AS avg_days_used
FROM devices
GROUP BY description
HAVING total_devices >= 5
ORDER BY avg_days_used DESC;

-- ============================================
-- ENCOUNTER ANALYSIS
-- ============================================

-- 16. Encounter Types Distribution
SELECT 
    encounterclass,
    COUNT(*) AS encounter_count,
    ROUND(AVG(base_encounter_cost), 2) AS avg_cost
FROM encounters
GROUP BY encounterclass
ORDER BY encounter_count DESC;

-- 17. Healthcare Provider Utilization
SELECT 
    p.name AS provider_name,
    p.speciality,
    COUNT(e.id) AS encounter_count,
    p.city,
    p.state
FROM providers p
LEFT JOIN encounters e ON p.id = e.provider
GROUP BY p.id, p.name, p.speciality, p.city, p.state
ORDER BY encounter_count DESC
LIMIT 20;

-- 18. Average Length of Stay
SELECT 
    encounterclass,
    COUNT(*) AS encounter_count,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, start, stop) / 24.0), 2) AS avg_length_of_stay_days
FROM encounters
WHERE stop IS NOT NULL
GROUP BY encounterclass
ORDER BY avg_length_of_stay_days DESC;

-- ============================================
-- COST ANALYSIS
-- ============================================

-- 19. Total Healthcare Expenses by Patient
SELECT 
    p.id,
    CONCAT(p.first, ' ', p.last) AS patient_name,
    p.healthcare_expenses,
    p.healthcare_coverage,
    ROUND(p.healthcare_expenses - p.healthcare_coverage, 2) AS out_of_pocket
FROM patients p
ORDER BY p.healthcare_expenses DESC
LIMIT 20;

-- 20. Most Expensive Conditions
SELECT 
    c.description,
    COUNT(DISTINCT c.patient) AS patient_count,
    ROUND(AVG(p.healthcare_expenses), 2) AS avg_patient_expense
FROM conditions c
JOIN patients p ON c.patient = p.id
GROUP BY c.description
HAVING patient_count >= 10
ORDER BY avg_patient_expense DESC
LIMIT 20;

-- ============================================
-- OBSERVATION ANALYSIS
-- ============================================

-- 21. Most Common Observations
SELECT 
    description,
    type,
    COUNT(*) AS observation_count,
    units
FROM observations
GROUP BY description, type, units
ORDER BY observation_count DESC
LIMIT 20;

-- 22. Patient Health Trends (BMI Example)
SELECT 
    patient,
    DATE_FORMAT(date, '%Y-%m') AS month,
    AVG(CAST(value AS DECIMAL(10,2))) AS avg_value
FROM observations
WHERE description LIKE '%Body Mass Index%'
    AND value REGEXP '^[0-9]+'
GROUP BY patient, DATE_FORMAT(date, '%Y-%m')
ORDER BY patient, month;

-- ============================================
-- COMPLEX QUERIES
-- ============================================

-- 23. Patients with Multiple Chronic Conditions
SELECT 
    p.id,
    CONCAT(p.first, ' ', p.last) AS patient_name,
    YEAR(CURDATE()) - YEAR(p.birthdate) AS age,
    p.gender,
    COUNT(DISTINCT c.description) AS condition_count,
    GROUP_CONCAT(DISTINCT c.description SEPARATOR '; ') AS conditions
FROM patients p
JOIN conditions c ON p.id = c.patient
WHERE c.stop IS NULL  -- Active conditions
GROUP BY p.id, patient_name, age, p.gender
HAVING condition_count >= 3
ORDER BY condition_count DESC;

-- 24. Medication Adherence Analysis
SELECT 
    patient,
    description,
    COUNT(*) AS refill_count,
    MIN(start) AS first_prescription,
    MAX(start) AS last_prescription,
    DATEDIFF(MAX(start), MIN(start)) AS days_between_first_last
FROM medications
GROUP BY patient, description
HAVING refill_count > 1
ORDER BY refill_count DESC;

-- 25. Emergency Department Utilization
SELECT 
    p.id,
    CONCAT(p.first, ' ', p.last) AS patient_name,
    COUNT(e.id) AS ed_visits,
    YEAR(CURDATE()) - YEAR(p.birthdate) AS age
FROM patients p
JOIN encounters e ON p.id = e.patient
WHERE e.encounterclass = 'emergency'
GROUP BY p.id, patient_name, age
HAVING ed_visits >= 3
ORDER BY ed_visits DESC;
