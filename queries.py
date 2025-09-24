from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
DB_URI = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@" \
         f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
engine = create_engine(DB_URI, future=True)

def run(q, params=None):
    with engine.connect() as conn:
        df = pd.read_sql_query(text(q), conn, params=params)
    return df

queries = {
    "q1": ("How many food providers and receivers are there in each city",
           "SELECT City, COUNT(DISTINCT Provider_ID) AS providers_count FROM providers GROUP BY City;"),

    "q2": ("Which type of food provider contributes the most food",
           "SELECT Provider_Type, COUNT(*) AS listings FROM food_listings GROUP BY Provider_Type ORDER BY listings DESC;"),

    "q3": ("Contact information of food providers in a specific city (example: 'Hyderabad')",
           "SELECT Name, Contact, Address FROM providers WHERE City = :city;", {'city': 'Hyderabad'}),

    "q4": ("Which receivers have claimed the most food",
           "SELECT r.Name, COUNT(*) AS claims_count FROM claims c JOIN receivers r ON c.Receiver_ID=r.Receiver_ID "
           "GROUP BY r.Name ORDER BY claims_count DESC;"),

    "q5": ("Total quantity of food available",
           "SELECT SUM(Quantity) AS total_quantity FROM food_listings;"),

    "q6": ("City with highest number of food listings",
           "SELECT Location AS City, COUNT(*) AS listings FROM food_listings GROUP BY Location ORDER BY listings DESC LIMIT 1;"),

    "q7": ("Most commonly available food types",
           "SELECT Food_Type, COUNT(*) AS count FROM food_listings GROUP BY Food_Type ORDER BY count DESC;"),

    "q8": ("How many food claims made for each food item",
           "SELECT f.Food_Name, COUNT(*) AS claims FROM claims c JOIN food_listings f ON c.Food_ID=f.Food_ID "
           "GROUP BY f.Food_Name ORDER BY claims DESC;"),

    "q9": ("Provider with highest number of successful food claims",
           "SELECT p.Name, COUNT(*) AS successful_claims FROM claims c JOIN food_listings f ON c.Food_ID=f.Food_ID "
           "JOIN providers p ON f.Provider_ID=p.Provider_ID WHERE c.Status='Completed' "
           "GROUP BY p.Name ORDER BY successful_claims DESC LIMIT 1;"),

    "q10": ("Percentage of claims by status",
            "SELECT Status, ROUND(COUNT(*)*100/(SELECT COUNT(*) FROM claims),2) AS percent FROM claims GROUP BY Status;"),

    "q11": ("Average quantity of food claimed per receiver",
            "SELECT r.Name, AVG(f.Quantity) AS avg_quantity FROM claims c JOIN receivers r ON c.Receiver_ID=r.Receiver_ID "
            "JOIN food_listings f ON c.Food_ID=f.Food_ID GROUP BY r.Name ORDER BY avg_quantity DESC;"),

    "q12": ("Which meal type is claimed the most",
            "SELECT f.Meal_Type, COUNT(*) AS claims FROM claims c JOIN food_listings f ON c.Food_ID=f.Food_ID "
            "GROUP BY f.Meal_Type ORDER BY claims DESC;"),

    "q13": ("Total quantity donated by each provider",
            "SELECT p.Name, SUM(f.Quantity) AS total_donated FROM food_listings f JOIN providers p "
            "ON f.Provider_ID=p.Provider_ID GROUP BY p.Name ORDER BY total_donated DESC;"),

    "q14": ("Top items near expiry (next 3 days)",
            "SELECT * FROM food_listings WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 DAY) ORDER BY Expiry_Date ASC;"),

    "q15": ("Daily claims trend (last 30 days)",
            "SELECT DATE(Timestamp) as day, COUNT(*) as claims FROM claims WHERE Timestamp >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY day ORDER BY day;")
}

if __name__ == "__main__":
    for k, value in queries.items():
        # Flexible unpacking
        if len(value) == 3:
            desc, sql, params = value
        else:
            desc, sql = value
            params = None

        print("=== ", k, desc)
        df = run(sql, params)
        print(df.head())
        df.to_csv(f"output_{k}.csv", index=False)
