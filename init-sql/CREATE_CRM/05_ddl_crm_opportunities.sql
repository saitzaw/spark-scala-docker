------------------------------------------------------------
-- CRM Opportunities Schema
------------------------------------------------------------
-- This script creates the Opportunities table for the CRM system.
------------------------------------------------------------
-- Ensure the script is run in a transaction block
-- 
-- Auther: <> Version: <> Date: <>
-- Author: Sai Thiha Zaw Version: 1.0  Date: 2025-06-02
------------------------------------------------------------

DROP TABLE IF EXISTS opportunities CASCADE;
-- Opportunities
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    name VARCHAR(100),
    value DECIMAL(12,2),
    stage VARCHAR(50),  -- e.g., prospecting, proposal, closed
    probability INTEGER CHECK (probability BETWEEN 0 AND 100),
    close_date DATE,
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    notes TEXT,
    metadata JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_opportunities_stage ON opportunities(stage);
CREATE INDEX idx_opportunities_close_date ON opportunities(close_date);
CREATE INDEX idx_opportunities_metadata ON opportunities USING GIN (metadata);