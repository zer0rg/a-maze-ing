# A-Maze-Ing

*This project has been created as part of the 42 curriculum by amarcill, rgerman-.*

---

## Description

**A-Maze-Ing** is a maze generator and solver developed in Python. The project allows creating mazes of customizable dimensions, visualizing them in real-time through a graphical interface, and automatically finding the optimal solution between an entry and exit point.

### Main Features

- Maze generation using the **iterative DFS (Depth-First Search) algorithm**
- Real-time visualization with animation of the generation process
- Automatic solving using **bidirectional BFS**
- Support for perfect and imperfect mazes (with multiple paths)
- Configurable seed to reproduce identical mazes
- Background color customization
- Maze export to text file

---

## Instructions

### Prerequisites

- Python 3.10 or higher
- Linux operating system (requires X11 for visualization)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/zer0rg/a-maze-ing.git
cd a-maze-ing
```

2. Install the MLX library (included in the project):
```bash
pip install libs/mlx-2.2-py3-none-any.whl
```

### Execution

```bash
python3 a_maze_ing.py <configuration_file>
```

Example:
```bash
python3 a_maze_ing.py configs/20x20.txt
```

### Interactive Menu Usage

Once executed, the program displays a menu with the following options:

1. **New Maze** - Generate a new maze
   - With animation (slower, shows the process)
   - Without animation (instant rendering)
2. **Show the solution path** - Display the maze solution
3. **Change walls color** - Change walls color (hexadecimal format)
4. **Exit** - Exit the program

**Controls in the graphical window:**
- Press `Q` to abort generation/solving and return to menu

---

## Configuration File

The configuration file is a plain text file with the following format:

```
WIDTH=<width>
HEIGHT=<height>
ENTRY=<x>,<y>
EXIT=<x>,<y>
OUTPUT_FILE=<filename>
PERFECT=<True|False>
SEED=<number>
```

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `WIDTH` | Integer (1-100) | Maze width in cells | Yes |
| `HEIGHT` | Integer (1-100) | Maze height in cells | Yes |
| `ENTRY` | Coordinate (x,y) | Maze entry point | Yes |
| `EXIT` | Coordinate (x,y) | Maze exit point | Yes |
| `OUTPUT_FILE` | String | Output file name | Yes |
| `PERFECT` | Boolean | `True` for perfect maze (single path), `False` to add extra paths | Yes |
| `SEED` | Integer | Seed to reproduce the same maze | No |

### Configuration File Example

```
# 20x20 maze with seed
WIDTH=20
HEIGHT=20
ENTRY=1,1
EXIT=20,20
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=12345
```

> **Note:** Lines starting with `#` are comments and are ignored.

---

## Generation Algorithm

### Iterative DFS (Depth-First Search)

We chose the **iterative DFS with backtracking** algorithm for maze generation.

#### How does it work?

1. A random initial cell is selected
2. It is marked as visited
3. While there are cells in the stack:
   - Get unvisited neighbors of the current cell
   - If there are available neighbors:
     - Choose one randomly
     - Break the wall between the current cell and the chosen one
     - Mark the new cell as visited and add it to the stack
   - If there are no available neighbors:
     - Backtrack (return to the previous element in the stack)

#### Why did we choose this algorithm?

1. **Implementation simplicity**: The algorithm is easy to understand and implement
2. **Long passage mazes**: Generates mazes with long, winding corridors, visually appealing
3. **Memory efficiency**: Using the iterative version with explicit stack, we avoid deep recursion problems
4. **Perfect maze guarantee**: Always generates a perfect maze (exactly one path exists between any pair of cells)
5. **Easy visualization**: The generation process is intuitive and easy to animate step by step

#### Complexity

- **Time**: O(n) where n is the number of cells
- **Space**: O(n) for the stack in the worst case

---

## Solving Algorithm

### Bidirectional BFS

To find the solution, we implemented **bidirectional BFS** which searches simultaneously from the entry and exit.

#### Advantages

- Significantly reduces the search space
- Always finds the shortest path
- More efficient than unidirectional BFS for long distances

---

## Reusable Code

### Independent Modules

| Module | Description | Reusability |
|--------|-------------|-------------|
| `src/Cell.py` | Represents a maze cell | Can be used in any grid/matrix project |
| `src/Generator.py` | DFS maze generator | Reusable for any maze application |
| `src/Solver.py` | Bidirectional BFS solver | Applicable to any graph search problem |
| `src/Config.py` | Configuration parser | Adaptable for other projects with config files |
| `custom_typing/maze.py` | Types and constants | Base for projects with cardinal directions |

### Generator Reuse Example

```python
from src.Config import Config
from src.Generator import Generator

# Create configuration
config = Config("my_config.txt")

# Generate maze with specific seed
generator = Generator(config)
generator.generate()

# Access the generated maze
maze = generator.maze
for coord, cell in maze.items():
    print(f"Cell {coord}: walls={cell.walls}")
```

---

## Team and Project Management

### Team Roles

| Member | Role | Responsibilities |
|--------|------|------------------|
| **amarcill** | Lead Developer | Architecture, generation/solving algorithms, program logic |
| **rgerman-** | Visualization Developer | Rendering, graphical interface, MLX integration |

### Planning

#### Initial Plan
1. **Week 1**: Architecture design and data structures
2. **Week 2**: DFS generator implementation
3. **Week 3**: Solver and rendering implementation
4. **Week 4**: Testing, documentation, and polish

#### Actual Evolution
- MLX integration required more time than expected
- Seed functionality was added for reproducible testing
- Interactive menu was expanded for better UX

### Retrospective

#### ✅ What worked well
- Clear division of responsibilities
- Use of TypeAlias to clarify data types
- Modular architecture that facilitated testing
- Constant communication between team members

#### 🔄 What could be improved
- Add automated unit tests
- Implement more generation algorithms (Prim, Kruskal)
- Improve error handling in the graphical interface
- More detailed inline documentation

### Tools Used

| Tool | Purpose |
|------|---------|
| **Git/GitHub** | Version control and collaboration |
| **VS Code** | Code editor with Python extensions |
| **MLX** | Graphics library for visualization |
| **GitHub Copilot** | Assistance with documentation and refactoring |

---

## Resources

### Official Documentation
- [Python Documentation](https://docs.python.org/3/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)

### Maze Algorithms
- [Maze Generation Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Think Labyrinth - Maze Algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Jamis Buck - Maze Generation](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)

### Bidirectional BFS
- [Bidirectional Search - Wikipedia](https://en.wikipedia.org/wiki/Bidirectional_search)

### AI Usage

**GitHub Copilot** was used as a development assistant for the following tasks:

| Task | Description |
|------|-------------|
| **Documentation** | Generation and translation of docstrings following PEP 257 |
| **Refactoring** | Suggestions to improve code structure |
| **README** | Assistance in writing this document |

> **Note**: All algorithm code (DFS, bidirectional BFS) was manually implemented by the team. AI was primarily used for documentation tasks and readability improvements.

---

## License

This project is part of the 42 educational curriculum and is intended for academic purposes only.

---

## Contact

- **amarcill** - [GitHub](https://github.com/amarcill)
- **rgerman-** - [GitHub](https://github.com/rgerman-)
