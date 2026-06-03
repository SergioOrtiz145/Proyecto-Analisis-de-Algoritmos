import time


def generar_rectangulos_candidatos(r, c, area, ancho, alto):
    candidatos = []

    # Generar todos los rectángulos posibles, el área es igual a la pista
    for r1 in range(max(0, r - area + 1), r + 1):

        for c1 in range(max(0, c - area + 1), c + 1):

            # Buscar todas las combinaciones altura × ancho que produzcan el área
            for altura in range(1, area + 1):

                if area % altura != 0:
                    continue

                ancho_rect = area // altura

                r2 = r1 + altura - 1
                c2 = c1 + ancho_rect - 1

                # El rectángulo debe estar dentro del tablero
                if r2 >= alto or c2 >= ancho:
                    continue

                # La pista debe estar dentro del rectángulo
                if r1 <= r <= r2 and c1 <= c <= c2:
                    candidatos.append(
                        (r1, c1, r2, c2)
                    )

    return candidatos


def obtener_celdas(r1, c1, r2, c2):
    celdas = set()

    # Obtener todas las posiciones ocupadas por el rectángulo
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            celdas.add((r, c))

    return celdas


class MRVFCSolver:

    def __init__(self, ancho, alto, pistas):
        self.ancho = ancho
        self.alto = alto

        # Métricas para el desempeño
        self.nodes_explored = 0
        self.backtracks = 0
        self.max_depth = 0
        self.pruned_branches = 0

        self.pistas = dict(pistas)

        self.dominios = {}

        # Construir el dominio inicial de cada pista
        for posicion, numero in pistas.items():
            self.dominios[posicion] = (
                generar_rectangulos_candidatos(
                    posicion[0],
                    posicion[1],
                    numero,
                    ancho,
                    alto
                )
            )

    def solve(self):
        inicio = time.perf_counter()

        # Copia de trabajo de los dominios
        dominios_actuales = {}

        for pista, dominio in self.dominios.items():
            dominios_actuales[pista] = list(dominio)

        # Pistas ya resueltas
        asignadas = {}

        # Celdas ocupadas por rectángulos ya elegidos
        ocupadas = set()

        solucion = self._backtrack(
            dominios_actuales,
            asignadas,
            ocupadas,
            0
        )

        tiempo = time.perf_counter() - inicio

        return solucion, tiempo

    def _backtrack(self, dominios, asignadas, ocupadas, profundidad):
        self.nodes_explored += 1

        if profundidad > self.max_depth:
            self.max_depth = profundidad

        # Caso base: todas las pistas ya tienen rectángulo asignado y no se superponen
        if len(asignadas) == len(self.pistas):
            return dict(asignadas)

        # MRV: escoger la pista con menos candidatos disponibles
        pista = self._mrv( dominios, asignadas )

        # Intentar cada rectángulo posible
        for rectangulo in dominios[pista]:
            celdas_rectangulo = obtener_celdas(
                rectangulo[0],
                rectangulo[1],
                rectangulo[2],
                rectangulo[3]
            )

            # No dejar que haya superposición
            if len(celdas_rectangulo & ocupadas) > 0:
                continue

            # Asignar temporalmente el rectángulo
            asignadas[pista] = rectangulo

            nuevas_ocupadas = (
                ocupadas | celdas_rectangulo
            )

            # Forward Checking: actualizar dominios restantes
            nuevos_dominios, vacio = (
                self._forward_check(dominios,asignadas,nuevas_ocupadas)
            )

            if vacio:
                # Alguna pista se quedó sin opciones
                self.pruned_branches += 1

            else:
                resultado = self._backtrack(
                    nuevos_dominios,
                    asignadas,
                    nuevas_ocupadas,
                    profundidad + 1
                )

                # Solución encontrada
                if resultado is not None:
                    return resultado

            # Deshacer decisión (Backtracking)
            del asignadas[pista]

            self.backtracks += 1

        return None

    def _mrv(self, dominios, asignadas):
        mejor_pista = None
        menor_dominio = float("inf")

        # Buscar la pista más restringida
        for pista in self.pistas:
            if pista in asignadas:
                continue

            cantidad = len(dominios[pista])

            if cantidad < menor_dominio:
                menor_dominio = cantidad
                mejor_pista = pista

        return mejor_pista

    def _forward_check(self, dominios,asignadas, ocupadas):
        nuevos_dominios = {}

        # Revisar las pistas aún no asignadas
        for pista, candidatos in dominios.items():
            if pista in asignadas:
                nuevos_dominios[pista] = candidatos
                continue

            filtrados = []

            # Eliminar candidatos incompatibles
            for rectangulo in candidatos:
                celdas = obtener_celdas(
                    rectangulo[0],
                    rectangulo[1],
                    rectangulo[2],
                    rectangulo[3]
                )

                if len(celdas & ocupadas) == 0:
                    filtrados.append(rectangulo)

            # Si una pista pierde todas sus opciones, esta rama no puede llegar a una solución
            if len(filtrados) == 0:
                return nuevos_dominios, True

            nuevos_dominios[pista] = filtrados

        return nuevos_dominios, False