class Board:

    _LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    m_Width   = None
    m_Height  = None
    m_Grid    = None
    m_Regions = None
    m_NextId  = None

    def __init__( self, w, h, hints ):
        self.m_Width   = w
        self.m_Height  = h
        self.m_Grid    = [
            { 'hint': None, 'region': None }
            for _ in range( w * h )
        ]
        self.m_Regions = {}
        self.m_NextId  = 1

        for ( r, c ), num in hints.items():
            self.m_Grid[ r * w + c ][ 'hint' ] = num

    def finished( self ):
        return all( cell[ 'region' ] is not None for cell in self.m_Grid )

    def has_won( self ):
        return self.finished()

    def inside( self, r, c ):
        return 0 <= r < self.m_Height and 0 <= c < self.m_Width


    def get_hints( self ):
        hints = {}
        for r in range( self.m_Height ):
            for c in range( self.m_Width ):
                h = self.m_Grid[ r * self.m_Width + c ][ 'hint' ]
                if h is not None:
                    hints[ ( r, c ) ] = h


        return hints

    def get_region_id( self, r, c ):
        return self.m_Grid[ r * self.m_Width + c ][ 'region' ]

    def get_regions( self ):
        return dict( self.m_Regions )


    def place( self, r1, c1, r2, c2 ):
        # normalizar esquinas
        r1, r2 = min( r1, r2 ), max( r1, r2 )
        c1, c2 = min( c1, c2 ), max( c1, c2 )

        # dentro del tablero
        if not ( self.inside( r1, c1 ) and self.inside( r2, c2 ) ):
            return ( -1, False, 'Rectangle outside the board' )

        celdas = [
            ( r, c )
            for r in range( r1, r2 + 1 )
            for c in range( c1, c2 + 1 )
        ]
        area = len( celdas )

        # celdas libres
        for r, c in celdas:
            if self.m_Grid[ r * self.m_Width + c ][ 'region' ] is not None:
                return ( -1, False, f'The cell ({r},{c}) is already in other region' )
        

        # exactamente una pista dentro
        pistas = [ ( r, c ) for r, c in celdas
                   if self.m_Grid[ r * self.m_Width + c ][ 'hint' ] is not None ]
        if len( pistas ) == 0:
            return ( -1, False, 'Rectangle does not contain any hint.' )
        if len( pistas ) > 1:
            return ( -1, False, f'Rectangle contains {len(pistas)} hints, but can only have 1.' )

        # el área tiene que ser igual al número de la pista
        numero = self.m_Grid[ pistas[0][0] * self.m_Width + pistas[0][1] ][ 'hint' ]
        if area != numero:
            return ( -1, False,
                     f'Area {area} and hint {numero} are not equal in ({pistas[0][0]},{pistas[0][1]}).' )

        # registrar
        id_reg = self.m_NextId
        self.m_NextId += 1
        for r, c in celdas:
            self.m_Grid[ r * self.m_Width + c ][ 'region' ] = id_reg
        self.m_Regions[ id_reg ] = ( r1, c1, r2, c2 )

        return ( area, True, f'Region {id_reg} added (Area {area}).' )

    def remove( self, id_reg ):
        # elimina una region por su id
        if id_reg not in self.m_Regions:
            return ( False, f'Region {id_reg} not found' )
        r1, c1, r2, c2 = self.m_Regions[ id_reg ]
        for r in range( r1, r2 + 1 ):
            for c in range( c1, c2 + 1 ):
                self.m_Grid[ r * self.m_Width + c ][ 'region' ] = None
        del self.m_Regions[ id_reg ]
        return ( True, f'Region {id_reg} eliminated.' )

    def __str__( self ):
        W = self.m_Width

        # encabezado de columnas
        col_header = '      ' + ''.join( f' c{c:<2}' for c in range( W ) )
        sep        = '      ' + '+---' * W + '+'

        lines = [ col_header, sep ]

        for r in range( self.m_Height ):
            fila = f'r{r:<4} |'
            for c in range( W ):
                cell = self.m_Grid[ r * W + c ]
                hint = cell[ 'hint' ]
                rid  = cell[ 'region' ]
                if hint is not None:
                    contenido = str( hint ).center( 3 )
                elif rid is not None:
                    letra     = self._LETRAS[ ( rid - 1 ) % len( self._LETRAS ) ]
                    contenido = f' {letra} '
                else:
                    contenido = '   '
                fila += contenido + '|'
            
            lines.append( fila )
            lines.append( sep )
        

        return '\n'.join( lines )
