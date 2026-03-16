import os
import pymysql
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import google.generativeai as genai
import json
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

# Database Config
DB_URL = os.getenv("TIDB_CONNECTION_STRING")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Specialized Search Categories
CITIES = ["London", "Berlin", "Paris", "Amsterdam", "Barcelona", "Madrid", "Warsaw", "Stockholm", "Helsinki", "Copenhagen", "Zurich", "Vienna", "Prague", "Lisbon", "Dublin", "Brussels", "Milan", "Munich", "Oslo", "Budapest"]
NICHES = [
    "Generative AI", "LLMs", "AI in Healthcare", "AI in Finance", "LegalTech", 
    "Cybersecurity AI", "AI in Manufacturing", "Computer Vision", "MLOps", 
    "AI Ethics", "AI Startup Summit", "AI Hackathons", "Fintech Innovations", 
    "Ecommerce Strategy", "Gaming Industry", "Digital Business (DnB)", 
    "SaaS Trends", "Web3 & Blockchain", "Cloud Computing"
]

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

def perform_autonomous_research():
    """
    Uses Gemini 2.0 Flash with Google Search Grounding to find new events.
    """
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found.")
        return []

    # Pick 3 random cities and 2 random niches to keep the search fresh daily
    selected_cities = random.sample(CITIES, 3)
    selected_niches = random.sample(NICHES, 3)
    
    query_context = f"focusing on {', '.join(selected_cities)} and sectors like {', '.join(selected_niches)}"
    print(f"Researching: {query_context}")

    # Use Gemini 2.0 Flash with Google Search Tool
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Search for upcoming Technology and AI events, conferences, and meetups in Europe for 2026 and 2027.
    Specifically look for events in {', '.join(selected_cities)} related to {', '.join(selected_niches)}.
    
    For each event found, provide:
    - event_name
    - event_date (YYYY-MM-DD)
    - city
    - country
    - industry (Choose: AI, Fintech, Ecommerce, Gaming, DnB (Digital Business), Healthcare, LegalTech, or SaaS)
    - description (1-2 sentences)
    - source_url
    
    Rules:
    1. Only future events located in Europe.
    2. Format the output as a valid JSON array of objects.
    3. Ensure dates are strictly YYYY-MM-DD.
    """
    
    try:
        # We use tools to enable grounding if supported by the model
        response = model.generate_content(
            prompt,
            tools=[{'google_search_retrieval': {}}]
        )
        
        content = response.text
        # Cleanup JSON formatting
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "[" in content and "]" in content:
            # Fallback for when it doesn't use markdown fences
            start = content.find("[")
            end = content.rfind("]") + 1
            content = content[start:end]
            
        events = json.loads(content)
        return events
    except Exception as e:
        print(f"Autonomous Research Error: {e}")
        return []

def run_agent():
    print(f"\n--- AI Events Europe Collector: Autonomous Run [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ---")
    
    stats = {
        "events_found": 0,
        "events_inserted": 0,
        "duplicates_skipped": 0,
        "errors": 0
    }
    
    # 1. Research & Extract
    events = perform_autonomous_research()
    stats["events_found"] = len(events)
    
    if not events:
        print("No new events found in this pass.")
        return
    
    # 2. Persist to Database
    print(f"Found {len(events)} potential events. Synchronizing with TiDB...")
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            for event in events:
                try:
                    sql = """
                    INSERT INTO ai_events_europe (event_name, event_date, city, country, industry, description, source_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        event.get("event_name"),
                        event.get("event_date"),
                        event.get("city"),
                        event.get("country"),
                        event.get("industry", "AI"),
                        event.get("description"),
                        event.get("source_url")
                    ))
                    stats["events_inserted"] += 1
                except pymysql.err.IntegrityError:
                    stats["duplicates_skipped"] += 1
                except Exception as e:
                    print(f"Error inserting {event.get('event_name')}: {e}")
                    stats["errors"] += 1
            
            connection.commit()
    finally:
        connection.close()
    
    print("\n✅ Run Completed Successfully.")
