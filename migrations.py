import sqlite3

with sqlite3.connect('filters.db') as conn:
    c = conn.cursor()
    c.execute('''
    CREATE TABLE filters (
        user_id INTEGER PRIMARY KEY,
        query TEXT,
        location TEXT,
        last_alerted_at TEXT
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS geo_zones (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        geo_zone_id INTEGER,
        FOREIGN KEY (geo_zone_id) REFERENCES geo_zones(id)
    )
    ''')

    conn.commit()
    print("Base de données créée avec succès.")