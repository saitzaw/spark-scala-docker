import os
from dotenv import load_dotenv

# Load from .env file
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / ".env"  # adjust if needed
load_dotenv(dotenv_path)

print(f"Loading environment variables from: {dotenv_path}")
# Access variables
def env_parameter(): 
    jdbc_url = os.getenv("JDBC_URL")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    spark_master = os.getenv("SPARK_MASTER")
    pg_jar = os.getenv("PG_JAR")
    event_log_dir = os.getenv("EVENT_LOG_DIR")
    pg_driver = os.getenv("PG_DIRIVER")
    minio_user = os.getenv("MINIO_USER")
    minio_pass = os.getenv("MINIO_PASSWORD")


    return {
        'jdbc_url': jdbc_url,
        'db_user': db_user, 
        'db_password': db_password, 
        'spark_master': spark_master,
        'pg_jar': pg_jar,
        'event_log_dir': event_log_dir,
        'pg_driver': pg_driver,
        'minio_user': minio_user,
        'minio_pass': minio_pass
        }
