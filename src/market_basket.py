import pandas as pd
import sqlite3
from mlxtend.frequent_patterns import apriori, association_rules

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

# df_germany is the DataFrame you extracted earlier (Country == Germany)
# Expected columns (based on your earlier schema): InvoiceNo, Description, Quantity

# 1) Group by InvoiceNo + Description, sum quantities
grp = (df_country.groupby(["InvoiceNo", "Description"], as_index=False)["Quantity"].sum())
print(grp)

# 2) Unpack/pivot: rows=InvoiceNo, columns=unique descriptions, values=total quantities
pivot = grp.pivot_table(
    index="InvoiceNo",
    columns="Description",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)

# 3) One-hot encoding: True if description exists in invoice, else False
#    (exists if total quantity > 0)
onehot = pivot.map(lambda x: True if x > 0 else False)
#print(onehot)

# 4) Apriori + association rules
#    min_support/min_conf can be tuned
frequent_itemsets = apriori(onehot, min_support=0.01, use_colnames=True)

rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.3
)

# Show top rules (edit as needed)
rules = rules.sort_values(["confidence", "lift"], ascending=False)
print(rules.head(10))

# rules now contains the extracted association rules
