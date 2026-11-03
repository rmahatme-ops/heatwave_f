# heatwave_f

# Heatwave Intelligence System

A Python-based web application developed using **Streamlit** to monitor regional temperature records and demonstrate the use of Data Structures and Algorithms (DSA).

The application allows users to upload temperature data, view temperature summaries, identify heatwave risk categories, and explore different data structures and algorithms through interactive demonstrations.

## 1. Project Objectives

- Monitor temperature records across different regions.
- Display temperature information through tables and visualizations.
- Classify temperature readings into different risk categories.
- Demonstrate the practical application of Data Structures and Algorithms.
- Provide an interactive and easy-to-use dashboard.

## 2. Technologies Used

- **Python** – Main programming language.
- **Streamlit** – Web application framework.
- **Pandas** – Data handling and processing.
- **Heapq** – Priority queue implementation.
- **Collections (deque)** – Queue-related operations.

## 3. Features

### Temperature Dashboard
- Upload temperature records using a CSV file.
- View regional temperature data.
- Display temperature summaries.
- Classify readings as Normal, Warning, or Severe.
- View heatwave-related alerts.

### Data Structures Demonstration
- Singly Linked List
- Doubly Linked List concept
- Circular Linked List concept
- Stack
- Queue
- Circular Queue
- Priority Queue
- Deque
- Binary Search Tree
- Graph traversal using BFS and DFS
- Set, Map, Dictionary
- Union-Find

### Algorithms Demonstration
- Bubble Sort
- Insertion Sort
- Counting Sort
- Linear Search
- Binary Search

## 4. Project Structure

```text
Heatwave-Intelligence-System/
│
├── app.py
├── requirements.txt
└── README.md
```

## 5. Installation and Setup

### Step 1: Install Python

Make sure Python is installed on your computer.

### Step 2: Install Required Libraries

Open the terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

Execute the following command:

```bash
streamlit run app.py
```

### Step 4: Open the Application

Streamlit will open the application in your browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

## 6. Input CSV Format

The application accepts a CSV file containing the following columns:

| Date | Region | Temperature |
|---|---|---:|
| 2026-05-01 | Mumbai | 38 |
| 2026-05-02 | Pune | 42 |
| 2026-05-03 | Nashik | 46 |

**Important:** The CSV file must contain these column names:

- `Date`
- `Region`
- `Temperature`

## 7. Temperature Classification

The application uses illustrative temperature thresholds:

| Temperature | Category |
|---|---|
| Below 40°C | Normal |
| 40°C to below 45°C | Warning |
| 45°C and above | Severe |

These thresholds are used only for academic demonstration and are not official meteorological warning standards.

## 8. Data Structures and Algorithms Used

| Topic | Application |
|---|---|
| Linked List | Storing temperature records |
| Stack | Demonstrating LIFO operations |
| Queue | Demonstrating FIFO operations |
| Circular Queue | Reusing queue positions |
| Priority Queue | Prioritizing temperature records |
| Binary Search Tree | Organizing temperature values |
| Graph | Representing connections between regions |
| BFS and DFS | Traversing regional connections |
| Set | Storing unique regions |
| Dictionary | Mapping regions to temperature records |
| Sorting | Arranging temperature values |
| Searching | Finding specific temperature values |

## 9. Limitations

- The application uses uploaded or sample data.
- It does not fetch live weather information.
- Temperature categories are illustrative.
- It is an academic prototype and does not issue official heatwave alerts.
- Some data structures are demonstrated in simplified form.

## 10. Future Scope

- Integration with live weather APIs.
- More advanced temperature trend analysis.
- Interactive regional maps.
- Improved alert notifications.
- Additional data structure demonstrations.

## 11. Conclusion

The Heatwave Intelligence System demonstrates how Data Structures and Algorithms can be applied to a practical temperature-monitoring problem. It combines Python, Streamlit, and Pandas to create an interactive application while connecting theoretical DSA concepts with real-world use cases.

---

**Developed as an academic project for Data Structures and Algorithms (DSA).**
