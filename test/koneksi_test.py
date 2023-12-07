import importer_test
from services.koneksi import mainConnection

connection=mainConnection()
cursor=connection.cursor()
cursor.execute("SELECT * FROM server")
result=cursor.fetchall()

print(result)