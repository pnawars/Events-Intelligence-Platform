import pymysql
import os
from urllib.parse import urlparse

def setup_db():
    conn_str = "mysql://48hhx8G87hrZ5PK.root:8q7SrDhOrc57uVbY@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/sys"
    url = urlparse(conn_str)
    
    # Connect without database first to create it
    connection = pymysql.connect(
        host=url.hostname,
        port=url.port,
        user=url.username,
        password=url.password,
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ca': None} # This enables SSL/TLS
    )
    
    try:
        with connection.cursor() as cursor:
            # Create database
            print("Creating database ai_events_db...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS ai_events_db")
            cursor.execute("USE ai_events_db")
            
            # Create table
            print("Creating table ai_events_europe...")
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS ai_events_europe (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_name VARCHAR(255) NOT NULL,
                event_date DATE NOT NULL,
                city VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL,
                description TEXT,
                source_url VARCHAR(511),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY ux_event (event_name, event_date, city)
            );
            """
            cursor.execute(create_table_sql)
            connection.commit()
            print("Database and table setup successfully.")
    finally:
        connection.close()

if __name__ == "__main__":
    setup_db()
