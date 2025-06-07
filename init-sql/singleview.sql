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

SELECT
    c.id AS customer_id,
    c.name AS customer_name,
    c.industry,
    c.region,
    c.phone AS customer_phone,
    c.website,
    c.tags,
    c.metadata::jsonb ->> 'customer_tier' AS customer_tier,

    ct.full_name AS contact_name,
    ct.email AS contact_email,
    ct.phone AS contact_phone,
    ct.title AS contact_title,

    l.full_name AS lead_name,
    l.email AS lead_email,
    l.phone AS lead_phone,
    l.status AS lead_status,
    l.source AS lead_source,
    l.metadata AS lead_metadata,

    o.name AS opportunity_name,
    o.value AS opportunity_value,
    o.stage AS opportunity_stage,
    o.close_date,
    o.probability,
    o.notes AS opportunity_notes,

    a.subject AS last_activity_subject,
    a.activity_type AS last_activity_type,
    a.notes AS last_activity_notes,
    a.context::jsonb ->> 'duration_minutes' AS activity_duration,

    ord.id AS latest_order_id,
    ord.order_date,
    ord.total_amount,

    t.amount AS last_transaction_amount,
    t.timestamp as trasnscation_date

FROM customers c

LEFT JOIN contacts ct ON ct.customer_id = c.id
LEFT JOIN leads l ON l.assigned_to IS NOT NULL AND l.metadata::jsonb ->> 'region' = c.region
LEFT JOIN opportunities o ON o.customer_id = c.id
LEFT JOIN activities a ON a.contact_id = ct.id
LEFT JOIN orders ord ON ord.customer_id = c.id
LEFT JOIN (
    SELECT DISTINCT ON (order_id)
        id,
        order_id,
        amount,
        timestamp
    FROM transactions
    ORDER BY order_id, timestamp DESC
) AS t ON t.order_id = ord.id;
