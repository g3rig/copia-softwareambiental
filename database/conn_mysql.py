import pymysql
from datetime import datetime
from decouple import config


def get_connection():
  conn = pymysql.connect(
    host=config('HOST'),
    user=config('USER'),
    password=config('PASSWORD'),
    db=config('DBNAME')
  )
  return conn

def insert_mul1(data_mul1):
  conn_open = True
  try:
    conn = get_connection()
    with conn:
      with conn.cursor() as cursor:
        query = 'INSERT INTO mul_1(fecha_m1, hora_m1, p1tmt1, p1tmt2, p1tmt3, p1tmt4, p1tp1, p1tp2, p1tp3, p1tp4, p1tp5, p1tl1, p1ts3, p1ts1, p1ts2, p2co2_2, p1co2_1, p2co2_1) VALUES %s'
        cursor.execute(query, (data_mul1,))
        conn.commit()
  except Exception as e:
    print(f'Ocurrió un error: {e}')
  finally:
    if conn_open:
      conn.close()
      conn_open = False

def insert_mul2(data_mul2):
  conn_open = True
  try:
    conn = get_connection()
    with conn:
      with conn.cursor() as cursor:
        query = 'INSERT INTO mul_2(fecha_m2, hora_m2, p2tmt1, p2tmt2, p2tmt3, p2tmt4, p2tmt5, p2tmt6, p2tt1, p2tt2, p2tt3, p2tt4, p2tt5, p2tt6, p2tt7, co2au, tempau, hrau) VALUES %s'
        cursor.execute(query, (data_mul2,))
        conn.commit()
  except Exception as e:
    print(f'Ocurrió un error: {e}')
  finally:
    if conn_open:
      conn.close()
      conn_open = False

""" conn = pymysql.connect(
    host=config('HOST'),
    user=config('USER'),
    password=config('PASSWORD'),
    db=config('DBNAME')
  )

try:
  with conn:
    with conn.cursor() as cursor:
      try:
        archivo = open('Datos/MUL_1_12_2022.txt', 'r')
        for i in archivo:
          lista = (i.split(','))
          fecha, hora, p1tmt1, p1tmt2, p1tmt3, p1tmt4, p1tp1, p1tp2, p1tp3, p1tp4, p1tp5, p1tl1, p1ts3, p1ts1, p1ts2, p2co2_2, p1co2_1, p2co2_1 = lista
          fecha = datetime.strptime(fecha.strip(), "%d/%m/%Y").date()
          hora = datetime.strptime(hora.strip(), "%H:%M:%S").time()
          query = 'INSERT INTO mul_1(fecha_m1, hora_m1, p1tmt1, p1tmt2, p1tmt3, p1tmt4, p1tp1, p1tp2, p1tp3, p1tp4, p1tp5, p1tl1, p1ts3, p1ts1, p1ts2, p2co2_2, p1co2_1, p2co2_1) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
          values = (fecha, hora, float(p1tmt1), float(p1tmt2), float(p1tmt3), float(p1tmt4), float(p1tp1), float(p1tp2), float(p1tp3), float(p1tp4), float(p1tp5), float(p1tl1), float(p1ts3), float(p1ts1), float(p1ts2), float(p2co2_2), float(p1co2_1), float(p2co2_1))
          cursor.execute(query, values)
          conn.commit()
      except Exception as e:
        print(f'Ocurrió un error al abrir el archivo: {e}')
      finally:
        archivo.close()
        print('Fin del archivo MUL_1')
      try:
        archivo = open('Datos/MUL_2_12_2022.txt', 'r')
        for i in archivo:
          lista = (i.split(','))
          fecha, hora, p2tmt1, p2tmt2, p2tmt3, p2tmt4, p2tmt5, p2tmt6, p2tt1, p2tt2, p2tt3, p2tt4, p2tt5, p2tt6, p2tt7, co2au, tempau, hrau = lista
          fecha = datetime.strptime(fecha.strip(), "%d/%m/%Y").date()
          hora = datetime.strptime(hora.strip(), "%H:%M:%S").time()
          query = 'INSERT INTO mul_2(fecha_m2, hora_m2, p2tmt1, p2tmt2, p2tmt3, p2tmt4, p2tmt5, p2tmt6, p2tt1, p2tt2, p2tt3, p2tt4, p2tt5, p2tt6, p2tt7, co2au, tempau, hrau) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
          values = (fecha, hora, float(p2tmt1), float(p2tmt2), float(p2tmt3), float(p2tmt4), float(p2tmt5), float(p2tmt6), float(p2tmt1), float(p2tmt2), float(p2tmt3), float(p2tmt4), float(p2tmt5), float(p2tmt6), float(p2tt7), float(co2au), float(tempau), float(hrau))
          cursor.execute(query, values)
          conn.commit()
      except Exception as e:
        print(f'Ocurrió un error al abrir el archivo: {e}')
      finally:
        archivo.close()
        print('Fin del archivo MUL_2')
except Exception as e:
  print(f'Ocurrió un error: {e}') """
