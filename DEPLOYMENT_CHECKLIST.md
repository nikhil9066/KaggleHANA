# ✅ Deployment Checklist - Simple Backend ETL

## Pre-Deployment (5 minutes)

### 1. Get Your Files Ready
- [ ] Download `simple_etl.py`
- [ ] Download `requirements_simple.txt` 
- [ ] Download `manifest_simple.yml`
- [ ] Download folders: `api/`, `db/`, `utils/`

### 2. Rename Files
```bash
mv requirements_simple.txt requirements.txt
mv manifest_simple.yml manifest.yml
```

### 3. Update manifest.yml

Open `manifest.yml` and update **2 things**:

**A. Your Complete Kaggle Key:**
```yaml
KAGGLE_USERNAME: nikhilprao
KAGGLE_KEY: 80____________de8  # ← PUT YOUR COMPLETE KEY HERE
```

From your kaggle.json:
```json
{
  "username": "nikhilprao",
  "key": "80...your_full_key_here...de8"
}
```

**B. Verify HANA Credentials:**
```yaml
HANA_ADDRESS: a0b0b370-2621-4f9c-95c3-2063833ac9ef.hana.prod-us10.hanacloud.ondemand.com
HANA_PASSWORD: Qwerty!123456  # ← Is this correct?
HANA_USER: DBADMIN  # ← Is this correct?
```

---

## Deployment (2 minutes)

### Option A: Using CF CLI

```bash
# 1. Login
cf login -a https://api.cf.us10.hana.ondemand.com

# When prompted:
# - Email: your-email@company.com
# - Password: your-password
# - Org: Select "KATBOTZ LLC"
# - Space: Select "Migration_Test"

# 2. Navigate to project
cd kaggle-hana-etl

# 3. Deploy
cf push
```

### Option B: Using SAP BAS

```
1. Open SAP BAS
2. Upload your project files (or git clone)
3. Open Terminal
4. cd kaggle-hana-etl
5. cf push
```

---

## Post-Deployment (2 minutes)

### 1. Check Logs
```bash
cf logs kaggle-hana-etl --recent
```

**Look for:**
```
✅ Successfully fetched XXX rows from Kaggle
✅ Connected to SAP HANA
✅ Schema 'SP500_DATA' ready
✅ Table 'SP500_DATA.STOCK_PRICES' ready
✅ Successfully processed XXX rows
✅ ETL Process completed successfully!
```

### 2. Verify in HANA

Open SAP HANA Database Explorer and run:

```sql
-- Quick check
SELECT COUNT(*) FROM "SP500_DATA"."STOCK_PRICES";

-- Should return: 12000+ rows
```

**If you see data** → ✅ **SUCCESS!**

---

## Quick Reference

### File Structure
```
kaggle-hana-etl/
├── simple_etl.py          ← Main script
├── requirements.txt       ← Dependencies
├── manifest.yml           ← Your credentials
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

### What Gets Created in HANA
```
Schema: SP500_DATA
  └── Table: STOCK_PRICES
       ├── Columns: TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME, etc.
       └── Data: 12000+ rows of S&P 500 stock prices
```

### Useful Commands
```bash
# View logs
cf logs kaggle-hana-etl --recent

# Check app status
cf app kaggle-hana-etl

# Restart (if needed)
cf restart kaggle-hana-etl

# Delete and redeploy
cf delete kaggle-hana-etl
cf push
```

---

## Troubleshooting

### ❌ "Kaggle API authentication failed"
→ Check KAGGLE_KEY in manifest.yml (must be complete key)

### ❌ "HANA connection failed"
→ Check HANA_ADDRESS, HANA_PASSWORD in manifest.yml

### ❌ "Schema creation failed"
→ Check HANA user has CREATE SCHEMA permission

### ❌ App crashes immediately
→ Check logs: `cf logs kaggle-hana-etl --recent`

---

## Success Criteria

✅ **You're done when:**
1. `cf push` completes without errors
2. Logs show "ETL Process completed successfully!"
3. SQL query returns data from STOCK_PRICES table
4. You see 12000+ rows in HANA

---

## Next Steps After Success

### Run Queries
```sql
-- Get Apple stock data
SELECT * FROM "SP500_DATA"."STOCK_PRICES"
WHERE "TICKER" = 'AAPL'
ORDER BY "DATE" DESC
LIMIT 10;

-- Top stocks by volume
SELECT "TICKER", "DATE", "VOLUME"
FROM "SP500_DATA"."STOCK_PRICES"
ORDER BY "VOLUME" DESC
LIMIT 10;
```

### Schedule Regular Updates
- Use CF Tasks: `cf run-task kaggle-hana-etl "python simple_etl.py"`
- Or subscribe to Job Scheduler service

---

## The Magic

**You provide:**
- ✅ Kaggle credentials
- ✅ HANA credentials

**Script automatically:**
- ✅ Creates schema SP500_DATA
- ✅ Creates table STOCK_PRICES
- ✅ Downloads S&P 500 data from Kaggle
- ✅ Inserts into HANA
- ✅ Shows statistics

**You DON'T need to:**
- ❌ Create schema manually
- ❌ Create tables manually
- ❌ Write SQL
- ❌ Transform data manually

---

**Ready? Update manifest.yml and run `cf push`!** 🚀
