import os
import pandas as pd
from sqlalchemy import create_engine, Text, Float, DateTime
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "job_market_db")

def load_to_mysql(df: pd.DataFrame):
    print("[3/3] Loading cleaned data into MySQL...")
    
    # Create MySQL connection string
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)

    # Map SQL types explicitly so text fields don't get truncated
    dtype_mapping = {
        'job_id': Text(),
        'company': Text(),
        'position': Text(),
        'location': Text(),      # <-- Text allows up to 65,535 characters
        'avg_salary': Float(),
        'currency': Text(),
        'posted_date': DateTime()
    }

    # Write to MySQL table (if_exists='replace' will drop the old schema with tight columns)
    df.to_sql(
        name='dim_jobs',
        con=engine,
        if_exists='replace',
        index=False,
        dtype=dtype_mapping
    )
    
    print("ETL Pipeline Completed Successfully!")

if __name__ == "__main__":
    # Test execution with dummy/sample dataframe if run standalone
    from scripts.clean import clean_himalayas_jobs
    df = clean_himalayas_jobs()
    load_to_mysql(df)