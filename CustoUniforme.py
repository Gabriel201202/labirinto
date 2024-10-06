from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue

def custo_uniforme(m, start, goal):
    open_list = PriorityQueue()
    open_list.put((0, start))
    g_score = {start: 0}
    ucs_path = {}

    while not open_list.empty():
        currCell = open_list.get()[1]

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

                if childCell not in g_score or temp_g_score < g_score[childCell]:
                    g_score[childCell] = temp_g_score
                    open_list.put((g_score[childCell], childCell))
                    ucs_path[childCell] = currCell

    fwd_path = {}
    cell = goal
    if cell not in ucs_path:
        print("Caminho não encontrado!")
        return None, 0

    total_cost = 0
    while cell != start:
        fwd_path[ucs_path[cell]] = cell
        cell = ucs_path[cell]
        total_cost += 1

    return fwd_path, total_cost


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
        "labirinto - Página1.csv",
        "labirinto - Página2.csv",
        "labirinto - Página3.csv"
    ]

    jogar_fases(labirintos)