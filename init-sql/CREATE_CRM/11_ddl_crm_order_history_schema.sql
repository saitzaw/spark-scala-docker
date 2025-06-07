------------------------------------------------------------
-- CRM Users Schema
------------------------------------------------------------
-- This script creates the users table for the CRM system.
------------------------------------------------------------
-- Ensure the script is run in a transaction block
-- 
-- Auther: <> Version: <> Date: <>
-- Author: Sai Thiha Zaw Version: 1.0  Date: 2025-06-07
------------------------------------------------------------

CREATE TABLE order_history (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
CREATE INDEX idx_order_history_order_id ON order_history(order_id);