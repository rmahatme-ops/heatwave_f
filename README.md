# heatwave_f
# 🌡️ Heatwave Watch

### Climate Intelligence for Heatwave Monitoring and Early Warning

## 1. Project Overview

Heatwave Watch is a Python-based web application developed using Streamlit. It analyzes historical temperature data and demonstrates different Data Structures and Algorithms (DSA) concepts.

The application helps users explore temperature records, identify high-temperature regions, and understand how data structures make data storage and searching more efficient.

## 2. Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## 3. Data Structures Implemented

1. **Linked List:** Stores recently viewed records.
2. **Stack:** Maintains recent user actions.
3. **Queue:** Processes heatwave alerts using FIFO.
4. **AVL Tree:** Supports efficient timestamp-based searching.
5. **Hash Table / Dictionary:** Groups records by region and season.
6. **Set:** Stores unique regions and seasons.

## 4. Algorithms Implemented

### Searching
- Linear Search
- Binary Search

### Sorting
- Bubble Sort
- Insertion Sort
- Counting Sort

## 5. Application Modules

- **Dashboard:** Displays an overview of temperature data.
- **Explore Records:** Allows users to explore and search records.
- **DSA Laboratory:** Demonstrates data structures and algorithms.
- **Alerts and Activity:** Displays alerts and recent actions.
- **About Project:** Provides project information.

## 6. Dataset

The application uses `heatwave_data.csv`.

The dataset contains the following columns:

- Region
- Date
- Latitude
- Longitude
- Tmax (Maximum Temperature)

## 7. Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
