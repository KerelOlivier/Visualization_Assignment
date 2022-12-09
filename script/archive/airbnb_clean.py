from datetime import datetime

import numpy as np
import pandas as pd

df = pd.read_csv("Visualization_Assignment/data/airbnb_open_data.csv")

# Fixing column names
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.lower()

# Only NY so country not necessary
df = df.drop(["country", "country_code"], axis=1)

# Removing duplicated rows
df.drop_duplicates(keep="first", inplace=True)
# dropping duplicate license row- keeping one with more information
df.drop(df.index[72947], inplace=True)
# Only populated for duplicate row
df = df.drop(["license"], axis=1)

# Fix host ID connected to two hosts
df['host_id'] = np.where(df.id==24728144, df.host_id.max()+1, df.host_id)

# Fix neighbourhood names
df["neighbourhood_group"].replace(
    ["manhatan", "brookln"], ["Manhattan", "Brooklyn"], inplace=True
)

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

# Clean price and service fee
df["price"] = df["price"].apply(
    lambda x: x.replace("$", "") if pd.isna(x) == False else x
)
df["service_fee"] = df["service_fee"].apply(
    lambda x: x.replace("$", "") if pd.isna(x) == False else x
)
df["service_fee"] = df["service_fee"].astype(float)
df["price"] = df["price"].apply(
    lambda x: x.replace(",", "") if pd.isna(x) == False else x
)  # Some prices have commas
df["price"] = df["price"].astype(float)

# Fixing minimum nights
df["minimum_nights"].replace({pd.NA: np.nan}, inplace=True)
df["minimum_nights"] = np.where(df["minimum_nights"] < 0, np.nan, df["minimum_nights"])
df["minimum_nights"] = np.where(
    df["minimum_nights"] > 2000, np.nan, df["minimum_nights"]
)

# Last review date
df['last_review'] = pd.to_datetime(df['last_review'])
df["last_review"] = np.where(
    df["last_review"] > datetime.now(), np.datetime64("NaT"), df["last_review"]
)

# Filling neighbourhood nulls
nh = df[['neighbourhood_group','neighbourhood']].drop_duplicates()
nh = nh[~nh.neighbourhood_group.isna()]

df = pd.merge(df, nh, how="left", on='neighbourhood')
df['neighbourhood_group'] = np.where(df.neighbourhood_group_x.isna(), df.neighbourhood_group_y, df.neighbourhood_group_x)
df = df.drop(['neighbourhood_group_x','neighbourhood_group_y'], axis=1)

df.to_csv("Visualization_Assignment/data/airbnb_open_data_clean.csv", index=False)
