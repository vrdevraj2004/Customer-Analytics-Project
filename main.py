
# -----------------------------
# CUSTOMER DATA CLEANING & FEATURE ENGINEERING
# -----------------------------

import pandas as pd
import numpy as np
from tabulate import tabulate
import random

# -----------------------------
# 0. DISPLAY SETTINGS
# -----------------------------
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# -----------------------------
# 1. LOAD DATASET
# -----------------------------
df = pd.read_csv('customer_shopping_behavior.csv')

# -----------------------------
# 2. INITIAL DATA INSPECTION
# -----------------------------
print("\n--- Data Description ---")
print(df.describe(include='all').transpose())

print("\n--- Missing Values ---")
print(df.isnull().sum().to_frame(name='Missing Values'))

# -----------------------------
# 3. CLEAN MISSING VALUES
# -----------------------------
# Fill missing Review Ratings with median per Category
if 'Review Rating' in df.columns and 'Category' in df.columns:
    df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
        lambda x: x.fillna(x.median())
    )

print("\n--- Missing Values After Cleaning ---")
print(df.isnull().sum().to_frame(name='No More Missing Values'))

# -----------------------------
# 4. RENAME AND STANDARDIZE COLUMNS
# -----------------------------
df.columns = df.columns.str.lower().str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

# -----------------------------
# 5. FEATURE ENGINEERING
# -----------------------------
# Rating Category
df['rating_category'] = df['review_rating'].apply(
    lambda x: 'Low' if x <= 2 else ('Medium' if x <= 4 else 'High')
)

# Spending Segment
df['spending_segment'] = pd.cut(
    df['purchase_amount'],
    bins=[0, 50, 150, 300, 1000],
    labels=['Low','Medium','High','Very High']
)

# Simulate purchase_date if missing
if 'purchase_date' not in df.columns:
    df['purchase_date'] = pd.to_datetime(
        [f"2023-{random.randint(1,12)}-{random.randint(1,28)}" for _ in range(len(df))]
    )
else:
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])

# Extract Month and Weekday
df['month'] = df['purchase_date'].dt.month
df['weekday'] = df['purchase_date'].dt.day_name()

# -----------------------------
# 6. CUSTOMER & CATEGORY SUMMARIES
# -----------------------------
customer_summary = df.groupby('customer_id').agg(
    total_spent=('purchase_amount','sum'),
    avg_rating=('review_rating','mean'),
    purchase_count=('purchase_amount','count')
).reset_index()

category_summary = df.pivot_table(
    index='category',
    values='purchase_amount',
    aggfunc=['sum','mean','count']
)

# -----------------------------
# 7. OUTLIERS
# -----------------------------
outliers = df[df['purchase_amount'] > df['purchase_amount'].quantile(0.99)]
low_rating_high_spend = df[(df['purchase_amount']>150) & (df['review_rating']<=2)]

# -----------------------------
# 8. TABLE PRINT FUNCTION
# -----------------------------
def print_table(title, table, columns=None, transpose=False):
    print(f"\n--- {title} ---")
    if columns is not None:
        table = table[columns]
    if transpose:
        table = table.transpose()
    print(tabulate(table, headers='keys', tablefmt='grid'))

# -----------------------------
# 9. DISPLAY DATA
# -----------------------------
display_cols = [
    'customer_id','age','gender','item_purchased','category',
    'purchase_amount','review_rating','rating_category','spending_segment'
]
print_table("Cleaned Data (first 10 rows)", df.head(10), columns=display_cols)

print_table("Customer Summary (first 5 rows)", customer_summary.head())
print_table("Category Summary", category_summary, transpose=True)

outlier_cols = ['customer_id','category','purchase_amount','review_rating','rating_category','spending_segment']
print_table("Outlier Transactions (High Purchase Amount)", outliers, columns=outlier_cols)

# -----------------------------
# 10. SAVE CLEANED DATA TO CSV
# -----------------------------
df.to_csv('customer_shopping_behavior_cleaned.csv', index=False)
print("\n✅ Cleaned and enriched dataset saved as 'customer_shopping_behavior_cleaned.csv'")
