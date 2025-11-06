# 🚀 Simple Backend ETL Setup Guide

## What This Does

**Simple backend script that:**
1. ✅ Fetches S&P 500 data from Kaggle
2. ✅ Automatically creates schema `SP500_DATA` in HANA
3. ✅ Automatically creates table `STOCK_PRICES`
4. ✅ Inserts all data into HANA
5. ✅ Shows statistics
6. ✅ Done!

**NO web interface, NO Flask, just pure ETL!**

---

## Files You Need

```
kaggle-hana-etl/
├── simple_etl.py              ← Main script
├── requirements_simple.txt    ← Dependencies (rename to requirements.txt)
├── manifest_simple.yml        ← Cloud Foundry config (rename to manifest.yml)
├── api/
│   ├── __init__.py
│   └── kaggle_api.py
├── db/
│   ├── __init__.py
│   └── hana_client.py
└── utils/
    ├── __init__.py
    └── config.py
```

---

## Step-by-Step Setup

### Step 1: Prepare Files

1. **Download all files** from outputs folder
2. **Rename files**:
   ```bash
   mv requirements_simple.txt requirements.txt
   mv manifest_simple.yml manifest.yml
   ```

### Step 2: Update manifest.yml

Open `manifest.yml` and update:

```yaml
env:
  # ADD YOUR FULL KAGGLE KEY HERE
  KAGGLE_USERNAME: nikhilprao
  KAGGLE_KEY: 80_PUT_YOUR_COMPLETE_KEY_HERE_de8  # ← Update this!
  
  # VERIFY YOUR HANA CREDENTIALS
  HANA_ADDRESS: your-hana-address.hanacloud.ondemand.com  # ← Check this
  HANA_PASSWORD: Qwerty!123456  # ← Check this
```

**Important**: Replace the Kaggle key with your FULL key from kaggle.json!

---

## Deploy to Cloud Foundry

### Option 1: Using CF CLI (From Laptop)

```bash
# 1. Login
cf login -a https://api.cf.us10.hana.ondemand.com
# Select org: KATBOTZ LLC
# Select space: Migration_Test

# 2. Navigate to project
cd kaggle-hana-etl

# 3. Deploy
cf push
```

### Option 2: Using SAP Business Application Studio

1. **Open SAP BAS**
2. **Upload files** or clone from Git
3. **Update manifest.yml**
4. **Open Terminal**:
   ```bash
   cd kaggle-hana-etl
   cf push
   ```

---

## What Happens When You Deploy

```
[Deploy] → [Install Dependencies] → [Run simple_etl.py]
              ↓
    [Connect to Kaggle] → [Download S&P 500 Data]
              ↓
    [Connect to HANA] → [Create Schema: SP500_DATA]
              ↓
    [Create Table: STOCK_PRICES]
              ↓
    [Insert Data] → [Show Statistics] → [Done!]
```

---

## View Logs

After deployment, check logs:

```bash
cf logs kaggle-hana-etl --recent
```

**You should see:**
```
[INFO] Starting Kaggle to HANA ETL Process
[INFO] [STEP 1] Fetching data from Kaggle...
[INFO] ✅ Successfully fetched 12000+ rows from Kaggle
[INFO] [STEP 2] Connecting to SAP HANA...
[INFO] ✅ Connected to SAP HANA
[INFO] [STEP 3] Creating schema (if not exists)...
[INFO] ✅ Schema 'SP500_DATA' ready
[INFO] [STEP 4] Creating table (if not exists)...
[INFO] ✅ Table 'SP500_DATA.STOCK_PRICES' ready
[INFO] [STEP 5] Inserting data into HANA...
[INFO] ✅ Successfully processed 12000+ rows
[INFO] [STEP 6] Retrieving database statistics...
[INFO] ========================================
[INFO] DATABASE STATISTICS
[INFO] ========================================
[INFO] Total rows in table: 12000+
[INFO] Unique tickers: 500+
[INFO] Date range: 2013-02-08 to 2018-02-07
[INFO] ========================================
[INFO] ✅ ETL Process completed successfully!
```

---

## Verify Data in HANA

### Login to SAP HANA Database Explorer

Run these SQL queries:

```sql
-- 1. Check schema exists
SELECT * FROM SYS.SCHEMAS WHERE SCHEMA_NAME = 'SP500_DATA';

-- 2. Check table exists
SELECT * FROM SYS.TABLES 
WHERE SCHEMA_NAME = 'SP500_DATA' AND TABLE_NAME = 'STOCK_PRICES';

-- 3. View data
SELECT * FROM "SP500_DATA"."STOCK_PRICES" 
ORDER BY "DATE" DESC 
LIMIT 10;

-- 4. Get statistics
SELECT 
    COUNT(*) AS TOTAL_ROWS,
    COUNT(DISTINCT "TICKER") AS UNIQUE_TICKERS,
    MIN("DATE") AS EARLIEST_DATE,
    MAX("DATE") AS LATEST_DATE,
    AVG("CLOSE") AS AVG_CLOSE_PRICE
FROM "SP500_DATA"."STOCK_PRICES";

-- 5. See specific stock (e.g., Apple)
SELECT * FROM "SP500_DATA"."STOCK_PRICES"
WHERE "TICKER" = 'AAPL'
ORDER BY "DATE" DESC
LIMIT 10;

-- 6. Top 10 stocks by volume
SELECT "TICKER", "DATE", "VOLUME", "CLOSE"
FROM "SP500_DATA"."STOCK_PRICES"
ORDER BY "VOLUME" DESC
LIMIT 10;
```

