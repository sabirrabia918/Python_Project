import sqlite3, os
from config import DB_PATH

def save(launches):
    os.makedirs("data", exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS launches(
            id TEXT PRIMARY KEY, name TEXT, status TEXT,
            agency TEXT, agency_type TEXT, net TEXT,
            fail_reason TEXT, mission_type TEXT
        )""")
    con.executemany(
        "INSERT OR REPLACE INTO launches VALUES (?,?,?,?,?,?,?,?)",
        [(l.id, l.name, l.status, l.agency, l.agency_type,
          l.net.isoformat(), l.fail_reason, l.mission_type)
         for l in launches],
    )
    con.commit()
    con.close()