-- Seed leads
INSERT INTO leads (source, full_name, email, phone, status, assigned_to, metadata) VALUES
  ('Web', 'Derek Cole', 'derek.cole@example.com', '555-3001', 'contacted', 1, '{"interest": "CRM"}'),
  ('Email Campaign', 'Tina Brooks', 'tina.brooks@example.com', '555-3002', 'new', 2, '{"lead_score": 68}'),
  ('Event', 'Alex Reed', 'alex.reed@example.com', '555-3003', 'qualified', 3, '{"region": "Asia-Pacific"}');
