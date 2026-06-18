import os
import time
import duckdb

print("  Starting Phase 2: Compacting and Converting Data to Parquet...")

RAW_DATA_PATH = "data/1_raw_json/*.json"
OPTIMIZED_DATA_PATH = "data/2_optimized_parquet"

# Create the optimized directory if it doesn't exist
os.makedirs(OPTIMIZED_DATA_PATH, exist_ok=True)

# Start a timer to see how long the optimization process takes
start_time = time.time()

# This SQL command reads ALL the JSONs, compacts them, converts them to columnar, 
# and physically partitions them into separate folders based on the 'category' column.
ctx = duckdb.connect()
ctx.execute(f"PRAGMA threads=4;") # Tells DuckDB to use multi-threading

print(" Reading raw files, compressing, and partitioning by Category...")
ctx.execute(f"""
    COPY (SELECT * FROM '{RAW_DATA_PATH}') 
    TO '{OPTIMIZED_DATA_PATH}' 
    (FORMAT 'PARQUET', PARTITION_BY 'category', OVERWRITE_OR_IGNORE 1);
""")

end_time = time.time()
print(f" Optimization Complete in {round(end_time - start_time, 2)} seconds!")