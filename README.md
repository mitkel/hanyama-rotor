# Hanayama Rotor Solver

This command-line interface (CLI) client is designed to solve and visualize the Hanayama rotor puzzle.
By inputting an initial and a final state, the client computes the shortest path between these two states, if one exists, and can visualize the state space of the puzzle.

## Features
- **Solve Puzzles:** Find the shortest path from an initial state to a final state.
- **Visualize Solutions:** Optionally generate visualizations of the puzzle's state space and the solution path.
- **Customizable States:** Input custom initial and final states for the puzzle.

## Installation
1. Clone the repository:
```bash
git clone git@github.com:mitkel/hanyama-rotor.git
cd hanayama-rotor
```
2. Install dependencies:
```bash
conda env create --file environment.yml
```

**Note:** This tool requires Graphviz to be installed for generating visualizations.
Graphviz is an open-source graph visualization software that is not included with this package and must be installed separately.
Please follow the installation instructions on the Graphviz website for your operating system.
After installing Graphviz, ensure that the dot executable is in your system's PATH so that it can be used by this tool.

## Usage
Run the client from the command line, specifying the initial state, final state, and whether to visualize the solution.

### Basic syntax
```bash
python cli.py [options]
```

### Options
- `--initial-state <state>`: Specifies the initial state of the puzzle. The state should be a string representation of the puzzle's configuration.
- `--final-state <state>`: Specifies the final state of the puzzle you aim to achieve.
- `--visualize`: Enables visualization of the state space and solution path. Visualizations will be saved to the specified path.

### Examples
1. Find a solution from the default initial state to the default final state:
```bash
python cli.py
```
2. Solve the puzzle with custom initial and final states
```bash
python cli.py --initial-state "+01+12" --final-state "+11-01"
```
3. Solve the puzzle and visualize the state space
```bash
python cli.py --visualize --initial-state "+01+12" --final-state "+11-01"
```

## Puzzle State Representation
The puzzle state is represented as a 6 character string.
First 3 charaters describe the position of the golden part and last 3 characters describe the position of the silver part.

- The first character indicates the orientation (+ for positive, - for negative). Orientation depends on the side the "ROTOR" sign is facing.
- The second character represents the position of the inner axis, counting clockwise from zero starting with the narrowest arm.
- The third character represents the position of the outer axis, counting clockwise from zero starting with the widest loop.

![Axes names][./res/gold-element-position.jpeg]

For example, "+20" represents an element with a positive orientation, an inner axis position of 2, and an outer axis position of 0.