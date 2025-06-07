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
CREATE TABLE product_details (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    specification TEXT,
    image_url TEXT,
    warranty_info TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE(product_id)
);
CREATE INDEX idx_product_details_product_id ON product_details(product_id);