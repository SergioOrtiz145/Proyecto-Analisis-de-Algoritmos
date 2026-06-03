class Board:

    _LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    m_Ancho      = None
    m_Alto       = None
    m_Grilla     = None
    m_Regiones   = None
    m_SiguienteId = None

    def __init__( self, ancho, alto, pistas ):

        self.m_Ancho  = ancho
        self.m_Alto   = alto

        self.m_Grilla = [
            { 'pista': None, 'region': None }
            for _ in range( ancho * alto )
        ]

        self.m_Regiones   = {}
        self.m_SiguienteId = 1

        for ( fila, columna ), numero in pistas.items():
            self.m_Grilla[ fila * ancho + columna ][ 'pista' ] = numero

    def finished( self ):
        return all(
            celda[ 'region' ] is not None
            for celda in self.m_Grilla
        )

    def has_won( self ):
        return self.finished()

    def inside( self, fila, columna ):
        return (
            0 <= fila < self.m_Alto and
            0 <= columna < self.m_Ancho
        )

    def get_hints( self ):

        pistas = {}

        for fila in range( self.m_Alto ):
            for columna in range( self.m_Ancho ):

                pista = self.m_Grilla[
                    fila * self.m_Ancho + columna
                ][ 'pista' ]

                if pista is not None:
                    pistas[ ( fila, columna ) ] = pista

        return pistas

    def get_region_id( self, fila, columna ):

        return self.m_Grilla[
            fila * self.m_Ancho + columna
        ][ 'region' ]

    def get_regions( self ):
        return dict( self.m_Regiones )

    def place( self, fila1, columna1, fila2, columna2 ):

        # Normalizar esquinas
        fila1, fila2 = min( fila1, fila2 ), max( fila1, fila2 )
        columna1, columna2 = min( columna1, columna2 ), max( columna1, columna2 )

        # Verificar que esté dentro del tablero
        if not (
            self.inside( fila1, columna1 ) and
            self.inside( fila2, columna2 )
        ):
            return (
                -1,
                False,
                'El rectángulo está fuera del tablero.'
            )

        celdas = [
            ( fila, columna )
            for fila in range( fila1, fila2 + 1 )
            for columna in range( columna1, columna2 + 1 )
        ]

        area = len( celdas )

        # Verificar que las celdas estén libres
        for fila, columna in celdas:

            if self.m_Grilla[
                fila * self.m_Ancho + columna
            ][ 'region' ] is not None:

                return (
                    -1,
                    False,
                    f'La celda ({fila},{columna}) ya pertenece a otra región.'
                )

        # Buscar pistas dentro del rectángulo
        pistas = [
            ( fila, columna )
            for fila, columna in celdas
            if self.m_Grilla[
                fila * self.m_Ancho + columna
            ][ 'pista' ] is not None
        ]

        if len( pistas ) == 0:
            return (
                -1,
                False,
                'El rectángulo no contiene ninguna pista.'
            )

        if len( pistas ) > 1:
            return (
                -1,
                False,
                f'El rectángulo contiene {len(pistas)} pistas, pero solo puede contener una.'
            )

        # Validar área
        fila_pista, columna_pista = pistas[ 0 ]

        numero = self.m_Grilla[
            fila_pista * self.m_Ancho + columna_pista
        ][ 'pista' ]

        if area != numero:

            return (
                -1,
                False,
                f'El área ({area}) no coincide con la pista ({numero}) '
                f'en ({fila_pista},{columna_pista}).'
            )

        # Registrar región
        id_region = self.m_SiguienteId
        self.m_SiguienteId += 1

        for fila, columna in celdas:

            self.m_Grilla[
                fila * self.m_Ancho + columna
            ][ 'region' ] = id_region

        self.m_Regiones[ id_region ] = (
            fila1,
            columna1,
            fila2,
            columna2
        )

        return (
            area,
            True,
            f'Región {id_region} agregada (área {area}).'
        )

    def remove( self, id_region ):

        if id_region not in self.m_Regiones:
            return (
                False,
                f'Región {id_region} no encontrada.'
            )

        fila1, columna1, fila2, columna2 = self.m_Regiones[ id_region ]

        for fila in range( fila1, fila2 + 1 ):
            for columna in range( columna1, columna2 + 1 ):

                self.m_Grilla[
                    fila * self.m_Ancho + columna
                ][ 'region' ] = None

        del self.m_Regiones[ id_region ]

        return (
            True,
            f'Región {id_region} eliminada.'
        )

    def __str__( self ):

        ancho = self.m_Ancho

        encabezado = (
            '      ' +
            ''.join(
                f' c{columna:<2}'
                for columna in range( ancho )
            )
        )

        separador = (
            '      ' +
            '+---' * ancho +
            '+'
        )

        lineas = [ encabezado, separador ]

        for fila in range( self.m_Alto ):

            texto_fila = f'f{fila:<4} |'

            for columna in range( ancho ):

                celda = self.m_Grilla[
                    fila * ancho + columna
                ]

                pista  = celda[ 'pista' ]
                region = celda[ 'region' ]

                if pista is not None:

                    contenido = str( pista ).center( 3 )

                elif region is not None:

                    letra = self._LETRAS[
                        ( region - 1 ) % len( self._LETRAS )
                    ]

                    contenido = f' {letra} '

                else:
                    contenido = '   '

                texto_fila += contenido + '|'

            lineas.append( texto_fila )
            lineas.append( separador )

        return '\n'.join( lineas )