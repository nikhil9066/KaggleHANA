# SAP S/4HANA Built-in Data Migration Tools Guide

**Version**: 1.0.0
**Last Updated**: November 7, 2025
**Applies to**: SAP S/4HANA 2020, 2021, 2022, 2023

---

## Table of Contents

1. [Overview of S/4HANA Migration Tools](#overview-of-s4hana-migration-tools)
2. [Migration Cockpit (LTMC)](#migration-cockpit-ltmc)
3. [SAP S/4HANA Migration Object Modeler (LTMOM)](#sap-s4hana-migration-object-modeler-ltmom)
4. [Legacy System Migration Workbench (LSMW)](#legacy-system-migration-workbench-lsmw)
5. [SAP Data Services](#sap-data-services)
6. [Direct Transfer from SAP ECC (SAP S/4HANA System Conversion)](#direct-transfer-from-sap-ecc)
7. [Rapid Data Migration (RDM)](#rapid-data-migration-rdm)
8. [SAP Cloud Platform Integration](#sap-cloud-platform-integration)
9. [Tool Comparison Matrix](#tool-comparison-matrix)
10. [Step-by-Step Migration Procedures](#step-by-step-migration-procedures)

---

## Overview of S/4HANA Migration Tools

SAP S/4HANA provides multiple built-in tools for data migration, each suited for different scenarios:

```
┌─────────────────────────────────────────────────────────────────┐
│              SAP S/4HANA Built-in Migration Tools               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ Migration        │  │  Migration       │                     │
│  │ Cockpit (LTMC)   │  │  Object Modeler  │                     │
│  │                  │  │  (LTMOM)         │                     │
│  │ ★ Primary Tool   │  │  ★ Customize     │                     │
│  └──────────────────┘  └──────────────────┘                     │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ LSMW             │  │  SAP Data        │                     │
│  │ (Legacy)         │  │  Services        │                     │
│  │                  │  │                  │                     │
│  │ ★ Legacy Support │  │  ★ Complex ETL   │                     │
│  └──────────────────┘  └──────────────────┘                     │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ System           │  │  Rapid Data      │                     │
│  │ Conversion       │  │  Migration (RDM) │                     │
│  │                  │  │                  │                     │
│  │ ★ ECC to S/4     │  │  ★ Cloud Edition │                     │
│  └──────────────────┘  └──────────────────┘                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### When to Use Which Tool?

| Source System | Target S/4HANA | Recommended Tool | Complexity |
|---------------|----------------|------------------|------------|
| SAP ECC | On-Premise/Cloud | System Conversion | High |
| Oracle/SQL Server | On-Premise | Migration Cockpit (LTMC) | Medium |
| Legacy SAP | On-Premise | LSMW | Medium |
| External DB | On-Premise | SAP Data Services | High |
| Cloud Applications | S/4HANA Cloud | RDM + CPI | Medium |
| Excel/CSV Files | Any | Migration Cockpit (LTMC) | Low |

---

## Migration Cockpit (LTMC)

### Overview

**Migration Cockpit (LTMC)** is SAP's **primary recommended tool** for data migration to S/4HANA. It provides a user-friendly interface for migrating master data and transactional data from various sources.

### Key Features

- ✅ **Pre-delivered Migration Objects**: 100+ pre-configured objects (customers, materials, sales orders, etc.)
- ✅ **File Upload Support**: Excel, CSV, XML formats
- ✅ **Direct Database Transfer**: Connect to Oracle, SQL Server, DB2
- ✅ **Data Validation**: Built-in validation rules
- ✅ **Simulation Mode**: Test before actual migration
- ✅ **Error Handling**: Detailed error logs with correction capabilities
- ✅ **Incremental Loading**: Support for delta uploads

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Migration Cockpit (LTMC)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Source Data                                                     │
│  ↓                                                               │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │ Excel/CSV    │   │ Oracle DB    │   │ SQL Server   │        │
│  │ Files        │   │              │   │              │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            ↓                                     │
│         ┌──────────────────────────────────┐                    │
│         │  Data Staging (LTMC Tables)      │                    │
│         │  • Validation                     │                    │
│         │  • Transformation                 │                    │
│         │  • Error Checking                 │                    │
│         └──────────────────┬────────────────┘                    │
│                            ↓                                     │
│         ┌──────────────────────────────────┐                    │
│         │  Migration Objects               │                    │
│         │  • /SAPAPO/MATMAP (Materials)    │                    │
│         │  • /SAPAPO/LOCMAP (Locations)    │                    │
│         │  • /SAPAPO/CUSTMAP (Customers)   │                    │
│         └──────────────────┬────────────────┘                    │
│                            ↓                                     │
│         ┌──────────────────────────────────┐                    │
│         │  S/4HANA Business Objects        │                    │
│         │  • BAPIs/APIs                     │                    │
│         │  • IDoc Processing                │                    │
│         └──────────────────┬────────────────┘                    │
│                            ↓                                     │
│                   S/4HANA Database                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step: Migration Cockpit (LTMC)

### Prerequisites

1. **System Access**
   - SAP S/4HANA system access with authorization object `S_LTMC_ALL`
   - SAP GUI or SAP Fiori Launchpad access

2. **Data Preparation**
   - Source data in Excel/CSV format **OR**
   - Direct database connection configured

3. **SAP Notes Applied**
   - Check SAP Note 2267138 - Migration Cockpit FAQ
   - Check SAP Note 2360557 - Migration Cockpit Performance

---

### Phase 1: Activate Migration Objects

#### Step 1.1: Access Migration Cockpit

**Via SAP GUI:**
```
Transaction Code: LTMC
```

**Via SAP Fiori:**
```
Navigate to: SAP Fiori Launchpad → Migration → Migration Cockpit
```

#### Step 1.2: Activate Migration Object

1. Click **"Activate Migration Objects"** tile
2. Search for your object (e.g., "Business Partner")

   **Common Migration Objects:**
   | Object Name | Technical ID | Use Case |
   |-------------|--------------|----------|
   | Business Partner | 0BP_IDEN | Customer/Supplier master |
   | Material Master | 0MATERIAL_IDEN | Product data |
   | Sales Order | 0SORDER_IDEN | Sales transactions |
   | Purchase Order | 0PORDER_IDEN | Procurement data |
   | GL Accounts | 0GL_ACCOUNT_IDEN | Chart of accounts |
   | Cost Centers | 0COSTCENTER_IDEN | Controlling master |
   | Fixed Assets | 0ASSET_IDEN | Asset master |

3. Select the object and click **"Activate"**
4. System will generate:
   - Staging tables (e.g., `/SAPAPO/MATMAP_STG`)
   - Validation rules
   - Mapping logic

**Screenshot Reference:**
```
╔════════════════════════════════════════════════════════════╗
║  Activate Migration Objects                                ║
╠════════════════════════════════════════════════════════════╣
║  Search: [Business Partner_____________]  [Search]         ║
║                                                            ║
║  ☐ 0BP_IDEN          Business Partner                     ║
║  ☐ 0MATERIAL_IDEN    Material Master                      ║
║  ☐ 0SORDER_IDEN      Sales Order                          ║
║  ☐ 0CUSTOMER_IDEN    Customer                             ║
║                                                            ║
║  [Activate Selected]  [Deactivate]  [Check Status]        ║
╚════════════════════════════════════════════════════════════╝
```

#### Step 1.3: Verify Activation

1. Go to **"Migration Object Overview"**
2. Check status = **"Active"** (green light)
3. Note the **Template File Name** (for Excel upload)

---

### Phase 2: Create Migration Project

#### Step 2.1: Create New Project

1. In LTMC, click **"Create Migration Project"**
2. Fill in project details:

   ```
   ┌─────────────────────────────────────────────────┐
   │ Create Migration Project                        │
   ├─────────────────────────────────────────────────┤
   │                                                 │
   │ Project Name:        [ORA_TO_S4_MIGRATION____] │
   │ Description:         [Oracle to S/4HANA ______] │
   │                      [Business Partner Data ___] │
   │ Migration Object:    [0BP_IDEN______________▼] │
   │ Data Source:         [⦿ File Upload            │
   │                       ○ Direct Transfer         │
   │                       ○ Staging Table          │
   │                                                 │
   │ [Create]  [Cancel]                              │
   └─────────────────────────────────────────────────┘
   ```

3. Click **"Create"**

#### Step 2.2: Project Created

- System assigns a **Project ID** (e.g., `000000000001`)
- Project status = **"In Preparation"**

---

### Phase 3: Prepare Source Data

#### Option A: File Upload (Excel/CSV)

##### Step 3A.1: Download Template

1. In your migration project, click **"Download Template"**
2. System provides an Excel file with:
   - **Required fields** (red columns)
   - **Optional fields** (white columns)
   - **Data validation rules**
   - **Sample data** (first row)

**Example Template Structure:**
```
┌────────┬──────────────┬──────────────┬────────────┬─────────────┐
│ Field  │ BP_NUMBER    │ BP_NAME      │ BP_TYPE    │ BP_CATEGORY │
├────────┼──────────────┼──────────────┼────────────┼─────────────┤
│ Sample │ 1000001      │ ACME Corp    │ 2          │ 1           │
├────────┼──────────────┼──────────────┼────────────┼─────────────┤
│ Data   │              │              │            │             │
│ Row 1  │              │              │            │             │
└────────┴──────────────┴──────────────┴────────────┴─────────────┘

Legend:
- Red columns = Mandatory
- BP_TYPE: 1=Person, 2=Organization
- BP_CATEGORY: 1=Customer, 2=Supplier, 3=Both
```

##### Step 3A.2: Fill Template with Source Data

**Option 1: Manual Entry**
- Copy data from Oracle/Excel into template

**Option 2: Use Middleware (Recommended)**
```python
# Python script to export Oracle data to LTMC Excel template
import cx_Oracle
import pandas as pd

# Connect to Oracle
oracle_conn = cx_Oracle.connect('user/password@oracle_db')

# Extract business partner data
query = """
    SELECT
        CUSTOMER_ID as BP_NUMBER,
        CUSTOMER_NAME as BP_NAME,
        '2' as BP_TYPE,
        '1' as BP_CATEGORY,
        STREET as STREET,
        CITY as CITY,
        POSTAL_CODE as POSTAL_CODE,
        COUNTRY as COUNTRY
    FROM CUSTOMERS
"""
df = pd.read_sql(query, oracle_conn)

# Load LTMC template
template = pd.read_excel('LTMC_BP_Template.xlsx', sheet_name='Data')

# Merge data into template
for col in df.columns:
    if col in template.columns:
        template[col] = df[col]

# Save populated template
template.to_excel('LTMC_BP_Data_Populated.xlsx', index=False)

print(f"✅ Exported {len(df)} records to LTMC template")
```

##### Step 3A.3: Validate Template Data

Before upload, ensure:
- ✅ No empty required fields
- ✅ Data types match (numbers as numbers, dates as dates)
- ✅ Date format: `DD.MM.YYYY` (SAP standard)
- ✅ No special characters in key fields
- ✅ Lookup values valid (e.g., Country codes)

#### Option B: Direct Transfer (Database to Database)

##### Step 3B.1: Configure Source System

1. In LTMC project, select **"Direct Transfer"**
2. Create source system connection:

   ```
   Transaction Code: SM59 (RFC Destinations)

   ┌─────────────────────────────────────────────────┐
   │ RFC Destination                                 │
   ├─────────────────────────────────────────────────┤
   │ RFC Destination:  [ORACLE_SOURCE___]            │
   │ Connection Type:  [TCP/IP Connection___]        │
   │ Description:      [Oracle Source DB___]         │
   │                                                 │
   │ Technical Settings:                             │
   │ Host:             [oracle-db.company.com___]    │
   │ Port:             [1521___]                     │
   │                                                 │
   │ Logon & Security:                               │
   │ User:             [sap_migration_user___]       │
   │ Password:         [****************___]         │
   │                                                 │
   │ [Save]  [Test Connection]                       │
   └─────────────────────────────────────────────────┘
   ```

3. Test connection - should show **"Connection OK"**

##### Step 3B.2: Define Source Structure

1. In LTMC, go to **"Define Source Structure"**
2. Map source table/columns to S/4HANA fields:

   ```
   Source Table: CUSTOMERS (Oracle)

   ┌──────────────────┬────────────┬─────────────────────┐
   │ Source Field     │ Mapping    │ Target Field (S/4)  │
   ├──────────────────┼────────────┼─────────────────────┤
   │ CUSTOMER_ID      │ ───────────→ BP_NUMBER            │
   │ CUSTOMER_NAME    │ ───────────→ BP_NAME              │
   │ CUST_TYPE        │ ─┐         │                     │
   │                  │  │ Rule 1  │                     │
   │                  │  └────────→ BP_TYPE              │
   │ ADDRESS_LINE1    │ ───────────→ STREET               │
   │ CITY             │ ───────────→ CITY                 │
   │ ZIP              │ ───────────→ POSTAL_CODE          │
   │ COUNTRY_CODE     │ ───────────→ COUNTRY              │
   └──────────────────┴────────────┴─────────────────────┘

   Transformation Rule 1:
   IF CUST_TYPE = 'PERSON' THEN BP_TYPE = '1'
   IF CUST_TYPE = 'COMPANY' THEN BP_TYPE = '2'
   ```

3. Define filters (optional):
   ```sql
   -- Only migrate active customers
   WHERE STATUS = 'ACTIVE'
     AND CREATED_DATE >= '2020-01-01'
   ```

4. Save source structure definition

---

### Phase 4: Load Data to Staging

#### Step 4.1: Upload File (if using File Upload)

1. In migration project, click **"Upload File"**
2. Select your populated Excel/CSV file
3. Click **"Upload"**

**Progress Indicator:**
```
╔════════════════════════════════════════════════╗
║  Uploading File...                             ║
╠════════════════════════════════════════════════╣
║  File: LTMC_BP_Data_Populated.xlsx             ║
║  Size: 2.5 MB                                  ║
║                                                ║
║  Progress: [████████████████████░░░░] 85%      ║
║                                                ║
║  Records processed: 8,500 / 10,000             ║
║  Estimated time remaining: 30 seconds          ║
╚════════════════════════════════════════════════╝
```

#### Step 4.2: Or Execute Direct Transfer

1. In migration project, click **"Execute Direct Transfer"**
2. System extracts data from source and loads to staging
3. Monitor progress in **"Transfer Monitor"**

#### Step 4.3: Review Staging Data

1. Click **"Display Staging Data"**
2. Review loaded records in staging table
3. Check for any obvious issues

**Staging Table View:**
```
┌──────────┬─────────────┬──────────────┬────────┬─────────┐
│ Row      │ BP_NUMBER   │ BP_NAME      │ Status │ Message │
├──────────┼─────────────┼──────────────┼────────┼─────────┤
│ 00001    │ 1000001     │ ACME Corp    │ ✅ OK  │         │
│ 00002    │ 1000002     │ TechCo Inc   │ ✅ OK  │         │
│ 00003    │ 1000003     │ GlobalTrade  │ ✅ OK  │         │
│ ...      │ ...         │ ...          │ ...    │         │
│ 10000    │ 1010000     │ EndUser LLC  │ ✅ OK  │         │
└──────────┴─────────────┴──────────────┴────────┴─────────┘

Summary: 10,000 records loaded to staging
```

---

### Phase 5: Validate Data

#### Step 5.1: Run Validation

1. Click **"Start Validation"**
2. System performs:
   - ✅ **Field validations**: Required fields, data types, lengths
   - ✅ **Business validations**: Valid country codes, currency codes
   - ✅ **Duplicate checks**: No duplicate BP numbers
   - ✅ **Foreign key checks**: Referenced objects exist
   - ✅ **Custom validations**: Business rules (if configured)

**Validation Progress:**
```
╔════════════════════════════════════════════════╗
║  Validation Running...                         ║
╠════════════════════════════════════════════════╣
║  Phase 1: Field Validation     [✅ Complete]   ║
║  Phase 2: Business Rules       [✅ Complete]   ║
║  Phase 3: Duplicate Check      [⏳ Running]    ║
║  Phase 4: Foreign Keys         [⏸ Pending]    ║
║  Phase 5: Custom Rules         [⏸ Pending]    ║
║                                                ║
║  Records validated: 7,234 / 10,000             ║
╚════════════════════════════════════════════════╝
```

#### Step 5.2: Review Validation Results

**Validation Summary:**
```
╔════════════════════════════════════════════════╗
║  Validation Complete                           ║
╠════════════════════════════════════════════════╣
║  Total Records:        10,000                  ║
║  ✅ Valid Records:     9,850                   ║
║  ❌ Invalid Records:   150                     ║
║  ⚠️  Warnings:         25                      ║
║                                                ║
║  Success Rate: 98.5%                           ║
║                                                ║
║  [View Error Log]  [Download Error Report]     ║
╚════════════════════════════════════════════════╝
```

#### Step 5.3: Review and Fix Errors

1. Click **"View Error Log"**
2. Review errors:

   ```
   ┌──────┬─────────────┬──────────────┬─────────────────────────────┐
   │ Row  │ BP_NUMBER   │ Error Field  │ Error Message               │
   ├──────┼─────────────┼──────────────┼─────────────────────────────┤
   │ 0123 │ 1000123     │ COUNTRY      │ Invalid country code 'XX'   │
   │ 0456 │ 1000456     │ POSTAL_CODE  │ Postal code too long (>10)  │
   │ 0789 │             │ BP_NUMBER    │ Required field is empty     │
   │ 1012 │ 1001012     │ DUPLICATE    │ BP_NUMBER already exists    │
   └──────┴─────────────┴──────────────┴─────────────────────────────┘
   ```

3. **Fix errors** using one of these methods:

   **Method A: Fix in Staging Table (SAP GUI)**
   ```
   Transaction: SE16N
   Table: /SAPAPO/MATMAP_STG (or your staging table)

   1. Search for error row by BP_NUMBER
   2. Click "Edit" (requires authorization)
   3. Fix the field value
   4. Save
   ```

   **Method B: Re-upload Corrected File**
   ```
   1. Download error report (Excel)
   2. Fix errors in source file
   3. Delete failed records from staging
   4. Re-upload corrected file
   ```

   **Method C: Use Middleware to Auto-Fix**
   ```python
   # Python script to auto-correct common errors
   import pandas as pd

   # Load error report
   errors = pd.read_excel('LTMC_Error_Report.xlsx')

   # Auto-fix common issues
   for idx, row in errors.iterrows():
       if row['Error_Field'] == 'COUNTRY':
           # Map invalid codes to valid ones
           if row['Value'] == 'XX':
               row['Corrected_Value'] = 'US'  # Default to US

       if row['Error_Field'] == 'POSTAL_CODE':
           # Truncate to 10 characters
           row['Corrected_Value'] = row['Value'][:10]

   # Export corrected values
   errors.to_excel('LTMC_Corrections.xlsx', index=False)
   ```

4. **Re-run validation** after fixes
5. Repeat until validation success rate is acceptable (typically >99%)

---

### Phase 6: Simulate Migration

#### Step 6.1: Run Simulation

**Purpose**: Test the migration without actually creating data in S/4HANA.

1. Click **"Start Simulation"**
2. System will:
   - ✅ Call BAPIs in test mode
   - ✅ Check for authorization issues
   - ✅ Validate business logic
   - ✅ Identify potential runtime errors
   - ❌ **NOT create** actual data

**Simulation Progress:**
```
╔════════════════════════════════════════════════╗
║  Simulation Running...                         ║
╠════════════════════════════════════════════════╣
║  Processing records in batches of 100          ║
║                                                ║
║  Batch 1/100:  [✅ Complete] 100/100 success   ║
║  Batch 2/100:  [✅ Complete] 98/100 success    ║
║  Batch 3/100:  [⏳ Running]  45/100 processed  ║
║  Batch 4/100:  [⏸ Pending]                    ║
║  ...                                           ║
║                                                ║
║  Estimated completion: 12 minutes              ║
╚════════════════════════════════════════════════╝
```

#### Step 6.2: Review Simulation Results

**Simulation Summary:**
```
╔════════════════════════════════════════════════╗
║  Simulation Complete                           ║
╠════════════════════════════════════════════════╣
║  Total Records:         9,850                  ║
║  ✅ Successful:         9,735                  ║
║  ❌ Failed:             115                    ║
║  ⚠️  Warnings:          50                     ║
║                                                ║
║  Success Rate: 98.8%                           ║
║                                                ║
║  Common Errors:                                ║
║  • Missing pricing conditions (45)             ║
║  • Invalid tax classification (30)             ║
║  • Duplicate check failed (25)                 ║
║  • Authorization missing (15)                  ║
║                                                ║
║  [View Error Details]  [Export Log]            ║
╚════════════════════════════════════════════════╝
```

#### Step 6.3: Analyze and Fix Simulation Errors

**Common Simulation Errors and Solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| "Authorization missing" | User lacks authorization for BAPI | Request authorization object (e.g., `F_BUPA_GRP`) |
| "Pricing condition not found" | Referenced condition record missing | Create master data dependencies first |
| "Company code not defined" | Company code doesn't exist | Create company code in IMG (SPRO) |
| "Duplicate business partner" | BP already exists in system | Use "Update" mode instead of "Insert" |
| "Field XXXX is not ready for input" | Field not enabled in config | Check customizing (SPRO) for the field |

#### Step 6.4: Re-run Simulation

- Fix issues identified in simulation
- Re-run simulation until success rate >99%
- **Do not proceed to migration** until simulation is clean

---

### Phase 7: Execute Migration

#### Step 7.1: Final Pre-Migration Checks

**Checklist before Go-Live:**
```
Pre-Migration Checklist:
─────────────────────────────────────────────────
[ ] ✅ Validation passed (>99% success)
[ ] ✅ Simulation passed (>99% success)
[ ] ✅ All errors resolved or documented
[ ] ✅ Backup taken of S/4HANA system
[ ] ✅ Change freeze in effect (no config changes)
[ ] ✅ Migration window scheduled and approved
[ ] ✅ Rollback plan documented
[ ] ✅ Support team on standby
[ ] ✅ Stakeholders notified
[ ] ✅ Go/No-Go approval obtained
```

#### Step 7.2: Execute Migration

1. Click **"Start Migration"**
2. Confirm migration dialog:

   ```
   ╔════════════════════════════════════════════════╗
   ║  ⚠️  Start Migration Confirmation              ║
   ╠════════════════════════════════════════════════╣
   ║  This will create REAL DATA in the system.     ║
   ║                                                ║
   ║  Project:      ORA_TO_S4_MIGRATION             ║
   ║  Object:       Business Partner                ║
   ║  Records:      9,850                           ║
   ║  Estimated:    ~45 minutes                     ║
   ║                                                ║
   ║  Are you sure you want to proceed?             ║
   ║                                                ║
   ║  [✅ Yes, Start Migration]  [❌ Cancel]        ║
   ╚════════════════════════════════════════════════╝
   ```

3. Click **"Yes, Start Migration"**

#### Step 7.3: Monitor Migration Progress

**Live Migration Monitor:**
```
╔════════════════════════════════════════════════╗
║  Migration Running - DO NOT CLOSE              ║
╠════════════════════════════════════════════════╣
║  Project: ORA_TO_S4_MIGRATION                  ║
║  Started: 2025-11-07 22:00:00                  ║
║                                                ║
║  Overall Progress: [██████████████░░░░] 72%    ║
║                                                ║
║  Status Details:                               ║
║  • Processed:      7,100 / 9,850               ║
║  • Successful:     7,055                       ║
║  • Failed:         45                          ║
║  • Warnings:       12                          ║
║                                                ║
║  Current Batch: 71/99                          ║
║  Batch Progress: [████████░░] 80%              ║
║                                                ║
║  Performance:                                  ║
║  • Records/min:    165                         ║
║  • Time elapsed:   43 minutes                  ║
║  • Time remaining: ~17 minutes                 ║
║                                                ║
║  [Pause]  [View Live Errors]  [Export Log]     ║
╚════════════════════════════════════════════════╝
```

**Background Job Information:**
```
Migration runs as background job
Job Name: LTMC_MIGRATE_000000000001
Job ID: 12345678

Monitor via:
Transaction: SM37 (Job Overview)
```

#### Step 7.4: Migration Complete

**Final Results:**
```
╔════════════════════════════════════════════════╗
║  ✅ Migration Complete                         ║
╠════════════════════════════════════════════════╣
║  Project:          ORA_TO_S4_MIGRATION         ║
║  Completed:        2025-11-07 22:47:32         ║
║  Duration:         47 minutes 32 seconds       ║
║                                                ║
║  Results:                                      ║
║  • Total Records:      9,850                   ║
║  • ✅ Successfully Created: 9,805              ║
║  • ❌ Failed:           45                     ║
║  • ⚠️  Warnings:        23                     ║
║                                                ║
║  Success Rate: 99.5% ✅                        ║
║                                                ║
║  Data Created in S/4HANA:                      ║
║  • Business Partners: 9,805                    ║
║  • Addresses: 9,805                            ║
║  • Bank Details: 3,245                         ║
║                                                ║
║  [View Details]  [Download Report]  [Finish]   ║
╚════════════════════════════════════════════════╝
```

---

### Phase 8: Post-Migration Validation

#### Step 8.1: Verify Data in S/4HANA

**Method 1: View Business Partners (SAP GUI)**
```
Transaction: BP (Business Partner Maintenance)

1. Enter BP Number (e.g., 1000001)
2. Verify:
   ✅ General Data tab
   ✅ Address tab
   ✅ Bank Details tab
   ✅ Control tab
```

**Method 2: Query via SQL**
```sql
-- Check total count
SELECT COUNT(*) as BP_COUNT
FROM BUT000;  -- Business Partner master table

-- Sample records
SELECT
    PARTNER as BP_NUMBER,
    NAME_ORG1 as BP_NAME,
    BPKIND as BP_KIND
FROM BUT000
ORDER BY PARTNER
LIMIT 100;
```

**Method 3: Use LTMC Reports**
```
Transaction: LTMC → Reports → Migration Report

Filter:
• Project: ORA_TO_S4_MIGRATION
• Status: Successful

Output: List of all created BP numbers
```

#### Step 8.2: Reconciliation with Source

**Reconciliation Query:**
```sql
-- Compare counts between Oracle and S/4HANA
-- Oracle:
SELECT COUNT(*) as ORACLE_COUNT FROM CUSTOMERS WHERE STATUS = 'ACTIVE';

-- S/4HANA:
SELECT COUNT(*) as HANA_COUNT FROM BUT000
WHERE PARTNER BETWEEN '1000001' AND '1010000';

-- Compare sample data
-- Oracle:
SELECT CUSTOMER_ID, CUSTOMER_NAME, CITY
FROM CUSTOMERS WHERE CUSTOMER_ID = '1000001';

-- S/4HANA:
SELECT PARTNER, NAME_ORG1, CITY1
FROM BUT000 WHERE PARTNER = '1000001';
```

**Automated Reconciliation Script:**
```python
# Python reconciliation script
import cx_Oracle
from pyrfc import Connection

# Connect to Oracle
oracle_conn = cx_Oracle.connect('user/password@oracle')
oracle_cursor = oracle_conn.cursor()

# Connect to S/4HANA via RFC
s4_conn = Connection(
    ashost='s4hana-host',
    sysnr='00',
    client='100',
    user='user',
    passwd='password'
)

# Extract Oracle count
oracle_cursor.execute("SELECT COUNT(*) FROM CUSTOMERS WHERE STATUS='ACTIVE'")
oracle_count = oracle_cursor.fetchone()[0]

# Extract S/4HANA count
result = s4_conn.call('RFC_READ_TABLE',
    QUERY_TABLE='BUT000',
    OPTIONS=[{'TEXT': "PARTNER BETWEEN '1000001' AND '1010000'"}]
)
s4_count = len(result['DATA'])

# Compare
print(f"Oracle Count: {oracle_count}")
print(f"S/4HANA Count: {s4_count}")
print(f"Difference: {oracle_count - s4_count}")

if oracle_count == s4_count:
    print("✅ Reconciliation PASSED")
else:
    print("❌ Reconciliation FAILED - Investigate discrepancies")
```

#### Step 8.3: Handle Failed Records

**Review Failed Records:**
```
Transaction: LTMC → Project → Display Error Records

Filter: Status = Failed
```

**Export Failed Records:**
1. Select failed records
2. Click **"Export to Excel"**
3. Review error messages
4. Decide on remediation:
   - ✅ Fix data and re-migrate
   - ✅ Create manually in system
   - ✅ Accept as exception (document reason)

**Re-migrate Failed Records:**
1. Fix errors in staging table
2. Select failed records only
3. Click **"Restart Migration for Selected Records"**
4. Monitor progress

---

## SAP S/4HANA Migration Object Modeler (LTMOM)

### Overview

**LTMOM** is used to **create custom migration objects** when pre-delivered objects don't meet your needs.

### When to Use LTMOM?

- ❌ Pre-delivered migration object doesn't exist
- ❌ Pre-delivered object missing required fields
- ✅ You have custom Z-tables to migrate
- ✅ You need custom validation logic
- ✅ Complex transformations required

### Step-by-Step: Create Custom Migration Object

#### Step 1: Access LTMOM

```
Transaction Code: LTMOM
```

#### Step 2: Create New Migration Object

1. Click **"Create"**
2. Fill in object details:

   ```
   ┌──────────────────────────────────────────────┐
   │ Create Migration Object                      │
   ├──────────────────────────────────────────────┤
   │ Technical Name:  [ZCUSTOM_OBJECT_IDEN___]    │
   │ Description:     [Custom Sales Data______]   │
   │ Object Category: [⦿ Master Data              │
   │                   ○ Transaction Data         │
   │                                              │
   │ [Continue]                                   │
   └──────────────────────────────────────────────┘
   ```

#### Step 3: Define File Structure

1. Define columns for template file:

   ```
   ┌─────┬────────────────┬──────────┬─────────┬───────────┐
   │ Seq │ Field Name     │ Type     │ Length  │ Mandatory │
   ├─────┼────────────────┼──────────┼─────────┼───────────┤
   │ 010 │ SALES_DOC      │ CHAR     │ 10      │ [✓]       │
   │ 020 │ SALES_ITEM     │ NUMC     │ 6       │ [✓]       │
   │ 030 │ MATERIAL       │ CHAR     │ 18      │ [✓]       │
   │ 040 │ QUANTITY       │ QUAN     │ 13      │ [✓]       │
   │ 050 │ UNIT           │ UNIT     │ 3       │ [✓]       │
   │ 060 │ NET_PRICE      │ CURR     │ 15      │ [ ]       │
   │ 070 │ CURRENCY       │ CUKY     │ 5       │ [ ]       │
   └─────┴────────────────┴──────────┴─────────┴───────────┘
   ```

2. Save file structure

#### Step 4: Define Transfer Structure

Map file fields to S/4HANA table fields:

```
File Field → S/4HANA Table Field

SALES_DOC  → VBAK-VBELN (Sales Document Number)
SALES_ITEM → VBAP-POSNR (Item Number)
MATERIAL   → VBAP-MATNR (Material Number)
QUANTITY   → VBAP-KWMENG (Order Quantity)
UNIT       → VBAP-VRKME (Sales Unit)
NET_PRICE  → VBAP-NETPR (Net Price)
CURRENCY   → VBAP-WAERK (Currency)
```

#### Step 5: Define Validation Rules

Add custom validations:

```abap
* Check material exists
SELECT SINGLE matnr FROM mara
  WHERE matnr = @ls_data-material.
IF sy-subrc <> 0.
  MESSAGE e001(zmig) INTO lv_message.  "Material does not exist
  APPEND lv_message TO et_errors.
ENDIF.

* Check quantity > 0
IF ls_data-quantity <= 0.
  MESSAGE e002(zmig) INTO lv_message.  "Quantity must be positive
  APPEND lv_message TO et_errors.
ENDIF.
```

#### Step 6: Define Migration API

Choose API method for data transfer:

**Options:**
1. **BAPI** (Business API)
   - Example: `BAPI_SALESORDER_CREATEFROMDAT2`
   - Pro: Standard SAP API, well-documented
   - Con: May not support all fields

2. **IDoc** (Intermediate Document)
   - Example: `ORDERS05` (Sales Order IDoc)
   - Pro: Asynchronous processing, handles large volumes
   - Con: More complex error handling

3. **Direct Table Update** (Not Recommended)
   - Direct INSERT into database tables
   - Pro: Fastest
   - Con: Bypasses business logic, integrity issues

**Recommended: Use BAPI**

```abap
* Call BAPI to create sales order
CALL FUNCTION 'BAPI_SALESORDER_CREATEFROMDAT2'
  EXPORTING
    order_header_in  = ls_header
  IMPORTING
    salesdocument    = lv_vbeln
  TABLES
    return           = lt_return
    order_items_in   = lt_items
    order_partners   = lt_partners.

IF lv_vbeln IS NOT INITIAL.
  * Success - commit work
  CALL FUNCTION 'BAPI_TRANSACTION_COMMIT'
    EXPORTING
      wait = 'X'.
ELSE.
  * Failure - collect errors
  LOOP AT lt_return INTO ls_return WHERE type = 'E'.
    APPEND ls_return-message TO et_errors.
  ENDLOOP.
ENDIF.
```

#### Step 7: Test Custom Object

1. Activate migration object
2. Create test project in LTMC
3. Upload sample data (5-10 records)
4. Run validation and simulation
5. Fix any issues
6. Document for production use

---

## Legacy System Migration Workbench (LSMW)

### Overview

**LSMW** is the **legacy tool** for data migration, predating Migration Cockpit. Still used for:
- Complex transformations
- Batch Input (BDC) recordings
- Custom IDocs

### When to Use LSMW?

| Scenario | Use LSMW? | Reason |
|----------|-----------|--------|
| Standard business objects (BP, Material) | ❌ No | Use LTMC instead (easier) |
| Custom Z-tables | ✅ Yes | LSMW supports any table |
| Complex field mappings | ✅ Yes | LSMW has powerful transformation rules |
| Legacy migration from SAP R/3 | ✅ Yes | LSMW designed for this |
| Recording-based migration | ✅ Yes | LSMW supports BDC recordings |

### LSMW Step-by-Step

#### Step 1: Access LSMW

```
Transaction Code: LSMW
```

#### Step 2: Create Project

```
┌──────────────────────────────────────────────┐
│ Create LSMW Project                          │
├──────────────────────────────────────────────┤
│ Project:       [ZBUSINESS_PARTNER_MIG___]    │
│ Subproject:    [BP_FROM_ORACLE___________]   │
│ Object:        [BUSINESS_PARTNER_________]   │
│                                              │
│ [Create]                                     │
└──────────────────────────────────────────────┘
```

#### Step 3: Choose Transfer Method

**14 Steps in LSMW:**

```
LSMW Workflow:
├─ Step 1:  Maintain Object Attributes
├─ Step 2:  Maintain Source Structures
├─ Step 3:  Maintain Source Fields
├─ Step 4:  Maintain Structure Relations
├─ Step 5:  Maintain Field Mapping and Conversion Rules
├─ Step 6:  Maintain Fixed Values, Translations, User-Defined Routines
├─ Step 7:  Specify Files
├─ Step 8:  Assign Files
├─ Step 9:  Read Data
├─ Step 10: Display Read Data
├─ Step 11: Convert Data
├─ Step 12: Display Converted Data
├─ Step 13: Start Direct Input Program (or IDoc/BAPI/BDC)
└─ Step 14: Display Statistics
```

**Choose Method:**
- **Standard Batch/Direct Input**: Fastest, for SAP standard programs
- **Batch Input Recording (BDC)**: Record transaction, replay with data
- **LSMW-BAPI**: Call BAPI functions
- **IDoc**: Generate IDoc messages

#### Step 4: Define Source Structure

```
Source Structure: ZBPSOURCE
├─ BP_HEADER (Segment)
│  ├─ BP_NUMBER (Field, CHAR 10)
│  ├─ BP_NAME (Field, CHAR 40)
│  └─ BP_CATEGORY (Field, CHAR 1)
└─ BP_ADDRESS (Segment)
   ├─ STREET (Field, CHAR 60)
   ├─ CITY (Field, CHAR 40)
   └─ POSTAL_CODE (Field, CHAR 10)
```

#### Step 5: Upload Source File

```
File Format: CSV
File Name: BP_DATA.csv
Delimiter: Comma (,)

Sample Data:
BP_NUMBER,BP_NAME,BP_CATEGORY,STREET,CITY,POSTAL_CODE
1000001,ACME Corporation,1,123 Main St,New York,10001
1000002,TechCo Inc,1,456 Tech Ave,San Francisco,94102
```

#### Step 6: Field Mapping

```
Source Field         Conversion Rule       Target Field
─────────────────    ─────────────────    ──────────────────────
BP_NUMBER            →                    BUT000-PARTNER
BP_NAME              →                    BUT000-NAME_ORG1
BP_CATEGORY          → RULE_001           BUT000-BPKIND
STREET               →                    ADRC-STREET
CITY                 →                    ADRC-CITY1
POSTAL_CODE          →                    ADRC-POST_CODE1

Conversion Rule RULE_001:
IF BP_CATEGORY = '1' THEN BPKIND = '0002'.  "Organization
IF BP_CATEGORY = '2' THEN BPKIND = '0001'.  "Person
```

#### Step 7: Execute Migration

1. Read Data (Step 9)
2. Display Read Data (Step 10) - verify loaded correctly
3. Convert Data (Step 11)
4. Display Converted Data (Step 12) - verify conversions
5. Start Direct Input (Step 13) - actual migration
6. Display Statistics (Step 14) - review results

**Statistics Output:**
```
╔════════════════════════════════════════════╗
║  LSMW Migration Statistics                 ║
╠════════════════════════════════════════════╣
║  Records read:       10,000                ║
║  Records converted:  10,000                ║
║  Records processed:  10,000                ║
║  Successfully posted: 9,987                ║
║  Errors:              13                   ║
║                                            ║
║  Success Rate: 99.87%                      ║
╚════════════════════════════════════════════╝
```

---

## Direct Transfer from SAP ECC

### Overview

For **SAP ECC to SAP S/4HANA** migration, use SAP's standard system conversion tools.

### Migration Approaches

#### Approach 1: Greenfield (New Implementation)

**Process:**
1. Install new S/4HANA system
2. Configure from scratch
3. Migrate data using LTMC/LSMW
4. Cutover to new system

**Pros:**
- ✅ Clean start, no legacy issues
- ✅ Simplify processes
- ✅ Modern architecture

**Cons:**
- ❌ Longer implementation (12-24 months)
- ❌ More expensive
- ❌ Higher risk

#### Approach 2: Brownfield (System Conversion)

**Process:**
1. Upgrade ECC to latest version (EHP8)
2. Run SAP Readiness Check
3. Execute Database Migration Option (DMO) with System Conversion
4. Convert to S/4HANA

**Pros:**
- ✅ Faster (3-6 months)
- ✅ All data/config preserved
- ✅ Lower risk

**Cons:**
- ❌ Carries forward legacy issues
- ❌ May not simplify processes

### System Conversion Step-by-Step

#### Step 1: Pre-Conversion Checks

**Run SAP Readiness Check:**
```
Transaction: /SDF/RC_START_CHECK

The tool analyzes:
✅ Simplification items (incompatible programs/tables)
✅ Custom code compatibility (ABAP Test Cockpit)
✅ Add-on compatibility
✅ Sizing requirements
✅ Business function activation
```

#### Step 2: Execute DMO with System Conversion

**DMO (Database Migration Option)** combines:
- Database migration (e.g., Oracle → SAP HANA)
- Release upgrade (ECC 6.0 → S/4HANA 2023)
- Unicode conversion (if needed)

**Tool: Software Update Manager (SUM) with DMO**

```
Phases:
├─ Phase 1: Extraction (Oracle)
│  └─ Export data from Oracle using R3load
├─ Phase 2: Configuration
│  └─ Configure target HANA database
├─ Phase 3: Import (HANA)
│  └─ Import data to HANA database
├─ Phase 4: Upgrade
│  └─ Upgrade to S/4HANA release
└─ Phase 5: Post-Processing
   └─ Activate business functions, run reports
```

**Typical Timeline:**
- Small system (<100 GB): 12-24 hours
- Medium system (100 GB - 1 TB): 2-5 days
- Large system (>1 TB): 5-14 days

#### Step 3: Post-Conversion Activities

```
Mandatory Post-Conversion Steps:
├─ Run IMG Activity: S/4HANA Conversion (SPRO)
├─ Execute Simplification Item Checks
├─ Activate New Fiori Apps
├─ Test Critical Business Processes
└─ Perform User Acceptance Testing (UAT)
```

---

## Rapid Data Migration (RDM)

### Overview

**RDM** is SAP's cloud-based migration tool for **SAP S/4HANA Cloud** edition.

### Key Differences from LTMC

| Feature | LTMC (On-Premise) | RDM (Cloud) |
|---------|-------------------|-------------|
| Deployment | SAP GUI / Fiori | Web-based |
| Infrastructure | Customer-managed | SAP-managed |
| Migration Objects | 100+ objects | 50+ objects (cloud-relevant) |
| Customization | Highly customizable | Pre-configured |
| Data Volume | Unlimited | Limited per tenant |

### RDM Migration Process

#### Step 1: Access RDM

```
URL: https://<your-tenant>.s4hana.ondemand.com/migrationcockpit
```

#### Step 2: Download Templates

1. Select migration object (e.g., "Business Partner")
2. Download Excel template
3. Template includes:
   - Required fields (marked)
   - Data validations
   - Sample data

#### Step 3: Populate Template

- Export data from source system (Oracle, ECC, etc.)
- Fill template with middleware (Python script)
- Validate locally before upload

#### Step 4: Upload to RDM

1. Click "Upload File"
2. System validates file format
3. Data staged in cloud

#### Step 5: Validate & Migrate

1. Run validation
2. Review errors
3. Execute migration
4. Monitor via dashboard

**Cloud Advantage**: SAP manages infrastructure, automatic scaling

---

## SAP Cloud Platform Integration

### Overview

For real-time data integration between Oracle and S/4HANA Cloud, use **SAP Cloud Platform Integration (CPI)**.

### Architecture

```
┌─────────────┐
│   Oracle    │
│   Database  │
└──────┬──────┘
       │ JDBC Adapter
       ↓
┌─────────────────────────────────┐
│ SAP Cloud Platform Integration  │
│                                 │
│  ┌──────────────────────────┐  │
│  │  Integration Flow        │  │
│  │  • Data Mapping          │  │
│  │  • Transformation        │  │
│  │  • Error Handling        │  │
│  └──────────────────────────┘  │
└──────────────┬──────────────────┘
               │ OData API
               ↓
       ┌───────────────┐
       │  S/4HANA      │
       │  Cloud        │
       └───────────────┘
```

### Use Case: Real-Time Customer Sync

**Scenario**: When new customer created in Oracle, automatically create in S/4HANA

**CPI Integration Flow:**
1. **Trigger**: Oracle database change (CDC)
2. **Read**: Extract customer data via JDBC
3. **Transform**: Map Oracle fields → S/4HANA OData
4. **Validate**: Check required fields
5. **Load**: POST to S/4HANA OData API
6. **Confirm**: Log success/failure

---

## Tool Comparison Matrix

### Comprehensive Comparison

| Criteria | LTMC | LTMOM | LSMW | Data Services | RDM | System Conversion |
|----------|------|-------|------|---------------|-----|-------------------|
| **Ease of Use** | ★★★★★ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ | ★★☆☆☆ |
| **Customization** | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ |
| **Performance** | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★★★ |
| **Data Volume** | Large | Large | Medium | Very Large | Medium | Very Large |
| **Learning Curve** | Low | Medium | High | High | Low | Very High |
| **SAP Recommendation** | ✅ Primary | ✅ Custom objects | ⚠️ Legacy | ✅ Complex ETL | ✅ Cloud | ✅ ECC→S/4 |
| **Cost** | Included | Included | Included | License | Included | Project |
| **Best For** | Standard objects | Z-tables | Legacy | Multi-source ETL | Cloud | ECC conversion |

### Decision Tree

```
Start: Need to migrate data to S/4HANA
│
├─ From SAP ECC?
│  └─ Yes → Use System Conversion (DMO)
│
├─ To S/4HANA Cloud?
│  └─ Yes → Use RDM (Rapid Data Migration)
│
├─ Standard business object (BP, Material, etc.)?
│  └─ Yes → Use LTMC (Migration Cockpit) ✅ RECOMMENDED
│
├─ Custom Z-table or complex transformation?
│  ├─ Simple → Use LTMOM + LTMC
│  └─ Complex → Use LSMW or SAP Data Services
│
├─ Very large data volume (TB+)?
│  └─ Yes → Use SAP Data Services
│
└─ Real-time integration?
   └─ Yes → Use SAP Cloud Platform Integration (CPI)
```

---

## Best Practices

### 1. Always Start with LTMC

- ✅ Easiest tool to use
- ✅ Best performance for standard objects
- ✅ SAP's current recommended approach
- ✅ Future-proof (actively developed)

### 2. Validate Early and Often

- Run validation after every data change
- Don't wait until the end to validate
- Fix errors incrementally

### 3. Use Simulation Extensively

- Never skip simulation
- Simulation catches 80% of issues before production
- Run simulation multiple times if needed

### 4. Batch Your Data

- Don't migrate all data at once
- Use waves: Master Data → Historical → Current
- Allows for learning and adjustment

### 5. Automate Where Possible

- Use Python/middleware to:
  - Extract from source
  - Populate templates
  - Auto-correct common errors
- Saves time on large migrations

### 6. Document Everything

- Field mappings
- Transformation rules
- Error resolutions
- Performance metrics

### 7. Test in Sandbox First

- Always test in dev/QA system first
- Validate with business users
- Performance test with production volumes

### 8. Plan for Rollback

- Keep source system available (read-only)
- Take backups before migration
- Have rollback procedure documented

### 9. Monitor Performance

- Track records/minute
- Identify bottlenecks (network, CPU, API limits)
- Optimize batch sizes

### 10. Provide Hypercare Support

- First 2 weeks after go-live are critical
- Have support team available 24/7
- Quick resolution of data issues

---

## Common Issues and Resolutions

### Issue 1: "Migration object not found"

**Cause**: Migration object not activated

**Solution**:
```
Transaction: LTMC → Activate Migration Objects
Select object → Activate
```

### Issue 2: "Authorization missing"

**Cause**: User lacks required authorization

**Solution**:
```
Required roles:
• SAP_LTMC_DESIGNER (create projects)
• SAP_LTMC_EXECUTOR (run migrations)
• Plus: Business object auth (e.g., S_BUPA_GRP for BP)
```

### Issue 3: "Performance is slow"

**Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| Large batch size | Reduce batch size from 1000 → 100 |
| Network latency | Deploy middleware closer to S/4HANA |
| Database locks | Run migration in off-hours |
| API rate limits | Add delays between API calls |

### Issue 4: "Data not appearing in S/4HANA"

**Troubleshooting steps**:
```
1. Check migration log for errors
2. Verify BAPI returned success message
3. Check if data in draft mode (needs activation)
4. Refresh cache (Transaction: /nex)
5. Check authorization to view data
```

### Issue 5: "Duplicate key error"

**Cause**: Record already exists in S/4HANA

**Solutions**:
```
Option 1: Change to "Update" mode instead of "Create"
Option 2: Delete existing records (if test data)
Option 3: Use different number range
```

---

## Summary

### Key Takeaways

1. **LTMC is the primary tool** - Use for 80% of migrations
2. **LTMOM for customization** - When LTMC doesn't fit
3. **LSMW for legacy** - Only for complex scenarios
4. **RDM for cloud** - S/4HANA Cloud migrations
5. **System Conversion for ECC** - Brownfield approach

### Migration Checklist

**Pre-Migration:**
- [ ] Tool selected based on requirements
- [ ] Migration object activated
- [ ] Templates downloaded and populated
- [ ] Source data extracted and validated
- [ ] Test migration completed in sandbox
- [ ] Performance benchmarks established

**During Migration:**
- [ ] Validation passed (>99%)
- [ ] Simulation passed (>99%)
- [ ] Backup taken
- [ ] Migration executed
- [ ] Progress monitored
- [ ] Errors handled in real-time

**Post-Migration:**
- [ ] Data verified in S/4HANA
- [ ] Reconciliation with source completed
- [ ] Failed records handled
- [ ] Performance metrics documented
- [ ] User acceptance testing passed
- [ ] Go-live approval obtained

---

## Additional Resources

### SAP Documentation

- [Migration Cockpit Overview](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/4f8e247b05b84a60ad1e8c6f575099ab)
- [Migration Object Modeler](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/9a0ea59e07554b36a41a72dbdc2f05e1)
- [LSMW Documentation](https://help.sap.com/docs/ABAP_PLATFORM/8e534a7e1db94f269bf5f9c0c3b18e88)
- [System Conversion Guide](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/c9e38929d93c434ab2ea02e20aec07bf)

### SAP Notes

- 2267138 - Migration Cockpit FAQ
- 2360557 - Migration Cockpit Performance
- 2308516 - Available Migration Objects
- 2769565 - Custom Migration Objects

### Training

- **SAP Learning Hub**: S/4HANA Migration courses
- **openSAP**: Free "Move to SAP S/4HANA" courses
- **SAP Community**: Migration forums and blogs

---

**Document Version**: 1.0.0
**Last Updated**: November 7, 2025
**Status**: Production Ready ✅

---

### Navigation

- **← Back to [Master Migration Guide](ORACLE_TO_S4HANA_MIGRATION_GUIDE.md)** - Oracle to S/4HANA migration overview
- **→ View [Project README](README.md)** - Middleware technical implementation
- **→ View [Migration Results](outputs/MIGRATION_RESULTS.md)** - Real-world migration evidence
