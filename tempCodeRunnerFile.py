# -------------------------------
# Complete Food Delivery Data Script (No order amount)
# -------------------------------

import pandas as pd
import sqlite3

# -------------------------------
# Step 1: Load Datasets
# -------------------------------

# Load orders.csv
orders = pd.read_csv("orders.csv")
print("Orders dataset loaded:")
print(orders.head())

# Load users.json
users = pd.read_json("users.json")
print("\nUsers dataset loaded:")
print(users.head())

# Load restaurants.sql into in-memory SQLite DB
conn = sqlite3.connect(":memory:")

with open("restaurants.sql") as f:
    sql_script = f.read()

conn.executescript(sql_script)

# Read restaurants table
restaurants = pd.read_sql_query("SELECT * FROM restaurants", conn)
print("\nRestaurants dataset loaded:")
print(restaurants.head())

# -------------------------------
# Step 2: Clean column names
# -------------------------------
# Remove any leading/trailing whitespace
orders.columns = orders.columns.str.strip()
users.columns = users.columns.str.strip()
restaurants.columns = restaurants.columns.str.strip()

# -------------------------------
# Step 3: Merge Datasets
# -------------------------------
# Merge orders with users, then with restaurants
final_df = orders.merge(users, on="user_id", how="left") \
                 .merge(restaurants, on="restaurant_id", how="left")

print("\nFinal merged dataset:")
print(final_df.head())

# -------------------------------
# Step 4: Perform Calculations
# -------------------------------

# Total orders per user
total_orders_per_user = final_df.groupby("user_id")["order_id"].count()
print("\nTotal orders per user:")
print(total_orders_per_user)

# Total orders per restaurant
total_orders_per_restaurant = final_df.groupby("restaurant_id")["order_id"].count()
print("\nTotal orders per restaurant:")
print(total_orders_per_restaurant)

# Top 5 users by number of orders
top_users_by_orders = total_orders_per_user.sort_values(ascending=False).head(5)
print("\nTop 5 users by number of orders:")
print(top_users_by_orders)

# Top 5 restaurants by number of orders
top_restaurants_by_orders = total_orders_per_restaurant.sort_values(ascending=False).head(5)
print("\nTop 5 restaurants by number of orders:")
print(top_restaurants_by_orders)

# Most popular cuisine
if 'cuisine' in final_df.columns:
    popular_cuisine = final_df['cuisine'].value_counts().head(5)
    print("\nTop 5 cuisines by number of orders:")
    print(popular_cuisine)

# -------------------------------
# Step 5: Save Final Dataset
# -------------------------------
final_df.to_csv("final_food_delivery_dataset.csv", index=False)
print("\nFinal merged dataset saved as 'final_food_delivery_dataset.csv'")
