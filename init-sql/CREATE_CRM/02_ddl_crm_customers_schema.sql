------------------------------------------------------------
-- CRM Customers Schema
------------------------------------------------------------
-- This script creates the Customers table for the CRM system.
------------------------------------------------------------
-- Ensure the script is run in a transaction block
-- 
-- Auther: <> Version: <> Date: <>
-- Author: Sai Thiha Zaw Version: 1.0  Date: 2025-06-02
------------------------------------------------------------

DROP TABLE IF EXISTS customers CASCADE;

-- Customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(100),
    region VARCHAR(50),
    phone VARCHAR(20),
    website VARCHAR(255),
    tags TEXT[],                         -- tag support
    metadata JSONB DEFAULT '{}'::JSONB,  -- flexible attributes (custom fields)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_customers_region ON customers(region);
CREATE INDEX idx_customers_industry ON customers(industry);
CREATE INDEX idx_customers_metadata ON customers USING GIN (metadata);