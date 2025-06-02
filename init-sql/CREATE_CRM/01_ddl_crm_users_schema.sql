------------------------------------------------------------
-- CRM Users Schema
------------------------------------------------------------
-- This script creates the users table for the CRM system.
------------------------------------------------------------
-- Ensure the script is run in a transaction block
-- 
-- Auther: <> Version: <> Date: <>
-- Author: Sai Thiha Zaw Version: 1.0  Date: 2025-06-02
------------------------------------------------------------

DROP TABLE IF EXISTS users CASCADE;
-- Users (Sales reps)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'sales',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_role ON users(role);