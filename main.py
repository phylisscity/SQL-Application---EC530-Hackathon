import pandas as pd
import sqlite3
from utils.db_utils import create_table_from_csv



def main():
    csv_path = 'data/sample.csv'  # CSV file created
    db_path = 'database/sheet.db'
    table_name = 'sample_table'



    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    create_table_from_csv(csv_path, conn, table_name)
    conn.close()


if __name__ == '__main__':
    main()
