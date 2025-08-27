from z3 import *
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import importlib.util
import sys
from collections import defaultdict
import re
import networkx as nx
from z3 import Solver, Int, Or, Not
import networkx as nx
from z3 import Int, Or, Solver
from networkx.readwrite import json_graph
import json
import os
import re
import re
import json
import os
import networkx as nx
from networkx.readwrite import json_graph
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash
# Directory to save unique subgraphs
output_dir = "subgraphs"
os.makedirs(output_dir, exist_ok=True)
patterns_hash_set = set()
def parse_constraint(constraint):
    """
    Handles constraints that are either raw tuples or formatted strings.
    Returns extracted nodes or an empty list if the constraint is invalid.
    """
    if isinstance(constraint, tuple):
        # If the constraint is already a tuple, return it inside a list
        return [constraint]

    constraint_str = str(constraint)

    # Regex-based extraction for "no_equal_" constraints
    match = re.match(r"no_equal_\(([\d\s,]+)\)_\(([\d\s,]+)\)", constraint_str)
    if match:
        try:
            node1 = tuple(map(int, match.group(1).split(",")))
            node2 = tuple(map(int, match.group(2).split(",")))
            return [node1, node2]
        except ValueError as e:
            print(f"Error parsing node identifiers in constraint '{constraint_str}': {e}")
            return []
    # Catch-all for invalid constraints
    print(f"Invalid constraint format: {constraint}")
    return []
def extract_unique_patterns(unsat_core, G, node_values, output_dir="output"):
    """
    Processes unsat core constraints to extract unique subgraph patterns.
    Saves unique subgraphs as JSON files.
    """
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    subgraph_nodes = set()
    for constraint in unsat_core:
        # print(f"Processing constraint: {constraint}")
        nodes = parse_constraint(constraint)  # <-- This should correctly parse tuples and strings now

        if isinstance(nodes, list) and len(nodes) > 0:
            for node in nodes:
                if isinstance(node, tuple):
                    subgraph_nodes.add(node)

    print(f"Nodes extracted for the subgraph: {subgraph_nodes}")

    if not subgraph_nodes:
        print("No valid nodes extracted. Skipping subgraph creation.")
        return

    # Create the subgraph
    core_subgraph = G.subgraph(subgraph_nodes).copy()

    # Attach `node_values` as node attributes for visualization
    for node in core_subgraph.nodes():
        core_subgraph.nodes[node]['values'] = node_values.get(node, [])

    # Debug print the subgraph's nodes and edges
    # print(f"Subgraph nodes: {core_subgraph.nodes(data=True)}")
    # print(f"Subgraph edges: {list(core_subgraph.edges())}")

    # Compute WL hash for the subgraph
    wl_hash = weisfeiler_lehman_graph_hash(core_subgraph)
    # print(f"Computed WL hash for subgraph: {wl_hash}")
    # print(patterns_hash_set)
    if wl_hash not in patterns_hash_set:
        patterns_hash_set.add(wl_hash)

        # Serialize the subgraph to JSON
        subgraph_data = json_graph.node_link_data(core_subgraph)
        json_file_path = os.path.join(output_dir, f"subgraph_{wl_hash}.json")

        try:
            with open(json_file_path, "w") as f:
                json.dump(subgraph_data, f, indent=4)
            print(f"Unique subgraph saved to {json_file_path}")
        except IOError as e:
            print(f"Error saving subgraph JSON: {e}")
    else:
        print(f"Duplicate pattern for hash {wl_hash}. Skipping.")



def get_benchmark(name):
    '''
    @type  name: string
    @param name: name of the benchmark to evaluate
    @rtype : (matrix a, pair b, int c)
    @return: a -> sudoku instance,
             b -> tuple of row and column of the chosen cell
             c -> value to be negated
    '''
    # Path to the module
    module_path = "theorems/benchmarks.py"
    module_name = "benchmarks"

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    fn = getattr(module, name)
    return fn()

