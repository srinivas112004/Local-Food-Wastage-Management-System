import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine
from datetime import date
from queries import queries, run as run_query_func  # Import queries + run function

st.set_page_config(page_title="Local Food Wastage System", layout="wide")
st.title("🍽 Local Food Wastage Management System")

engine = get_engine()

@st.cache_data
def run_query(q, params=None):
    with engine.connect() as conn:
        return pd.read_sql_query(text(q), conn, params=params)

menu = st.sidebar.selectbox("Menu", ["View Data", "Add Food", "Update Food", "Delete Food", "Analysis & Queries"])

# ------------------------ VIEW DATA ------------------------
if menu == "View Data":
    st.header("Food listings")
    df = run_query("SELECT f.*, p.Name as Provider_Name, p.Contact as Provider_Contact FROM food_listings f LEFT JOIN providers p ON f.Provider_ID=p.Provider_ID;")
    st.write("Total listings:", len(df))
    city = st.multiselect("Filter by City", options=sorted(df['Location'].dropna().unique()))
    food_type = st.multiselect("Filter by Food Type", options=sorted(df['Food_Type'].dropna().unique()))
    if city:
        df = df[df['Location'].isin(city)]
    if food_type:
        df = df[df['Food_Type'].isin(food_type)]
    st.dataframe(df)

# ------------------------ ADD FOOD ------------------------
elif menu == "Add Food":
    st.header("Add new food listing")
    with st.form("add_form"):
        food_id = st.number_input("Food ID", min_value=1, step=1)
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        expiry = st.date_input("Expiry Date", value=date.today())
        provider_id = st.number_input("Provider ID", min_value=1, step=1)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("Location / City")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        submitted = st.form_submit_button("Add")
    if submitted:
        try:
            insert = text("""INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                             VALUES (:id, :name, :qty, :expiry, :pid, :ptype, :loc, :ftype, :mtype)""")
            with engine.begin() as conn:
                conn.execute(insert, {
                    "id": int(food_id), "name": food_name, "qty": int(quantity),
                    "expiry": expiry, "pid": int(provider_id), "ptype": provider_type,
                    "loc": location, "ftype": food_type, "mtype": meal_type
                })
            st.success("Food listing added.")
        except Exception as e:
            st.error("Error adding food: " + str(e))

# ------------------------ UPDATE FOOD ------------------------
elif menu == "Update Food":
    st.header("Update food listing")
    df = run_query("SELECT Food_ID, Food_Name, Quantity, Expiry_Date FROM food_listings;")
    if df.empty:
        st.info("No listings found.")
    else:
        fid = st.selectbox("Select Food ID", df["Food_ID"].tolist())
        row = df[df["Food_ID"] == fid].iloc[0]
        new_qty = st.number_input("Quantity", value=int(row["Quantity"]), step=1)
        new_exp = st.date_input("Expiry Date", value=pd.to_datetime(row["Expiry_Date"]).date())
        if st.button("Update"):
            try:
                with engine.begin() as conn:
                    conn.execute(text("UPDATE food_listings SET Quantity=:q, Expiry_Date=:e WHERE Food_ID=:id"),
                                 {"q": int(new_qty), "e": new_exp, "id": int(fid)})
                st.success("Updated.")
            except Exception as e:
                st.error("Update failed: " + str(e))

# ------------------------ DELETE FOOD ------------------------
elif menu == "Delete Food":
    st.header("Delete food listing")
    df = run_query("SELECT Food_ID, Food_Name FROM food_listings;")
    if df.empty:
        st.info("No listings found.")
    else:
        fid = st.selectbox("Select Food ID to delete", df["Food_ID"].tolist())
        if st.button("Delete"):
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM food_listings WHERE Food_ID = :id"), {"id": int(fid)})
                st.success("Deleted.")
            except Exception as e:
                st.error("Delete failed: " + str(e))

# ------------------------ ANALYSIS & QUERIES ------------------------
elif menu == "Analysis & Queries":
    st.header("Analysis & Queries")

    # Dynamic city selector for q3
    if "q3" in queries:
        cities_df = run_query("SELECT DISTINCT City FROM providers ORDER BY City;")
        city_choice = st.selectbox("Select city for Q3", cities_df["City"].tolist())
        desc, sql, _ = queries["q3"]
        queries["q3"] = (desc, sql, {"city": city_choice})

    # Loop through and display each query
    for k, value in queries.items():
        if len(value) == 3:
            desc, sql, params = value
        else:
            desc, sql = value
            params = None

        st.subheader(f"{k}: {desc}")
        df = run_query_func(sql, params)
        st.dataframe(df)

        # CSV download for each query
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {k} CSV",
            data=csv,
            file_name=f"{k}.csv",
            mime="text/csv"
        )
