import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import psycopg2

load_dotenv()
database_url = os.getenv("DATABASE_URL")

URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
ns = {"ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}

# --- 1. Τράβα & διάβασε τα δεδομένα ---
response = requests.get(URL)
response.raise_for_status()
root = ET.fromstring(response.content)

time_cube = root.find(".//ecb:Cube[@time]", ns)
date = time_cube.attrib["time"]

# Φτιάχνουμε μια λίστα με (ημερομηνία, νόμισμα, ισοτιμία)
rows = []
for cube in time_cube.findall("ecb:Cube", ns):
    rows.append((date, cube.attrib["currency"], cube.attrib["rate"]))

print(f"Βρέθηκαν {len(rows)} ισοτιμίες για {date}")

# --- 2. Γράψε τα στη βάση ---
connection = psycopg2.connect(database_url)
cursor = connection.cursor()

# Σβήνουμε πρώτα ό,τι υπάρχει ήδη για αυτή την ημερομηνία (για να μην διπλογράφουμε)
cursor.execute("DELETE FROM raw_rates WHERE rate_date = %s;", (date,))

# Βάζουμε τις νέες γραμμές
cursor.executemany(
    "INSERT INTO raw_rates (rate_date, currency, rate) VALUES (%s, %s, %s);",
    rows
)

connection.commit()
print(f"Γράφτηκαν {len(rows)} γραμμές στον πίνακα raw_rates!")

cursor.close()
connection.close()