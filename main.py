from pyamaze import maze, agent, textLabel
from queue import PriorityQueue


def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(m):
    start = (m.rows, m.cols)
    goal = (1, 1)

    open_list = PriorityQueue()
    open_list.put((h(start, goal), h(start, goal), start))

    a_path = {}
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0

    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)

    while not open_list.empty():
        currCell = open_list.get()[2]

        if currCell == goal:
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, goal)

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open_list.put((f_score[childCell], h(childCell, goal), childCell))
                    a_path[childCell] = currCell

    fwd_path = {}
    cell = goal
    while cell != start:
        fwd_path[a_path[cell]] = cell
        cell = a_path[cell]

    return fwd_path


if __name__ == '__main__':
    m = maze()
    m.CreateMaze(loadMaze="labirinto - Página1.csv")

    path = a_star(m)

    a = agent(m, footprints=True)
    m.tracePath({a: path})

    l = textLabel(m, 'Custo da Solução', len(path) + 1)

    m.run()
