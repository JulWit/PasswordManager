"""
import sqlcipher3

conn = sqlcipher3.connect("testing.db")
conn.execute('pragma key="test"')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

sql ='''CREATE TABLE EMPLOYEE(
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20),
   AGE INT,
   SEX CHAR(1),
   INCOME FLOAT
)'''
cursor.execute(sql)
print("Table created successfully........")

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()
"""
import sqlcipher3


class Database:
    def __init__(self, url, password):
        self.url = url
        self.password = password
        self.connection = sqlcipher3.connect(self.url)
