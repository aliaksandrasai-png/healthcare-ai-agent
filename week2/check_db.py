import sqlite3

conn = sqlite3.connect("week2/scheduler.db")
cursor = conn.cursor()

# Какие таблицы есть
tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()
print("Tables:", tables)

# Сколько докторов
doctors = cursor.execute("SELECT * FROM doctors").fetchall()
print(f"\nDoctors ({len(doctors)}):")
for d in doctors:
    print(" ", d)

# Сколько слотов
slot_count = cursor.execute("SELECT COUNT(*) FROM slots").fetchone()[0]
print(f"\nTotal slots: {slot_count}")

# Какие даты есть
dates = cursor.execute(
    "SELECT DISTINCT date FROM slots ORDER BY date"
).fetchall()
print(f"\nDates in DB: {[d[0] for d in dates]}")

# Первые 5 слотов
sample = cursor.execute("SELECT * FROM slots LIMIT 5").fetchall()
print(f"\nSample slots:")
for s in sample:
    print(" ", s)

# Конкретные слоты Dr. Smith
print("\n--- Dr. Smith schedule ---")
smith_slots = cursor.execute(
    "SELECT date, time, status FROM slots WHERE doctor_id=1 ORDER BY date, time"
).fetchall()
for s in smith_slots:
    print(" ", s)

print("\n--- Dr. Johnson 2026-04-28 ---")
johnson = cursor.execute(
    "SELECT date, time, status FROM slots WHERE doctor_id=2 AND date='2026-04-28' ORDER BY time"
).fetchall()
for s in johnson:
    print(" ", s)

conn.close()