def add_sudoku_initial_constraints(s, puzzle):

    """
    Add initial Sudoku constraints to the solver.
    @type  solver: Solver
    @param solver: Z3 Solver instance
    @type  puzzle: list[list[int]]
    @param puzzle: 9x9 Sudoku grid
    @rtype : list[list[Int]]
    @return: 9x9 matrix of symbolic integer variables
    """
    grid = [[Int(f'grid_{r}_{c}') for c in range(9)] for r in range(9)]

    # Initial constraints based on the puzzle
    for r_idx in range(9):
        for c_idx in range(9):
            if puzzle[r_idx][c_idx] == 0:
                s.add(grid[r_idx][c_idx] >= 1)
                s.add(grid[r_idx][c_idx] <= 9)
            else:
                s.add(grid[r_idx][c_idx] == puzzle[r_idx][c_idx])

        # Adding row constraints
    for r_idx in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                s.assert_and_track(grid[r_idx][i] != grid[r_idx][j], f"row_({r_idx},{i})_distinct_row_({r_idx},{j})")

    # Adding column constraints
    for c_idx in range(9):
        for i in range(9):
            for j in range(i + 1, 9):
                s.assert_and_track(grid[i][c_idx] != grid[j][c_idx], f"col_({i},{c_idx})_distinct_col_({j},{c_idx})")

    # Adding box constraints
    for x in range(3):
        for y in range(3):
            box_cells = [grid[3 * x + i][3 * y + j] for i in range(3) for j in range(3)]
            for i in range(9):
                for j in range(i + 1, 9):
                    s.assert_and_track(box_cells[i] != box_cells[j], f"box_({x}_{y},{i})distinctbox_({x}_{y},{j})")
    

    return grid

