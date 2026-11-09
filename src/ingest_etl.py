import pandas as pd
import sqlite3
#from mlxtend.frequent_patterns import apriori, association_rules

# 1) Read the CSV data from a URL using Pandas
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-AI0273EN-SkillsNetwork/labs/v1/m3/data/Project_data.csv"  # <-- replace with the real URL
df = pd.read_csv(url)

print("Initial dataset length:", len(df))
#print(df.head())

# Ensure expected columns exist (optional but helpful)
required_cols = ["InvoiceNo", "StockCode", "CustomerID"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")
#print("Column avilable")

# 2) Remove entries based on the given conditions
invalid_stockcodes = {"M", "D", "C2", "POST"}

df_clean = df[
    ~df["InvoiceNo"].astype(str).str.startswith("C") &  # a) InvoiceNo starts with 'C'
    ~df["StockCode"].isin(invalid_stockcodes) &          # b) StockCode in list
    df["CustomerID"].notna()                             # c) CustomerID is missing
].copy()

print("Cleaned dataset length:", len(df_clean))

# 3) Load the final data to an SQLite3 database/table
db_name = "Invoice_Records"
table_name = "Purchase_transactions"
conn = sqlite3.connect(db_name)
try:
    df_clean.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {len(df_clean)} rows into {table_name} in {db_name}.")
  
    # 4) Run a sample query to display the first 5 rows
    sample_query = f"SELECT * FROM {table_name} LIMIT 5;"
    preview = pd.read_sql_query(sample_query, conn)
    print("\nFirst 5 rows:")
    print(preview)
    country_query=f"select * from {table_name} where country='Germany';"
    df_country=pd.read_sql_query(country_query,conn)
    print(df_country.head())
finally:
    conn.close()

