import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from collections import deque
import time

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="Heatwave Watch",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #F7F9FC; color: #202938; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E7EAF0; }
    [data-testid="stHeader"] { background: rgba(247,249,252,0.9); }
    h1, h2, h3 { color: #182230; }
    div[data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #E7EAF0;
        padding: 16px; border-radius: 12px;
    }
    .hero {
        background: linear-gradient(110deg, #FFF4E8, #FFFFFF);
        border: 1px solid #F5D9C1; border-radius: 14px;
        padding: 22px 24px; margin-bottom: 18px;
    }
    .small-note { color: #667085; font-size: 0.88rem; }
    .stButton>button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🌡️ Heatwave Watch</h1>
  <p style="margin-bottom:0;color:#475467;">
    Climate Intelligence for Heatwave Monitoring and Early Warning
  </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATA STRUCTURES: AVL TREE
# One AVL tree is maintained for each (region, season) group.
# Key = (date ordinal, latitude, longitude)
# ------------------------------------------------------------
class AVLNode:
    def __init__(self, key, record):
        self.key = key
        self.record = record
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    return node.height if node else 0

def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))

def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0

def rotate_right(y):
    x = y.left
    middle = x.right
    x.right = y
    y.left = middle
    update_height(y)
    update_height(x)
    return x

def rotate_left(x):
    y = x.right
    middle = y.left
    y.left = x
    x.right = middle
    update_height(x)
    update_height(y)
    return y

def avl_insert(root, key, record):
    if root is None:
        return AVLNode(key, record)
    if key < root.key:
        root.left = avl_insert(root.left, key, record)
    elif key > root.key:
        root.right = avl_insert(root.right, key, record)
    else:
        root.record = record
        return root

    update_height(root)
    balance = balance_factor(root)

    # LL case
    if balance > 1 and key < root.left.key:
        return rotate_right(root)
    # RR case
    if balance < -1 and key > root.right.key:
        return rotate_left(root)
    # LR case
    if balance > 1 and key > root.left.key:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    # RL case
    if balance < -1 and key < root.right.key:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root

def avl_search(root, key):
    current = root
    while current:
        if key == current.key:
            return current.record
        current = current.left if key < current.key else current.right
    return None

def avl_range_query(root, start_ordinal, end_ordinal, results):
    """Inorder traversal with pruning; returns records in chronological order."""
    if root is None:
        return
    if root.key[0] >= start_ordinal:
        avl_range_query(root.left, start_ordinal, end_ordinal, results)
    if start_ordinal <= root.key[0] <= end_ordinal:
        results.append(root.record)
    if root.key[0] <= end_ordinal:
        avl_range_query(root.right, start_ordinal, end_ordinal, results)

def avl_count(root):
    if root is None:
        return 0
    return 1 + avl_count(root.left) + avl_count(root.right)

# ------------------------------------------------------------
# LINKED LIST: recent readings
# ------------------------------------------------------------
class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, value):
        node = ListNode(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def get_items(self, limit=10):
        items, current = [], self.head
        while current and len(items) < limit:
            items.append(current.value)
            current = current.next
        return items

# ------------------------------------------------------------
# STACK: last-in-first-out action history
# ------------------------------------------------------------
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if self.items else None
    def peek(self):
        return self.items[-1] if self.items else None

# ------------------------------------------------------------
# QUEUE: first-in-first-out alert processing
# ------------------------------------------------------------
class Queue:
    def __init__(self):
        self.items = deque()
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        return self.items.popleft() if self.items else None
    def display(self):
        return list(self.items)

# ------------------------------------------------------------
# SORTING ALGORITHMS FROM THE SYLLABUS
# ------------------------------------------------------------
def bubble_sort(values):
    arr = list(values)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def insertion_sort(values):
    arr = list(values)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def counting_sort(values):
    arr = [int(round(float(x))) for x in values]
    if not arr:
        return []
    minimum, maximum = min(arr), max(arr)
    counts = [0] * (maximum - minimum + 1)
    for value in arr:
        counts[value - minimum] += 1
    result = []
    for index, count in enumerate(counts):
        result.extend([index + minimum] * count)
    return result

# ------------------------------------------------------------
# SEARCHING ALGORITHMS FROM THE SYLLABUS
# ------------------------------------------------------------
def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1

def binary_search(values, target):
    low, high = 0, len(values)-1
    while low <= high:
        mid = (low + high) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# ------------------------------------------------------------
# DATA LOADING AND INDEXING
# ------------------------------------------------------------
SEASON_ORDER = ["Winter", "Summer", "Monsoon", "Post-Monsoon"]

def get_season(month):
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Summer"
    if month in (6, 7, 8, 9):
        return "Monsoon"
    return "Post-Monsoon"

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        raw = pd.read_csv(uploaded_file)
    else:
        raw = pd.read_csv("heatwave_data.csv")

    required = {"region", "date", "lat", "lon", "tmax"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError("CSV is missing required columns: " + ", ".join(sorted(missing)))

    raw = raw.copy()
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    raw["tmax"] = pd.to_numeric(raw["tmax"], errors="coerce")
    raw["lat"] = pd.to_numeric(raw["lat"], errors="coerce")
    raw["lon"] = pd.to_numeric(raw["lon"], errors="coerce")
    raw = raw.dropna(subset=["region", "date", "lat", "lon", "tmax"])
    raw["season"] = raw["date"].dt.month.map(get_season)
    raw["date_only"] = raw["date"].dt.date
    return raw.sort_values(["region", "season", "date", "lat", "lon"]).reset_index(drop=True)

@st.cache_resource
def build_region_season_index(data):
    # Dictionary/Hash Table: (region, season) -> AVL tree root
    index = {}
    for row in data.itertuples(index=False):
        group = (row.region, row.season)
        key = (row.date.toordinal(), float(row.lat), float(row.lon))
        record = {
            "region": row.region,
            "season": row.season,
            "date": row.date,
            "lat": float(row.lat),
            "lon": float(row.lon),
            "tmax": float(row.tmax)
        }
        index[group] = avl_insert(index.get(group), key, record)
    return index

# ------------------------------------------------------------
# SIDEBAR: DATA SOURCE
# ------------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a module",
    ["Dashboard", "Explore Records", "DSA Lab", "Alerts & Activity", "About the Project"]
)
st.sidebar.divider()
st.sidebar.subheader("Dataset")
uploaded = st.sidebar.file_uploader("Upload heatwave CSV", type=["csv"])
st.sidebar.caption("Default file: heatwave_data.csv in the same project folder.")

try:
    data = load_data(uploaded)
except FileNotFoundError:
    st.error("Dataset not found. Place heatwave_data.csv beside app.py or upload it using the sidebar.")
    st.stop()
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

if data.empty:
    st.error("The CSV does not contain usable records.")
    st.stop()

# Hash table index is built once and cached.
index = build_region_season_index(data)

# Set ADT: unique regions and seasons
regions_set = set(data["region"].unique())
seasons_set = set(data["season"].unique())
regions = sorted(regions_set)

# Session-level Stack, Queue and Linked List
if "action_stack" not in st.session_state:
    st.session_state.action_stack = Stack()
if "alert_queue" not in st.session_state:
    st.session_state.alert_queue = Queue()
if "recent_list" not in st.session_state:
    st.session_state.recent_list = LinkedList()
if "threshold" not in st.session_state:
    st.session_state.threshold = 40.0

# Add records meeting the selected threshold to the alert queue once per session.
if "queued_alert_keys" not in st.session_state:
    st.session_state.queued_alert_keys = set()

# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------
if page == "Dashboard":
    st.subheader("Overview")
    st.caption("Explore historical maximum-temperature observations across regions and seasons.")

    threshold = st.sidebar.slider(
        "Heat alert threshold (°C)", 35.0, 50.0,
        float(st.session_state.threshold), 0.5
    )
    st.session_state.threshold = threshold

    alert_data = data[data["tmax"] >= threshold]
    avg_temp = data["tmax"].mean()
    max_temp = data["tmax"].max()
    alert_count = len(alert_data)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total records", f"{len(data):,}")
    c2.metric("Regions", len(regions_set))
    c3.metric("Average Tmax", f"{avg_temp:.1f} °C")
    c4.metric("Records above threshold", f"{alert_count:,}")

    st.divider()
    left, right = st.columns(2)
    with left:
        st.markdown("### Average temperature by region")
        region_avg = data.groupby("region", as_index=False)["tmax"].mean().sort_values("tmax", ascending=False)
        fig = px.bar(region_avg, x="region", y="tmax", color="tmax",
                     color_continuous_scale="Oranges",
                     labels={"region":"Region", "tmax":"Average Tmax (°C)"})
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("### Temperature trend over time")
        yearly = data.assign(year=data["date"].dt.year).groupby("year", as_index=False)["tmax"].mean()
        fig = px.line(yearly, x="year", y="tmax", markers=True,
                      labels={"year":"Year", "tmax":"Average Tmax (°C)"})
        fig.update_traces(line_color="#E87524")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Seasonal temperature pattern")
    seasonal = data.groupby("season", as_index=False)["tmax"].mean()
    seasonal["season"] = pd.Categorical(seasonal["season"], categories=SEASON_ORDER, ordered=True)
    seasonal = seasonal.sort_values("season")
    fig = px.bar(seasonal, x="season", y="tmax", color="tmax",
                 color_continuous_scale="OrRd",
                 labels={"season":"Season", "tmax":"Average Tmax (°C)"})
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Highest temperature observations")
    st.dataframe(data.nlargest(10, "tmax")[["region","date","lat","lon","tmax","season"]],
                 use_container_width=True, hide_index=True)

# ------------------------------------------------------------
# EXPLORE RECORDS: HASH TABLE + AVL TREE
# ------------------------------------------------------------
elif page == "Explore Records":
    st.subheader("Region-wise and time-based record explorer")
    st.write("The Dictionary locates a region-season group. Its AVL Tree stores records by date and supports ordered range queries.")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_region = st.selectbox("Select region", regions)
    with col2:
        selected_season = st.selectbox("Select season", SEASON_ORDER)
    with col3:
        st.metric("Indexed groups", len(index))

    available = data[(data["region"] == selected_region) & (data["season"] == selected_season)]
    if available.empty:
        st.info("No records are available for this region and season.")
    else:
        min_date = available["date"].min().date()
        max_date = available["date"].max().date()
        d1, d2 = st.columns(2)
        start_date = d1.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
        end_date = d2.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

        if start_date > end_date:
            st.warning("Start date must be earlier than or equal to end date.")
        else:
            root = index.get((selected_region, selected_season))
            results = []
            avl_range_query(root, start_date.toordinal(), end_date.toordinal(), results)
            result_df = pd.DataFrame(results)
            st.metric("Records returned by AVL range query", f"{len(result_df):,}")
            if not result_df.empty:
                st.dataframe(result_df, use_container_width=True, hide_index=True)
                chart = result_df.groupby("date", as_index=False)["tmax"].mean()
                fig = px.line(chart, x="date", y="tmax", markers=True,
                              labels={"date":"Date", "tmax":"Average Tmax (°C)"})
                fig.update_traces(line_color="#E87524")
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
                st.plotly_chart(fig, use_container_width=True)
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download filtered records", csv, "filtered_heatwave_records.csv", "text/csv")
            else:
                st.info("No records found in the selected date range.")

    st.divider()
    st.markdown("### Exact record search using AVL Tree")
    st.caption("Search uses date, latitude and longitude as the composite key.")
    search_date = st.date_input("Record date", value=min_date if not available.empty else date.today(), key="exact_date")
    if not available.empty:
        coords = available[available["date"].dt.date == search_date][["lat","lon"]].drop_duplicates()
        if not coords.empty:
            options = [f"{r.lat}, {r.lon}" for r in coords.itertuples(index=False)]
            chosen = st.selectbox("Coordinate (latitude, longitude)", options)
            if st.button("Search exact record"):
                lat_value, lon_value = map(float, chosen.split(", "))
                key = (search_date.toordinal(), lat_value, lon_value)
                found = avl_search(index.get((selected_region, selected_season)), key)
                st.session_state.action_stack.push(f"Exact search: {selected_region}, {search_date}")
                st.session_state.recent_list.add_front(found if found else {
                    "region": selected_region, "date": str(search_date), "result": "Not found"
                })
                if found:
                    st.success("Record found in the AVL Tree.")
                    st.json({k: str(v) if k == "date" else v for k, v in found.items()})
                else:
                    st.warning("Record not found.")
        else:
            st.info("No coordinates are available for this date in the selected group.")

# ------------------------------------------------------------
# DSA LAB: SEARCHING AND SORTING
# ------------------------------------------------------------
elif page == "DSA Lab":
    st.subheader("DSA Laboratory")
    st.write("Try the searching and sorting algorithms included in the course syllabus.")
    sample = data["tmax"].dropna().head(500).round(0).astype(int).tolist()

    tab1, tab2 = st.tabs(["Searching", "Sorting"])
    with tab1:
        st.markdown("#### Linear Search vs Binary Search")
        target = st.number_input("Temperature value to search (°C)", value=int(sample[0]), step=1)
        if st.button("Run search algorithms"):
            start = time.perf_counter()
            linear_index = linear_search(sample, int(target))
            linear_time = time.perf_counter() - start

            sorted_sample = sorted(sample)
            start = time.perf_counter()
            binary_index = binary_search(sorted_sample, int(target))
            binary_time = time.perf_counter() - start

            a, b = st.columns(2)
            a.metric("Linear Search", "Found" if linear_index != -1 else "Not found")
            a.caption(f"Index: {linear_index} | Time: {linear_time:.8f} sec")
            b.metric("Binary Search", "Found" if binary_index != -1 else "Not found")
            b.caption(f"Sorted-list index: {binary_index} | Time: {binary_time:.8f} sec")
            st.session_state.action_stack.push(f"Searched for {int(target)}°C")

        st.info("Binary Search requires sorted data. The app sorts a copy before running it.")

    with tab2:
        st.markdown("#### Compare sorting algorithms")
        sort_count = st.slider("Number of sample values (keep small for Bubble Sort)", 10, 150, 40)
        values = sample[:sort_count]
        algorithm = st.selectbox("Choose algorithm", ["Bubble Sort", "Insertion Sort", "Counting Sort"])
        if st.button("Sort sample"):
            start = time.perf_counter()
            if algorithm == "Bubble Sort":
                sorted_values = bubble_sort(values)
            elif algorithm == "Insertion Sort":
                sorted_values = insertion_sort(values)
            else:
                sorted_values = counting_sort(values)
            elapsed = time.perf_counter() - start
            st.success(f"{algorithm} completed in {elapsed:.8f} seconds.")
            st.write("Original values:", values)
            st.write("Sorted values:", sorted_values)
            st.session_state.action_stack.push(f"Applied {algorithm}")

    st.divider()
    st.markdown("### Complexity reference")
    complexity = pd.DataFrame([
        ["Linear Search", "O(n)", "O(1)"],
        ["Binary Search", "O(log n)", "O(1)"],
        ["Bubble Sort", "O(n²)", "O(1)"],
        ["Insertion Sort", "O(n²)", "O(1)"],
        ["Counting Sort", "O(n + k)", "O(n + k)"],
        ["AVL Search / Insert", "O(log n)", "O(log n) recursive stack for insert"],
        ["Hash Table lookup", "O(1) average", "O(n) total storage"],
    ], columns=["Algorithm / Structure", "Time complexity", "Space complexity"])
    st.dataframe(complexity, use_container_width=True, hide_index=True)

# ------------------------------------------------------------
# ALERTS & ACTIVITY: QUEUE + STACK + LINKED LIST
# ------------------------------------------------------------
elif page == "Alerts & Activity":
    st.subheader("Alerts and activity")
    threshold = st.slider("Alert threshold (°C)", 35.0, 50.0, 40.0, 0.5, key="alert_threshold")
    hot = data[data["tmax"] >= threshold].nlargest(100, "tmax")

    st.markdown("### Heatwave alert queue (FIFO)")
    st.caption("The highest-temperature records are added to the queue for demonstration. A real system would enqueue new AWS readings as they arrive.")
    if st.button("Load next 20 alerts into queue"):
        for row in hot.head(20).itertuples(index=False):
            key = (row.region, str(row.date), float(row.lat), float(row.lon))
            if key not in st.session_state.queued_alert_keys:
                st.session_state.alert_queue.enqueue({
                    "region": row.region, "date": str(row.date.date()),
                    "lat": float(row.lat), "lon": float(row.lon), "tmax": float(row.tmax)
                })
                st.session_state.queued_alert_keys.add(key)
        st.success("Alert records added to the queue.")

    q1, q2 = st.columns(2)
    q1.metric("Alerts waiting", len(st.session_state.alert_queue.items))
    if q2.button("Process next alert"):
        processed = st.session_state.alert_queue.dequeue()
        if processed:
            st.session_state.action_stack.push(f"Processed alert: {processed['region']} {processed['date']}")
            st.success(f"Processed: {processed['region']} — {processed['tmax']:.1f} °C")
        else:
            st.info("The alert queue is empty.")
    queue_items = st.session_state.alert_queue.display()
    if queue_items:
        st.dataframe(pd.DataFrame(queue_items), use_container_width=True, hide_index=True)
    else:
        st.info("No pending alerts.")

    st.divider()
    st.markdown("### Stack: recent actions (LIFO)")
    st.write("Last action:", st.session_state.action_stack.peek() or "No actions yet")
    s1, s2 = st.columns(2)
    if s1.button("Undo / pop last action"):
        removed = st.session_state.action_stack.pop()
        st.info(f"Removed: {removed}" if removed else "Stack is empty.")
    if s2.button("Clear action history"):
        st.session_state.action_stack.items.clear()
        st.success("Action history cleared.")
    if st.session_state.action_stack.items:
        st.write(list(reversed(st.session_state.action_stack.items)))
    else:
        st.caption("No action history.")

    st.divider()
    st.markdown("### Linked List: recent viewed records")
    recent = st.session_state.recent_list.get_items(10)
    if recent:
        st.dataframe(pd.DataFrame(recent), use_container_width=True, hide_index=True)
    else:
        st.caption("Search an exact record in Explore Records to add it to this linked list.")

# ------------------------------------------------------------
# ABOUT / DESIGN DOCUMENT SUMMARY
# ------------------------------------------------------------
elif page == "About the Project":
    st.subheader("Project design and DSA mapping")
    st.markdown("""
    **Problem:** Heatwave behaviour varies by region and season. A large historical dataset
    and continuously arriving weather observations need efficient storage, searching and
    chronological retrieval.

    **Solution:** Heatwave Watch organizes observations by region and season using a
    Dictionary (Hash Table). Each group points to an AVL Tree keyed by
    (date, latitude, longitude). The AVL Tree maintains balance and supports efficient
    exact searches and date-range traversal.

    **Dataset fields:** `region`, `date`, `lat`, `lon`, `tmax`.

    **Season grouping used in this prototype:**
    - Winter: December–February
    - Summer: March–May
    - Monsoon: June–September
    - Post-Monsoon: October–November

    **Important:** The alert threshold is configurable for demonstration. It is not presented
    as an official IMD heatwave declaration criterion. The application analyses the supplied
    historical CSV; it does not generate a meteorological forecast or issue official warnings.
    """)
    mapping = pd.DataFrame([
        ["Introduction to DS", "Data organization, static vs dynamic structures, complexity"],
        ["Linked List", "Recent viewed records"],
        ["Stack", "Action history and pop operation"],
        ["Queue", "Pending alert processing using FIFO"],
        ["Tree", "AVL Tree for timestamp-based record indexing"],
        ["Set", "Unique region and season collections"],
        ["Map / Dictionary", "Region-season to AVL root mapping"],
        ["Searching", "Linear Search and Binary Search demonstrations"],
        ["Sorting", "Bubble, Insertion and Counting Sort demonstrations"],
    ], columns=["Syllabus topic", "Application implementation"])
    st.dataframe(mapping, use_container_width=True, hide_index=True)

    st.markdown("### Complexity of the main design")
    st.write("""
    - Dictionary lookup: average O(1) to locate a region-season group.
    - AVL exact search: O(log n) within that group.
    - AVL insertion: O(log n) within that group.
    - AVL date-range query: O(log n + k) when locating the first relevant records
      and returning k matching records in a balanced range traversal.
    - Extra memory: O(n) for stored records and AVL nodes.
    """)
    st.caption("This is an academic prototype based on the supplied use case and CSV dataset. Validate operational thresholds and forecasts with qualified meteorological sources before real-world use.")
