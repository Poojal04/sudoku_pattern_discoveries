# Sudoku Proof Systems

## Project Overview
This undergraduate project aims to identify well-known Sudoku patterns using formal methods, enabling the system to learn them automatically instead of manual discovery. The focus is on developing an inductive learner to generate proof systems for Sudoku solving. By analyzing multiple Sudoku puzzles, the system can detect new patterns within the proof system itself.

## Approach
- Utilizes **Z3 solver** for constraint-based Sudoku solving.
- Applies additional constraints to negate specific cell values to analyze unsatisfiability.
- Extracts minimal constraints (unsat core) to determine key conflicting conditions.
- Represents conflicts as a **graph** to visualize constraint dependencies.
- Implements an **algorithm** to analyze local patterns in Sudoku grids using **ego subgraphs** and satisfiability checks.
- Identifies known patterns like **Naked Pairs** and **X-Wings** by analyzing unsat cores and subgraph structures.

## Key Components
- **Z3 Solver Constraints:**
  - Row, column, and subgrid uniqueness constraints.
  - Negating specific cell values to force unsatisfiability.
- **Unsat Core Analysis:**
  - Extracts minimal conflicting constraints.
  - Used to detect recurring Sudoku-solving patterns.
- **Graph Representation:**
  - Nodes represent Sudoku cells with possible values.
  - Edges represent conflicting constraints (row, column, block constraints).
- **Pattern Detection Algorithm:**
  - Analyzes subgraphs with a radius of **k** to detect local Sudoku patterns.
  - Uses satisfiability checks to infer logical deductions.

## Identified Patterns
- **Naked Pairs:** Two cells in a row/column/block with identical possible values.
- **X-Wings:** A value appearing in only two possible positions in two rows/columns, forming a rectangle that eliminates possibilities elsewhere.
