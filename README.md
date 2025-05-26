# 🏋️ Gym Management Data Analysis

This project provides a data pipeline and analysis for a gym management system, including database models, data population from JSON files, and analytics on staff performance and revenue.

---

## 📁 Project Structure

- `database.py` — SQLAlchemy models and in-memory SQLite setup.
- `database_populator.py` — Populates the database from JSON files and runs analytics queries.
- `server.py` — Flask server (obfuscated).
- `__main__.py` — Starts the server and fetches lead data.
- `json_files/` — Contains data files for clubs, leads, members, staff, and subscriptions.
- `requirements.txt` — Python dependencies.

## Setup

1. **Install Python 3.9+**  
   Make sure you have Python installed.

2. **Install dependencies**  
   Run:
   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare Data**  
   Ensure all JSON files are present in the `json_files/` directory.

## How to Run

### 1. Start the Flask Server

The server is started automatically by running `__main__.py`.  
It will also fetch lead data from the `/lead` endpoint and save it to `lead_data.json`.

```sh
python __main__.py
```

### 2. Populate the Database and Run Analytics

Run the database populator script to load data and print analytics:

```sh
python database_populator.py
```

## Interpreting Results

When you run `database_populator.py`, you will see output like:

- **Conversion Rate per Staff (last 3 months only):**  
  Shows the percentage of leads converted by each staff member in the last 3 months.

- **Revenue Share per Staff (% of total):**  
  Shows each staff member's share of total revenue from subscriptions.

- **Avg Revenue per Conversion (% of top staff):**  
  Compares the average revenue per conversion for each staff member as a percentage of the top performer.

Use these metrics to evaluate staff performance and revenue contribution.

---

**Note:**  
- The database is in-memory and resets on each run.
- You can modify the JSON files in `json_files/` to test with different data.
