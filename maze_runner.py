from matplotlib.pyplot import plot, show, xticks, yticks
from numpy import array
from random import randint


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def qpush(self, cell):
        if cell not in self.queue:
            self.queue.append(cell)
        self.queue.sort(key=lambda point: point.f)

    def qpop(self):
        if not self.queue:
            return None
        return self.queue.pop(0)

    def filled(self):
        return True if self.queue else False

    @staticmethod
    def get_cost(target_node, open_nodes):
        for node in open_nodes.queue:
            if node == target_node:
                return node.cost()
        return -1


class Cell:
    def __init__(self, x, y, f, Parent):
        self.x = x
        self.y = y
        self.cartesian = (x, y)
        self.f = f
        self.Parent = Parent

    def cords(self):
        return (self.x, self.y)

    def cost(self):
        return self.f

    def parent(self):
        return self.Parent

    def __eq__(self, other_node):
        return self.x == other_node.x and self.y == other_node.y

    def __contains__(self, iterable):
        for item in iterable:
            if self.cords() == item.cords() and self.parent() == item.parent():
                return True
        return False


MAZE_HEIGHT = 19
MAZE_WIDTH = 19


def main():
    start = (
        randint(0, MAZE_HEIGHT),
        randint(0, MAZE_HEIGHT),
    )  # eval(input("Enter starting co-ordinates: "))
    goal = (
        randint(0, MAZE_HEIGHT),
        randint(0, MAZE_HEIGHT),
    )  # eval(input("Enter goal's co-ordinates: "))
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    obstructions = {
        (randint(0, MAZE_HEIGHT), randint(0, MAZE_WIDTH))
        for i in range((MAZE_HEIGHT * MAZE_WIDTH) // 2)
    }  # eval(input("Enter obstructions' list: "))
    if start in obstructions:
        obstructions.remove(start)
    if goal in obstructions:
        obstructions.remove(goal)
    diagonal_movement = True
    solution, message, explored = solve_maze(
        start, goal, obstructions, diagonal_movement
    )
    print(message)
    plots(
        [item[0] for item in solution],
        [item[1] for item in solution],
        obstructions,
        explored,
        start,
        goal,
    )


def solve_maze(start, goal, obstructions=set(), diagonal_movement=False):
    explored = []
    open_nodes = PriorityQueue()
    open_nodes.qpush(
        Cell(start[0], start[1], f(start, start, goal, diagonal_movement), None)
    )
    while open_nodes.filled():
        current = open_nodes.qpop()
        explored.append(current)
        for node in possible_steps(current.cords(), obstructions, diagonal_movement):
            node = Cell(
                node[0], node[1], f(node, start, goal, diagonal_movement), current
            )
            if node.cords() == goal:
                optimal = reconstructed_path(node)
                explored = set([item.cords() for item in explored])
                return optimal, "Maze Solved.", explored
            elif (
                PriorityQueue.get_cost(node, open_nodes) < node.cost()
                and PriorityQueue.get_cost(node, open_nodes) >= 0
            ):
                continue
            elif node in explored:
                continue
            open_nodes.qpush(node)
    explored = set([item.cords() for item in explored])
    return [], "Path not possible.", explored


def reconstructed_path(node):
    optimal_path = []
    while node:
        optimal_path.append(node.cords())
        node = node.parent()
    return optimal_path[::-1]


def h(node, goal, diagonal_movement):
    if isinstance(node, Cell):
        node = node.cords()
    if isinstance(goal, Cell):
        goal = goal.cords()
    if diagonal_movement:
        return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** (1 / 2)
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def g(node, start, diagonal_movement):
    if isinstance(node, Cell):
        node = node.cords()
    if isinstance(start, Cell):
        start = start.cords()
    if diagonal_movement:
        return ((node[0] - start[0]) ** 2 + (node[1] - start[1]) ** 2) ** (1 / 2)
    return abs(node[0] - start[0]) + abs(node[1] - start[1])


def f(node, start, goal, diagonal_movement):
    return h(node, goal, diagonal_movement) + g(node, start, diagonal_movement)


def plots(xpts, ypts, obstructions, explored, start, goal):
    xticks(array([i for i in range(0, MAZE_WIDTH + 1)]))
    yticks(array([i for i in range(0, MAZE_HEIGHT + 1)]))
    plot(
        array([item[0] for item in obstructions]),
        array([item[1] for item in obstructions]),
        "o",
        color="k",
    )
    plot(
        array([item[0] for item in explored]),
        array([item[1] for item in explored]),
        "o",
        color="b",
    )
    plot(array(xpts), array(ypts), marker="o", color="y")
    plot(array([start[0]]), array([start[1]]), "o", color="g")
    plot(array([goal[0]]), array([goal[1]]), "o", color="r")
    show()


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


if __name__ == "__main__":
    main()
