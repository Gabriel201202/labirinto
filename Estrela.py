from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue


def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(m, start, goal):
    open_list = PriorityQueue()  # O(1) - Inicialização da lista de prioridade
    open_list.put((0, h(start, goal), start))  # O(log n) - Inserção na lista de prioridade
    g_score = {start: 0}  # O(1) - Inicialização da pontuação g
    f_score = {start: h(start, goal)}  # O(1) - Inicialização da pontuação f
    a_path = {}  # O(1) - Inicialização do caminho

    while not open_list.empty():  # O(n log n) - Loop até que a lista esteja vazia, onde n é o número de células
        currCell = open_list.get()[2]  # O(log n) - Remoção do menor elemento da lista de prioridade

        if currCell == goal:  # O(1) - Verificação se o objetivo foi alcançado
            break  # O(1)

        for d in 'ESNW':  # O(4) - Iteração sobre as 4 direções possíveis
            if m.maze_map[currCell][d]:  # O(1) - Verificação se a direção está aberta
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)  # O(1) - Cálculo da célula adjacente
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)  # O(1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])  # O(1)
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])  # O(1)

                temp_g_score = g_score[currCell] + 1  # O(1) - Cálculo do g_score temporário
                temp_f_score = temp_g_score + h(childCell, goal)  # O(1) - Cálculo do f_score temporário

                if childCell not in f_score or temp_f_score < f_score[childCell]:  # O(1) - Verificação da pontuação f
                    g_score[childCell] = temp_g_score  # O(1) - Atualização do g_score
                    f_score[childCell] = temp_f_score  # O(1) - Atualização do f_score
                    open_list.put((f_score[childCell], h(childCell, goal), childCell))  # O(log n) - Inserção na lista de prioridade
                    a_path[childCell] = currCell  # O(1) - Registro do caminho

    fwd_path = {}  # O(1) - Inicialização do caminho final
    cell = goal  # O(1)

    if cell not in a_path:  # O(1) - Verificação se o caminho foi encontrado
        print("Caminho não encontrado!")  # O(1)
        return None, 0  # O(1)

    total_cost = 0  # O(1) - Inicialização do custo total
    while cell != start:  # O(n) - Loop para reconstruir o caminho, onde n é o número de células no caminho
        fwd_path[a_path[cell]] = cell  # O(1) - Registro do caminho
        cell = a_path[cell]  # O(1) - Atualização da célula
        total_cost += 1  # O(1) - Incremento do custo

    return fwd_path, total_cost  # O(1) - Retorno do caminho e do custo total



def jogar_fases(labirintos):
    """Função para rodar múltiplas fases (labirintos) sequencialmente e calcular o custo total"""
    fase_atual = 1
    custo_total = 0  # Variável para armazenar o custo acumulado

    start = tuple(map(int, input('Digite a linha e coluna do ponto inicial (separado por espaço): ').split()))

    for labirinto in labirintos:
        print(f"\nFase {fase_atual}: {labirinto}")

        if fase_atual == 1:
            goal = tuple(map(int, input('Digite a linha e coluna do ponto final (separado por espaço): ').split()))
        else:
            start = prev_goal  # Usa o ponto final anterior como ponto inicial da fase atual
            goal = tuple(map(int, input(f'Digite a linha e coluna do ponto final para a fase {fase_atual} (separado por espaço): ').split()))

        m = maze()
        m.CreateMaze(goal[0], goal[1], loadMaze=labirinto, theme=COLOR.black)

        path, custo_fase = a_star(m, start, goal)

        if path is None:
            print(f"Você falhou na fase {fase_atual}! Tente novamente.")
            break

        a = agent(m, start[0], start[1], footprints=True, shape='square', filled=True)
        m.tracePath({a: path})

        l = textLabel(m, f'Custo da Solução - Fase {fase_atual}', custo_fase)
        m.run()

        custo_total += custo_fase
        print(f"Parabéns! Você completou a fase {fase_atual}. Custo dessa fase: {custo_fase}")

        prev_goal = goal  # Atualiza o ponto final anterior para ser o ponto inicial da próxima fase

        fase_atual += 1

    if fase_atual > len(labirintos):
        print(f"Você completou todas as fases! Custo total: {custo_total}")


if __name__ == '__main__':
    labirintos = [
        "labirinto - Página1.csv",
        "labirinto - Página2.csv",
        "labirinto - Página3.csv"
    ]

    # Chama a função para jogar as fases
    jogar_fases(labirintos)