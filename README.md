# 🧭 Dijkstra's Pathfinder

A **Python** project visualizing **Dijkstra's pathfinding algorithm** using **Pygame** and **Tkinter**. This application allows users to set a start point, a target, and obstacles on a grid, then finds the shortest path using Dijkstra's algorithm.

## 🎯 Features
- **Interactive Grid:** Create obstacles, define a starting point, and set a target for the algorithm.
- **Visualization:** See each step of the algorithm in real-time, with cells color-coded to show different states.
- **Control Buttons:** Start or reset the pathfinding process with a single click.

## ⚙️ Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Dijkstra-Pathfinder.git
    ```
2. **Install required libraries:**
    ```bash
    pip install pygame
    ```
3. **Run the application:**
    ```bash
    python dijkstra_pathfinder.py
    ```

## 🧩 How to Use

1. **Set Start Point:** Left-click on any cell to set the start point.
2. **Set Walls:** Left-click on other cells to add obstacles.
3. **Set Target Point:** Right-click on a cell to set the target.
4. **Run Pathfinding:** Click on **START** to run the Dijkstra algorithm.
5. **Reset Grid:** Click on **RESET** to clear the grid and start over.

## 🖌️ Color Key
| Color | Meaning        |
|-------|----------------|
| Light Blue | Start point |
| Yellow     | Target point |
| Gray       | Unvisited cell |
| Black      | Wall/obstacle |
| Light Green | Visited cell |
| Orange     | Path traced back to the start |

## 🛠️ Code Overview

- **`Box` Class:** Represents each cell in the grid, tracks properties like walls, visited status, and neighbors.
- **Pathfinding Logic:** Implements Dijkstra's algorithm by exploring cells until the target is found.
- **GUI and Control Logic:** Pygame-based grid and Tkinter message boxes to enhance user interactivity.

## 📋 Project Structure

```plaintext
.
├── dijkstra_pathfinder.py      # Main program file
├── README.md                   # Project README file
```

## ✨ Future Enhancements
- Add support for **weighted pathfinding** (considering different terrain types).
- Include **A* Algorithm** for comparison with Dijkstra's algorithm.
- Add a **Save & Load** feature for custom grid setups.

## 👥 Contributors

- **Muskan(https://github.com/bhmuskan)** - Author

## 📄 License
This project is licensed under the MIT License.

---
