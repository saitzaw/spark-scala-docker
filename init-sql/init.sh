# create a schema 
for f in /sql_scripts/CREATE/*.sql; do
  psql -U sparkuser -d sparkdb -f "$f"
done

# insert seed data 
for f in /sql_scripts/INSERT/*.sql; do
  psql -U sparkuser -d sparkdb -f "$f"
done