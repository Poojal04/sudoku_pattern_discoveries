import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Example Sudoku grid
sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Convert the Sudoku grid to a DataFrame
df = pd.DataFrame(sudoku_grid)

# Replace zeros with empty strings to represent empty cells
df.replace(0, "", inplace=True)

# Display the DataFrame as a table
print(df)

# Replacing None with np.nan for better handling in the plot
df = pd.DataFrame(sudoku_grid)
df.replace(0, np.nan, inplace=True)
# Create a colored plot with NaNs
plt.figure(figsize=(8, 8))
ax = sns.heatmap(df, annot=True, fmt="g", cbar=False, cmap="Blues", linewidths=2, linecolor='black',
                 annot_kws={"size": 16}, square=True)
# Adjust the plot aesthetics
plt.title('Sudoku Grid with Colors', fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14, rotation=0)
plt.show()
