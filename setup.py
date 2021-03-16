import mysql.connector
import db_config

conn = mysql.connector.connect(user = db_config.mysql['user'], password = db_config.mysql['password'],
							   host = db_config.mysql['host'], database = db_config.mysql['database'])

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS THREADS(
        THREAD_ID INT PRIMARY KEY,
        OP_NAME VARCHAR(255),
        OP_TEXT TEXT,
        OP_TIMESTAMP INT);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS COMMENTS(
        COMMENT_ID INT PRIMARY KEY,
        THREAD_ID INT,
        USERNAME VARCHAR(255),
        COMMENT_TIMESTAMP INT,
        COMMENT_TEXT TEXT,
        TOP_LEVEL BOOLEAN)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS USERS(
        USER_ID INT AUTO_INCREMENT PRIMARY KEY,
        USERNAME VARCHAR(255))
        """)

cursor.execute("""CREATE TABLE IF NOT EXISTS THREAD_HREFS(
        THREAD_HREF VARCHAR(255),
        SUBFORUM VARCHAR(255))
        """)

conn.close()
