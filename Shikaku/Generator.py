import random

MAX_RETRIES = 200   # intentos máximos de generación


# Generar puzzle
def generate( w, h, seed=None ):
    
    rng = random.Random( seed )

    for intento in range( 1, MAX_RETRIES + 1 ):

        # Generar una partición aleatoria del tablero
        solucion = _partition( w, h, rng )
        if solucion is None:
            continue   # greedy no cubrió todo, reintentar

        # Elegir una pista por rectángulo
        hints = _extract_hints( solucion, rng )

        return {
                'name' : f'Random {w}×{h} (seed={seed or "?"})',
                'size' : ( w, h ),
                'hints': hints,
                'tip'  : f'Randomly generated puzzle — {len(hints)} hints.',
            }
            
    raise RuntimeError(
        f'Could not generate a valid puzzle for {w}×{h} '
        f'after {MAX_RETRIES} attempts.'
    )



# Partición aleatoria

def _partition( w, h, rng ):
    total   = w * h
    libre   = list( range( total ) )   # Índices libres, en orden
    ocupado = [ False ] * total
    rects   = []

    max_area = max( 2, ( w * h ) // 3 )   # Cap de área para evitar rects enormes

    while libre:
        # Celda libre más arriba-izquierda
        k    = libre[ 0 ]
        r0   = k // w
        c0   = k % w

        candidatos = _rects_from( r0, c0, w, h, ocupado, max_area )

        if not candidatos:
            return None   # Sin opciones → fallo

        # Ponderación: favorece áreas entre 2 y 6
        pesos = [ _weight( r1, c1, r2, c2 ) for r1, c1, r2, c2 in candidatos ]
        rect  = rng.choices( candidatos, weights=pesos, k=1 )[ 0 ]

        r1, c1, r2, c2 = rect
        rects.append( rect )
        
        for r in range( r1, r2 + 1 ):
            for c in range( c1, c2 + 1 ):
                ocupado[ r * w + c ] = True

        libre = [ i for i in libre if not ocupado[ i ] ]


    return rects



def _rects_from( r0, c0, w, h, ocupado, max_area ):
    candidatos = []
    
    for r2 in range( r0, h ):
        
        for c2 in range( c0, w ):
            area = ( r2 - r0 + 1 ) * ( c2 - c0 + 1 )
            
            if area > max_area:
                break   # columna más ancha tampoco servirá en esta fila
            
            # verificar que todas las celdas estén libres
            ok = all(
                not ocupado[ r * w + c ]
                for r in range( r0, r2 + 1 )
                for c in range( c0, c2 + 1 )
            )
            
            if ok:
                candidatos.append( ( r0, c0, r2, c2 ) )
            else:
                break   # si esta columna falla, las siguientes también
        
    
    return candidatos


def _weight( r1, c1, r2, c2 ):
    area = ( r2 - r1 + 1 ) * ( c2 - c1 + 1 )
    if area == 1:
        return 0.3   # penalizar celdas solitarias
    if 2 <= area <= 8:
        return 3.0
    return 1.0       # áreas grandes, peso neutro


def _extract_hints( solucion, rng ):
    hints = {}
    for r1, c1, r2, c2 in solucion:
        area  = ( r2 - r1 + 1 ) * ( c2 - c1 + 1 )
        celdas = [
            ( r, c )
            for r in range( r1, r2 + 1 )
            for c in range( c1, c2 + 1 )
        ]
        pos = rng.choice( celdas )
        hints[ pos ] = area

    return hints

DIFICULTADES = {
    'facil'  : ( 4, 4 ),
    'medio'  : ( 6, 6 ),
    'dificil': ( 8, 8 ),
    'experto': ( 10, 10 ),
}

def generate_by_difficulty( dificultad, seed=None ):
    w, h = DIFICULTADES[ dificultad ]
    return generate( w, h, seed=seed )

