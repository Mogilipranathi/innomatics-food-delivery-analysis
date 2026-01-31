import pandas as pd
import sqlite3

print("Starting...")

#  Load Orders CSV
orders = pd.read_csv("orders.csv")

#  Load Users JSON
users = pd.read_json("users.json")

#  Load Restaurants SQL
conn = sqlite3.connect("restaurants.db", timeout=30)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS restaurants;")
conn.commit()

print("Loading restaurants SQL...")
with open("restaurants.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.commit()
print("Restaurants loaded!")

# Load restaurants table
restaurants = pd.read_sql("SELECT * FROM restaurants", conn)

#  Merge datasets (LEFT JOIN)
df = pd.merge(orders, users, on="user_id", how="left")
df = pd.merge(df, restaurants, on="restaurant_id", how="left")

#  Save final dataset
df.to_csv("final_food_delivery_dataset.csv", index=False)
print("Final dataset created!")

#  ANSWERS (NO membership_type ANYWHERE)

print("\n ANSWERS\n")

#  Total orders by Gold members
print("Gold orders:", df[df["membership"] == "Gold"].shape[0])

#  Total revenue from Hyderabad
print(
    "Hyderabad revenue:",
    round(df[df["city"] == "Hyderabad"]["total_amount"].sum())
)

#  Distinct users
print("Distinct users:", df["user_id"].nunique())

#  Average order value for Gold members
print(
    "Gold AOV:",
    round(df[df["membership"] == "Gold"]["total_amount"].mean(), 2)
)

#  Orders with rating >= 4.5
print(
    "Orders rating >= 4.5:",
    df[df["rating"] >= 4.5].shape[0]
)

#  Orders in top revenue city among Gold members
top_city = (
    df[df["membership"] == "Gold"]
    .groupby("city")["total_amount"]
    .sum()
    .idxmax()
)

print(
    "Gold orders in top city:",
    df[
        (df["membership"] == "Gold") &
        (df["city"] == top_city)
    ].shape[0]
)
