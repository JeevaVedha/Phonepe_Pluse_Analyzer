import os
import pandas as pd
from sqlalchemy import create_engine

# --- Database connection details ---
db_user = 'postgres'            # change to your actual Postgres username
db_password = 'password123'   # change to your actual Postgres password
db_host = 'localhost'
db_port = '5432'
db_name = 'Phonepe_Pulse'

# --- Create SQLAlchemy engine ---
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# --- Folder with your CSV files ---
csv_folder = 'Data_extract'

# --- Loop over each CSV file in the folder ---
for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_folder, filename)
        table_name = os.path.splitext(filename)[0].lower()  # remove .csv and make lowercase
        
        print(f"🔹 Processing file: {filename} → Table: {table_name}")

        # Read CSV into DataFrame
        df = pd.read_csv(file_path)
        

        # Upload DataFrame to Postgres
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        print(f"✅ Uploaded {len(df)} rows to table '{table_name}'.")

print("🎉 All CSV files have been uploaded to Postgres!")
