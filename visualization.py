import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

COLOR_PALETTE = [
    "#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93",
    "#FF9F1C", "#00A6A6", "#9B5DE5", "#F15BB5", "#2EC4B6",
    "#E71D36", "#007F5F", "#6A0572"
]


def visualize_on_tk(frame: tk.Frame, graph: nx.Graph, colors: list, title: str = "Graph Coloring"):
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(title)
    pos = nx.spring_layout(graph, seed=42)

    ordered_nodes = sorted(graph.nodes())
    node_colors_map = {node: COLOR_PALETTE[colors[i] - 1]
    if colors[i] > 0 and colors[i] <= len(COLOR_PALETTE)
    else "#CCCCCC"
       for i, node in enumerate(ordered_nodes)}

    node_color_list = [node_colors_map.get(node, "#CCCCCC") for node in graph.nodes()]

    nx.draw(graph, pos, ax=ax, with_labels=True,
            node_color=node_color_list, node_size=700, font_color="white", font_weight="bold")

    for w in frame.winfo_children():
        w.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    #


def visualize_fitness_plot(frame: tk.Frame, history: list):
    for w in frame.winfo_children():
        w.destroy()

    if not history:
        return

    fig = plt.Figure(figsize=(6, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(history)
    ax.set_title("Cultural Algorithm Performance")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness (1.0 = Solved)")
    ax.grid(True)



    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)