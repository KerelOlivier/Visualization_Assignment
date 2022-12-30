from datetime import datetime

import numpy as np
import pandas as pd

df = pd.read_csv("Visualization_Assignment/data/airbnb_open_data_full.csv")

# Select columns
df = df[['id', 'name', 'host_id', 'host_name','neighbourhood_cleansed','neighbourhood_group_cleansed','latitude','longitude','amenities','price','calculated_host_listings_count']]

# Rename neighbourhood columns
df.rename(columns={'neighbourhood_cleansed': 'neighbourhood', 'neighbourhood_group_cleansed': 'neighbourhood_group'}, inplace=True)

# Setting data type as category
df["neighbourhood_group"] = df["neighbourhood_group"].astype("category")
df["neighbourhood"] = df["neighbourhood"].astype("category")

# Setting data type to int
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].astype(
    "Int64"
)

# Clean neighbourhood
df["neighbourhood"] = np.where(df['neighbourhood']=='Chelsea, Staten Island', 'Chelsea', df['neighbourhood'])

# Creating neighbourhood counts
df_group_neighbourhood = df.groupby(['host_id','neighbourhood'], as_index=False).size()
df_group_neighbourhood.rename(columns={'size': 'host_listings_neighbourhood_count'}, inplace=True)
df_group_neighbourhood_group = df.groupby(['host_id','neighbourhood_group'], as_index=False).size()
df_group_neighbourhood_group.rename(columns={'size': 'host_listings_neighbourhood_group_count'}, inplace=True)

df = df.merge(df_group_neighbourhood, on=['host_id','neighbourhood'], how='left')
df = df.merge(df_group_neighbourhood_group, on=['host_id','neighbourhood_group'], how='left')

# Create fire alarm and carbon monoxide columns
df['has_fire_alarm'] = df.amenities.apply(lambda x: "Smoke alarm" in x)
df['has_co_monitor'] = df.amenities.apply(lambda x: "Carbon monoxide alarm" in x)

df = df.drop("amenities", axis=1)

# Clean price
df["price"] = df["price"].apply(
    lambda x: x.replace("$", "") if pd.isna(x) == False else x
)
df["price"] = df["price"].apply(
    lambda x: x.replace(",", "") if pd.isna(x) == False else x
)  # Some prices have commas
df["price"] = df["price"].astype(float)

df.to_csv("Visualization_Assignment/data/airbnb_open_data_full_clean.csv", index=False)
