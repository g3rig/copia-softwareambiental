import mysql.connector
from decouple import config

conn = mysql.connector.connect(
  host=config('HOST'),
  user=config('USER'),
  password=config('PASSWORD'),
  db=config('DBNAME')
)

cursor = conn.cursor()

query = "SELECT * FROM mul_1 ORDER BY id_reg_mul1 DESC limit 1"
cursor.execute(query)

res = cursor.fetchall()

for resultado in res:
  print(res)

cursor.close()
conn.close()