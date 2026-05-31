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

            # el jugador decide qué rectángulo colocar
            accion = self.m_Player.play()

            # procesar la acción
            if accion is None:
                # jugador abandona
                break

            tipo = accion.get( 'tipo' )

            if tipo == 'colocar':
                r1, c1, r2, c2 = accion[ 'coords' ]
                self.m_Board.place( r1, c1, r2, c2 )

            elif tipo == 'eliminar':
                id_reg = accion[ 'id' ]
                self.m_Board.remove( id_reg )

            elif tipo == 'noop':
                pass
            
        print( str( self.m_Board ) )
        print( '-' * 42 )

        if self.m_Board.has_won():
            print( 'You won! :-D  The board is complete.' )
        else:
            print( 'The board is incomplete.' )