import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df_hotel = pd.read_csv('../data/Hotels_Properties_Citywide.csv')

df_hotel_clean = df_hotel.dropna(inplace=False)

df_hotel_clean_2 = df_hotel_clean[["PARID", "Borough", "Latitude", "Longitude"]]

df_hotel_clean_2['Borough'] = df_hotel_clean_2['Borough'].replace(['1', '2', '3', '4', '5'], 
['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island'])

df_hotel_clean_2['Borough'] = df_hotel_clean_2['Borough'].replace(['MANHATTAN', 'BRONX', 'BROOKLYN', 'QUEENS', 'STATEN IS'], 
['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island'])

df_hotel_sorted = df_hotel_clean_2.sort_values(by=['Borough'], inplace=False)
df_hotel_sorted1 = df_hotel_sorted.rename({'PARID': 'parid', 'Borough': 'neighbourhood group', 'Latitude': 'latitude', 'Longitude':'longitude'}, axis=1)

df_hotel_sorted1.parid.nunique() == df_hotel_sorted1.shape[0]

df_hotel_sorted1['hotel_counts_per_neighbourhood_group'] = df_hotel_sorted1.groupby('neighbourhood group')['neighbourhood group'].transform('count')

df_hotel_sorted1.reset_index(drop=True, inplace=True)

df_hotel_sorted1 = df_hotel_sorted1.rename({'neighbourhood group': 'neighbourhood_group'}, axis=1)

df_hotel_sorted1['latitude'] = df_hotel_sorted1['latitude'].round(5)
df_hotel_sorted1['longitude'] = df_hotel_sorted1['longitude'].round(5)
df_hotel_sorted1.head()

df_hotel_sorted1.to_csv('../data/Hotels_clean_sorted.csv', index = False)

df_airbnb = pd.read_csv('../data/airbnb_open_data_full_clean.csv')
df_airbnb.value_counts(['neighbourhood_group']).sort_index()

df_airbnb['airbnb_counts_per_neighbourhood_group'] = df_airbnb.groupby('neighbourhood_group')['neighbourhood_group'].transform('count')
df_airbnb.head()

df_hotel_temp = df_hotel_sorted1[['neighbourhood_group', 'hotel_counts_per_neighbourhood_group']].copy()

df_hotel_temp.drop_duplicates(subset='neighbourhood_group', keep="last", inplace=True)

df_hotel_temp.reset_index(drop=True, inplace=True)
df_hotel_temp.head()

df_airbnb_temp = df_airbnb[['neighbourhood_group', 'airbnb_counts_per_neighbourhood_group']].copy()

df_airbnb_temp.drop_duplicates(subset='neighbourhood_group', keep="last", inplace=True)

df_airbnb_temp.reset_index(drop=True, inplace=True)
df_airbnb_temp.head()

df_hotel_airbnb = pd.merge(df_hotel_temp, df_airbnb_temp, on='neighbourhood_group', how='outer')
df_hotel_airbnb.head()

df_hotel_airbnb.to_csv('../data/Hotels_Airbnbs_merged.csv', index = False)