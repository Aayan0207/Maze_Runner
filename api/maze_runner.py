from heapq import heappush, heappop

MAZE_HEIGHT = 19
MAZE_WIDTH = 19


class Cell:
    def __init__(self, x, y, f, Parent):
        self.x = x
        self.y = y
        self.f = f
        self.parent = Parent

    def coords(self):
        return (self.x, self.y)

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def solve_maze(start, goal, obstructions=None, diagonal_movement=False):
    if not obstructions:
        obstructions = set()
    explored = set()
    open_nodes = []  # Heap
    start_cell = Cell(
        start[0], start[1], f(start, start, goal, diagonal_movement), None
    )
    heappush(open_nodes, start_cell)
    while open_nodes:
        current = heappop(open_nodes)
        explored.add(current)
        for node in possible_steps(current.coords(), obstructions, diagonal_movement):
            node = Cell(
                node[0], node[1], f(node, start, goal, diagonal_movement), current
            )
            if node.coords() == goal:
                optimal = reconstructed_path(node)
                return optimal, "Maze Solved.", [item.coords() for item in explored]
            if node in explored:
                continue
            heappush(open_nodes, node)
    return [], "Path not possible.", [item.coords() for item in explored]


def reconstructed_path(node):
    optimal_path = []
    while node:
        optimal_path.append(node.coords())
        node = node.parent
    return optimal_path[::-1]


def h(node, goal, diagonal_movement):
    if isinstance(node, Cell):
        node = node.coords()
    if isinstance(goal, Cell):
        goal = goal.coords()
    if diagonal_movement:
        return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** (1 / 2)
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def g(node, start, diagonal_movement):
    if isinstance(node, Cell):
        node = node.coords()
    if isinstance(start, Cell):
        start = start.coords()
    if diagonal_movement:
        return ((node[0] - start[0]) ** 2 + (node[1] - start[1]) ** 2) ** (1 / 2)
    return abs(node[0] - start[0]) + abs(node[1] - start[1])


def f(node, start, goal, diagonal_movement):
    return h(node, goal, diagonal_movement) + g(node, start, diagonal_movement)


def possible_steps(cell, obstructions, diagonal_movement):
    steps = [
        (cell[0], cell[1] - 1),
        (cell[0], cell[1] + 1),
        (cell[0] - 1, cell[1]),
        (cell[0] + 1, cell[1]),
    ]
    if diagonal_movement:
        steps.extend(
            [
                (cell[0] + 1, cell[1] + 1),
                (cell[0] + 1, cell[1] - 1),
                (cell[0] - 1, cell[1] + 1),
                (cell[0] - 1, cell[1] - 1),
            ]
        )
    for step in steps[:]:
        if (
            step in obstructions
            or step[0] < 0
            or step[0] > MAZE_HEIGHT
            or step[1] < 0
            or step[1] > MAZE_WIDTH
        ):
            steps.remove(step)
    return steps
