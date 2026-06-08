Social Media Moderation Analytics 

OVEVIEW
This project is a Social Media Moderation Analytics Programme designed to help users explore, analyse, and interpret patterns in social media data. It enables moderators to load datasets, clean and prepare records, and perform analytical tasks such as identifying report trends, engagement patterns, and relationships between moderation levels and user behaviour.

TECHNOLOGIES USED
Python 3
pandas – data processing and analysis
matplotlib – visualisations
tkinter – GUI
sqlite3 – database storage
json – data backup format

HOW TO RUN
Ensure Python 3 is installed

Install required libraries:
pip install pandas matplotlib

Run the application:
python gui.py

In the GUI:
Select CSV files (or use defaults):
- USERS.csv
- POSTS.csv
- INTERACTIONS.csv
- TOPICS.csv
Click Load Data
Click Clean Data
Run analytics from the dashboard

FILE STRUCTURE
submission/
│
├── backend.py                  # Data processing and analytics logic
├── gui.py                      # Graphical user interface
├── backup.json                 # JSON backup (generated at runtime)
├── backup.db                   # SQLite database (generated at runtime)
├── audit_log.txt               # Audit log file (generated at runtime)
|
├── database_structure_dump.sql # SQL database structure
|
└── README.md                   # Project documentation

This project is developed for educational purposes and is not intended for commercial use.
