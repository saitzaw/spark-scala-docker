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

DROP TABLE IF EXISTS activities CASCADE;
-- Activities
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    activity_type VARCHAR(50),  -- call, email, meeting, etc.
    subject VARCHAR(255),
    notes TEXT,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context JSONB DEFAULT '{}'::JSONB  -- call logs, meeting info, etc.
);

-- Indexes for performance optimization
CREATE INDEX idx_activities_type ON activities(activity_type);
CREATE INDEX idx_activities_contact_id ON activities(contact_id);
CREATE INDEX idx_activities_context ON activities USING GIN (context);