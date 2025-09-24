# db_setup.py
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "food_wastage")

ROOT_URI = f"mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/"
DB_URI = f"mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}?charset=utf8mb4"

# connect to server (no db) to create db
engine_root = create_engine(ROOT_URI, future=True)
with engine_root.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
    print("Database ensured:", DB_NAME)

engine = create_engine(DB_URI, future=True)
with engine.connect() as conn:
    # create providers
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS providers (
      Provider_ID INT PRIMARY KEY,
      Name VARCHAR(255),
      Type VARCHAR(100),
      Address TEXT,
      City VARCHAR(100),
      Contact VARCHAR(50)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS receivers (
      Receiver_ID INT PRIMARY KEY,
      Name VARCHAR(255),
      Type VARCHAR(100),
      City VARCHAR(100),
      Contact VARCHAR(50)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS food_listings (
      Food_ID INT PRIMARY KEY,
      Food_Name VARCHAR(255),
      Quantity INT,
      Expiry_Date DATE,
      Provider_ID INT,
      Provider_Type VARCHAR(100),
      Location VARCHAR(100),
      Food_Type VARCHAR(100),
      Meal_Type VARCHAR(100),
      FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS claims (
      Claim_ID INT PRIMARY KEY,
      Food_ID INT,
      Receiver_ID INT,
      Status VARCHAR(50),
      Timestamp DATETIME,
      FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
      FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
    );
    """))
    print("Tables ensured.")