def construct_graph_from_unsat_core(core):
    """
    Construct a graph from the unsat core constraints.
    
    Nodes represent Sudoku cells as (row, column, block). 
    Edges are labeled based on the type of constraint ('row', 'col', 'box').

    @type core: list[str]
    @param core: Unsat core constraints
    @rtype: nx.Graph
    @return: Graph representation of the constraints
    """
    def get_block_index(r, c):
        return 3 * (r // 3) + (c // 3)

    G = nx.Graph()
    for constraint in core:
        constraint_str = constraint.sexpr()
        # Parse row constraints
        if "row_" in constraint_str:
            match = re.findall(r'row_\((\d+),(\d+)\)_distinct_row_\((\d+),(\d+)\)', constraint_str)
            if match:
                r1, c1, r2, c2 = map(int, match[0])
                b1, b2 = get_block_index(r1, c1), get_block_index(r2, c2)
                node1, node2 = (r1, c1, b1), (r2, c2, b2)
                G.add_edge(node1, node2, label="row")

        # Parse column constraints
        elif "col_" in constraint_str:
            match = re.findall(r'col_\((\d+),(\d+)\)_distinct_col_\((\d+),(\d+)\)', constraint_str)
            if match:
                r1, c1, r2, c2 = map(int, match[0])
                b1, b2 = get_block_index(r1, c1), get_block_index(r2, c2)
                node1, node2 = (r1, c1, b1), (r2, c2, b2)
                G.add_edge(node1, node2, label="col")

        # Parse box constraints
        elif "box_" in constraint_str:
            match = re.findall(r'box_\((\d+)_(\d+),(\d+)\)distinctbox_\((\d+)_(\d+),(\d+)\)', constraint_str)
            if match:
                x1, y1, idx1, x2, y2, idx2 = map(int, match[0])
                # Compute row and column from box index
                r1, c1 = 3 * x1 + (idx1 // 3), 3 * y1 + (idx1 % 3)
                r2, c2 = 3 * x2 + (idx2 // 3), 3 * y2 + (idx2 % 3)
                b1, b2 = get_block_index(r1, c1), get_block_index(r2, c2)
                node1, node2 = (r1, c1, b1), (r2, c2, b2)
                G.add_edge(node1, node2, label="box")

    return G

def check_and_propagate(graph, node_values,puzzle):
    """
    Propagate committed values through the graph.
    @type  graph: nx.Graph
    @param graph: Graph of Sudoku constraints
    @type  node_values: defaultdict
    @param node_values: Mapping of nodes to their possible values
    """
    for node in graph.nodes():
        r, c, b = node
        if puzzle[r][c] != 0:
            value = puzzle[r][c]
            node_values[node] = [value] 
    committed = True
    while committed:
        committed = False
        for node in graph.nodes():
            if len(node_values[node]) == 1:
                committed_value = node_values[node][0]
                for neighbor in graph.neighbors(node):
                    if committed_value in node_values[neighbor]:
                        node_values[neighbor].remove(committed_value)
                        committed = True

def finding_patterns(k, graph, node_values):
    """
    Finds patterns in a graph by creating subgraphs centered around each node and analyzing them
    with Z3 to identify satisfiability issues.
    
    @type k: int
    @param k: Maximum distance from the center node to include in the subgraph
    @type graph: nx.Graph
    @param graph: The main graph
    @type node_values: dict
    @param node_values: Dictionary mapping nodes to their possible values
    """
    for center_node in graph.nodes():
        if len(node_values[center_node]) != 1:
            # Generate a subgraph centered around `center_node` with max distance `k`
            subgraph = nx.ego_graph(graph, center_node, radius=k, center=True)
            
            # Initialize solver for this subgraph
            solver = Solver()
            solver.set(':core.minimize', True)
            
            # Declare propositional variables for each node in the subgraph
            propositional_vars = {}
            for node in subgraph.nodes():
                possible_values = node_values[node]
                # Create an Int variable for the node, representing its possible values
                propositional_vars[node] = Int(f"node_{node}")
                # Add constraint: Node must take one of the possible values
                constraint = Or([propositional_vars[node] == value for value in possible_values])
                solver.add(constraint)  # Track constraint with a label
            
            # Add constraints to ensure a node's value cannot be equal to any of its neighbors' values
            for node in subgraph.nodes():
                for neighbor in subgraph.neighbors(node):
                    if neighbor in propositional_vars:
                        solver.assert_and_track((propositional_vars[node] != propositional_vars[neighbor]),
                                                f"no_equal_{node}_{neighbor}")
            
            # Check satisfiability by negating each possible value of the center node
            center_values = node_values[center_node]
            for value in center_values:
                # Negate the specific value for center_node and check satisfiability
                solver.push()  # Save the current solver state
                negated_constraint = Not(propositional_vars[center_node] == value)
                solver.add(negated_constraint)  # Track negation
                if solver.check() == unsat:
                    print(f"Subgraph centered at {center_node}: {value} is unsatisfiable with the node having the value.")
                    # Extract and print the unsat core
                    unsat_core = solver.unsat_core()
                    print("Unsat core constraints:", unsat_core)
                    extract_unique_patterns(unsat_core,graph,node_values,output_dir)
                solver.pop()  # Restore the solver sta``te

            for value in center_values:
                        # Negate the specific value for center_node and check satisfiability
                        solver.push()  # Save the current solver state
                        negated_constraint = (propositional_vars[center_node] == value)
                        # solver.assert_and_track(negated_constraint, f"positive_{center_node}_{value}")  # Track negation
                        if solver.check() == unsat:
                            print(f"Subgraph centered at {center_node}: {value} is unsatisfiable with the node not  having the value.")
                            
                            # Extract and print the unsat core
                            unsat_core = solver.unsat_core()
                            print("Unsat core constraints:", unsat_core)
                            extract_unique_patterns(unsat_core,graph,node_values,output_dir)
                        solver.pop()  # Restore the solver state
  # Restore the solver state


puzzle, (r, c), value = get_benchmark("benchmark1")
s = Solver()
grid = add_sudoku_initial_constraints(s, puzzle)
if s.check() == sat:
    m = s.model()
    # Evaluate the solved grid
    solved_grid = [[m.evaluate(grid[r_idx][c_idx]) for c_idx in range(9)] for r_idx in range(9)]
    # Prevent the same solution from being found again
    s.add(Or([grid[r_idx][c_idx] != solved_grid[r_idx][c_idx]
              for r_idx in range(9) for c_idx in range(9)]))
    if s.check() == unsat:
        unsat_core = s.unsat_core()
        G = construct_graph_from_unsat_core(unsat_core)
        node_values = defaultdict(lambda: list(range(1, 10)))
        check_and_propagate(G, node_values,puzzle)
        for k in range(1, 3):
            print("k: ",k)
            finding_patterns(k, G, node_values)
        print("\nFinal Node Values:")
        # for node, values in node_values.items():
        #     print(f"Node {node}: {values}")