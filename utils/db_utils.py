import pandas as pd
import sqlite3



def infer_sqlite_type(value):
    
    """Maps a Python value to an SQLite data type."""
    
    if pd.api.types.is_integer_dtype(value):
        
        return 'INTEGER'
    
    elif pd.api.types.is_float_dtype(value):
        
        return 'REAL'
    
    else:
        
        return 'TEXT'
    
    

def create_table_from_csv(csv_path, conn, table_name):
    
    """Inspects a CSV file and creates a matching table in SQLite."""
    
    df = pd.read_csv(csv_path)


    columns = []
    
    for col in df.columns:
        
        dtype = infer_sqlite_type(df[col])
        
        columns.append(f'"{col}" {dtype}')

    schema = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"

    try:
        
        cursor = conn.cursor()
        
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")  # Remove existing for clean start
        
        cursor.execute(schema)
        
        print(f"[✓] Table '{table_name}' created with schema.")
        
    except Exception as e:
        
        print(f"[!] Failed to create table: {e}")



    # Optional: load data after creating schema manually
    
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
    print(f"[✓] Data inserted into '{table_name}'.")

