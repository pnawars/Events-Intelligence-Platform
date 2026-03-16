from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pymysql
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("TIDB_CONNECTION_STRING", "mysql://48hhx8G87hrZ5PK.root:8q7SrDhOrc57uVbY@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/ai_events_db")

def get_db_connection():
    url = urlparse(DB_URL)
    return pymysql.connect(
        host=url.hostname,
        port=url.port,
        user=url.username,
        password=url.password,
        database=url.path.lstrip('/') or "ai_events_db",
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ca': None}
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ai_events_europe ORDER BY event_date ASC")
            events = cursor.fetchall()
        connection.close()
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM ai_events_europe")
            total = cursor.fetchone()['total']
            
            cursor.execute("SELECT country, COUNT(*) as count FROM ai_events_europe GROUP BY country")
            countries = cursor.fetchall()
            
            cursor.execute("SELECT city, COUNT(*) as count FROM ai_events_europe GROUP BY city")
            cities = cursor.fetchall()

            cursor.execute("SELECT industry, COUNT(*) as count FROM ai_events_europe GROUP BY industry")
            industries = cursor.fetchall()

        connection.close()
        return jsonify({
            "total": total,
            "countries": countries,
            "cities": cities,
            "industries": industries
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
