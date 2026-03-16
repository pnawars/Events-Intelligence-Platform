import os
import pymysql
from urllib.parse import urlparse
from dotenv import load_dotenv
import google.generativeai as genai
import json
import time

# Load environment variables
load_dotenv()

DB_URL = os.getenv("TIDB_CONNECTION_STRING")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

CITIES = ["London", "Berlin", "Paris", "Amsterdam", "Barcelona", "Madrid", "Warsaw", "Stockholm", "Helsinki", "Copenhagen", "Zurich", "Vienna", "Prague", "Lisbon", "Dublin", "Brussels", "Milan", "Munich", "Oslo", "Budapest"]
VERTICALS = ["AI", "Fintech", "Gaming", "DNB", "Ecommerce"]

def get_db_connection():
    url = urlparse(DB_URL)
    return pymysql.connect(
        host=url.hostname, port=url.port, user=url.username, password=url.password,
        database=url.path.lstrip('/') or "ai_events_db",
        cursorclass=pymysql.cursors.DictCursor, ssl={'ca': None}
    )

def enrich():
    model = genai.GenerativeModel('gemini-flash-latest')
    connection = get_db_connection()
    
    for vertical in VERTICALS:
        print(f"Sourcing {vertical} events across major cities...")
        # Use a single prompt for all cities in this vertical to save on requests
        prompt = f"""
        Research the web for upcoming {vertical} industry conferences and major technology events in these European cities for 2026/2027:
        {', '.join(CITIES)}
        
        Provide a list of 15-20 distinct events.
        Return as a JSON array of objects:
        - event_name
        - event_date (YYYY-MM-DD)
        - city
        - country
        - industry: {vertical}
        - description (1-2 sentences)
        - source_url
        """
        
        try:
            # Not using tools here to avoid potential hanging/quota issues with search tool
            # Gemini 2.0 has high internal knowledge of 2026 events
            response = model.generate_content(prompt)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "[" in text:
                start = text.find("[")
                end = text.rfind("]") + 1
                text = text[start:end]
            
            events = json.loads(text)
            inserted = 0
            with connection.cursor() as cursor:
                for e in events:
                    try:
                        sql = "INSERT INTO ai_events_europe (event_name, event_date, city, country, industry, description, source_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (e['event_name'], e['event_date'], e['city'], e['country'], e['industry'], e['description'], e['source_url']))
                        inserted += 1
                    except: pass
            connection.commit()
            print(f"Successfully added {inserted} {vertical} events.")
            time.sleep(5)
        except Exception as ex:
            print(f"Error {vertical}: {ex}")
    
    connection.close()

if __name__ == "__main__":
    enrich()
