from ..Solver import MRVFCSolver


class Player:

    def __init__( self ):

        self.m_Ancho = None
        self.m_Alto = None
        self.m_Pistas = None

        self.m_Historial = []
        self.m_Movimientos = 0

        self._cola = []

    def init( self, ancho, alto, pistas ):

        self.m_Ancho = ancho
        self.m_Alto = alto
        self.m_Pistas = dict( pistas )

        self.m_Historial = []
        self.m_Movimientos = 0
        self._cola = []

        print( "\n  [Solver] Calculando solución..." )
        self._compute_solution()

    def _compute_solution( self ):
        solver = MRVFCSolver(
            self.m_Ancho,
            self.m_Alto,
            self.m_Pistas
        )

        solucion, tiempo = solver.solve()

        if solucion is None:

            print( "\n  [Solver] No se encontró una solución." )
            return

        print( f"\n  [Solver] Solución encontrada en " f"{tiempo:.6f} segundos" )

        print( f"  [Solver] Nodos explorados: " f"{solver.nodos_explorados}" )

        print(f"  [Solver] Retrocesos realizados: " f"{solver.backtracks}" )

        print( f"  [Solver] Profundidad máxima alcanzada: " f"{solver.max_profundidad}" )

        print( f"  [Solver] Ramas podadas: " f"{solver.ramas_podadas}\n" )

        for pista, rectangulo in solucion.items():
            fila1, columna1, fila2, columna2 = rectangulo

            self._cola.append(
                {
                    "tipo": "colocar",
                    "coords": ( fila1, columna1, fila2, columna2 )
                }
            )

    def play( self ):
        if len( self._cola ) == 0:
            return None

        accion = self._cola.pop( 0 )
        self.m_Movimientos += 1
        fila1, columna1, fila2, columna2 = accion[ "coords" ]

        print( f"  [Solver] Movimiento {self.m_Movimientos}: " f"({fila1},{columna1}) -> ({fila2},{columna2})\n")

        return accion

    def report( self, id_region ):
        self.m_Historial.append( id_region )