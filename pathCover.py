# =============================================================
# HLAVNY SPUSTITELNY SUBOR — Path Cover pomocou SAT solvera
# ZADAJTE CESTU K VASMU MINISAT SOLVERU nizsie ↓↓↓
# =============================================================

import sat

# sem zadajte cestu k Vasmu minisatu
SAT_SOLVER_PATH = "/opt/homebrew/bin/minisat"

class PathCover(object):

    def v(self, path, pos, i, n):
        """
        path: cislo cesty (0, ..., k-1)
        pos: pozicia vo vnutri cesty (0..n-1)
        i: index vrchola (0, ..., n-1)
        n: pocet vrcholov
        k: pocet ciest
        """
        # unikatne kodovanie - vrchol i je na pozicii pos v ceste path
        return n * n * path + n * pos + i + 1
    
    def dekoder(self, code, n):
        x = code - 1
        path = x // (n*n)
        r = x % (n*n)
        pos = r // n
        i = r % n
        return path, pos, i

    def find(self, edges, k):
        """ 
        Pokusi sa najst pokrytie vrcholov kubickeho grafu pomocou najviac k disjunktnych ciest.
        Vracia zoznam ciest (kazda ako zoznam vrcholov v poradi), alebo prazdny zoznam ak sa nepodari.

        :param edges: n x n matica susednosti, edges[i][j] == True ak je hrana z i do j
        :param k: pocet povolenych ciest
        :return: zoznam ciest alebo prazdny zoznam ak sa nepodari
        """
        
        n = len(edges) # number of vertices in the graph

        solver = sat.SatSolver(SAT_SOLVER_PATH)
        w = sat.DimacsWriter('pathcover_cnf_in.txt')

        # kazdy vrchol sa objavi raz v nejakom path na pos
        for i in range(n):
            clause = [self.v(path, pos, i, n) for path in range(k) for pos in range(n)]
            w.writeClause(clause)  # aspon raz
            for a in clause:
                for b in clause:
                    if a < b:
                        w.writeImpl(a, -b) # nie na viacerych miestach
                        
        # v rovnakych path ani na jednej pos nie su dve rozne vrcholy
        #   (na pozicii pos v ceste path je max 1 vrchol)
        for path in range(k):
            for pos in range(n):
                for i in range(n):
                    for j in range(i+1, n):
                        w.writeImpl(self.v(path, pos, i, n), -self.v(path, pos, j, n))
        
        # ak v grafe nie je hrana z i do j, 
        #   nemozu byt susedmi v rovnakej ceste
        for path in range(k):
            for pos in range(n-1):                    
                for i in range(n):
                    for j in range(n):
                        if not edges[i][j]:
                            next_pos = pos + 1
                            w.writeImpl(self.v(path, pos, i, n), -self.v(path, next_pos, j, n))
                        
        w.close()
        ok, sol = solver.solve(w, 'pathcover_cnf_out.txt')
        if not ok: return []

        positions = []
       
        for x in sol:
            if x > 0:
                path, pos, i = self.dekoder(x, n)
                positions.append((path, pos, i))

        # zostavenie ciest
        from collections import defaultdict
        paths = defaultdict(lambda: [None] * n)
        for path, pos, i in positions:
            paths[path][pos] = i

        # Odstranenie prazdnych pozicii a ciest
        result = []
        for p in range(k):
            path = [v for v in paths[p] if v is not None]
            if path:
                result.append(path)
        return result    


if __name__ == "__main__":
    
    from data import GraphLibrary
    gl = GraphLibrary()
    pc = PathCover()

    # vstup pre find
    my_graph, n = gl.get("g_20")

    for k in range(n):
        paths = pc.find(my_graph, k)
        if paths: break

    print("Cesty pokryvajuce vrcholy: ")
    for path in paths:
        print(path)
    if not path:
        print("Ziadne cesty")