from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue

def custo_uniforme(m, start, goal):
    open_list = PriorityQueue()
    open_list.put((0, start))
    a_path = {}
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0

    while not open_list.empty():
        curr_cost, currCell = open_list.get()

        if currCell == goal:
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:  # Verifica se há caminho
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)  # Leste
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)  # Oeste
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])  # Norte
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])  # Sul

                temp_g_score = g_score[currCell] + 1

                if temp_g_score < g_score[childCell]:
                    g_score[childCell] = temp_g_score
                    open_list.put((temp_g_score, childCell))
                    a_path[childCell] = currCell

    fwd_path = {}
    if goal in a_path:
        cell = goal
        while cell != start:
            fwd_path[a_path[cell]] = cell
            cell = a_path[cell]

    return fwd_path

if __name__ == '__main__':
    try:
        start = tuple(map(int, input('Digite a linha e coluna do ponto inicial (separado por espaço): ').split()))
        goal = tuple(map(int, input('Digite a linha e coluna do ponto final (separado por espaço): ').split()))

        m = maze()
        m.CreateMaze(goal[0], goal[1], loadMaze="labirinto - Página1.csv")  # Cria o labirinto

        start = (start[0], start[1])
        goal = (goal[0], goal[1])

        if start not in m.grid or goal not in m.grid:
            print("Células de início ou chegada inválidas. Tente novamente.")
        else:
            path = custo_uniforme(m, start, goal)

            if path:
                a = agent(m, start[0], start[1], footprints=True)
                m.tracePath({a: path})
                l = textLabel(m, 'Custo da Solução', len(path) + 1)
                m.run()
            else:
                print("Não foi possível encontrar um caminho do ponto inicial ao ponto final.")
    except ValueError:
        print("Entrada inválida. Por favor, insira números inteiros.")