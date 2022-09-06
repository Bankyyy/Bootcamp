# -*- coding: utf-8 -*-

# -- Project --

# # Final Project - Analyzing Sales Data
# 
# **Date**: 21 August 2022
# 
# **Author**: Tanakom Thumob-um (Bank DataRockie)
# 
# **Course**: `Pandas Foundation`


# import data
import pandas as pd
df = pd.read_csv("sample-store.csv")

# preview top 5 rows
df.head()

# shape of dataframe
df.shape

# see data frame information using .info()
df.info()

# We can use `pd.to_datetime()` function to convert columns 'Order Date' and 'Ship Date' to datetime.


# example of pd.to_datetime() function
pd.to_datetime(df['Order Date'].head(), format='%m/%d/%Y')

# TODO - convert order date and ship date to datetime in the original dataframe
df

col_names = list(df.columns)
clean_col_names = []

for name in col_names:
    temp = name.lower().replace(" ", "").replace("-", "")
    clean_col_names.append(temp)

columns = clean_col_names

df.columns = clean_col_names

df_date = df[["orderdate", "shipdate"]]

df["orderdate"] = pd.to_datetime(df['orderdate']).dt.date
df["shipdate"] = pd.to_datetime(df['orderdate']).dt.date
df


# TODO - count nan in postal code column
col_names = list(df.columns)
clean_col_names = []

for name in col_names:
    temp = name.lower().replace(" ", "").replace("-", "")
    clean_col_names.append(temp)

columns = clean_col_names

df.columns = clean_col_names

df["postalcode"].isna().sum()

# TODO - filter rows with missing values
df.isna().sum()

# TODO - Explore this dataset on your owns, ask your own questions
# Group orderdate to quarter and find mean,sum,min,max,std in column sales, profit, quantity
df['orderdate'] = pd.to_datetime(df['orderdate'], errors='coerce') #This line from stackoverflow
result = df.groupby(df["orderdate"].dt.to_period('Q'))[["sales", "profit", "quantity"]]\
    .agg(["mean", "sum", "min", "max", "std"])\
    .reset_index()

result

# ## Data Analysis Part
# 
# Answer 10 below questions to get credit from this course. Write `pandas` code to find answers.


# TODO 01 - how many columns, rows in this dataset
count_col = len(df.columns)
count_row = len(df)

print(count_col,count_row)

# TODO 02 - is there any missing values?, if there is, which colunm? how many nan values?
# There is missing values in postalcode coulumn and there is 11 of them.
df.isna().sum()

# TODO 03 - your friend ask for `California` data, filter it and export csv for him
cali_data = df[df["state"] == "California"]

cali_data.to_csv("data_for_bff.csv")

# TODO 04 - your friend ask for all order data in `California` and `Texas` in 2017 (look at Order Date), send him csv file
df1 = df.query("state == 'Texas' or state == 'California'")
df1[(df1["orderdate"] > "2017-01-01") & (df1["orderdate"] < "2017-12-31")]

df1.to_csv("CaliTxs2017.csv")

df1

# TODO 05 - how much total sales, average sales, and standard deviation of sales your company make in 2017
# Copy from above
result = df.groupby(df["orderdate"].dt.to_period('Y'))[["sales", "profit", "quantity"]]\
    .agg(["mean", "sum", "min", "max", "std"])\
    .reset_index()

result.head(1)

# TODO 06 - which Segment has the highest profit in 2018
y18 = df[(df["orderdate"] > "2018-01-01") & (df["orderdate"] < "2018-12-31")]
highProfit18 = y18.groupby(["segment"]).sum().sort_values("profit", ascending=False)
highProfit18["profit"]

# TODO 07 - which top 5 States have the least total sales between 15 April 2019 - 31 December 2019
y19 = df[(df["orderdate"] > "2019-04-15") & (df["orderdate"] < "2019-12-31")]

least19 = y19.groupby(["state"]).sum().sort_values("sales", ascending=True)

top5 = least19["sales"]

top5.head()


# TODO 08 - what is the proportion of total sales (%) in West + Central in 2019 e.g. 25% 
West = df[(df["orderdate"] > "2019-01-01") & (df["orderdate"] < "2019-12-31") & (df["region"] == "West")]["sales"].sum()
Cen = df[(df["orderdate"] > "2019-01-01") & (df["orderdate"] < "2019-12-31") & (df["region"] == "Central")]["sales"].sum()
total19 = df[(df["orderdate"] > "2019-01-01") & (df["orderdate"] < "2019-12-31")]["sales"].sum()

(West+Cen)/total19*100

# TODO 09 - find top 10 popular products in terms of number of orders vs. total sales during 2019-2020
y19_20 = df[(df["orderdate"] > "2019-01-01") & (df["orderdate"] < "2020-12-31")]
sumquant = y19_20.groupby("productname")["quantity"].sum().sort_values(ascending=False).head(10)
sumsale = y19_20.groupby("productname")["sales"].sum().sort_values(ascending=False).head(10)

dfvs = pd.concat([sumquant.reset_index(drop=False), sumsale.reset_index(drop=False)], axis= 1)

print(dfvs)



# TODO 10 - plot at least 2 plots, any plot you think interesting :)
# Q1-Q4 sales, profit, quantity growth rate

df_y = df.groupby(df["orderdate"].dt.to_period('Q'))[["sales", "profit", "quantity"]].sum().reset_index()

df_y.groupby("orderdate")[["sales", "profit", "quantity"]].sum().plot(kind='bar', color=['green', 'yellow', 'black'])


df_x = df.groupby("region")[["sales", "profit", "quantity"]].sum()
df_x.plot.pie(subplots=True, figsize=(11, 6))

# TODO Bonus - use np.where() to create new column in dataframe to help you answer your own questions
# Find what product that has most sales but still loss maybe because of discount
import numpy as np

df["Class"] = np.where(df["profit"] > 0 , "Profit", "Loss")
df.sort_values(["sales","profit"],ascending=False).groupby("profit").head(100)


# Thank you P'Toy and Google

