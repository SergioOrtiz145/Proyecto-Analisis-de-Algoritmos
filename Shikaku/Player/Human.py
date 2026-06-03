class Player:

    m_Width   = None
    m_Height  = None
    m_Hints   = None
    m_History = None
    m_Moves   = 0

    def __init__( self ):
        pass

    def init( self, w, h, hints ):
        self.m_Width   = w
        self.m_Height  = h
        self.m_Hints   = dict( hints )
        self.m_History = []
        self.m_Moves   = 0

        print( self._help() )

    def play( self ):

        while True:

            raw = input( '  > ' ).strip()

            if not raw:
                continue

            tokens = raw.lower().split()
            cmd    = tokens[ 0 ]

            # Salir
            if cmd in ( 's', 'q', 'quit', 'exit' ):
                return None

            # Ayuda
            if cmd in ( '?', 'help', 'h' ):
                print( self._help() )
                return { 'tipo': 'noop' }

            # Mostrar pistas
            if cmd in ( 'p', 'hints' ):
                self._show_hints()
                return { 'tipo': 'noop' }

            # Deshacer
            if cmd in ( 'u', 'undo' ):
                if self.m_History:
                    id_reg = self.m_History[ -1 ] 
                    return {
                        'tipo': 'eliminar',
                        'id': id_reg
                    }

                else:
                    print( '  No hay movimientos para deshacer.' )
                    return { 'tipo': 'noop' }

            # Eliminar región
            if cmd in ( 'e', 'del', 'delete' ):
                if len( tokens ) < 2:
                    print( '  Uso: e <id>' )
                    continue
                try:
                    return {
                        'tipo': 'eliminar',
                        'id': int( tokens[ 1 ] )
                    }
                except ValueError:
                    print( '  El id debe ser un número.' )
                    continue

            # Colocar rectángulo
            try:
                nums = [ int( t ) for t in tokens[ :4 ] ]
                if len( nums ) < 4:
                    print( '  Debe ingresar 4 números: fila1 col1 fila2 col2' )
                    continue

                r1, c1, r2, c2 = nums
                self.m_Moves += 1
                
                return {
                    'tipo': 'colocar',
                    'coords': ( r1, c1, r2, c2 )
                }

            except ValueError:
                print( f'  Comando no reconocido: "{raw}". ' 'Escriba ? para ver la ayuda.' )
                continue
            
    def _show_hints( self ):
        print( "\nPistas:" )

        for ( r, c ), valor in self.m_Hints.items():
            print( f"  ({r},{c}) -> {valor}" )

        print()

    def _help( self ):

        return (
            '\n ═══════════════════════════════════════════\n'
            '║           COMANDOS SHIKAKU                ║\n'
            '╠═══════════════════════════════════════════╣\n'
            '║  f1 c1 f2 c2   Colocar rectángulo         ║\n'
            '║                Ejemplo: 0 0 1 2           ║\n'
            '║  e <id>        Eliminar región            ║\n'
            '║  u / undo      Deshacer último movimiento ║\n'
            '║  p / hints     Mostrar pistas             ║\n'
            '║  ? / help      Mostrar esta ayuda         ║\n'
            '║  s / quit      Salir                      ║\n'
            '════════════════════════════════════════════╣ \n'
            '║  Las coordenadas comienzan en 0.          ║\n'
            '║  El área del rectángulo debe coincidir    ║\n'
            '║  con el número de la pista.               ║\n'
            '╚═══════════════════════════════════════════╝'
        )