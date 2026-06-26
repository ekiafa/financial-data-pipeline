import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
database_url = os.getenv("DATABASE_URL")

connection = psycopg2.connect(database_url)
cursor = connection.cursor()

# Το SQL που φτιάχνει τον πίνακα
create_sql = """
CREATE TABLE IF NOT EXISTS raw_rates (
    rate_date   DATE,
    currency    VARCHAR(3),
    rate        NUMERIC
);
"""

cursor.execute(create_sql)
connection.commit()   # "σώσε" την αλλαγή στη βάση

print("Ο πίνακας raw_rates είναι έτοιμος!")

cursor.close()
connection.close()