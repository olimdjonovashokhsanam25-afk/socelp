-- Run this in your PostgreSQL terminal or GUI (e.g., pgAdmin / DBeaver)
CREATE TABLE IF NOT EXISTS alert_logs (
    id SERIAL PRIMARY KEY,
    alert_name VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL, -- e.g., 'High', 'Medium', 'Low'
    target_url TEXT NOT NULL,
    screenshot_path VARCHAR(255),  -- Filepath to saved evidence
    arrival_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning-fast SOC dashboard querying
CREATE INDEX idx_alert_severity ON alert_logs(severity);
CREATE INDEX idx_alert_arrival_time ON alert_logs(arrival_time);
