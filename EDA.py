#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv('vehicles.csv')


# # Data Exploration

df.head()
df.tail()
df.shape
df.columns
df.info()

### Data Cleaning


# Finding missing values

print("\nMissing values:\n", df.isnull().sum())

# Drop columns with too many missing values or irrelevant ones
df = df.drop(['county', 'size', 'VIN', 'lat', 'long', 'posting_date'], axis=1)
df = df.dropna(subset=['model', 'price', 'year'])

# Filling missing values

df['year'] = df['year'].fillna(df['year'].median())
df['odometer'] = df['odometer'].fillna(df['odometer'].median())
df['manufacturer'] = df['manufacturer'].fillna(df['manufacturer'].mode()[0])
df['fuel'] = df['fuel'].fillna(df['fuel'].mode()[0])
df['transmission'] = df['transmission'].fillna(df['transmission'].mode()[0])
df['condition'] = df['condition'].fillna('unknown')
df['paint_color'] = df['paint_color'].fillna('unknown')
df['cylinders'] = df['cylinders'].fillna('unknown')
df['title_status'] = df['title_status'].fillna(df['title_status'].mode()[0])
df['drive'] = df['drive'].fillna('unknown')
df['type'] = df['type'].fillna('unknown')
df = df.dropna(subset=['description'])

print(df.isnull().sum())

print(df.describe(include='all'))



# Example for filtering price outliers
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['price'] >= (Q1 - 1.5 * IQR)) & (df['price'] <= (Q3 + 1.5 * IQR))]

# Example for filtering odometer outliers
Q1_odometer = df['odometer'].quantile(0.25)
Q3_odometer = df['odometer'].quantile(0.75)
IQR_odometer = Q3_odometer - Q1_odometer
df = df[(df['odometer'] >= (Q1_odometer - 1.5 * IQR_odometer)) & (df['odometer'] <= (Q3_odometer + 1.5 * IQR_odometer))]

df['price'].hist(bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Price')
plt.ylabel('Count')
plt.title('Distribution of Used Car Prices (Cleaned)')
plt.show()

df['odometer'].hist(bins=30, color='lightgreen', edgecolor='black')
plt.xlabel('Odometer (miles)')
plt.ylabel('Count')
plt.title('Distribution of Odometer Values (Cleaned)')
plt.show()

sns.scatterplot(x='odometer', y='price', data=df)
plt.title('Price vs. Odometer (Cleaned Data)')
plt.show()

# Select numeric columns for histograms
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# Plot histograms
plt.figure(figsize=(15, 10))
for i, col in enumerate(numeric_cols, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df[col], bins=30, kde=True)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Scatter plot for price vs. year
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='year', y='price', alpha=0.5)
plt.title('Price vs. Year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.show()


numeric_cols = ['price', 'year', 'odometer']

# Create the correlation matrix
corr_matrix = df[numeric_cols].corr()

# Plot the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
plt.title('Correlation Heatmap of Numeric Features')
plt.show()


plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='price')
plt.title('Box Plot of Car Prices to Detect Outliers')
plt.show()


plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='manufacturer', y='price')
plt.xticks(rotation=90)
plt.title('Price Distribution by Manufacturer')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='condition', y='price')
plt.title('Price Distribution by Car Condition')
plt.show()


# Count plot for 'manufacturer'
plt.figure(figsize=(12, 6))
sns.countplot(data=df, y='manufacturer', order=df['manufacturer'].value_counts().index[:10])
plt.title('Top 10 Manufacturers')
plt.xlabel('Count')
plt.ylabel('Manufacturer')
plt.show()

# Count plot for 'fuel'
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='fuel', order=df['fuel'].value_counts().index)
plt.title('Fuel Type Distribution')
plt.xlabel('Fuel Type')
plt.ylabel('Count')
plt.show()


avg_price_by_fuel = df.groupby('fuel')['price'].mean().sort_values()

plt.figure(figsize=(8, 6))
avg_price_by_fuel.plot(kind='barh', color='green')
plt.title('Average Price by Fuel Type')
plt.xlabel('Average Price')
plt.ylabel('Fuel Type')
plt.show()