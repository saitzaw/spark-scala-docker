------------------------------------------------------------
-- CRM Contacts Schema
------------------------------------------------------------
-- This script creates the Contacts table for the CRM system.
------------------------------------------------------------
-- Ensure the script is run in a transaction block
-- 
-- Auther: <> Version: <> Date: <>
-- Author: Sai Thiha Zaw Version: 1.0  Date: 2025-06-02
------------------------------------------------------------

DROP TABLE IF EXISTS contacts CASCADE;
-- Contacts
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    title VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contacts_customer_id ON contacts(customer_id);