---

## How Does Schema/Table Creation Work?

### The Code Does This Automatically:

```python
# Step 1: Check if schema exists
SELECT COUNT(*) FROM SYS.SCHEMAS WHERE SCHEMA_NAME = 'SP500_DATA'

# Step 2: If not exists, create it
CREATE SCHEMA "SP500_DATA"

# Step 3: Check if table exists
SELECT COUNT(*) FROM SYS.TABLES 
WHERE SCHEMA_NAME = 'SP500_DATA' AND TABLE_NAME = 'STOCK_PRICES'

# Step 4: If not exists, create it with this structure
CREATE TABLE "SP500_DATA"."STOCK_PRICES" (
    "ID" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "TICKER" NVARCHAR(20),
    "DATE" DATE,
    "OPEN" DECIMAL(18,6),
    "HIGH" DECIMAL(18,6),
    "LOW" DECIMAL(18,6),
    "CLOSE" DECIMAL(18,6),
    "VOLUME" BIGINT,
    "DAILY_RANGE" DECIMAL(18,6),
    "DAILY_RETURN" DECIMAL(18,6),
    "TIMESTAMP" TIMESTAMP,
    UNIQUE ("TICKER", "DATE")
)

# Step 5: Insert data
INSERT INTO "SP500_DATA"."STOCK_PRICES" (...) VALUES (...)
```

**You don't need to do ANY of this manually!** 🎉

---

## Database Schema Explained

### Table: `SP500_DATA.STOCK_PRICES`

| Column | Type | Description |
|--------|------|-------------|
| ID | INTEGER | Auto-increment primary key |
| TICKER | NVARCHAR(20) | Stock symbol (AAPL, MSFT, etc.) |
| DATE | DATE | Trading date |
| OPEN | DECIMAL | Opening price |
| HIGH | DECIMAL | Highest price of the day |
| LOW | DECIMAL | Lowest price of the day |
| CLOSE | DECIMAL | Closing price |
| VOLUME | BIGINT | Number of shares traded |
| DAILY_RANGE | DECIMAL | HIGH - LOW (calculated) |
| DAILY_RETURN | DECIMAL | % change from previous day (calculated) |
| TIMESTAMP | TIMESTAMP | When record was inserted |

**Unique Constraint**: (TICKER, DATE) - prevents duplicate entries

---

## Running Locally (Optional - For Testing)

If you want to test before deploying:

### 1. Create .env file

```bash
KAGGLE_USERNAME=nikhilprao
KAGGLE_KEY=80_your_full_key_de8
KAGGLE_DATASET=camnugent/sandp500

HANA_ADDRESS=your-address.hanacloud.ondemand.com
HANA_PORT=443
HANA_USER=DBADMIN
HANA_PASSWORD=your_password
HANA_SCHEMA=SP500_DATA
HANA_TABLE=STOCK_PRICES
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
python simple_etl.py
```

---

## Scheduling (Run Automatically)

### Option 1: Cloud Foundry Tasks (Manual Trigger)

```bash
# Run the ETL as a one-time task
cf run-task kaggle-hana-etl "python simple_etl.py" --name etl-task
```

### Option 2: Job Scheduler (Automatic)

1. Subscribe to **Job Scheduler Service** in SAP BTP
2. Create a job that runs `simple_etl.py`
3. Set schedule (e.g., daily at 2 AM)

### Option 3: Cron Job (If running on server)

```bash
# Add to crontab
0 2 * * * cd /path/to/kaggle-hana-etl && python simple_etl.py
```

---

## Troubleshooting

### Problem: "Failed to fetch data from Kaggle"
**Solution**: Check your Kaggle credentials in manifest.yml

### Problem: "Failed to connect to SAP HANA"
**Solutions**:
- Verify HANA_ADDRESS is correct
- Verify HANA_PASSWORD is correct
- Check HANA instance is running

### Problem: "Schema creation failed"
**Solution**: Make sure your HANA user (DBADMIN) has permissions to create schemas

### Problem: No data inserted
**Check logs**:
```bash
cf logs kaggle-hana-etl --recent
```

---

## Complete Checklist

Before deploying:

- [ ] All files organized in folder
- [ ] `requirements_simple.txt` renamed to `requirements.txt`
- [ ] `manifest_simple.yml` renamed to `manifest.yml`
- [ ] `manifest.yml` updated with FULL Kaggle key
- [ ] `manifest.yml` updated with correct HANA credentials
- [ ] Logged into Cloud Foundry
- [ ] In correct space: `Migration_Test`

Deploy:
- [ ] Run `cf push`
- [ ] Check logs: `cf logs kaggle-hana-etl --recent`
- [ ] Verify data in HANA with SQL queries

---

## Summary

**What you need:**
1. ✅ Kaggle credentials (username + full API key)
2. ✅ HANA credentials (address, user, password)
3. ✅ Empty HANA database instance

**What the script does:**
1. ✅ Creates schema automatically
2. ✅ Creates table automatically
3. ✅ Fetches data from Kaggle
4. ✅ Inserts into HANA
5. ✅ Shows statistics

**What you DON'T need:**
- ❌ Pre-create schema
- ❌ Pre-create tables
- ❌ Web interface
- ❌ Manual data transformation

---

**Just update manifest.yml and run `cf push`!** 🚀
