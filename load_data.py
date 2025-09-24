# load_data.py
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DB = os.getenv("DB_NAME", "food_wastage")

DB_URI = f"mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/{DB}?charset=utf8mb4"
engine = create_engine(DB_URI, future=True)

def load_csv_to_table(csv_path, table_name, dtype_map=None, parse_dates=None):
    df = pd.read_csv(csv_path, parse_dates=parse_dates)
    # Data cleaning: drop duplicates and NaNs in PK columns
    if table_name == 'providers':
        df = df.drop_duplicates(subset=['Provider_ID']).fillna('')
    if table_name == 'receivers':
        df = df.drop_duplicates(subset=['Receiver_ID']).fillna('')
    if table_name == 'food_listings':
        # ensure Expiry_Date as date
        if 'Expiry_Date' in df.columns:
            df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], errors='coerce').dt.date
        df = df.drop_duplicates(subset=['Food_ID']).fillna('')
    if table_name == 'claims':
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.drop_duplicates(subset=['Claim_ID']).fillna('')
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":
    load_csv_to_table("data/providers_data.csv", "providers")
    load_csv_to_table("data/receivers_data.csv", "receivers")
    load_csv_to_table("data/food_listings_data.csv", "food_listings", parse_dates=['Expiry_Date'])
    load_csv_to_table("data/claims_data.csv", "claims", parse_dates=['Timestamp'])
