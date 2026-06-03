import importlib.util, sys
import Shikaku.Game
from Shikaku.Generator import generate_by_difficulty, DIFICULTADES
from Shikaku.Player.Human import Player as HumanPlayer
from Shikaku.Player.Synthetic import Player as SyntheticPlayer

def ImportLibrary( module_name, filename ):
  spec = importlib.util.spec_from_file_location( module_name, filename )
  if spec is None:
    print( f'Error: Could not create module specification for {filename}' )
    return None

  module = importlib.util.module_from_spec( spec )
  sys.modules[ module_name ] = module
  try:
    spec.loader.exec_module( module )
    return module
  except Exception as e:
    print( f'Error executing module {filename}: {e}' )
    del sys.modules[ module_name ]
  
  return None

def lanzar( data, PlayerClass ):
    player = PlayerClass()
    w, h   = data[ 'size' ]
    hints  = data[ 'hints' ]
    print( f'\n  Nivel  : {data["name"]}' )
    game = Shikaku.Game.Game( w, h, hints, player )
    game.solve()
 
 
def main( argv ):
 
    if len( argv ) >= 2:
        # ── argumentos por línea de comandos ──
        if argv[ 0 ].lower() == 'random':
            if len( argv ) < 3:
                print( 'Usage: python playShikaku.py random <difficulty> <player> [seed]' )
                print( f'Dificultades: {list(DIFICULTADES.keys())}' )
                sys.exit( 1 )
                
            dif, nom_player = argv[1].lower(), argv[2].lower()
            seed            = int( argv[3] ) if len(argv) >= 4 else None
            
            if nom_player == "human":
                PlayerClass = HumanPlayer

            elif nom_player == "synthetic":
                PlayerClass = SyntheticPlayer

            else:
                print( f'Jugador inválido "{nom_player}". ' 'Opciones: human, synthetic') 
                sys.exit(1)
            
            if dif not in DIFICULTADES:
                print( f'Dificultad Invalida "{dif}". Opciones: {list(DIFICULTADES.keys())}' )
                sys.exit( 1 )
                
            if PlayerClass is None:
                print( f'Jugador Invalido "{nom_player}". Opciones: Human Player' )
                sys.exit( 1 )
                
            print( f'  Generando tablero random ({dif})…' )
            data = generate_by_difficulty( dif, seed=seed )
        else:
            # nivel fijo
            num_nivel, nom_player = int( argv[0] ), argv[1].lower()
            #data        = load_level( num_nivel )
            PlayerClass = HumanPlayer
            
            if data is None:
                print( f'Nivel {num_nivel} no existe. Valido: 1-4' )
                sys.exit( 1 )
                
            if PlayerClass is None:
                print( f'Jugador Invalido "{nom_player}". Opciones: Human Player' )
                sys.exit( 1 )

 
    lanzar( data, PlayerClass )
 
if __name__ == '__main__':
    try:
        main( sys.argv[ 1: ] )
    except KeyboardInterrupt:
        print( '\n\n  Juego interrumpido. \n' )

      