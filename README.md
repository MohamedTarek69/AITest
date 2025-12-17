<h1 align="center">🎨 Graph Coloring Problem Solver</h1>
<p align="center">
  <b>Python | Tkinter | NetworkX | Matplotlib</b>  
</p>
<p align="center">
  A desktop application for solving and visualizing the <b>Graph Coloring Problem</b> using <b>Backtracking</b> and a <b>Cultural Algorithm</b>.
</p>

---

## 🏗️ Project Overview

The **Graph Coloring Solver** is an interactive GUI-based application that allows users to:

* Build graphs manually or randomly
* Choose a coloring algorithm
* Visualize the colored graph
* Analyze algorithm performance

The project is designed for **AI, Algorithms, and Optimization courses**, providing both **exact** and **metaheuristic** solutions.

---

## 🎯 Goals

* Solve the Graph Coloring Problem efficiently
* Compare deterministic vs. evolutionary approaches
* Visualize solutions and convergence behavior
* Provide an educational, easy-to-use interface

---

## ✨ Main Features

| Feature                   | Description                                      |
| ------------------------- | ------------------------------------------------ |
| 🧩 Graph Builder          | Create graphs manually or generate random graphs |
| 🔗 Edge Management        | Add and remove edges using a GUI                 |
| 🎨 Coloring Visualization | Color-coded graph display                        |
| 🧠 Backtracking Algorithm | Exact solution with degree-based ordering        |
| 🌍 Cultural Algorithm     | Evolutionary approach with belief space          |
| 📈 Fitness Plot           | Visualize convergence over generations           |
| ⏹️ Early Stopping         | Stop CA when a valid coloring is found           |

---

## 🧱 Architecture

The project follows a **Modular Architecture**:

* **GUI Layer** → Tkinter (Notebook-based layout)
* **Algorithm Layer** → Backtracking & Cultural Algorithm
* **Visualization Layer** → Matplotlib + NetworkX

```
project/
│── main.py
│── gui_app.py
│── algorithms.py
│── visualization.py
```

---

## 🧰 Tech Stack

| Category             | Technology                       |
| -------------------- | -------------------------------- |
| **Language**         | Python 3                         |
| **GUI**              | Tkinter (ttk Notebook)           |
| **Graph Processing** | NetworkX                         |
| **Visualization**    | Matplotlib                       |
| **Algorithms**       | Backtracking, Cultural Algorithm |

---

## 🧠 Algorithms Explained

### 🔵 Backtracking Algorithm

* Exact and complete search method
* Uses **Most Constrained Variable (Degree Heuristic)**
* Guarantees a solution if one exists
* Slower for large graphs

**Steps:**

1. Order nodes by descending degree
2. Try assigning colors sequentially
3. Backtrack on conflicts

---

### 🟢 Cultural Algorithm (Metaheuristic)

* Population-based evolutionary algorithm
* Inspired by social evolution
* Uses a **Belief Space** to guide solutions

**Components:**

* Population of candidate colorings
* Fitness function based on conflicts
* Crossover & mutation operators
* Belief space influencing new generations

**Fitness Function:**

```
fitness = 1 / (1 + number_of_conflicts)
```

---

## 📊 Fitness Visualization

* Displays fitness vs. generation
* Helps analyze convergence speed
* Fitness = 1.0 means a valid coloring (0 conflicts)

---

## 🧪 User Workflow

1. Enter number of vertices
2. Create empty or random graph
3. Add/remove edges (1-based indexing)
4. Choose number of colors
5. Select algorithm
6. Run and visualize results

---

## 🧩 GUI Tabs Overview

### ⚙️ Graph Setup & Run

* Graph creation
* Edge management
* Algorithm selection
* Parameter configuration

### 📊 Results & Visualization

* Colored graph display
* Fitness convergence plot
* Execution time and solution details

---

## ⏱️ Performance Output

For each run, the application displays:

* Coloring result
* Number of conflicts
* Fitness value
* Execution time

---

## 🚀 How to Run

```bash
pip install networkx matplotlib
python main.py
```

---

## 📚 Educational Value

This project is ideal for learning:

* Graph Coloring Problem
* Constraint Satisfaction Problems (CSP)
* Backtracking search
* Evolutionary & Cultural Algorithms
* Algorithm visualization

---

## 👨‍🎓 Author

**Mohamed Tarek**
Computer Science / AI Student

---

## ⭐ Future Improvements

* Add Genetic Algorithm
* Step-by-step backtracking visualization
* Export results to file
* Support large graphs optimization

---

<p align="center">🔥 Built for learning, visualization, and algorithm comparison 🔥</p>
