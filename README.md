# Project High-Scale-Reality: Benchmarking Data Lake Optimization under Synthetic Workloads

## 📌 Executive Summary
During peak traffic events like Black Friday, e-commerce platforms experience massive surges in streaming clickstream and transactional data. When data is ingested naively as fragmented, uncompressed files, downstream analytical queries become slow, CPU-heavy, and financially expensive. 

**Project High-Scale-Reality** bridges this gap by creating a local benchmarking environment. I simulated a high-volume data bottleneck by generating **5,000,000 rows** of transaction data split into hundreds of individual, raw JSON files. I then engineered a storage optimization layer that automatically compacts and converts this unstructured data into a high-performance, partitioned columnar format using **Apache Parquet** layouts.

## 📊 The Core Metrics (X → Y)
By shifting from unorganized, row-oriented text storage to an optimized columnar data lake structure, the system achieved massive efficiency gains:

| Metric | Before (Naively Ingested JSON) | After (Optimized Parquet) | Total Impact |
| :--- | :--- | :--- | :--- |
| **Storage Footprint** | 1.04 GB (~1,065 MB) | [162.44] MB | **Saved [84.82]% Disk Space** |
| **Query Execution Time** | [5.96] seconds | [0.25] seconds | **Runs [23.7]x FASTER (Cold Read)** |

## 🏗️ Architecture & Data Pipeline
The project follows a structured three-phase pipeline executed entirely in a local environment to isolate hardware resource utilization:

1. **Ingestion & Chaos Simulation (Phase 1):** A custom Python generator utilizing the `Faker` library continuously outputs batches of fake customer transactions directly to disk, creating a "small file problem" bottleneck.
2. **Storage Optimization Layer (Phase 2):** Utilizing `DuckDB`'s vectorized query engine, the pipeline processes the fragmented JSON files, executes multi-threaded file compaction, and rewrites the data into highly compressed `.parquet` structures.
3. **Partitioning Strategy:** Data is physically partitioned on disk by product `category` folders, allowing query engines to prune irrelevant directories dynamically.

## 🧠 Key Engineering Takeaways
* **Columnar vs. Row Storage:** Moving to Parquet allowed the analytical queries to isolate and scan *only* the specific columns required for the aggregations (like `price`), skipping irrelevant text data entirely.
* **Cold vs. Warm Reads:** Benchmarking revealed a massive jump in subsequent query runs (up to 90x faster). This provided deep practical insights into how modern operating systems handle file descriptor caching in RAM to eliminate disk I/O bottlenecks.

## 🛠️ Tech Stack & Tools
* **Language:** Python
* **Analytical Engine:** DuckDB (Vectorized SQL Execution)
* **Data Synthesis:** Faker, UUID
