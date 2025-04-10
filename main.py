import sqlite3
from utils.db_utils import create_table_from_csv
import os


def list_tables(conn):
    """Displays all tables in the current SQLite DB."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\n📋 Existing Tables:")
    for t in tables:
        print(f" - {t[0]}")
    print()


def run_query(conn):
    """Prompts user to input an SQL query and executes it."""
    query = input("Enter your SQL query:\n> ")
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            print("\n📄 Results:")
            for row in rows:
                print(row)
        else:
            print("[✓] Query executed. No results returned.")
    except Exception as e:
        print(f"[!] SQL Error: {e}")


def main():
    db_path = 'database/sheet.db'
    conn = sqlite3.connect(db_path)

    print("🤖 Welcome to your CSV-SQL assistant!")
    print("Type 'load' to load a CSV")
    print("Type 'tables' to list tables")
    print("Type 'query' to run a SQL query")
    print("Type 'exit' to quit\n")

    while True:
        command = input(">>> ").strip().lower()

        if command == 'exit':
            print("👋 Bye!")
            break

        elif command == 'load':
            csv_path = input("Enter path to CSV (e.g., data/sample.csv):\n> ").strip()
            table_name = input("Enter table name:\n> ").strip()

            if not os.path.exists(csv_path):
                print("[!] CSV file not found.")
                continue

            create_table_from_csv(csv_path, conn, table_name)

        elif command == 'tables':
            list_tables(conn)

        elif command == 'query':
            run_query(conn)

        else:
            print("[!] Unknown command. Try: load, tables, query, exit.")

    conn.close()

if __name__ == '__main__':
    main()
