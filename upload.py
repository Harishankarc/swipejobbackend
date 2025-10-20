import sqlite3
import csv

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    link TEXT
)
''')
conn.commit()

with open('indeed_jobs_list.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO jobs (title, company, location, link)
            VALUES (?, ?, ?, ?)
        ''', (row['Title'], row['Company'], row['Location'], row['Link']))

conn.commit()
conn.close()
print("Data inserted successfully!")
