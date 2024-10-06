from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue

def custo_uniforme(m, start, goal):
    open_list = PriorityQueue()  # O(1): criação da lista de prioridades
    open_list.put((0, start))  # O(log n): inserção do ponto inicial na fila
    g_score = {start: 0}  # O(1): inicialização do dicionário g_score
    ucs_path = {}  # O(1): inicialização do dicionário ucs_path

    while not open_list.empty():  # O(n): laço que itera até que a fila esteja vazia
        currCell = open_list.get()[1]  # O(log n): remoção da célula com menor custo

        if currCell == goal:  # O(1): verificação se a célula atual é o objetivo
            break

        for d in 'ESNW':  # O(1): iterando sobre as direções (norte, sul, leste, oeste)
            if m.maze_map[currCell][d]:  # O(1): verificação se o movimento na direção d é válido
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)  # O(1): criação da célula do filho
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)  # O(1): criação da célula do filho
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])  # O(1): criação da célula do filho
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])  # O(1): criação da célula do filho

                temp_g_score = g_score[currCell] + 1  # O(1): cálculo do novo custo g

                if childCell not in g_score or temp_g_score < g_score[childCell]:  # O(1): verificação de custo
                    g_score[childCell] = temp_g_score  # O(1): atualização do custo g para a célula filha
                    open_list.put((g_score[childCell], childCell))  # O(log n): inserção na fila de prioridade
                    ucs_path[childCell] = currCell  # O(1): armazenar a célula atual como pai da célula filha

    fwd_path = {}  # O(1): inicialização do dicionário fwd_path
    cell = goal  # O(1): inicialização da célula com o objetivo
    if cell not in ucs_path:  # O(1): verificação se o caminho foi encontrado
        print("Caminho não encontrado!")  # O(1): mensagem de erro
        return None, 0  # O(1): retorno se o caminho não foi encontrado

    total_cost = 0  # O(1): inicialização do custo total
    while cell != start:  # O(n): itera até que a célula seja a inicial
        fwd_path[ucs_path[cell]] = cell  # O(1): armazenar o caminho
        cell = ucs_path[cell]  # O(1): atualizar a célula para o pai
        total_cost += 1  # O(1): incrementar o custo total

    return fwd_path, total_cost  # O(1): retorno do caminho e custo total


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