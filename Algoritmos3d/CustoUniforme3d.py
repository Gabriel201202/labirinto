import csv
import ast
import heapq
import matplotlib.pyplot as plt

def load_maze_3d(filenames):
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

# O(N⋅6)+O(N⋅logN)
def custo_uniforme_3d(maze_map, start, goal):
    open_list = []  # 1
    heapq.heappush(open_list, (0, start))  # log N
    g_score = {start: 0}  # 1
    ucs_path = {}  # 1

    while open_list:  # N
        current_g, current = heapq.heappop(open_list)  # log N

        if current == goal:  # 1
            break  # 1

        for direction in 'ESNWUD':  # 6
            if maze_map.get(current, {}).get(direction, 0):  # 1
                if direction == 'E':
                    neighbor = (current[0], current[1] + 1, current[2])  # 1
                elif direction == 'W':
                    neighbor = (current[0], current[1] - 1, current[2])  # 1
                elif direction == 'N':
                    neighbor = (current[0] - 1, current[1], current[2])  # 1
                elif direction == 'S':
                    neighbor = (current[0] + 1, current[1], current[2])  # 1
                elif direction == 'U':
                    neighbor = (current[0], current[1], current[2] + 1)  # 1
                elif direction == 'D':
                    neighbor = (current[0], current[1], current[2] - 1)  # 1

                # Verifica se o vizinho não é uma parede
                if is_wall(neighbor, maze_map):  # 1
                    continue  # 1

                tentative_g_score = g_score[current] + 1  # 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:  # 2
                    g_score[neighbor] = tentative_g_score  # 1
                    heapq.heappush(open_list, (tentative_g_score, neighbor))  # log N
                    ucs_path[neighbor] = current  # 1

    if goal not in ucs_path:  # 1
        print("Caminho não encontrado!")  # 1
        return None  # 1

    path = []  # 1
    current = goal  # 1
    while current != start:  # N
        path.append(current)  # 1
        current = ucs_path.get(current)  # 1
        if current is None:  # 1
            print("Caminho não encontrado!")  # 1
            return None  # 1
    path.append(start)  # 1
    path.reverse()  # 1
    return path  # 1

def is_wall(cell, maze_map):
    dirs = maze_map.get(cell)
    if dirs and dirs['E'] == 0 and dirs['W'] == 0 and dirs['N'] == 0 and dirs['S'] == 0:
        return True
    return False

def plot_maze_3d(maze_map, path=None, start=None, goal=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    wall_cells = [cell for cell, dirs in maze_map.items() if is_wall(cell, maze_map)]
    open_cells = [cell for cell, dirs in maze_map.items() if not is_wall(cell, maze_map)]

    if open_cells:
        x_open, y_open, z_open = zip(*open_cells)
        ax.scatter(x_open, y_open, z_open, color='black', alpha=0.6, label='Células Abertas')

    if wall_cells:
        x_wall, y_wall, z_wall = zip(*wall_cells)
        ax.scatter(x_wall, y_wall, z_wall, color='orange', label='Paredes')

    if path:
        x_path, y_path, z_path = zip(*path)
        ax.plot(x_path, y_path, z_path, color='blue', marker='o', label='Caminho')

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
        start = get_input('Digite a linha, coluna e altura do ponto inicial (separado por espaço): ', maze_map, 'início')
        goal = get_input('Digite a linha, coluna e altura do ponto final (separado por espaço): ', maze_map, 'fim')

        if start == goal:
            print("O ponto inicial e final são os mesmos. O caminho é trivial.")
            plot_maze_3d(maze_map, path=[start], start=start, goal=goal)
        else:
            path = custo_uniforme_3d(maze_map, start, goal)

            if path:
                plot_maze_3d(maze_map, path, start, goal)
            else:
                print("Não foi possível encontrar um caminho do ponto inicial ao ponto final.")
