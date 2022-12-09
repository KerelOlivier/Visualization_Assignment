import numpy as np
import pandas as pd

df = pd.read_csv("airbnb_open_data_clean.csv")

# Setting data type as category
df["neighbourhood_group"] = df["neighbourhood_group"].astype("category")
df["cancellation_policy"] = df["cancellation_policy"].astype("category")
df["room_type"] = df["room_type"].astype("category")
df["host_identity_verified"] = df["host_identity_verified"].astype("category")

# Setting data type to int
df["construction_year"] = df["construction_year"].astype("Int64")
df["number_of_reviews"] = df["number_of_reviews"].astype("Int64")
df["review_rate_number"] = df["review_rate_number"].astype("Int64")
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].astype(
    "Int64"
)
df["availability_365"] = df["availability_365"].astype("Int64")

# Price and service fee to float
df["service_fee"] = df["service_fee"].astype(float)
df["price"] = df["price"].astype(float)

# Last review date
df['last_review'] = pd.to_datetime(df['last_review'])