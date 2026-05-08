import sqlite3

DB_PATH = "scheduler.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clean slate
cursor.execute("DROP TABLE IF EXISTS doctors")
cursor.execute("DROP TABLE IF EXISTS slots")

# Doctors (exact match for tests)
cursor.execute("CREATE TABLE doctors (id INTEGER PRIMARY KEY, name TEXT, department TEXT)")
cursor.executemany("INSERT INTO doctors VALUES (?, ?, ?)",
                   [(1, "Dr. Smith", "Family Medicine"),
                    (2, "Dr. Jones", "Cardiology")])

# Slots for tests: 2026-05-04 & 2026-05-15, times 09:00/10:00/14:00 — ALL available initially
cursor.execute("""CREATE TABLE IF NOT EXISTS slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT, time TEXT, doctor_id INTEGER,
    status TEXT DEFAULT 'available',
    patient_name TEXT, patient_phone TEXT, insurance TEXT,
    appointment_type TEXT DEFAULT 'primary'
)""")
dates = ["2026-05-04", "2026-05-15"]
times = ["09:00", "10:00", "14:00"]
for date in dates:
    for time in times:
        cursor.execute("INSERT OR REPLACE INTO slots (date, time, doctor_id, status) VALUES (?, ?, 1, 'available')", (date, time))  # Dr. Smith
        cursor.execute("INSERT OR REPLACE INTO slots (date, time, doctor_id, status) VALUES (?, ?, 2, 'available')", (date, time))  # Dr. Jones

conn.commit()
conn.close()
print("✅ DB initialized! 12 slots available (Dr. Smith/Jones, 2026-05-04/15).")
print("Run verify below.")