from ..Solver import MRVFCSolver


class Player:

    def __init__(self):

        self.m_Width = None
        self.m_Height = None
        self.m_Hints = None

        self.m_History = []
        self.m_Moves = 0

        self._queue = []

    def init(self, w, h, hints):

        self.m_Width = w
        self.m_Height = h
        self.m_Hints = dict(hints)

        self.m_History = []
        self.m_Moves = 0
        self._queue = []

        print("\n  [Solver] Calculando solución...")
        self._compute_solution()

    def _compute_solution(self):

        solver = MRVFCSolver(
            self.m_Width,
            self.m_Height,
            self.m_Hints
        )

        solucion, tiempo = solver.solve()

        if solucion is None:
            print("\n  [Solver] No se encontró solución.")
            return

        print( f"\n  [Solver] Solución encontrada en " f"{tiempo:.6f} segundos" )

        print( f"  [Solver] Nodos explorados: " f"{solver.nodes_explored}" )

        print( f"  [Solver] Retrocesos: " f"{solver.backtracks}" )

        print( f"  [Solver] Profundidad máxima: " f"{solver.max_depth}" )

        print( f"  [Solver] Ramas podadas: " f"{solver.pruned_branches}\n")

        for pista, rectangulo in solucion.items():
            r1, c1, r2, c2 = rectangulo
            self._queue.append(
                {
                    "tipo": "colocar",
                    "coords": (r1, c1, r2, c2)
                }
            )

    def play(self):

        if len(self._queue) == 0:
            return None

        accion = self._queue.pop(0)
        self.m_Moves += 1
        r1, c1, r2, c2 = accion["coords"]

        print( f" [Solver] Movimiento {self.m_Moves}: " f"({r1},{c1}) -> ({r2},{c2})\n")
        return accion

    def report(self, id_reg):
        self.m_History.append(id_reg)