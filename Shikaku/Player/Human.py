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
        print( self._help() )  # Help message, already likely in English

    def play( self ):
        while True:
            raw = input( '  > ' ).strip()
            if not raw:
                continue

            tokens = raw.lower().split()
            cmd    = tokens[ 0 ]

            # quit
            if cmd in ( 's', 'q', 'quit', 'exit' ):
                return None

            # help
            if cmd in ( '?', 'help', 'h' ):
                print( self._help() )
                return { 'type': 'noop' }

            # hints
            if cmd in ( 'p', 'hints' ):
                self._show_hints()
                return { 'type': 'noop' }

            # undo
            if cmd in ( 'u', 'undo' ):
                if self.m_History:
                    id_reg = self.m_History[-1]   # removed by report() when confirmed
                    return { 'type': 'delete', 'id': id_reg }
                else:
                    print( '  No moves to undo.' )
                    return { 'type': 'noop' }

            # delete region
            if cmd in ( 'e', 'del', 'delete' ):
                if len( tokens ) < 2:
                    print( '  Usage: e <id>' )
                    continue
                try:
                    return { 'type': 'delete', 'id': int( tokens[1] ) }
                except ValueError:
                    print( '  The id must be a number.' )
                    continue

            # place rectangle
            try:
                nums = [ int( t ) for t in tokens[:4] ]
                if len( nums ) < 4:
                    print( '  I need 4 numbers: r1 c1 r2 c2' )
                    continue
                r1, c1, r2, c2 = nums
                self.m_Moves += 1
                return { 'type': 'place', 'coords': ( r1, c1, r2, c2 ) }
            except ValueError:
                print( f'  Unrecognized command: "{raw}". Type ? for help.' )
                continue

    def _help( self ):
        return (
            '\n══════════════════════════════════════════\n'
            '║           SHIKAKU COMMANDS               ║\n'
            '╠══════════════════════════════════════════╣\n'
            '║  r1 c1 r2 c2  Place rectangle            ║\n'
            '║               Example: 0 0 1 2           ║\n'
            '║  e <id>        Delete region             ║\n'
            '║  u / undo      Undo last rectangle       ║\n'
            '║  p / hints     Show list of hints        ║\n'
            '║  ? / help      This screen               ║\n'
            '║  s / quit      Quit                      ║\n'
            '══════════════════════════════════════════\n'
            '║  Coordinates start at 0.                 ║\n'
            '║  Rectangle area must = hint number.      ║\n'
            '╚══════════════════════════════════════════╝'
        )
