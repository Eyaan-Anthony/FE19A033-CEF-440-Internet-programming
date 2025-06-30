import psycopg2

# connection establishment
conn = psycopg2.connect(
   database="postgres",
    user='postgres',
    password='password456',
    host='localhost',
    port= '5433'
)

conn.autocommit = True

# Creating a cursor object
cursor = conn.cursor()

# query to create a database 
sql = ''' CREATE database class_session_db '''

# executing above query
cursor.execute(sql)
print("Database has been created successfully !!")

# Closing the connection
conn.close()