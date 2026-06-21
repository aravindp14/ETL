STEEL PRICE ETL PIPELINE (PYTHON + SQLALCHEMY + MYSQL)
======================================================

A production-grade ETL pipeline that extracts global steel prices from ScrapMonster,
transforms the data, and loads it into a MySQL database using SQLAlchemy with UPSERT logic.
The pipeline is idempotent, modular, and follows industry-standard engineering practices.


------------------------------------------------------
FEATURES
------------------------------------------------------
• Web Scraping using requests + BeautifulSoup
• Data Cleaning & Transformation using pandas
• Database Loading using SQLAlchemy with:
    - Connection pooling
    - Safe transaction handling
    - UPSERT (ON DUPLICATE KEY UPDATE)
• Idempotent ETL (safe to run multiple times)
• Logging to file + console
• Production-grade structure (modular, testable, Airflow-ready)


------------------------------------------------------
TECH STACK
------------------------------------------------------
• Python 3.x
• Pandas
• Requests
• BeautifulSoup4
• SQLAlchemy
• PyMySQL
• MySQL (InnoDB)


------------------------------------------------------
PROJECT STRUCTURE
------------------------------------------------------
steel-price-etl/
│
├── etl.py                # Main ETL pipeline
├── requirements.txt      # Dependencies
├── README.txt            # Documentation
├── etl_log.txt           # Runtime logs
└── output/               # CSV outputs


------------------------------------------------------
DATABASE SCHEMA
------------------------------------------------------
CREATE TABLE steel_price (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metal_type VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    unit VARCHAR(50),
    currency VARCHAR(10),
    location VARCHAR(100),
    scraped_date DATETIME NOT NULL,
    reported_date DATE NOT NULL,
    UNIQUE (metal_type, reported_date, location)
);

The unique constraint ensures one price per metal per day per location.


------------------------------------------------------
ETL FLOW
------------------------------------------------------
1. EXTRACT
   - Scrapes steel prices from:
        • USA
        • China
        • Europe
        • World Export Market
   - Parses HTML tables safely
   - Maps currency & unit formats
   - Converts dates to Python datetime

2. TRANSFORM
   - Minimal transformation (data already normalized)
   - Future-proof for additional logic

3. LOAD
   - Saves CSV per location
   - Loads into MySQL using SQLAlchemy
   - Uses UPSERT to avoid duplicate key errors
   - Ensures idempotency


------------------------------------------------------
HOW TO RUN
------------------------------------------------------
python etl.py


------------------------------------------------------
KEY CONCEPTS DEMONSTRATED
------------------------------------------------------

1. ETL ARCHITECTURE
   - Extract → Transform → Load
   - Modular functions
   - Clean separation of concerns

2. WEB SCRAPING
   - HTML parsing
   - Table extraction
   - Data normalization

3. DATA ENGINEERING BEST PRACTICES
   - Idempotent pipelines
   - UPSERT logic
   - Connection pooling
   - Logging
   - Error handling

4. SQLALCHEMY PRODUCTION USAGE
   - engine.begin() for safe transactions
   - Named parameters (:param)
   - Avoiding metadata locks
   - Avoiding PyMySQL placeholder conflicts

5. DATABASE DESIGN
   - Unique constraints
   - Normalized schema
   - Timestamp tracking


------------------------------------------------------
INTERVIEW TALKING POINTS
------------------------------------------------------

1. Why SQLAlchemy instead of raw MySQL connector?
   - Connection pooling
   - Automatic transaction management
   - Cleaner parameter binding
   - Production-grade reliability

2. Why UPSERT?
   - Prevents duplicate key errors
   - Makes pipeline idempotent
   - Ensures latest data overwrites stale data

3. How did you avoid metadata locks?
   - Using engine.begin()
   - Ensuring connections auto-close
   - Avoiding persistent MySQL sessions

4. How did you ensure scalability?
   - Modular design
   - Stateless functions
   - Pool recycling
   - Ready for Airflow scheduling

5. What challenges did you solve?
   - SQLAlchemy placeholder mismatch
   - PyMySQL parameter binding
   - Metadata lock debugging
   - DataFrame accumulation bug
   - HTML structure inconsistencies


------------------------------------------------------
REQUIREMENTS
------------------------------------------------------
pandas
requests
beautifulsoup4
sqlalchemy
pymysql
