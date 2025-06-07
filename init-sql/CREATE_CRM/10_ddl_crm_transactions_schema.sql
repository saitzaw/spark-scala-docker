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

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    transaction_type VARCHAR(50),
    amount NUMERIC(10, 2),
    status VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
CREATE INDEX idx_transactions_order_id ON transactions(order_id);