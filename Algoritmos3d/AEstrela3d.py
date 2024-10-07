import csv
import ast
import heapq
import matplotlib.pyplot as plt

def h(cell1, cell2):
    """
    Calcula a distância de Manhattan entre duas células no espaço 3D.
    """
    x1, y1, z1 = cell1
    x2, y2, z2 = cell2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def load_maze_3d(filenames):
    """
    Carrega um labirinto 3D a partir de múltiplos arquivos CSV.

    Parâmetros:
        filenames (list): Lista de nomes de arquivos CSV, cada um representando uma camada do labirinto.

    Retorna:
        dict: Um dicionário mapeando coordenadas de células para suas direções possíveis.
    """
    maze_map = {}
    for z, filename in enumerate(filenames):
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        cell = ast.literal_eval(row['cell'])
                        maze_map[(cell[0], cell[1], z)] = {
                            'E': int(row.get('E', 0)),
                            'W': int(row.get('W', 0)),
                            'N': int(row.get('N', 0)),
                            'S': int(row.get('S', 0)),
                            'U': int(row.get('U', 0)),
                            'D': int(row.get('D', 0))
                        }
                    except (ValueError, SyntaxError) as e:
                        print(f"Erro ao parsear célula {row.get('cell', 'N/A')} no arquivo {filename}: {e}")
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado.")
    return maze_map

def a_star_3d(maze_map, start, goal):
    open_list = []
    heapq.heappush(open_list, (h(start, goal), 0, start))
    g_score = {start: 0}
    a_path = {}

    while open_list:
        current_f, current_g, current = heapq.heappop(open_list)

        if current == goal:
            break

        for direction in 'ESNWUD':
            if maze_map.get(current, {}).get(direction, 0):
                if direction == 'E':
                    neighbor = (current[0], current[1] + 1, current[2])
                elif direction == 'W':
                    neighbor = (current[0], current[1] - 1, current[2])
                elif direction == 'N':
                    neighbor = (current[0] - 1, current[1], current[2])
                elif direction == 'S':
                    neighbor = (current[0] + 1, current[1], current[2])
                elif direction == 'U':
                    neighbor = (current[0], current[1], current[2] + 1)
                elif direction == 'D':
                    neighbor = (current[0], current[1], current[2] - 1)

                # Verificar se o vizinho é uma parede antes de adicionar à lista aberta
                if not is_wall(neighbor, maze_map):
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + h(neighbor, goal)
                        heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))
                        a_path[neighbor] = current

    if goal not in a_path and start != goal:
        print("Caminho não encontrado!")
        return None

    # Reconstruir o caminho
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = a_path.get(current)
        if current is None:
            print("Caminho não encontrado!")
            return None
    path.append(start)
    path.reverse()
    return path

def is_wall(cell, maze_map):
    """
    Verifica se uma célula específica é uma parede.

    Parâmetros:
        cell (tuple): Coordenadas da célula (x, y, z).
        maze_map (dict): Mapa do labirinto 3D.

    Retorna:
        bool: True se a célula for uma parede, False caso contrário.
    """
    dirs = maze_map.get(cell)
    if dirs and dirs['E'] == 0 and dirs['W'] == 0 and dirs['N'] == 0 and dirs['S'] == 0:
        return True
    return False

def plot_maze_3d(maze_map, path=None, start=None, goal=None):
    """
    Plota o labirinto 3D, destacando o caminho encontrado se houver, e as paredes onde E, W, N, S são 0.

    Parâmetros:
        maze_map (dict): Mapa do labirinto 3D.
        path (list, opcional): Lista ordenada de células representando o caminho.
        start (tuple, opcional): Coordenadas da célula inicial.
        goal (tuple, opcional): Coordenadas da célula final.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Separar células com e sem paredes
    wall_cells = [cell for cell, dirs in maze_map.items()
                  if dirs['E'] == 0 and dirs['W'] == 0 and dirs['N'] == 0 and dirs['S'] == 0]
    open_cells = [cell for cell, dirs in maze_map.items()
                  if dirs['E'] == 1 or dirs['W'] == 1 or dirs['N'] == 1 or dirs['S'] == 1]

    # Plotar células sem paredes
    if open_cells:
        x_open, y_open, z_open = zip(*open_cells)
        ax.scatter(x_open, y_open, z_open, color='black', alpha=0.6, label='Células Abertas')

    # Plotar células com paredes
    if wall_cells:
        x_wall, y_wall, z_wall = zip(*wall_cells)
        ax.scatter(x_wall, y_wall, z_wall, color='orange', label='Paredes')

    # Se houver um caminho, destacá-lo
    if path:
        x_path, y_path, z_path = zip(*path)
        ax.plot(x_path, y_path, z_path, color='blue', marker='o', label='Caminho')

    # Destacar início e fim
    if start:
        ax.scatter(*start, color='green', s=100, label='Início')
    if goal:
        ax.scatter(*goal, color='red', s=100, label='Fim')

    ax.set_xlabel('Linha (X)')
    ax.set_ylabel('Coluna (Y)')
    ax.set_zlabel('Camada (Z)')
    ax.legend(loc='upper right')
    plt.show()

def get_input(prompt, maze_map, role):
    while True:
        try:
            coordinates = tuple(map(int, input(prompt).split()))
            if len(coordinates) != 3:
                raise ValueError
            cell = coordinates
            if cell not in maze_map:
                print(f"Célula {cell} não existe no labirinto. Por favor, insira uma célula válida.")
                continue
            if is_wall(cell, maze_map):
                print(f"Célula {cell} é uma parede e não pode ser usada como ponto {role}.")
                continue
            return cell
        except ValueError:
            print("Entrada inválida. Por favor, insira três números inteiros separados por espaço.")

if __name__ == '__main__':
    filenames = ["Algoritmos3d/labirinto - Página1 3d.csv", "Algoritmos3d/labirinto - Página2 3d.csv", "Algoritmos3d/labirinto - Página3 3d.csv"]
    maze_map = load_maze_3d(filenames)

    if not maze_map:
        print("Nenhum labirinto foi carregado. Verifique os arquivos CSV.")
    else:
        start = get_input('Digite a linha, coluna e altura do ponto inicial (separado por espaço): ', maze_map,
                          'início')
        goal = get_input('Digite a linha, coluna e altura do ponto final (separado por espaço): ', maze_map, 'fim')

        if start == goal:
            print("O ponto inicial e final são os mesmos. O caminho é trivial.")
            plot_maze_3d(maze_map, path=[start], start=start, goal=goal)
        else:
            path = a_star_3d(maze_map, start, goal)

            if path:
                plot_maze_3d(maze_map, path, start, goal)
            else:
                print("Não foi possível encontrar um caminho do ponto inicial ao ponto final.")