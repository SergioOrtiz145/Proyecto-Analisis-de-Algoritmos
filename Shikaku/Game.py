import copy
from .Board import Board

class Game:

    m_Board  = None
    m_Player = None

    def __init__( self, w, h, hints, player ):
        self.m_Board  = Board( w, h, hints )
        self.m_Player = player
        self.m_Player.init( w, h, hints )

    def solve( self ):
        while not self.m_Board.finished():
            print( str( self.m_Board ) )
            print( '-' * 42 )

            accion = self.m_Player.play()

            if accion is None:
                break

            tipo = accion.get( 'tipo' )

            if tipo == 'colocar':
                r1, c1, r2, c2 = accion[ 'coords' ]
                area, ok, msg  = self.m_Board.place( r1, c1, r2, c2 )

                if ok:
                    id_reg = self.m_Board.m_NextId - 1
                    self.m_Player.report( id_reg )
                    print( f'  ✓ {msg}' )
                else:
                    print( f'  ✗ {msg}' )

            elif tipo == 'eliminar':
                id_reg  = accion[ 'id' ]
                ok, msg = self.m_Board.remove( id_reg )

                if ok:
                    if hasattr( self.m_Player, 'm_Historial' ) and \
                       id_reg in self.m_Player.m_Historial:
                        self.m_Player.m_Historial.remove( id_reg )
                    print( f'  ✓ {msg}' )
                else:
                    print( f'  ✗ {msg}' )

            elif tipo == 'noop':
                pass

        print( str( self.m_Board ) )
        print( '-' * 42 )

        if self.m_Board.has_won():
            print( '¡Ganaste! El tablero está completo.' )
        else:
            print( 'El tablero está incompleto.' )