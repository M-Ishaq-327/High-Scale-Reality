import os
import uuid
import random
import json
from datetime import datetime
from faker import Faker

# Initialize Faker for realistic data generation
fake = Faker()

# Define where we want to save our messy data
OUTPUT_DIR = "data/1_raw_json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuration for our data flood
TOTAL_BATCHES = 500         # How many files we will create
RECORDS_PER_BATCH = 10000   # How many transactions per file (Total: 5 Million rows)

CATEGORIES = ["Electronics", "Clothing", "Home & Kitchen", "Beauty", "Sports"]
STATUSES = ["success", "success", "success", "failed"] # 75% success rate

print(f" Starting ... Generating {TOTAL_BATCHES} files ({TOTAL_BATCHES * RECORDS_PER_BATCH} total records).")

# Start the loop to create our chaotic "Before" state
for batch_num in range(1, TOTAL_BATCHES + 1):
    batch_data = []
    
    for _ in range(RECORDS_PER_BATCH):
        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "user_id": f"user_{random.randint(10000, 99999)}",
            "product_id": f"prod_{random.randint(100, 999)}",
            "category": random.choice(CATEGORIES),
            "price": round(random.uniform(10.0, 500.0), 2),
            "payment_status": random.choice(STATUSES)
        }
        batch_data.append(transaction)
    
    # Save this specific batch as an individual, uncompressed JSON file
    file_path = os.path.join(OUTPUT_DIR, f"transaction_batch_{batch_num}.json")
    with open(file_path, "w") as f:
        json.dump(batch_data, f)
        
    # Print progress every 50 batches so you know it's working
    if batch_num % 50 == 0:
        print(f"Created {batch_num}/{TOTAL_BATCHES} files...")

print("Phase 1 Data Generation Complete! The messy library is full.")