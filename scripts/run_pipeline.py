from scripts.extract import extract_himalayas_jobs
from scripts.clean import clean_himalayas_jobs
from scripts.load import load_to_mysql

def run_full_pipeline():
    print("==========================================")
    print(" Starting Job Market ETL Pipeline         ")
    print("==========================================")
    
    # Run Extract -> Clean -> Load
    raw_filepath = extract_himalayas_jobs(max_jobs=100)
    clean_df = clean_himalayas_jobs(raw_filepath)
    load_to_mysql(clean_df)

if __name__ == "__main__":
    run_full_pipeline()