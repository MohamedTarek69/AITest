import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import networkx as nx
import random
import sys

from algorithms import cultural_algorithm, backtracking_coloring
from visualization import visualize_on_tk, visualize_fitness_plot


class GraphColoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Coloring Problem Solver (Notebook Layout)")
        self.geometry("1000x650")

        self.graph = nx.Graph()

        # 1. Setup Notebook Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

        # 2. Tab 1: Setup and Run
        setup_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(setup_tab, text='⚙️ Graph Setup & Run')

        # 3. Tab 2: Results and Visualization
        results_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(results_tab, text='📊 Results & Visualization')

        # --- Content of Setup Tab ---

        setup_main_frame = ttk.Frame(setup_tab)
        setup_main_frame.pack(fill=tk.BOTH, expand=True)

        #  Left Column: Controls and Algorithm Params
        left_control_frame = ttk.Frame(setup_main_frame, width=300)
        left_control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        #  Right Column: Edges List
        right_list_frame = ttk.Frame(setup_main_frame)
        right_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Left Column Contents (Controls) ---

        ttk.Label(left_control_frame, text="Vertices (n):").pack(anchor=tk.W)
        self.n_entry = ttk.Entry(left_control_frame, width=20)
        self.n_entry.pack(fill=tk.X, pady=2)

        ttk.Button(left_control_frame, text="Create Empty Graph", command=self.create_graph).pack(fill=tk.X, pady=4)
        ttk.Button(left_control_frame, text="Generate Random Graph", command=self.generate_random_graph).pack(fill=tk.X,
                                                                                                              pady=4)

        ttk.Separator(left_control_frame).pack(fill=tk.X, pady=6)

        # Edge Input Frame
        ttk.Label(left_control_frame, text="Add Edge (u v) - 1-based: ").pack(anchor=tk.W)
        edge_input_frame = ttk.Frame(left_control_frame)
        edge_input_frame.pack(fill=tk.X)
        self.u_entry = ttk.Entry(edge_input_frame, width=6)
        self.u_entry.pack(side=tk.LEFT)
        self.v_entry = ttk.Entry(edge_input_frame, width=6)
        self.v_entry.pack(side=tk.LEFT, padx=4)
        ttk.Button(edge_input_frame, text="Add", command=self.add_edge).pack(side=tk.LEFT, padx=4)

        ttk.Separator(left_control_frame).pack(fill=tk.X, pady=6)

        # Algorithm Configuration
        ttk.Label(left_control_frame, text="Number of colors:").pack(anchor=tk.W)
        self.colors_entry = ttk.Entry(left_control_frame, width=20)
        self.colors_entry.insert(0, "3")
        self.colors_entry.pack(fill=tk.X, pady=2)

        ttk.Label(left_control_frame, text="Algorithm:").pack(anchor=tk.W, pady=(8, 0))
        self.algo_var = tk.StringVar(value="backtracking")
        self.algo_var.trace_add("write", lambda *args: self.toggle_ca_params())

        ttk.Radiobutton(left_control_frame, text="Backtracking", variable=self.algo_var, value="backtracking").pack(
            anchor=tk.W)
        ttk.Radiobutton(left_control_frame, text="Cultural Algorithm", variable=self.algo_var, value="cultural").pack(
            anchor=tk.W)

        # CA Parameters frame (Dynamic visibility)
        self.ca_params_frame = ttk.Frame(left_control_frame)
        self.ca_params_frame.pack_forget()

        ttk.Label(self.ca_params_frame, text="Population size:").pack(anchor=tk.W)
        self.pop_entry = ttk.Entry(self.ca_params_frame, width=20)
        self.pop_entry.insert(0, "20")
        self.pop_entry.pack(fill=tk.X)

        ttk.Label(self.ca_params_frame, text="Generations:").pack(anchor=tk.W)
        self.gen_entry = ttk.Entry(self.ca_params_frame, width=20)
        self.gen_entry.insert(0, "200")
        self.gen_entry.pack(fill=tk.X)

        ttk.Label(self.ca_params_frame, text="Belief size:").pack(anchor=tk.W)
        self.belief_entry = ttk.Entry(self.ca_params_frame, width=20)
        self.belief_entry.insert(0, "5")
        self.belief_entry.pack(fill=tk.X)

        # NEW CONTROL: Early Stopping Checkbox
        self.early_stop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.ca_params_frame,
            text="Enable Early Stopping (Stop if Fitness=1.0)",
            variable=self.early_stop_var
        ).pack(anchor=tk.W, pady=(5, 0))

        ttk.Button(left_control_frame, text="Run Algorithm", command=self.on_run).pack(fill=tk.X, pady=8)

        # --- Right Column Contents (Edges List) ---

        ttk.Label(right_list_frame, text="Current Edges (u v):").pack(anchor=tk.W)
        self.edges_listbox = tk.Listbox(right_list_frame, height=15)
        self.edges_listbox.pack(fill=tk.BOTH, expand=True, pady=2)

        ttk.Button(right_list_frame, text="Remove Selected Edge", command=self.remove_selected_edge).pack(fill=tk.X)

        # --- Content of Results Tab ---

        # Frame for Visualization and Plot
        vis_plot_frame = ttk.Frame(results_tab)
        vis_plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 6))

        # Left side for Graph Visualization
        self.vis_frame = ttk.Frame(vis_plot_frame, relief=tk.RIDGE, borderwidth=1)
        self.vis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Right side for Fitness Plot (New)
        self.plot_frame = ttk.Frame(vis_plot_frame, relief=tk.RIDGE, borderwidth=1)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Frame for Results Textbox at the bottom
        results_frame = ttk.Frame(results_tab)
        results_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(results_frame, text="Results:").pack(anchor=tk.W)
        self.result_text = tk.Text(results_frame, height=8, wrap=tk.WORD)
        self.result_text.pack(fill=tk.X, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    # ----- GUI Actions -----

    def toggle_ca_params(self):
        if self.algo_var.get() == "cultural":
            self.ca_params_frame.pack(fill=tk.X, pady=6)
        else:
            self.ca_params_frame.pack_forget()

    def create_graph(self):
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid n", "Please enter a positive integer.")
            return

        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(n))
        self.edges_listbox.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

        visualize_on_tk(self.vis_frame, self.graph, [], "Empty Graph")
        visualize_fitness_plot(self.plot_frame, [])

        self.status_var.set(f"Created empty graph with {n} vertices")

    def generate_random_graph(self):
        try:
            n_input = self.n_entry.get()
            n = int(n_input)
            if n <= 1:
                messagebox.showerror("Input Error", "Graph must have at least 2 vertices to form edges.")
                return
        except ValueError:
            messagebox.showerror("Invalid n", "Please enter a valid positive integer.")
            return

        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(n))
        self.edges_listbox.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

        p = random.uniform(0.15, 0.60)
        edges_added = 0
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < p:
                    self.graph.add_edge(u, v)
                    self.edges_listbox.insert(tk.END, f"{u + 1} {v + 1}")
                    edges_added += 1

        self.status_var.set(
            f"Generated random graph with {n} vertices and {edges_added} random edges (Density: {p:.2f})")

        visualize_on_tk(self.vis_frame, self.graph, [0] * n, f"Random Graph ({n} Nodes)")
        visualize_fitness_plot(self.plot_frame, [])

    def add_edge(self):
        try:
            u = int(self.u_entry.get()) - 1
            v = int(self.v_entry.get()) - 1
        except ValueError:
            messagebox.showerror("Invalid", "Enter valid integers.")
            return

        if u == v:
            messagebox.showerror("Invalid", "Self loops not allowed.")
            return
        if u not in self.graph.nodes() or v not in self.graph.nodes():
            messagebox.showerror("Invalid", "Vertices must be within range (1-based).")
            return
        if self.graph.has_edge(u, v):
            messagebox.showwarning("Duplicate", "Edge already exists.")
            return

        self.graph.add_edge(u, v)
        self.edges_listbox.insert(tk.END, f"{u + 1} {v + 1}")
        self.status_var.set(f"Added {u + 1}-{v + 1}")

    def remove_selected_edge(self):
        sel = self.edges_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        try:
            u_str, v_str = self.edges_listbox.get(idx).split()
            u, v = int(u_str) - 1, int(v_str) - 1
        except:
            return

        if self.graph.has_edge(u, v):
            self.graph.remove_edge(u, v)
        self.edges_listbox.delete(idx)
        self.status_var.set(f"Removed {u + 1}-{v + 1}")

    def on_run(self):
        if self.graph.number_of_nodes() == 0:
            messagebox.showerror("Empty", "Create a graph first.")
            return

        try:
            num_colors = int(self.colors_entry.get())
            if num_colors <= 0:
                messagebox.showerror("Invalid", "Number of colors must be positive.")
                return
            if self.algo_var.get() == "cultural":
                pop = int(self.pop_entry.get())
                gens = int(self.gen_entry.get())
                belief = int(self.belief_entry.get())
                if pop <= 0 or gens <= 0 or belief <= 0:
                    messagebox.showerror("Invalid", "CA parameters must be positive.")
                    return
        except ValueError:
            messagebox.showerror("Invalid", "All input fields must contain valid positive integers.")
            return

        algo = self.algo_var.get()
        self.notebook.select(1)

        thread = threading.Thread(target=self.run_algorithm,
                                  args=(algo, num_colors), daemon=True)
        thread.start()

    def _finish_run(self, colors: list, text: str, title: str, history: list = None):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

        visualize_on_tk(self.vis_frame, self.graph, colors, title)

        if history:
            visualize_fitness_plot(self.plot_frame, history)
        else:
            visualize_fitness_plot(self.plot_frame, [])

        self.status_var.set("Ready")

    def run_algorithm(self, algo: str, num_colors: int):
        self.status_var.set("Running...")
        time.sleep(0.1)

        start = time.time()
        colors = []
        text = ""
        title = ""
        history = None

        if algo == "backtracking":
            success, colors = backtracking_coloring(self.graph, num_colors)
            elapsed = time.time() - start

            if success:
                title = "Backtracking (Solved)"
                text = f"Backtracking Algorithm:\nSolution found using {num_colors} colors.\nColors: {colors}\nTime: {elapsed:.4f}s\n"
            else:
                title = "Backtracking (Failed)"
                text = f"Backtracking Algorithm:\nNo solution found using {num_colors} colors.\nTime: {elapsed:.4f}s\n"

        elif algo == "cultural":
            try:
                pop = int(self.pop_entry.get())
                gens = int(self.gen_entry.get())
                belief = int(self.belief_entry.get())
                stop_early = self.early_stop_var.get()
            except ValueError:
                self.status_var.set("Error: Invalid CA parameters.")
                return

            best, fit, history = cultural_algorithm(
                self.graph,
                num_colors=num_colors,
                population_size=pop,
                generations=gens,
                belief_size=belief,
                stop_early=stop_early
            )
            colors = best
            elapsed = time.time() - start
            conflicts = int((1 / fit) - 1)
            title = f"Cultural Algorithm (Fit: {fit:.3f})"

            text = (
                f"Cultural Algorithm:\n"
                f"Best fitness = {fit:.6f}\n"
                f"Conflicts = {conflicts} (0 is a solution)\n"
                f"Colors: {colors}\n"
                f"Time: {elapsed:.4f}s\n"
            )

        # Safely update the GUI in the main thread
        self.after(0, self._finish_run, colors, text, title, history)