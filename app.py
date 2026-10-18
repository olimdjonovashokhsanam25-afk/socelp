from datetime import datetime
import os
from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
import psycopg2

app = Flask(__name__)

# Database Configuration (Update with your local credentials)
DB_CONFIG = {
    "dbname": "your_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,
}


def take_screenshot(url, save_dir="static/screenshots"):
  """Captures a headless browser screenshot of the suspicious URL."""
  os.makedirs(save_dir, exist_ok=True)
  filename = f"screenshot_{int(datetime.now().timestamp())}.png"
  filepath = os.path.join(save_dir, filename)

  try:
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()
      page.goto(url, timeout=10000)
      page.screenshot(path=filepath)
      browser.close()
    return filepath
  except Exception as e:
    print(f"[-] Screenshot capture failed: {e}")
    return "error_capture.png"


@app.route("/splunk-webhook", methods=["POST"])
def splunk_webhook():
  """Receives Splunk webhook alert, captures a screenshot, and saves to SQL."""
  data = request.json or {}

  # Parse fields sent from Splunk's JSON payload
  result = data.get("result", {})
  alert_name = result.get("name", data.get("search_name", "Unknown Alert"))
  severity = result.get("severity", "Medium")
  url = result.get("url", "http://example.com")
  arrival_time = datetime.now()

  print(f"[+] Alert Received: {alert_name} | Severity: {severity}")

  # 1. Capture visual evidence
  screenshot_path = take_screenshot(url)

  # 2. Save metadata and evidence path to PostgreSQL
  try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO alert_logs (alert_name, severity, target_url, screenshot_path, arrival_time) 
               VALUES (%s, %s, %s, %s, %s)""",
        (alert_name, severity, url, screenshot_path, arrival_time),
    )
    conn.commit()
    cur.close()
    conn.close()
    print("[+] Alert successfully logged to database.")
  except Exception as db_error:
    print(f"[-] Database insertion error: {db_error}")
    return jsonify({"status": "error", "message": str(db_error)}), 500

  return (
      jsonify({
          "status": "success",
          "message": "Alert processed, screenshot captured, and logged to SQL.",
      }),
      200,
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)mmm
