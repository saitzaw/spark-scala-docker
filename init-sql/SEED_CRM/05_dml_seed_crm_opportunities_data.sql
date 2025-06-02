-- Seed opportunities
INSERT INTO opportunities (customer_id, name, value, stage, probability, close_date, assigned_to, notes, metadata) VALUES
  (1, 'CRM Upgrade Package', 30000.00, 'proposal', 60, '2025-07-15', 1, 'Evaluating custom reporting features', '{"priority": "high"}'),
  (2, 'Cloud Migration Support', 75000.00, 'negotiation', 80, '2025-08-10', 2, 'Negotiating licensing terms', '{"platform": "Azure"}');