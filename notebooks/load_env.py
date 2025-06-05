import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Access variables
def env_parameter(): 
    jdbc_url = os.getenv("JDBC_URL")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    spark_master = os.getenv("SPARK_MASTER")
    return {
        'jdbc_url': jdbc_url,
        'db_user': db_user, 
        'db_password': db_password, 
        'spark_master': spark_master}
