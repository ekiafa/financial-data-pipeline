import os
from dotenv import load_dotenv
import psycopg2

# Διαβάζει το .env και φορτώνει τις μεταβλητές
load_dotenv()

# Παίρνει το connection string από το .env
database_url = os.getenv("DATABASE_URL")

# Συνδέεται στη βάση
connection = psycopg2.connect(database_url)
cursor = connection.cursor()

# Ρωτάει τη βάση "τι ώρα έχεις;" — απλό τεστ
cursor.execute("SELECT now();")
result = cursor.fetchone()

print("Σύνδεση επιτυχής! Η βάση λέει ότι η ώρα είναι:", result[0])

# Κλείνει τη σύνδεση
cursor.close()
connection.close()