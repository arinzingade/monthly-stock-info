

# Monthly Stock Data Processing Pipeline

## Overview

This project provides a **Pandas-based data pipeline** that processes daily stock price data and produces **monthly aggregated OHLC data** along with **technical indicators** (SMA & EMA).
The pipeline reads a single CSV containing multiple stock symbols and outputs **one CSV file per ticker**, each representing **24 months** of data.

The implementation is **fully vectorized**, modular, and avoids any third-party technical analysis libraries.

---

## Features

* Converts **daily stock data to monthly frequency**
* Correct **OHLC aggregation logic**
* Calculates **Simple Moving Averages (SMA 10, SMA 20)**
* Calculates **Exponential Moving Averages (EMA 10, EMA 20)**
* Outputs **one CSV per stock symbol**
* Ensures **exactly 24 monthly records per ticker**

---

## Input Data Schema

The input CSV must contain the following columns:

```text
date, volume, open, high, low, close, adjclose, ticker
```

### Supported Tickers

```
AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA
```

---

## Output Specification

* **Frequency:** Monthly
* **Rows per file:** Exactly 24 (2 years)
* **File naming convention:**

  ```
  result_<TICKER>.csv
  ```
* **Generated Columns:**

  * date
  * open
  * high
  * low
  * close
  * volume
  * SMA_10
  * SMA_20
  * EMA_10
  * EMA_20

---

## Monthly Aggregation Logic

| Field  | Calculation                    |
| ------ | ------------------------------ |
| Open   | First trading day of the month |
| High   | Maximum price in the month     |
| Low    | Minimum price in the month     |
| Close  | Last trading day of the month  |
| Volume | Sum of monthly volume          |

> **Note:** Open and Close are *not averages* — they represent exact price snapshots.

---

## Project Structure

```text
data_pipeline.py
README.md
input/
  └── stock_data.csv
output/
  └── result_AAPL.csv
  └── result_AMD.csv
  └── ...
```

---

## Code Architecture

The pipeline is encapsulated in a single class:

### `DataPipeline`

#### Key Methods

| Method               | Description                         |
| -------------------- | ----------------------------------- |
| `load_data()`        | Reads CSV, parses dates, sorts data |
| `resample_monthly()` | Converts daily data to monthly OHLC |
| `add_indicators()`   | Adds SMA & EMA columns              |
| `write_per_ticker()` | Writes one CSV per ticker           |
| `process_pipeline()` | Orchestrates the full workflow      |

This modular design makes the code easy to test, extend, and maintain.

---  

## Usage

```python
from data_pipeline import DataPipeline

pipeline = DataPipeline()
pipeline.process_pipeline(
    input_csv="input_files/input.csv",
    output_dir="output_files"
)
```

---

## Validation Rules

* Each ticker **must have exactly 24 monthly records**
* The pipeline raises an error if this condition is violated
* Ensures data completeness and correctness

---

## Technical Constraints

* **Language:** Python
* **Library:** Pandas only
* **No third-party TA libraries**
* **Vectorized operations only**
* **No row-wise loops**

---

## Why This Approach?

* ✔ Accurate financial aggregation
* ✔ Industry-standard indicator formulas
* ✔ Efficient Pandas-native operations
* ✔ Scalable and production-ready
* ✔ Clear separation of concerns

---

## Future Enhancements (Optional)

* Add unit tests for indicator validation
* Support additional indicators
* Add CLI or configuration-based execution
* Handle missing months gracefully

---

## Author

**Arin Zingade**

---
