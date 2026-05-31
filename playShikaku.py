import importlib.util, sys
import Shikaku.Game
from Shikaku.Generator import generate_by_difficulty, DIFICULTADES
from Shikaku.Player.Human  import Player as HumanPlayer

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
    print( f'\n  Level  : {data["name"]}' )
    game = Shikaku.Game.Game( w, h, hints, player )
    game.solve()
 
 
def main( argv ):
 
    if len( argv ) >= 2:
        # ── argumentos por línea de comandos ──
        if argv[ 0 ].lower() == 'random':
            if len( argv ) < 3:
                print( 'Usage: python playShikaku.py random <difficulty> <player> [seed]' )
                print( f'Difficulties: {list(DIFICULTADES.keys())}' )
                sys.exit( 1 )
            dif, nom_player = argv[1].lower(), argv[2].lower()
            seed            = int( argv[3] ) if len(argv) >= 4 else None
            PlayerClass     = HumanPlayer
            if dif not in DIFICULTADES:
                print( f'Invalid difficulty "{dif}". Options: {list(DIFICULTADES.keys())}' )
                sys.exit( 1 )
            if PlayerClass is None:
                print( f'Invalid player "{nom_player}". Options: Human Player' )
                sys.exit( 1 )
            print( f'  Generating random puzzle ({dif})…' )
            data = generate_by_difficulty( dif, seed=seed )
        else:
            # nivel fijo
            num_nivel, nom_player = int( argv[0] ), argv[1].lower()
            #data        = load_level( num_nivel )
            PlayerClass = HumanPlayer
            if data is None:
                print( f'Level {num_nivel} does not exist. Valid: 1-4' )
                sys.exit( 1 )
            if PlayerClass is None:
                print( f'Invalid player "{nom_player}". Options: Human Player' )
                sys.exit( 1 )

 
    lanzar( data, PlayerClass )
 
if __name__ == '__main__':
    try:
        main( sys.argv[ 1: ] )
    except KeyboardInterrupt:
        print( '\n\n  Game interrupted. See you soon!\n' )

      