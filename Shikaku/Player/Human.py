class Player:

    m_Ancho   = None
    m_Alto    = None
    m_Pistas   = None
    m_Historial = None   
    m_Movimientos   = 0

    def __init__( self ):
        pass

    def init( self, w, h, hints ):
        self.m_Ancho   = w
        self.m_Alto  = h
        self.m_Pistas   = dict( hints )
        self.m_Historial = []
        self.m_Movimientos   = 0
        print( self._help() )

    def play( self ):
        while True:
            raw = input( '  > ' ).strip()
            if not raw:
                continue

            tokens = raw.lower().split()
            cmd    = tokens[ 0 ]

            # salir 
            if cmd in ( 's', 'salir', 'q', 'quit', 'exit' ):
                return None

            # ayuda
            if cmd in ( '?', 'ayuda', 'help', 'h' ):
                print( self._help() )
                return { 'tipo': 'noop' }

            # pistas
            if cmd in ( 'p', 'pistas' ):
                self._show_hints()
                return { 'tipo': 'noop' }

            # deshacer
            if cmd in ( 'u', 'deshacer', 'undo' ):
                if self.m_Historial:
                    id_reg = self.m_Historial[-1]   # lo elimina report() al confirmar
                    return { 'tipo': 'eliminar', 'id': id_reg }
                else:
                    print( '  Sin movimientos para deshacer.' )
                    return { 'tipo': 'noop' }

            # eliminar región
            if cmd in ( 'e', 'eliminar', 'del' ):
                if len( tokens ) < 2:
                    print( '  Uso: e <id>' )
                    continue
                try:
                    return { 'tipo': 'eliminar', 'id': int( tokens[1] ) }
                except ValueError:
                    print( '  El id debe ser un número.' )
                    continue

            # colocar rectángulo
            try:
                nums = [ int( t ) for t in tokens[:4] ]
                if len( nums ) < 4:
                    print( '  Necesito 4 números: r1 c1 r2 c2' )
                    continue
                r1, c1, r2, c2 = nums
                self.m_Movimientos += 1
                return { 'tipo': 'colocar', 'coords': ( r1, c1, r2, c2 ) }
            except ValueError:
                print( f'  Comando no reconocido: "{raw}". Escribe ? para ayuda.' )
                continue

    def report( self, id_reg ):
        self.m_Historial.append( id_reg )
    
    def _help( self ):
        return (
            '╔════════════════════════════════════════════╗\n'
            '║           COMANDOS  SHIKAKU                ║\n'
            '╠════════════════════════════════════════════╣\n'
            '║  r1 c1 r2 c2   Colocar rectángulo          ║\n'
            '║                Ejemplo: 0 0 1 2            ║\n'
            '║  e <id>        Eliminar región             ║\n'
            '║  u / deshacer  Deshacer último rect.       ║\n'
            '║  p / pistas    Ver lista de pistas         ║\n'
            '║  ? / ayuda     Esta pantalla               ║\n'
            '║  s / salir     Salir                       ║\n'
            '╠════════════════════════════════════════════╣\n'
            '║  Coordenadas empiezan en 0.                ║\n'
            '║  El área del rect. debe = número pista.    ║\n'
            '╚════════════════════════════════════════════╝'
        )

    def _show_hints( self ):
        print( '\n  Pistas del tablero:' )
        for ( r, c ), area in sorted( self.m_Pistas.items() ):
            print( f'  ({r},{c}) → {area}' )
        print()
