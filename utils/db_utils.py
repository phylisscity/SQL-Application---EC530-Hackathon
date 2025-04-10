import pandas as pd


def load_csv_to_sqlite(csv_path, conn, table_name):
    """Reads a CSV file and loads it into the SQLite DB under the given table name."""
    
    try:
        
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"[✓] Table '{table_name}' loaded successfully.")
        
    except Exception as e:
        
        
        print(f"[!] Error loading CSV to SQLite: {e}")
