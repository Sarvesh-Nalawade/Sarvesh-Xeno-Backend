import os
import sqlite3
import pymysql
from dotenv import load_dotenv

# Load MySQL credentials

# Reading .env as two possible locations (if code is run from project root or from within this folder)
load_dotenv("../../.env")
load_dotenv(".env")

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", None)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_DATABASE", "xeno_shopify")

sqlite_file = "temp_check.db"

# Connect to MySQL
mysql_conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    passwd=DB_PASS,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor,
)

# Create SQLite DB (overwrite every run)
if os.path.exists(sqlite_file):
    os.remove(sqlite_file)

sqlite_conn = sqlite3.connect(sqlite_file)
sqlite_cur = sqlite_conn.cursor()

# Export MySQL -> SQLite (all as TEXT for simplicity)
with mysql_conn.cursor() as cur:
    # Get list of all tables
    cur.execute("SHOW TABLES;")
    tables = [row[f"Tables_in_{DB_NAME}"] for row in cur.fetchall()]

    for table in tables:
        print(f"Processing table: {table}")

        # DESCRIBE needs backticks in case of reserved keywords
        cur.execute(f"DESCRIBE `{table}`")
        cols = [row["Field"] for row in cur.fetchall()]

        # Quote reserved keywords for SQLite
        safe_cols = [f'"{c}"' if c.lower() in ("default", "key", "order") else c for c in cols]

        # Create SQLite table (all TEXT)
        col_defs = ", ".join([f'{c} TEXT' for c in safe_cols])
        create_sql = f'CREATE TABLE "{table}" ({col_defs});'
        sqlite_cur.execute(create_sql)

        # Dump rows from MySQL
        cur.execute(f"SELECT * FROM `{table}`")
        rows = cur.fetchall()

        if rows:
            placeholders = ",".join("?" * len(cols))
            insert_sql = f'INSERT INTO "{table}" ({",".join(safe_cols)}) VALUES ({placeholders})'

            for row in rows:
                sqlite_cur.execute(
                    insert_sql,
                    tuple(str(v) if v is not None else None for v in row.values()),
                )

# Commit and close
sqlite_conn.commit()
sqlite_conn.close()
mysql_conn.close()

print(f"\n✅ Export completed.")
print(f"Check: ./{sqlite_file}")
