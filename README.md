# Events-Intelligence-Platform
This project contains an Antigravity agent that automatically discovers upcoming tech events across Europe using Gemini. It collects conferences, meetups, workshops, hackathons, and startup events, and stores them in TiDB Cloud for structured, deduplicated tracking.
# AI Events Intelligence Platform (Europe)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.0-orange.svg)](https://deepmind.google/technologies/gemini/)

An autonomous AI-driven discovery engine designed to track, categorize, and visualize the most impactful Artificial Intelligence events across Europe. Leveraging Gemini 2.0 with Google Search Grounding, this platform eliminates the manual effort of scouting for networking opportunities, hackathons, and conferences.

![Platform Screenshot](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/docs/dashboard_preview.png) *(Replace with your local screenshot after pushing)*

##  Vision
The **AI Events Intelligence Platform** isn't just a list; it's a predictive discovery tool. It autonomously scouts the live web to find niche gatherings in specialized sectors like **FinTech, LegalTech, Healthcare, and Gaming**, ensuring that developers, founders, and investors stay ahead of the curve.

##  Key Features
- ** Autonomous Web Scouting**: Powered by Gemini 2.0 Flash with live search grounding to discover events as they are announced.
- ** Intelligence Dashboard**: Premium glassmorphism UI with advanced filtering by:
  - **Industry**: (FinTech, LegalTech, Gaming, Healthcare, etc.)
  - **Geography**: 25+ major European tech hubs.
  - **Timeline**: Monthly and date-based precision.
- ** Persistence Layer**: Built on **TiDB Cloud** for sturdy, scalable storage with built-in deduplication.
- ** Daily Rotation**: The agent cycles its research parameters daily to ensure 360-degree coverage of the European AI scene.

##  Architecture
- **Backend**: Python / Flask
- **Database**: TiDB Cloud (MySQL compatible)
- **AI Engine**: Google Gemini 2.0 Flash
- **Frontend**: Vanilla CSS (Glassmorphism) & JS

## Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- A TiDB Cloud account (Free Tier works great)
- A Google Gemini API Key

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-events-europe-collector.git
cd ai-events-europe-collector
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
TIDB_CONNECTION_STRING=mysql://your_user:your_pass@your_host:4000/ai_events_db
GEMINI_API_KEY=your_api_key_here
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize & Run
```bash
# Set up the database table
python db_setup.py

# Run the first autonomous discovery pass
python agent.py

# Start the dashboard
python backend/api.py
```
Visit `http://127.0.0.1:5000` to see your intelligence platform in action.

##  Automating Enrichment
To make the platform truly autonomous, schedule the `daily_run.bat` (Windows) or a cron job (Linux/Mac) to execute `agent.py` once every 24 hours.

##  License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
