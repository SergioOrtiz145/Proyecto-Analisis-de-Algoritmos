"""
Contiene 3 versiones del algoritmo para comparación:
  1. Backtracking puro
  2. Backtracking + MRV estático
  3. Backtracking + MRV dinámico + Forward Checking

Compatibilidad: se integra con Board.py usando get_hints() y place().
"""

import time


def get_candidates(rows, cols, clues):
    """
    Para cada pista (r, c, area) genera todos los rectángulos
    posibles que la contengan y tengan el área correcta.

    Retorna: dict { (r, c, area): [ (r1, c1, r2, c2), ... ] }
    """
    candidates = {}
    for (r, c, area) in clues:
        rects = []
        for h in range(1, area + 1):
            if area % h != 0:
                continue
            w = area // h
            for r1 in range(max(0, r - h + 1), r + 1):
                r2 = r1 + h - 1
                if r2 >= rows:
                    continue
                for c1 in range(max(0, c - w + 1), c + 1):
                    c2 = c1 + w - 1
                    if c2 >= cols:
                        continue
                    rects.append((r1, c1, r2, c2))
        candidates[(r, c, area)] = rects
    return candidates


def rectangles_overlap(r1a, c1a, r2a, c2a, r1b, c1b, r2b, c2b):
    """True si dos rectángulos comparten al menos una celda."""
    return not (r2a < r1b or r2b < r1a or c2a < c1b or c2b < c1a)


def hints_to_clues(hints):
    """
    Convierte el dict que devuelve Board.get_hints()
    { (r,c): area } → lista de tuplas (r, c, area)
    """
    return [(r, c, area) for (r, c), area in hints.items()]


def apply_solution(board, solution):
    """
    Recibe el Board y el dict solución { (r,c,area): (r1,c1,r2,c2) }
    y llama a board.place() para cada rectángulo.
    Retorna True si todo se colocó correctamente.
    """
    for clue, (r1, c1, r2, c2) in solution.items():
        _, ok, msg = board.place(r1, c1, r2, c2)
        if not ok:
            print(f"  [!] Error al colocar {clue}: {msg}")
            return False
    return True


# ─────────────────────────────────────────────
#  VERSIÓN 1 — BACKTRACKING PURO
# ─────────────────────────────────────────────

class BacktrackingSolver:
    """
    Backtracking puro: itera las pistas en el orden original,
    prueba cada candidato y retrocede si hay conflicto.
    No usa ninguna heurística.
    """

    def __init__(self, board):
        self.rows = board.m_Height
        self.cols = board.m_Width
        self.clues = hints_to_clues(board.get_hints())
        self.all_candidates = get_candidates(self.rows, self.cols, self.clues)

        # Métricas
        self.nodes_explored = 0
        self.max_depth = 0

    def solve(self):
        solution = {}
        placed = []
        self.nodes_explored = 0
        self.max_depth = 0

        start = time.perf_counter()
        found = self._backtrack(0, solution, placed, 0)
        elapsed = time.perf_counter() - start

        return solution if found else None, elapsed

    def _backtrack(self, index, solution, placed, depth):
        self.nodes_explored += 1
        if depth > self.max_depth:
            self.max_depth = depth

        if index == len(self.clues):
            return True

        clue = self.clues[index]
        for rect in self.all_candidates[clue]:
            if any(rectangles_overlap(*rect, *p) for p in placed):
                continue

            solution[clue] = rect
            placed.append(rect)

            if self._backtrack(index + 1, solution, placed, depth + 1):
                return True

            del solution[clue]
            placed.pop()

        return False


# ─────────────────────────────────────────────
#  VERSIÓN 2 — BACKTRACKING + MRV ESTÁTICO
# ─────────────────────────────────────────────

class MRVStaticSolver:
    """
    Igual que el backtracking puro pero antes de empezar ordena
    las pistas de menor a mayor número de candidatos (MRV estático).
    El orden no cambia durante la búsqueda.
    """

    def __init__(self, board):
        self.rows = board.m_Height
        self.cols = board.m_Width
        clues = hints_to_clues(board.get_hints())
        self.all_candidates = get_candidates(self.rows, self.cols, clues)

        # Ordenar pistas por número de candidatos (ascendente)
        self.clues = sorted(clues, key=lambda c: len(self.all_candidates[c]))

        self.nodes_explored = 0
        self.max_depth = 0

    def solve(self):
        solution = {}
        placed = []
        self.nodes_explored = 0
        self.max_depth = 0

        start = time.perf_counter()
        found = self._backtrack(0, solution, placed, 0)
        elapsed = time.perf_counter() - start

        return solution if found else None, elapsed

    def _backtrack(self, index, solution, placed, depth):
        self.nodes_explored += 1
        if depth > self.max_depth:
            self.max_depth = depth

        if index == len(self.clues):
            return True

        clue = self.clues[index]
        for rect in self.all_candidates[clue]:
            if any(rectangles_overlap(*rect, *p) for p in placed):
                continue

            solution[clue] = rect
            placed.append(rect)

            if self._backtrack(index + 1, solution, placed, depth + 1):
                return True

            del solution[clue]
            placed.pop()

        return False


# ─────────────────────────────────────────────
#  VERSIÓN 3 — MRV DINÁMICO + FORWARD CHECKING
# ─────────────────────────────────────────────

