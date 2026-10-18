# socelp
i am doing this project aiming to make the documentation process way faster than usual. usually there will be cases where we may forget the time we receved the malicious alert and socelp's db integration and threat hunting intelligence acceelerates its process.
# 🛡️ Splunk Alert Evidence Capture & SQL Logging Pipeline

> An automated SecOps pipeline that receives Splunk security webhooks, automatically captures headless browser screenshots of flagged URLs for forensic evidence, and logs structured metadata directly into an SQL database.

---

## 📌 Features

- **⚡ Real-Time Ingestion:** Listens for incoming Splunk alerts via custom Webhook endpoints.
- **📸 Forensic Evidence Capture:** Uses Playwright to automatically take a screenshot of malicious/suspicious URLs upon alert arrival.
- **⏱️ Precise Timestamps:** Tracks exact arrival times down to the second.
- **🗄️ Structured Logging:** Categorizes severity (`High`, `Medium`, `Low`) and stores metadata in PostgreSQL with optimized database indexes.

---

## 📐 Architecture Flow

```text
[ Splunk SIEM ]
       │
       │  (HTTP POST Webhook)
       ▼
[ Flask REST API ]
       │
       ├────► 📸 Playwright (Captures URL Screenshot)
       │
       └────► 🗄️ PostgreSQL (Stores Metadata & Evidence Path)


🛠️ Tech Stack
Component      Technology
SIEM / Trigger    Splunk Enterprise
Backend API       Python 3, Flask
Automation & Capture    Playwright (Headless Chromium)
Database    PostgreSQL
Testing     cURL / Postman

├── app.py                 # Core Flask REST API & evidence collection logic
├── schema.sql             # SQL database table & index creation script
├── sample_payload.json    # Example Splunk payload for local testing
└── README.md              # Documentation
