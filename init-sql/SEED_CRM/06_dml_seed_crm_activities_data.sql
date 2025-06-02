-- Seed activities
INSERT INTO activities (activity_type, subject, notes, contact_id, user_id, context) VALUES
  ('call', 'Intro Call with Sarah Thomas', 'Overview of CRM solution benefits.', 1, 1, '{"duration_minutes": 20}'),
  ('email', 'Proposal Sent to Robert Allen', 'Shared pricing and solution overview.', 2, 2, '{"attachments": ["proposal_contoso.pdf"]}'),
  ('meeting', 'Product Demo for Emily Stone', 'Showcased inventory integration.', 3, 3, '{"platform": "Zoom", "duration_minutes": 45}');
