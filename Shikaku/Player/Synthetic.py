from ..Solver import MRVDynamicFCSolver, hints_to_clues


class Player:

    m_Width    = None
    m_Height   = None
    m_Hints    = None
    m_History  = None
    m_Moves    = 0

    # Cola de movimientos calculados por el solver
    _queue     = None

    def __init__( self ):
        pass

    def init( self, w, h, hints ):
        self.m_Width   = w
        self.m_Height  = h
        self.m_Hints   = dict( hints )
        self.m_History = []
        self.m_Moves   = 0
        self._queue    = []

        print( '\n  [Solver] Calculando solución…' )
        self._compute_solution()

    #  Calcular la solución completa de una vez
    def _compute_solution( self ):
        """
        Crea un Board temporal solo para pasárselo al solver,
        calcula la solución y llena la cola de movimientos.
        """
        # Importación local para evitar ciclos
        from ..Board import Board

        tmp    = Board( self.m_Width, self.m_Height, self.m_Hints )
        solver = MRVDynamicFCSolver( tmp )
        solution, elapsed = solver.solve()

        if solution is None:
            print( '  [Solver] ✗ No se encontró solución.' )
            return

        print( f'  [Solver] ✓ Solución encontrada en {elapsed:.4f}s '
               f'({solver.nodes_explored} nodos explorados, '
               f'profundidad máx. {solver.max_depth})' )

        # Cargar la cola: un movimiento 'colocar' por cada rectángulo
        for clue, ( r1, c1, r2, c2 ) in solution.items():
            self._queue.append( { 'tipo': 'colocar', 'coords': ( r1, c1, r2, c2 ) } )

    #  Interfaz que Game.solve() llama
    def play( self ):
        """
        Devuelve el siguiente movimiento de la cola.
        Si la cola está vacía, devuelve None (abandona).
        """
        if not self._queue:
            return None

        accion = self._queue.pop( 0 )
        self.m_Moves += 1
        r1, c1, r2, c2 = accion[ 'coords' ]
        print( f'  [Solver] Colocando rectángulo ({r1},{c1}) → ({r2},{c2})' )
        return accion

    #  Historial
    def report( self, id_reg ):
        self.m_History.append( id_reg )