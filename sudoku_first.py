from z3 import *
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def get_benchmark(name):
    '''
    @type  name: string
    @param name: name of the benchmark to evaluate
    @rtype : (matrix a, pair b, int c)
    @return: a -> sudoku instance,
             b -> tuple of row and column of the chosen cell
             c -> value to be negated
    '''
    import imp

    # Path to the module
    module_path = "./benchmarks.py"
    module_name = "benchmarks.py"

    module = imp.load_source(module_name, module_path)
    fn = getattr(module, name)
    return fn()


puzzle, (r, c), value = get_benchmark('benchmark5')

s = Solver()
s.set(':core.minimize', True)
grid = [[Int(f'grid_{r}_{c}') for c in range(9)] for r in range(9)]

for r_idx in range(9):
    for c_idx in range(9):
        if puzzle[r_idx][c_idx] == 0:
            s.assert_and_track(grid[r_idx][c_idx] >= 1, f"cell_range_r{r_idx}_c{c_idx}_min")
            s.assert_and_track(grid[r_idx][c_idx] <= 9, f"cell_range_r{r_idx}_c{c_idx}_max")
        else:
            s.assert_and_track(grid[r_idx][c_idx] == puzzle[r_idx][c_idx], f"puzzle_value_r{r_idx}_c{c_idx}")

for r_idx in range(9):
    s.assert_and_track(Distinct(grid[r_idx]), f"row_{r_idx}_distinct")

for c_idx in range(9):
    s.assert_and_track(Distinct([grid[r_idx][c_idx] for r_idx in range(9)]), f"col_{c_idx}_distinct")

for x in range(3):
    for y in range(3):
        s.assert_and_track(Distinct([grid[3 * x + i][3 * y + j] for i in range(3) for j in range(3)]), f"box_{x}_{y}_distinct")

forced_constraint = Not(grid[r][c] == value)  
s.assert_and_track(forced_constraint, f"negated_value_r{r}_c{c}")

if s.check() == unsat:
    print("The negated forced value leads to unsatisfiability.")
    core = s.unsat_core()
    print("Conflicting constraints:")
    for constraint in core:
        print(constraint)

    core_cells = set()
    for constraint in core:
        name = constraint.sexpr()
        if "puzzle_value" in name or "cell_range" in name: 
            parts = name.split("_")
            if len(parts) >= 4:
                r, c = int(parts[2][1]), int(parts[3][1])
                core_cells.add((r, c))

    unsat_df = pd.DataFrame(puzzle)
    unsat_df.replace(0, np.nan, inplace=True)

    plt.figure(figsize=(8, 8))
    ax = sns.heatmap(unsat_df, annot=True, fmt="g", cbar=False, cmap="Blues", linewidths=2, linecolor='black',
                     annot_kws={"size": 16}, square=True)

    for (r, c) in core_cells:
        ax.add_patch(plt.Rectangle((c, r), 1, 1, fill=False, edgecolor='red', lw=3))

    plt.title('Sudoku Grid with Conflicting Constraints Highlighted', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14, rotation=0)
    plt.show()

else:
    m = s.model()
    solution = [[m.evaluate(grid[r][c]).as_long() for c in range(9)] for r in range(9)]
    df = pd.DataFrame(solution)
    df.replace(0, np.nan, inplace=True)

    plt.figure(figsize=(8, 8))
    ax = sns.heatmap(df, annot=True, fmt="g", cbar=False, cmap="Blues", linewidths=2, linecolor='black',
                     annot_kws={"size": 16}, square=True)
    plt.title('Sudoku Solution Grid with Colors', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14, rotation=0)
    plt.show()
