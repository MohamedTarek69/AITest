import random
import networkx as nx


# --- Utility Functions ---

def fitness(graph: nx.Graph, colors: list) -> float:
    """Calculates the fitness based on the number of conflicts (edges connecting same-colored nodes)."""
    conflicts = 0
    # Create a color map {node: color} based on the ascending order of nodes (0, 1, 2,...)
    ordered_nodes = sorted(graph.nodes())
    color_map = {node: colors[i] for i, node in enumerate(ordered_nodes)}

    for u, v in graph.edges():
        if color_map.get(u) == color_map.get(v):
            conflicts += 1
    return 1.0 / (1 + conflicts)


def mutate(colors: list, num_colors: int) -> list:
    """Applies mutation by randomly changing the color of one node."""
    new_colors = colors[:]
    if not new_colors:
        return []

    node = random.randint(0, len(colors) - 1)
    new_colors[node] = random.randint(1, num_colors)
    return new_colors


def crossover(p1: list, p2: list) -> list:
    """Performs single-point crossover between two parents."""
    if len(p1) < 2:
        return p1[:]
    cut = random.randint(1, len(p1) - 1)
    return p1[:cut] + p2[cut:]


# --- Cultural Algorithm ---

def cultural_algorithm(graph: nx.Graph, num_colors: int = 3, population_size: int = 30,
                       generations: int = 300, belief_size: int = 5, stop_early: bool = True):
    """
    Implements the Cultural Algorithm for graph coloring.
    Returns: (best_colors, best_fit, fitness_history)
    """
    n = graph.number_of_nodes()
    if n == 0:
        return [], 0.0, []

    population = [[random.randint(1, num_colors) for _ in range(n)]
                  for _ in range(population_size)]
    belief_space = []
    fitness_history = []

    for gen in range(generations):
        fits = [fitness(graph, ind) for ind in population]
        best_idx = max(range(len(fits)), key=lambda i: fits[i])
        best = population[best_idx][:]
        best_fit = fits[best_idx]

        fitness_history.append(best_fit)

        # Early stopping logic
        if stop_early and best_fit == 1.0:
            break

        belief_space.append(best[:])
        if len(belief_space) > belief_size:
            belief_space.pop(0)

        new_pop = [best[:]]  # Elitism

        while len(new_pop) < population_size:
            # Parent selection (influenced by belief space)
            parent1 = random.choice(belief_space) if belief_space and random.random() < 0.7 else random.choice(
                population)
            parent2 = random.choice(population)

            child = crossover(parent1, parent2)

            # Influence phase from belief space
            if belief_space and random.random() < 0.5:
                for i in range(n):
                    if random.random() < 0.12:
                        child[i] = random.choice([b[i] for b in belief_space])

            # Mutation
            if random.random() < 0.25:
                child = mutate(child, num_colors)

            new_pop.append(child)

        population = new_pop

    return best, best_fit, fitness_history


# --- Backtracking Algorithm ---

def order_nodes_by_degree(graph: nx.Graph) -> list:
    """Sorts nodes by degree descending (Most Constrained Variable heuristic)."""
    return sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)


def is_safe_bt(graph: nx.Graph, node: int, color: int, colors: dict) -> bool:
    """Checks if assigning a color to a node is safe (no neighbor has the same color)."""
    for neighbor in graph.neighbors(node):
        if colors.get(neighbor) == color:
            return False
    return True


def backtracking_coloring(graph: nx.Graph, num_colors: int):
    """
    Implements the Backtracking (Greedy) algorithm for graph coloring.
    Returns: (success: bool, ordered_colors: list)
    """
    colors = {node: 0 for node in graph.nodes()}
    order = order_nodes_by_degree(graph)

    node_to_idx = {node: i for i, node in enumerate(sorted(graph.nodes()))}
    result_list = [0] * graph.number_of_nodes()

    def helper(idx: int) -> bool:
        if idx == len(order):
            return True
        node = order[idx]
        for c in range(1, num_colors + 1):
            if is_safe_bt(graph, node, c, colors):
                colors[node] = c
                if helper(idx + 1):
                    return True
                colors[node] = 0  # Backtrack
        return False

    success = helper(0)

    # Convert dictionary colors to an ordered list (0, 1, 2,...)
    if success:
        for node, color in colors.items():
            result_list[node_to_idx[node]] = color

    return success, result_list