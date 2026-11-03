
import streamlit as st
import pandas as pd
from collections import deque
import heapq

st.set_page_config(page_title="Heatwave Monitor", page_icon="🌡️", layout="wide")

st.title("🌡️ Heatwave Intelligence System")
st.caption("Temperature Monitoring using Data Structures and Algorithms")

# ------------------------------------------------
# 1. SAMPLE DATA
# ------------------------------------------------

data = {
    "Date": ["01-04-26", "02-04-26", "03-04-26", "01-04-26",
             "02-04-26", "03-04-26", "01-04-26", "02-04-26"],
    "Region": ["Mumbai", "Mumbai", "Mumbai", "Pune",
               "Pune", "Pune", "Nagpur", "Nagpur"],
    "Temperature": [38, 41, 43, 37, 42, 44, 45, 47]
}

df = pd.DataFrame(data)

# Allow CSV upload
uploaded = st.sidebar.file_uploader("Upload Temperature CSV", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)

# Check required columns
required = {"Date", "Region", "Temperature"}

if not required.issubset(df.columns):
    st.error("CSV must contain Date, Region and Temperature columns.")
    st.stop()

df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
df = df.dropna(subset=["Temperature", "Region"])

def severity(temp):
    if temp >= 45:
        return "Severe"
    elif temp >= 40:
        return "Warning"
    return "Normal"

df["Severity"] = df["Temperature"].apply(severity)

# ------------------------------------------------
# 2. DASHBOARD
# ------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard",
    "Linked List, Stack & Queue",
    "Trees & Graphs",
    "Set, Map & Dictionary",
    "Searching & Sorting"
])

with tab1:
    st.header("Temperature Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Records", len(df))
    c2.metric("Average Temperature",
              f"{df['Temperature'].mean():.1f} °C")
    c3.metric("Highest Temperature",
              f"{df['Temperature'].max()} °C")

    st.subheader("Regional Temperature Data")
    st.dataframe(df, use_container_width=True)

    st.subheader("Temperature Comparison")
    st.bar_chart(df.groupby("Region")["Temperature"].mean())

    st.subheader("Heatwave Alerts")
    alerts = df[df["Severity"] != "Normal"]

    if len(alerts) > 0:
        st.dataframe(alerts, use_container_width=True)
    else:
        st.success("No heatwave alerts.")

# ------------------------------------------------
# 3. LINKED LIST
# ------------------------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def display(self):
        result = []
        temp = self.head

        while temp:
            result.append(temp.data)
            temp = temp.next

        return result

# ------------------------------------------------
# 4. DOUBLY AND CIRCULAR LINKED LIST
# ------------------------------------------------

class DoublyList:
    def __init__(self):
        self.data = []

    def insert(self, value):
        self.data.append(value)

    def display(self):
        return self.data, self.data[::-1]


class CircularList:
    def __init__(self):
        self.data = []

    def insert(self, value):
        self.data.append(value)

    def display(self):
        return self.data

# ------------------------------------------------
# 5. STACK
# ------------------------------------------------

class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if self.items:
            return self.items.pop()
        return "Stack Empty"

# ------------------------------------------------
# 6. QUEUE AND CIRCULAR QUEUE
# ------------------------------------------------

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if self.items:
            return self.items.popleft()
        return "Queue Empty"


class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.items = [None] * size
        self.front = -1
        self.rear = -1

    def enqueue(self, value):
        if (self.rear + 1) % self.size == self.front:
            return False

        if self.front == -1:
            self.front = 0

        self.rear = (self.rear + 1) % self.size
        self.items[self.rear] = value
        return True

# ------------------------------------------------
# 7. PRIORITY QUEUE AND DEQUE
# ------------------------------------------------

class PriorityQueue:
    def __init__(self):
        self.items = []

    def insert(self, priority, value):
        heapq.heappush(self.items, (priority, value))

    def remove(self):
        if self.items:
            return heapq.heappop(self.items)
        return None


# ------------------------------------------------
# LINEAR DATA STRUCTURE INTERFACE
# ------------------------------------------------

with tab2:
    st.header("Linear Data Structures")

    values = df["Temperature"].tolist()

    ll = LinkedList()
    for v in values:
        ll.insert(v)

    st.subheader("Linked List")
    st.write("Temperature Nodes:", ll.display())

    dl = DoublyList()
    cl = CircularList()

    for v in values[:4]:
        dl.insert(v)
        cl.insert(v)

    st.subheader("Doubly Linked List")
    forward, backward = dl.display()
    st.write("Forward:", forward)
    st.write("Backward:", backward)

    st.subheader("Circular Linked List")
    st.write("Circular nodes:", cl.display(), "→ First node")

    st.divider()

    st.subheader("Stack (LIFO)")

    if "stack" not in st.session_state:
        st.session_state.stack = []

    value = st.number_input("Temperature to push", value=40)

    col1, col2 = st.columns(2)

    if col1.button("Push"):
        st.session_state.stack.append(value)

    if col2.button("Pop"):
        if st.session_state.stack:
            st.session_state.stack.pop()

    st.write("Stack:", st.session_state.stack)

    st.divider()

    st.subheader("Queue (FIFO)")

    if "queue" not in st.session_state:
        st.session_state.queue = []

    region = st.selectbox("Select region", df["Region"].unique())

    col1, col2 = st.columns(2)

    if col1.button("Enqueue"):
        st.session_state.queue.append(region)

    if col2.button("Dequeue"):
        if st.session_state.queue:
            st.session_state.queue.pop(0)

    st.write("Queue:", st.session_state.queue)

    st.divider()

    st.subheader("Circular Queue")

    cq = CircularQueue(5)

    for v in values[:4]:
        cq.enqueue(v)

    st.write("Circular Queue:", cq.items)

    st.subheader("Priority Queue")

    pq = PriorityQueue()

    for _, row in df.iterrows():
        priority = 1 if row["Severity"] == "Severe" else (
            2 if row["Severity"] == "Warning" else 3
        )
        pq.insert(priority, row["Region"])

    st.write("Alert processing order:", sorted(pq.items))

    st.subheader("Double Ended Queue")

    dq = deque(["Mumbai", "Pune", "Nagpur"])
    st.write("Deque:", list(dq))

