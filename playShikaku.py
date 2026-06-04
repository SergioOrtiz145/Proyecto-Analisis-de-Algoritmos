import sys
import Shikaku.Game
from Shikaku.Generator        import generate_by_difficulty, DIFICULTADES
from Shikaku.Player.Human     import Player as HumanPlayer
from Shikaku.Player.Synthetic import Player as SyntheticPlayer

def lanzar( data, PlayerClass ):
    player = PlayerClass()
    w, h   = data[ 'size' ]
    hints  = data[ 'hints' ]
    print( f'\n  Nivel  : {data["name"]}' )
    game = Shikaku.Game.Game( w, h, hints, player )
    game.solve()


def main( argv ):

    if len( argv ) >= 2:
        if argv[ 0 ].lower() == 'random':
            if len( argv ) < 3:
                print( 'Uso: python playShikaku.py random <dificultad> <jugador> [semilla]' )
                print( f'Dificultades: {list(DIFICULTADES.keys())}' )
                sys.exit( 1 )

            dif        = argv[ 1 ].lower()
            nom_player = argv[ 2 ].lower()
            seed       = int( argv[ 3 ] ) if len( argv ) >= 4 else None

            if dif not in DIFICULTADES:
                print( f'Dificultad "{dif}" inválida. Opciones: {list(DIFICULTADES.keys())}' )
                sys.exit( 1 )

            # Seleccionar clase de jugador según argumento
            if nom_player == 'human':
                PlayerClass = HumanPlayer
            elif nom_player == 'synthetic' or nom_player == 'solver':
                PlayerClass = SyntheticPlayer
            else:
                print( f'Jugador "{nom_player}" inválido. Opciones: human, solver' )
                sys.exit( 1 )

            print( f'  Generando puzzle aleatorio ({dif})...' )
            data = generate_by_difficulty( dif, seed=seed )
            lanzar( data, PlayerClass )

        else:
            print( f'Argumento "{argv[0]}" no reconocido.' )
            print( 'Uso: python playShikaku.py random <dificultad> <jugador> [semilla]' )
            sys.exit( 1 )

    else:
        print( 'Uso: python playShikaku.py random <dificultad> <jugador> [semilla]' )
        print( f'Dificultades: {list(DIFICULTADES.keys())}' )
        print( 'Jugadores: human, solver' )
        sys.exit( 1 )


if __name__ == '__main__':
    try:
        main( sys.argv[ 1: ] )
    except KeyboardInterrupt:
        print( '\n\n  Juego interrumpido. ¡Hasta pronto!\n' )