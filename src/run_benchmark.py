import time
import os
import duckdb

def get_folder_size_mb(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)

raw_folder = "data/1_raw_json"
optimized_folder = "data/2_optimized_parquet"

raw_size = get_folder_size_mb(raw_folder)
optimized_size = get_folder_size_mb(optimized_folder)

# 1. RUN THE SLOW BENCHMARK (JSON)
query_json = """
    SELECT category, ROUND(SUM(price), 2) as total_revenue, COUNT(*) as total_transactions
    FROM 'data/1_raw_json/*.json'
    GROUP BY category ORDER BY total_revenue DESC;
"""
start = time.time()
duckdb.execute(query_json).fetchall()
time_json = round(time.time() - start, 4)

# 2. RUN THE FAST BENCHMARK (PARQUET)
# Notice how we query the whole directory structure natively!
query_parquet = """
    SELECT category, ROUND(SUM(price), 2) as total_revenue, COUNT(*) as total_transactions
    FROM 'data/2_optimized_parquet/**/*.parquet'
    GROUP BY category ORDER BY total_revenue DESC;
"""
start = time.time()
duckdb.execute(query_parquet).fetchall()
time_parquet = round(time.time() - start, 4)

# 3. PRINT THE COMPARISON REPORT
print("\n --- THE ULTIMATE FAANG RECRUITER METRICS REPORT --- ")
print("-" * 55)
print(f" METRIC               | BEFORE (JSON) | AFTER (PARQUET)")
print("-" * 55)
print(f" Storage Footprint    | {raw_size:<13} MB | {optimized_size:<12} MB")
print(f"  Query Execution Time | {time_json:<13} sec| {time_parquet:<12} sec")
print("-" * 55)

space_saved = round(((raw_size - optimized_size) / raw_size) * 100, 2)
speedup = round((time_json / time_parquet), 1) if time_parquet > 0 else 0
print(f" Data Compression: Saved {space_saved}% disk space!")
print(f" Performance Boost: Query runs {speedup}x FASTER!")
print("-" * 55)