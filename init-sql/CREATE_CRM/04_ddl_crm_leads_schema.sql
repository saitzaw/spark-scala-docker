------------------------------------------------------------
-- CRM Leads Schema
------------------------------------------------------------
-- This script creates the Leads table for the CRM system.
------------------------------------------------------------
-- Ensure the script is run in a transaction block
-- 
-- Auther: <> Version: <> Date: <>
-- Author: Sai Thiha Zaw Version: 1.0  Date: 2025-06-02
------------------------------------------------------------

DROP TABLE IF EXISTS leads CASCADE;
-- Leads
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100),
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    status VARCHAR(50) DEFAULT 'new',
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    metadata JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_assigned_to ON leads(assigned_to);
CREATE INDEX idx_leads_metadata ON leads USING GIN (metadata);