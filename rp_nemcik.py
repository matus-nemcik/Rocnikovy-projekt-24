import itertools

'''    pracujeme s neorientovanym kubickm grafom    '''

def correct_input(vertex_count, edge_count):
    if vertex_count % 2 != 0: 
        print("Počet vrcholov musí byť párny.") 
        exit()
    if vertex_count < 4: 
        print("Počet vrcholov, musí byť väčší ako 4")
        exit()
    if edge_count != vertex_count * 3 // 2:
        print("Nesprávny počet hrán, vzhľadom na počet vrcholov.")
        exit()

def correct_uv(vertex_count, u, v):
    if u < 0 or v < 0 or u >= vertex_count or v >= vertex_count:
        print("Nesprávne vrcholy")
        exit()
    if v in graph[u]:
        print("Hrana už bola definovaná")
        exit()
    if u == v:
        print("Kubický graf nieosahuje slučky")
        exit()
    if len(graph[u]) >= 3 or len(graph[v]) >= 3:
        print("Kubický graf nemôže mať viac ako 3 susedov na vrchole.")
        exit()

# VSTUP
vertex_count, edge_count = map(int, input().split())
correct_input(vertex_count, edge_count)
graph = [[] for _ in range(vertex_count)]  # Ukladame ako zoznam susedov (indexujeme od 0)

for _ in range(edge_count):
    u, v = map(int, input().split())  # Hrana medzi u a v
    correct_uv(vertex_count, u, v)
    graph[u].append(v)  
    graph[v].append(u)

# HLADANIE POKRYTIA VRCHOLOV, CO NAJMENEJ CESTAMI, vyuzitim brute force algoritmu
def is_path(graph, path):
    """
    Funkcia na overenie, či je cesta validna
    """
    for vertex in range(len(path)-1):
        u, v = path[vertex], path[vertex+1]
        # Overenie, že medzi u a v existuje hrana v grafe
        if v not in graph[u]:
            return False
    return True

def find_min_covering_paths(graph, vertex_count):
    """
    Nájde najmenší počet ciest potrebných na pokrytie všetkých vrcholov grafu.
    """
    vertices = list(range(vertex_count))  # Vrcholy grafu
    best_paths = []

    # Generujeme všetky platné cesty (permútácie rôznych dĺžok)
    all_paths = []
    for r in range(1, vertex_count + 1):
        for perm in itertools.permutations(vertices, r):
            if is_path(graph, perm):
                all_paths.append(perm)
    
    # Hľadáme najmenšiu kombináciu ciest, ktorá pokryje všetky vrcholy
    for path_set_size in range(1, vertex_count + 1):
        for path_combination in itertools.combinations(all_paths, path_set_size):
            covered = set()
            for path in path_combination:
                covered.update(path)
            if len(covered) == len(vertices):  # Ak sú všetky vrcholy pokryté
                best_paths = path_combination
                return best_paths  # Vrátime najlepšie pokrytie

    return best_paths  # Ak nenájdeme, vrátime prázdny zoznam

#VÝSTUP
result = find_min_covering_paths(graph, vertex_count)
print("Najlepšie pokrytie vrcholov cestami:")
for path in result:
    print(path)



'''

1.VSTUP: (Najjednosuchší kubický graf)
4 6
0 1
0 3
1 2
2 3
1 3
0 2


2.VSTUP: (Petersenov graf)
10 15
0 4
0 6
0 1
1 7
1 2
2 8
2 3
3 9
3 4
4 5
5 7
5 8
6 8
6 9
7 9

3.VSTUP:
8 12
0 1
0 2
0 3
1 4
1 5
2 6
2 7
3 4
3 6
5 7
5 6
4 7

'''