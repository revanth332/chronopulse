from session import engine

conn = engine.connect()
print("Connected to Postgres!")
conn.close()