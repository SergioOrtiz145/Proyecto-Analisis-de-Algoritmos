import random

MAX_RETRIES = 200   # Máximo número de intentos para generar un tablero válido


# Generar puzzle
def generate( w, h, seed = None ):

    generador_aleatorio = random.Random( seed )

    for intento in range( 1, MAX_RETRIES + 1 ):

        # Generar una partición aleatoria del tablero
        solucion = _partition( w, h, generador_aleatorio )

        if solucion is None:
            continue

        # Elegir una pista para cada rectángulo
        pistas = _extract_hints( solucion, generador_aleatorio )

        return {
            'name' : f'Aleatorio {w}×{h} (seed={seed or "?"})',
            'size' : ( w, h ),
            'hints': pistas,
            'tip'  : f'Tablero generado aleatoriamente - {len( pistas )} pistas.'
        }

    raise RuntimeError(
        f'No fue posible generar un tablero válido de {w}×{h} '
        f'después de {MAX_RETRIES} intentos.'
    )


# Crear una partición aleatoria del tablero
def _partition( w, h, generador_aleatorio ):

    total_celdas = w * h

    libres = list( range( total_celdas ) )
    ocupadas = [ False ] * total_celdas

    rectangulos = []

    # Limitar el tamaño máximo de los rectángulos
    area_maxima = max( 2, ( w * h ) // 3 )

    while libres:

        # Tomar la celda libre más arriba y a la izquierda
        indice = libres[ 0 ]

        fila_inicial = indice // w
        columna_inicial = indice % w

        candidatos = _rects_from(
            fila_inicial,
            columna_inicial,
            w,
            h,
            ocupadas,
            area_maxima
        )

        if not candidatos:
            return None

        # Favorecer rectángulos de tamaño medio
        pesos = [
            _weight( r1, c1, r2, c2 )
            for r1, c1, r2, c2 in candidatos
        ]

        rectangulo = generador_aleatorio.choices(
            candidatos,
            weights = pesos,
            k = 1
        )[ 0 ]

        r1, c1, r2, c2 = rectangulo

        rectangulos.append( rectangulo )

        # Marcar las celdas del rectángulo como ocupadas
        for fila in range( r1, r2 + 1 ):
            for columna in range( c1, c2 + 1 ):
                ocupadas[ fila * w + columna ] = True

        # Actualizar lista de celdas libres
        libres = [
            indice
            for indice in libres
            if not ocupadas[ indice ]
        ]

    return rectangulos


def _rects_from(
    fila_inicial,
    columna_inicial,
    w,
    h,
    ocupadas,
    area_maxima
):

    candidatos = []

    for fila_final in range( fila_inicial, h ):
        for columna_final in range( columna_inicial, w ):
            area = (
                ( fila_final - fila_inicial + 1 ) *
                ( columna_final - columna_inicial + 1 )
            )

            if area > area_maxima:
                break

            # Verificar que todas las celdas estén libres
            valido = all(
                not ocupadas[ fila * w + columna ]
                for fila in range( fila_inicial, fila_final + 1 )
                for columna in range( columna_inicial, columna_final + 1 )
            )

            if valido:
                candidatos.append(
                    (
                        fila_inicial,
                        columna_inicial,
                        fila_final,
                        columna_final
                    )
                )
            else:
                break

    return candidatos


def _weight( r1, c1, r2, c2 ):
    area = ( r2 - r1 + 1 ) * ( c2 - c1 + 1 )

    if area == 1:
        return 0.3   # Penalizar rectángulos de una sola celda

    if 2 <= area <= 8:
        return 3.0   # Favorecer áreas medianas

    return 1.0       # Peso normal para áreas grandes


def _extract_hints( solucion, generador_aleatorio ):
    pistas = {}

    for r1, c1, r2, c2 in solucion:

        area = ( ( r2 - r1 + 1 ) * ( c2 - c1 + 1 ) )

        celdas = [
            ( fila, columna )
            for fila in range( r1, r2 + 1 )
            for columna in range( c1, c2 + 1 )
        ]

        posicion_pista = generador_aleatorio.choice( celdas )
        pistas[ posicion_pista ] = area

    return pistas


DIFICULTADES = {
    'facil'   : ( 4, 4 ),
    'medio'   : ( 6, 6 ),
    'dificil' : ( 8, 8 ),
    'experto' : ( 10, 10 )
}


def generate_by_difficulty( dificultad, seed = None ):
    ancho, alto = DIFICULTADES[ dificultad ]

    return generate(
        ancho,
        alto,
        seed = seed
    )