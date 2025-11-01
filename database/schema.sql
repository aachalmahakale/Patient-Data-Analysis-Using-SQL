-- Healthcare Database Schema
-- Database: healthcare_db
-- Description: Schema for healthcare data analysis system

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

-- ============================================
-- PATIENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS patients (
    id VARCHAR(36) PRIMARY KEY,
    birthdate DATE NOT NULL,
    deathdate DATE,
    ssn VARCHAR(11),
    drivers VARCHAR(20),
    passport VARCHAR(20),
    prefix VARCHAR(10),
    first VARCHAR(50) NOT NULL,
    last VARCHAR(50) NOT NULL,
    suffix VARCHAR(10),
    maiden VARCHAR(50),
    marital VARCHAR(1),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    gender VARCHAR(1) NOT NULL,
    birthplace VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    county VARCHAR(100),
    zip VARCHAR(10),
    lat DECIMAL(10, 6),
    lon DECIMAL(10, 6),
    healthcare_expenses DECIMAL(10, 2),
    healthcare_coverage DECIMAL(10, 2),
    INDEX idx_birthdate (birthdate),
    INDEX idx_gender (gender),
    INDEX idx_city (city),
    INDEX idx_state (state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- CONDITIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS conditions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start DATE NOT NULL,
    stop DATE,
    patient VARCHAR(36) NOT NULL,
    encounter VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(255) NOT NULL,
    INDEX idx_patient (patient),
    INDEX idx_description (description),
    INDEX idx_start_date (start),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- ALLERGIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS allergies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start DATE NOT NULL,
    stop DATE,
    patient VARCHAR(36) NOT NULL,
    encounter VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(255) NOT NULL,
    INDEX idx_patient (patient),
    INDEX idx_description (description),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- MEDICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS medications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start DATE NOT NULL,
    stop DATE,
    patient VARCHAR(36) NOT NULL,
    payer VARCHAR(36),
    encounter VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(255) NOT NULL,
    base_cost DECIMAL(10, 2),
    payer_coverage DECIMAL(10, 2),
    dispenses INT,
    totalcost DECIMAL(10, 2),
    reasoncode VARCHAR(20),
    reasondescription VARCHAR(255),
    INDEX idx_patient (patient),
    INDEX idx_description (description),
    INDEX idx_start_date (start),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- IMMUNIZATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS immunizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    patient VARCHAR(36) NOT NULL,
    encounter VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(255) NOT NULL,
    base_cost DECIMAL(10, 2),
    INDEX idx_patient (patient),
    INDEX idx_description (description),
    INDEX idx_date (date),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- DEVICES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start DATE NOT NULL,
    stop DATE,
    patient VARCHAR(36) NOT NULL,
    encounter VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(255) NOT NULL,
    udi VARCHAR(100),
    INDEX idx_patient (patient),
    INDEX idx_description (description),
    INDEX idx_start_date (start),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- ENCOUNTERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS encounters (
    id VARCHAR(36) PRIMARY KEY,
    start DATETIME NOT NULL,
    stop DATETIME,
    patient VARCHAR(36) NOT NULL,
    organization VARCHAR(36),
    provider VARCHAR(36),
    payer VARCHAR(36),
    encounterclass VARCHAR(50),
    code VARCHAR(20),
    description VARCHAR(255),
    base_encounter_cost DECIMAL(10, 2),
    total_claim_cost DECIMAL(10, 2),
    payer_coverage DECIMAL(10, 2),
    reasoncode VARCHAR(20),
    reasondescription VARCHAR(255),
    INDEX idx_patient (patient),
    INDEX idx_start (start),
    INDEX idx_provider (provider),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- OBSERVATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS observations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    patient VARCHAR(36) NOT NULL,
    encounter VARCHAR(36),
    code VARCHAR(20),
    description VARCHAR(255) NOT NULL,
    value VARCHAR(100),
    units VARCHAR(50),
    type VARCHAR(50),
    INDEX idx_patient (patient),
    INDEX idx_date (date),
    INDEX idx_description (description),
    FOREIGN KEY (patient) REFERENCES patients(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- PROVIDERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS providers (
    id VARCHAR(36) PRIMARY KEY,
    organization VARCHAR(36),
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(1),
    speciality VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(10),
    lat DECIMAL(10, 6),
    lon DECIMAL(10, 6),
    utilization INT DEFAULT 0,
    INDEX idx_speciality (speciality),
    INDEX idx_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- DISPLAY TABLE INFORMATION
-- ============================================
SHOW TABLES;
