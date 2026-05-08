import sqlite3
import sys

DB_PATH = "scheduler.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

if len(sys.argv) > 1:
    cmd = sys.argv[1]
else:
    cmd = "count"

if cmd == "setup_tc04":
    slot_id = cursor.execute("SELECT id FROM slots WHERE date='2026-05-04' AND time='10:00' AND doctor_id=1").fetchone()[0]
    cursor.execute("UPDATE slots SET status='booked', patient_name='John Doe', patient_phone='555-0100', insurance='BlueCross' WHERE id=?", (slot_id,))
    conn.commit()
    print("✅ TC-04 setup: John Doe booked 10:00 Dr. Smith")
elif cmd == "verify_10am":
    row = cursor.execute("SELECT status, patient_name FROM slots WHERE date='2026-05-04' AND time='10:00'").fetchone()
    print(f"10:00 slot: {row}")
elif cmd == "count":
    print(f"Slots total: {cursor.execute('SELECT COUNT(*) FROM slots').fetchone()[0]}")
    print(f"Doctors: {cursor.execute('SELECT COUNT(*) FROM doctors').fetchone()[0]}")

conn.close()