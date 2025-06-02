-- Seed customers
INSERT INTO customers (name, industry, region, phone, website, tags, metadata) VALUES
  ('Northwind Traders', 'Retail', 'North America', '555-1001', 'https://northwind.com', ARRAY['active', 'key'], '{"customer_tier": "platinum"}'),
  ('Contoso Ltd', 'Technology', 'Europe', '555-1002', 'https://contoso.com', ARRAY['prospect'], '{"platform": "Azure"}'),
  ('Adventure Works', 'Manufacturing', 'Asia', '555-1003', 'https://adventureworks.com', ARRAY['new'], '{"needs": "IoT integration"}');
