# Franchise V-2 Notes

## Web scraper gets data from espn.com

## Data goes into DB (probably mongo)

## Retrieve data from DB to prevent multiple scrapes

---

```python

# Database
def create_division_table(divisions):
    division_data = []
    for i, division in enumerate(divisions):
        division_data.append((i, division))

    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('DROP TABLE IF EXISTS Division')
        cursor.execute('''
            CREATE TABLE Division(
                division_id INT NOT NULL PRIMARY KEY,
                division_name TEXT NOT NULL
            )
        ''')
        cursor.executemany('INSERT INTO Division VALUES (?, ?)', division_data)
        cursor.execute('SELECT * FROM Division')
        rows = cursor.fetchall()
    return rows

```