# books_display.py

import sqlite3

# Prompt the user to enter the database path
db_path = input("Enter the path to your books.db file (e.g., books.db): ")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute SELECT * FROM titles
cursor.execute("SELECT * FROM titles")
rows = cursor.fetchall()

# Get column names using cursor.description
columns = [desc[0] for desc in cursor.description]

# Display results in tabular format
print("\nTitles Table:\n")
print("\t".join(columns))
for row in rows:
    print("\t".join(str(item) for item in row))

# Close the connection
conn.close()
