import pandas as pd
from sqlalchemy import create_engine

# Load the cleaned CSV
df = pd.read_csv('customer_shopping_behavior_cleaned.csv')

# PostgreSQL credentials
username = "postgres"
password = "admin123"  # your actual password
host = "localhost"
port = "5432"
database = "customer_behavior_db"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Load DataFrame into PostgreSQL
table_name = "customer"  # replace or keep as needed
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"✅ Data successfully loaded into table '{table_name}' in database '{database}'.")