# ------------------------------------------------
# 8. BINARY SEARCH TREE
# ------------------------------------------------

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        if root is None:
            return TreeNode(value)

        if value < root.value:
            root.left = self.insert(root.left, value)
        elif value > root.value:
            root.right = self.insert(root.right, value)

        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            result.append(root.value)
            self.inorder(root.right)

# ------------------------------------------------
# 9. GRAPH WITH BFS AND DFS
# ------------------------------------------------

graph = {
    "Mumbai": ["Pune"],
    "Pune": ["Mumbai", "Nashik"],
    "Nashik": ["Pune", "Nagpur"],
    "Nagpur": ["Nashik"]
}

def bfs(graph, start):
    visited = []
    queue = [start]

    while queue:
        node = queue.pop(0)

        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])

    return visited

def dfs(graph, start):
    visited = []

    def visit(node):
        if node not in visited:
            visited.append(node)

            for neighbour in graph[node]:
                visit(neighbour)

    visit(start)
    return visited

with tab3:
    st.header("Trees and Graphs")

    st.subheader("Binary Search Tree")

    tree = BST()
    result = []

    for v in values:
        tree.root = tree.insert(tree.root, v)

    tree.inorder(tree.root)

    st.write("Inorder Traversal:", result)

    st.caption("Inorder traversal of a BST displays values in ascending order.")

    st.subheader("Graph Representation")

    start = st.selectbox("Starting Region", list(graph.keys()))

    st.write("BFS Traversal:", bfs(graph, start))
    st.write("DFS Traversal:", dfs(graph, start))

# ------------------------------------------------
# 10. SET, MAP AND DICTIONARY
# ------------------------------------------------

with tab4:
    st.header("Set, Map and Dictionary")

    # Set: stores unique regions
    region_set = set(df["Region"])

    st.subheader("Set ADT")
    st.write("Unique Regions:", region_set)

    # Map/Dictionary: region -> temperatures
    region_map = {}

    for _, row in df.iterrows():
        region_map.setdefault(row["Region"], []).append(
            row["Temperature"]
        )

    st.subheader("Dictionary ADT")
    st.write("Region-wise Temperature Mapping:", region_map)

    selected = st.selectbox("Select region", list(region_map.keys()))

    st.write("Temperature readings:", region_map[selected])

    # Union-Find
    st.subheader("Union-Find Operations")

    parent = {r: r for r in region_set}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        parent[find(a)] = find(b)

    st.write("Initial partitions:", parent)

# ------------------------------------------------
# 11. SORTING ALGORITHMS
# ------------------------------------------------

def bubble_sort(arr):
    arr = arr.copy()

    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr


def insertion_sort(arr):
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1

        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1

        arr[j+1] = key

    return arr


def counting_sort(arr):
    if not arr:
        return []

    arr = [int(x) for x in arr]
    count = [0] * (max(arr)+1)

    for x in arr:
        count[x] += 1

    result = []

    for i in range(len(count)):
        result.extend([i] * count[i])

    return result

# ------------------------------------------------
# 12. SEARCHING ALGORITHMS
# ------------------------------------------------

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def binary_search(arr, target):
    low, high = 0, len(arr)-1

    while low <= high:
        mid = (low+high)//2

        if arr[mid] == target:
            return mid

        elif arr[mid] < target:
            low = mid+1

        else:
            high = mid-1

    return -1


with tab5:
    st.header("Searching and Sorting")

    numbers = [int(x) for x in values]

    st.write("Original Data:", numbers)

    algorithm = st.selectbox(
        "Select Sorting Algorithm",
        ["Bubble Sort", "Insertion Sort", "Counting Sort"]
    )

    if st.button("Sort Data"):

        if algorithm == "Bubble Sort":
            output = bubble_sort(numbers)

        elif algorithm == "Insertion Sort":
            output = insertion_sort(numbers)

        else:
            output = counting_sort(numbers)

        st.success(f"Sorted Data: {output}")

    st.divider()

    st.subheader("Searching")

    target = st.number_input("Enter temperature to search", value=40)

    if st.button("Linear Search"):
        st.write("Position:", linear_search(numbers, target))

    if st.button("Binary Search"):
        sorted_data = insertion_sort(numbers)
        st.write("Position in sorted data:",
                 binary_search(sorted_data, target))

    st.caption("Binary Search requires sorted data.")
    
# ------------------------------------------------
# END OF APPLICATION
# ------------------------------------------------

st.divider()
st.caption("Academic project | Data Structures and Algorithms")
