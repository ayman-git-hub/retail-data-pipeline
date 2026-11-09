#Multi-Store-Retail Data Pipeline & Market Basket Analysis

## Project Overview

#An automated data engineering and analytics pipeline designed to ingest point-of-sale (POS) transaction flat files, #validate data quality, load them into a centralized relational database, and perform data mining (Market Basket Analysis) #to uncover customer purchasing patterns.

## 🏗️ Architecture & Data Flow 

1.  **Extraction:** POS systems export daily transaction data into CSV flat files.
2.  **Transformation & Validation:** Python scripts check for required schemas, handle missing data types, and clean anomalies.
3.  **Loading:** Cleaned data is loaded into a structured SQLite database (`Invoice_Records.db`).
4.  **Data Mining:** The Apriori algorithm calculates **Support**, **Confidence**, and **Lift** to identify "Frequently Bought Together" product pairings.

## 🛠️ Tech Stack

-   **Language:** Python 3.x
-   **Data Manipulation:** Pandas, NumPy
-   **Database:** SQLite / SQLAlchemy
-   **Data Mining:** Mlxtend (Apriori & Association Rules)