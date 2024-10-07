from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue

#28 + n log n + 2log n + 2n
def custo_uniforme(m, start, goal):
    open_list = PriorityQueue()  # 1
    open_list.put((0, start))  # 1
    g_score = {start: 0}  #1
    ucs_path = {}  # 1

    while not open_list.empty():  # n log n
        currCell = open_list.get()[1]  # n

        if currCell == goal:  # 1
            break

        for d in 'ESNW':  # n
            if m.maze_map[currCell][d]:  # 1
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)  # 2
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)  # 2
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])  # 2
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])  # 2

                temp_g_score = g_score[currCell] + 1  # 1

                if childCell not in g_score or temp_g_score < g_score[childCell]:  # 1
                    g_score[childCell] = temp_g_score  # 1
                    open_list.put((g_score[childCell], childCell))  # log n
                    ucs_path[childCell] = currCell  # 1

    fwd_path = {}  # 1
    cell = goal  # 1
    if cell not in ucs_path:  # 1
        print("Caminho não encontrado!")  # 1
        return None, 0  # 1

    total_cost = 0  # 1
    while cell != start:  # n
        fwd_path[ucs_path[cell]] = cell  # 1
        cell = ucs_path[cell]  # 1
        total_cost += 1  # 1

    return fwd_path, total_cost  # 1

def jogar_fases(labirintos):
    """Função para rodar múltiplas fases (labirintos) sequencialmente e calcular o custo total"""
    fase_atual = 1
    custo_total = 0

    start = tuple(map(int, input('Digite a linha e coluna do ponto inicial (separado por espaço): ').split()))
    goal = tuple(map(int, input('Digite a linha e coluna do ponto final (separado por espaço): ').split()))

    for labirinto in labirintos:
        print(f"\nFase {fase_atual}: {labirinto}")

        if fase_atual > 1:
            start = prev_goal
            goal = tuple(map(int, input(f'Digite a linha e coluna do ponto final para a fase {fase_atual} (separado por espaço): ').split()))

        m = maze()
        m.CreateMaze(goal[0], goal[1], loadMaze=labirinto, theme=COLOR.black)

        path, custo_fase = custo_uniforme(m, start, goal)

        if path is None:
            print(f"Você falhou na fase {fase_atual}! Tente novamente.")
            break

        a = agent(m, start[0], start[1], footprints=True, shape='square', filled=True)
        m.tracePath({a: path})

        l = textLabel(m, f'Custo da Solução - Fase {fase_atual}', custo_fase)
        m.run()

        custo_total += custo_fase
        print(f"Parabéns! Você completou a fase {fase_atual}. Custo dessa fase: {custo_fase}")

        prev_goal = goal

        fase_atual += 1

    if fase_atual > len(labirintos):
        print(f"Você completou todas as fases! Custo total: {custo_total}")

if __name__ == '__main__':
    labirintos = [
        "labirinto - Página1 2d.csv",
        "labirinto - Página2 2d.csv",
        "labirinto - Página3 2d.csv"
    ]

    jogar_fases(labirintos)