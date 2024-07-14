import sqlite3

DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                company_api_key TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS location (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                location_name TEXT NOT NULL,
                location_country TEXT,
                location_city TEXT,
                location_meta TEXT,
                FOREIGN KEY(company_id) REFERENCES company(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_id INTEGER,
                sensor_name TEXT NOT NULL,
                sensor_category TEXT,
                sensor_meta TEXT,
                sensor_api_key TEXT NOT NULL,
                FOREIGN KEY(location_id) REFERENCES location(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id INTEGER,
                timestamp INTEGER,
                data JSON,
                FOREIGN KEY(sensor_id) REFERENCES sensor(id)
            )
        ''')
        conn.commit()
