import importer_test
from services.koneksi import customConnection
from mysql.connector import Error
import schedule
import time

connection=customConnection(
            host="192.168.230.84",
            port=3307,
            user="dev",
            password="password",
            # database="smartoffice"
        )
if connection.is_connected():
    print("Connected")
else:
    print("Not Connected")
    
def monitor():
    max_connections=0
    max_used_connections=0
    cursor=connection.cursor(dictionary=True)
    query="SHOW GLOBAL VARIABLES LIKE 'max_connections'"
    cursor.execute(query)
    result=cursor.fetchone()
    max_connections=result['Value']
    cursor.close()
    cursor=connection.cursor(dictionary=True)
    query="SHOW GLOBAL STATUS LIKE 'max_used_connections'"
    cursor.execute(query)
    result=cursor.fetchone()
    max_used_connections=result['Value']
    cursor.close()
    server_health=(int(max_used_connections)/int(max_connections))*100
    print(f"Max connections      : {max_connections}")
    print(f"Max used connections : {max_used_connections}")
    print(f"Server health        : {server_health}")
    print("=====================================")
    # connection.close()
   

schedule.every(1).seconds.do(monitor)

if __name__=="__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
    # monitor()