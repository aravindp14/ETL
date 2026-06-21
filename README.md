A collection of production‑grade ETL pipelines for commodity price extraction (Steel, Copper, Silver, Crude Oil, etc.).
Each commodity uses a different extraction strategy depending on the structure of its source website — including HTML table parsing, meta‑description scraping, regex extraction, and dynamic content handling.
All pipelines follow industry‑standard ETL architecture with SQLAlchemy UPSERT logic, structured logging, and idempotent database loads.

------------------------------------------------------
COMMODITY-SPECIFIC EXTRACTION LOGIC
------------------------------------------------------

Each commodity source website exposes data differently, so the ETL logic
is tailored per commodity. This repository demonstrates how a real-world
data engineer adapts extraction strategies based on the structure of the
source.

1. STEEL ETL (ScrapMonster)
   - Extracts data from HTML tables (<tbody><tr><td>)
   - Uses BeautifulSoup table parsing
   - Multiple locations (USA, China, Europe, World)
   - Clean column extraction (metal, price, unit, currency, date)

2. COPPER ETL (TradingEconomics)
   - TradingEconomics does NOT expose price in a table
   - Price, unit, and reported date appear inside the <meta name="description">
   - Extraction uses regex on meta description
   - Example pattern:
        "Copper increased to 4.52 USD/Lbs on June 19, 2026"
   - Requires:
        • Regex extraction
        • Date parsing
        • Unit mapping
        • Meta tag parsing

3. SILVER ETL (TradingEconomics)
   - Silver page structure differs from Copper
   - Sometimes price appears in a <p> tag instead of meta description
   - Requires fallback logic:
        • Try meta description
        • If missing, scan <p> tags for price patterns
   - Regex patterns differ:
        • Silver often uses "USD/oz"
        • Date format may vary

This demonstrates that ETL pipelines must adapt to the structure of each
data source rather than assuming a single extraction method works for all.
