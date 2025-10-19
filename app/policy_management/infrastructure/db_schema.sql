-- TMHCC Policy Management Database Schema

-- Policy Statuses lookup table
CREATE TABLE IF NOT EXISTS policy_statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(100)
);

-- Policy Types lookup table  
CREATE TABLE IF NOT EXISTS policy_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(100)
);

-- Main Policies table
CREATE TABLE IF NOT EXISTS policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_number VARCHAR(50) UNIQUE NOT NULL,
    insured_name VARCHAR(200) NOT NULL,
    premium_amount DECIMAL(15, 2) NOT NULL,
    premium_currency VARCHAR(3) NOT NULL DEFAULT 'GBP',
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    status_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (status_id) REFERENCES policy_statuses(id),
    FOREIGN KEY (type_id) REFERENCES policy_types(id)
);

-- Indexes for optimal query performance
CREATE INDEX IF NOT EXISTS idx_policies_policy_number ON policies(policy_number);
CREATE INDEX IF NOT EXISTS idx_policies_insured_name ON policies(insured_name);
CREATE INDEX IF NOT EXISTS idx_policies_status ON policies(status_id);
CREATE INDEX IF NOT EXISTS idx_policies_type ON policies(type_id);
CREATE INDEX IF NOT EXISTS idx_policies_period ON policies(period_start_date, period_end_date);
CREATE INDEX IF NOT EXISTS idx_policies_created_at ON policies(created_at);