# books_queries.py

import sqlite3
import pandas as pd

# Prompt user to enter the database path
db_path = input("Enter the path to your books.db file (e.g., books.db): ")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# a. Select all authors' last names in descending order
cursor.execute("SELECT last FROM authors ORDER BY last DESC")
print("\nAuthors' Last Names (Descending):")
for row in cursor.fetchall():
    print(row[0])

# b. Select all book titles in ascending order
cursor.execute("SELECT title FROM titles ORDER BY title ASC")
print("\nBook Titles (Ascending):")
for row in cursor.fetchall():
    print(row[0])

# c. Inner join: Books by a specific author
author_id = 1
query = """
SELECT titles.title, titles.copyright, titles.isbn
FROM titles
JOIN author_ISBN ON titles.isbn = author_ISBN.isbn
JOIN authors ON authors.id = author_ISBN.id
WHERE authors.id = ?
ORDER BY titles.title ASC
"""
cursor.execute(query, (author_id,))
print(f"\nBooks by Author ID {author_id}:")
for row in cursor.fetchall():
    print(row)

# d. Insert a new author
first_name, last_name = 'Jane', 'Smith'
cursor.execute("INSERT INTO authors (first, last) VALUES (?, ?)", (first_name, last_name))
conn.commit()
print(f"\nInserted new author: {first_name} {last_name}")

# e. Insert a new title and link to author
new_isbn = '9999999999'
new_title = 'Learning SQLite'
new_edition = 1
new_copyright = '2025'

# Check if the ISBN already exists
cursor.execute("SELECT * FROM titles WHERE isbn = ?", (new_isbn,))
if cursor.fetchone() is None:
    # Insert new book if ISBN is unique
    cursor.execute(
        "INSERT INTO titles (isbn, title, edition, copyright) VALUES (?, ?, ?, ?)",
        (new_isbn, new_title, new_edition, new_copyright)
    )
    print(f"Inserted new book: '{new_title}'")
else:
    print(f"Book with ISBN {new_isbn} already exists. Skipping insert.")

# Get new author's ID
cursor.execute("SELECT id FROM authors WHERE first = ? AND last = ?", (first_name, last_name))
new_author_id = cursor.fetchone()[0]

# Link in author_ISBN (only if not already linked)
cursor.execute("SELECT * FROM author_ISBN WHERE id = ? AND isbn = ?", (new_author_id, new_isbn))
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO author_ISBN (id, isbn) VALUES (?, ?)", (new_author_id, new_isbn))
    print(f"Linked author {first_name} {last_name} to book '{new_title}'")
else:
    print(f"Author already linked to book with ISBN {new_isbn}. Skipping link.")

conn.commit()
conn.close()
