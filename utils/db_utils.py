import pandas as pd
import sqlite3
import os


def infer_sqlite_type(value):
    """Maps a Python value to an SQLite data type."""
    if pd.api.types.is_integer_dtype(value):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(value):
        return 'REAL'
    else:
        return 'TEXT'


def table_exists(conn, table_name):
    """Checks if a table already exists in the SQLite DB."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None


def log_error(message):
    """Logs error messages to error_log.txt."""
    with open("error_log.txt", "a") as f:
        f.write(message + "\n")


def create_table_from_csv(csv_path, conn, table_name):
    
    """Creates or manages table creation with schema conflict handling."""
    df = pd.read_csv(csv_path)


    # Check if table already exists
    if table_exists(conn, table_name):
        print(f"[!] Table '{table_name}' already exists.")
        decision = input("Type 'o' to overwrite, 'r' to rename, or 's' to skip: ").strip().lower()

        if decision == 's':
            print("[✓] Skipping table creation.")
            return
        elif decision == 'r':
            new_name = input("Enter new table name: ").strip()
            table_name = new_name
        elif decision == 'o':
            try:
                conn.execute(f"DROP TABLE IF EXISTS {table_name};")
            except Exception as e:
                log_error(f"Error dropping table {table_name}: {e}")
        else:
            print("[!] Invalid option. Skipping.")
            return


    # Infer schema and create table
    columns = []
    for col in df.columns:
        dtype = infer_sqlite_type(df[col])
        columns.append(f'"{col}" {dtype}')

    schema = f"CREATE TABLE {table_name} ({', '.join(columns)});"

    try:
        conn.execute(schema)
        print(f"[✓] Table '{table_name}' created.")
    except Exception as e:
        print(f"[!] Failed to create table: {e}")
        log_error(f"Error creating table {table_name}: {e}")
        return

    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"[✓] Data inserted into '{table_name}'.")
    except Exception as e:
        print(f"[!] Failed to insert data: {e}")
        log_error(f"Error inserting into {table_name}: {e}")