class MRVDynamicFCSolver:
    """
    El algoritmo completo:
      - MRV Dinámico: en cada paso escoge la pista sin asignar
        que tenga MENOS candidatos válidos en ese momento.
      - Forward Checking: cada vez que se coloca un rectángulo,
        se eliminan de las listas de candidatos todos los que
        colisionarían con él. Se restauran al hacer backtrack.
    """

    def __init__(self, board):
        self.rows = board.m_Height
        self.cols = board.m_Width
        clues = hints_to_clues(board.get_hints())
        self.clues = clues

        base = get_candidates(self.rows, self.cols, clues)
        # Copia mutable por pista
        self.candidates = {clue: list(rects) for clue, rects in base.items()}

        self.nodes_explored = 0
        self.max_depth = 0

    def solve(self):
        solution = {}
        assigned = set()
        self.nodes_explored = 0
        self.max_depth = 0

        start = time.perf_counter()
        found = self._backtrack(solution, assigned, 0)
        elapsed = time.perf_counter() - start

        return solution if found else None, elapsed

    def _select_clue(self, assigned):
        """MRV dinámico: pista no asignada con menos candidatos actuales."""
        unassigned = [c for c in self.clues if c not in assigned]
        return min(unassigned, key=lambda c: len(self.candidates[c]))

    def _forward_check(self, placed_rect, assigned):
        """
        Elimina de las pistas no asignadas todos los candidatos
        que se solapen con placed_rect.
        Retorna {clue: [rects_eliminados]} para poder deshacer.
        """
        removed = {}
        for clue in self.clues:
            if clue in assigned:
                continue
            to_remove = [r for r in self.candidates[clue]
                         if rectangles_overlap(*r, *placed_rect)]
            if to_remove:
                removed[clue] = to_remove
                for r in to_remove:
                    self.candidates[clue].remove(r)
        return removed

    def _restore_candidates(self, removed):
        """Deshace el forward checking restaurando los candidatos eliminados."""
        for clue, rects in removed.items():
            self.candidates[clue].extend(rects)

    def _backtrack(self, solution, assigned, depth):
        self.nodes_explored += 1
        if depth > self.max_depth:
            self.max_depth = depth

        if len(assigned) == len(self.clues):
            return True

        clue = self._select_clue(assigned)

        if not self.candidates[clue]:
            return False

        for rect in list(self.candidates[clue]):
            solution[clue] = rect
            assigned.add(clue)

            removed = self._forward_check(rect, assigned)

            # Poda: si alguna pista quedó sin candidatos, no seguir
            dead_end = any(
                len(self.candidates[c]) == 0
                for c in self.clues if c not in assigned
            )

            if not dead_end:
                if self._backtrack(solution, assigned, depth + 1):
                    return True

            self._restore_candidates(removed)
            del solution[clue]
            assigned.discard(clue)

        return False


# ─────────────────────────────────────────────
#  BENCHMARK — compara las 3 versiones
# ─────────────────────────────────────────────

def benchmark(board, label="Tablero"):
    """
    Corre las 3 versiones sobre el mismo Board e imprime
    una tabla comparativa. NO modifica el tablero.
    """
    print(f"\n{'='*58}")
    print(f"  {label}  ({board.m_Height}×{board.m_Width}, "
          f"{len(board.get_hints())} pistas)")
    print(f"{'='*58}")
    print(f"  {'Algoritmo':<33} {'Tiempo(s)':>9} {'Nodos':>7} {'ProfMax':>7}")
    print(f"  {'-'*56}")

    solvers = [
        ("1. Backtracking puro",   BacktrackingSolver),
        ("2. MRV estático",        MRVStaticSolver),
        ("3. MRV dinámico + FC",   MRVDynamicFCSolver),
    ]

    for name, SolverClass in solvers:
        s = SolverClass(board)
        sol, elapsed = s.solve()
        status = "✓" if sol else "✗"
        print(f"  {status} {name:<33} {elapsed:>9.5f} "
              f"{s.nodes_explored:>7} {s.max_depth:>7}")

    print(f"{'='*58}")


# ─────────────────────────────────────────────
#  EJEMPLO DE USO CON Board
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Importar Board solo al ejecutar directamente
    # (en producción lo importa Game.py)
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from Board import Board

    # ── Tablero 4×4 ──────────────────────────
    hints_4x4 = {
        (0, 0): 2,
        (0, 3): 2,
        (1, 1): 4,
        (3, 0): 4,
        (3, 3): 4,
    }
    board_4 = Board(4, 4, hints_4x4)
    benchmark(board_4, "Tablero 4×4")

    # Aplicar la mejor solución al tablero y mostrarlo
    solver = MRVDynamicFCSolver(board_4)
    solution, _ = solver.solve()
    if solution:
        apply_solution(board_4, solution)
        print("\nTablero resuelto:")
        print(board_4)

    # ── Tablero 7×7 ──────────────────────────
    hints_7x7 = {
        (0, 1): 3,
        (0, 5): 4,
        (1, 3): 2,
        (2, 0): 6,
        (2, 6): 2,
        (3, 2): 4,
        (4, 5): 3,
        (5, 1): 6,
        (6, 4): 5,
        (6, 6): 3,
    }
    board_7 = Board(7, 7, hints_7x7)
    benchmark(board_7, "Tablero 7×7")