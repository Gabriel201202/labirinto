from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(m, start, goal):
    open_list = PriorityQueue()
    open_list.put((0, h(start, goal), start))
    g_score = {start: 0}
    f_score = {start: h(start, goal)}
    a_path = {}

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

                if childCell not in f_score or temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open_list.put((f_score[childCell], h(childCell, goal), childCell))
                    a_path[childCell] = currCell

    fwd_path = {}
    cell = goal
    if cell not in a_path:
        print("Caminho não encontrado!")
        return None

    while cell != start:
        fwd_path[a_path[cell]] = cell
        cell = a_path[cell]

    return fwd_path


if __name__ == '__main__':
    start = tuple(map(int, input('Digite a linha e coluna do ponto inicial (separado por espaço): ').split()))
    goal = tuple(map(int, input('Digite a linha e coluna do ponto final (separado por espaço): ').split()))

    m = maze()
    m.CreateMaze(goal[0], goal[1], loadMaze="labirinto - Página1.csv")

    path = a_star(m, start, goal)

    if path is not None:
        a = agent(m, start[0], start[1], footprints=True)
        m.tracePath({a: path})
        
        # Highlight specific cells using invisible agents
        # highlight_cells = [(1, 1), (3, 3)]
        # for cell in highlight_cells:
        #     highlight_agent = agent(m, cell[0], cell[1], footprints=False,filled=True ,color=COLOR.green)
        
        l = textLabel(m, 'Custo da Solução', len(path) + 1)
        m.run()
    else:
        print("Não foi possível encontrar um caminho do ponto inicial ao ponto final.")