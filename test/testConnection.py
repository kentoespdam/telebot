import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.path.abspath('..'))
from config.conn import mainConnection

def main():
    connection = mainConnection().build()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM server")
    result = cursor.fetchall()
    for row in result:
        print(row)

if __name__ == '__main__':
    main()