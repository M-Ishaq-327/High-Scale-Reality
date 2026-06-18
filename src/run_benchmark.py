import time
import psutil
import os
import duckdb

def get_folder_size_mb(folder_path):
    """Calculates total size of the folder in Megabytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)

print("🔍 Starting Phase 1 Baseline Benchmark...")

# 1. Measure the Storage Footprint
raw_folder = "data/1_raw_json"
folder_size = get_folder_size_mb(raw_folder)
print(f" Total files on disk: {len(os.listdir(raw_folder))} files")
print(f" Total raw data size: {folder_size} MB")

# 2. Prepare the Heavy Analytical SQL Query
# This query calculates total sales and total successful transactions per product category
query = """
    SELECT 
        category,
        ROUND(SUM(price), 2) as total_revenue,
        COUNT(*) as total_transactions,
        COUNT(CASE WHEN payment_status = 'success' THEN 1 END) as successful_transactions
    FROM 'data/1_raw_json/*.json'
    GROUP BY category
    ORDER BY total_revenue DESC;
"""

print("\n🏋️ Running heavy analytical query over thousands of unorganized JSONs...")

# Record the exact start time
start_time = time.time()

# Execute the query using DuckDB
result = duckdb.execute(query).fetchall()

# Record the exact end time
end_time = time.time()
execution_time = round(end_time - start_time, 4)

# Print the results
print("\n --- QUERY RESULTS ---")
for row in result:
    print(f"Category: {row[0]:<18} | Revenue: ${row[1]:<12} | Total Tx: {row[2]:<8} | Success Tx: {row[3]}")

print("------------------------")
print(f"\n  BASELINE METRIC (X): Query Execution Time = {execution_time} seconds")