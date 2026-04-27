import os
import sys

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo():
    """Muestra el título del juego con un marco decorativo."""
    print("\n" + "═" * 34)
    print("║          SHIKAKU             ║")
    print("║      El Juego de Rectángulos ║")
    print("╚" + "═" * 32 + "╝\n")

def mostrar_menu():
    """Dibuja el menú principal y devuelve la elección del usuario."""
    mostrar_titulo()
    print("  [1] Iniciar Partida")
    print("  [2] Cómo Jugar")
    print("  [3] Salir")
    print("\n" + "─" * 34)
    return input("  Elige una opción (1-3): ").strip()

def mostrar_instrucciones():
    """Pantalla con las reglas básicas de Shikaku."""
    limpiar_pantalla()
    mostrar_titulo()
    print("  REGLAS BÁSICAS DE SHIKAKU:")
    print("  • Divide la cuadrícula en regiones rectangulares.")
    print("  • Cada región debe contener exactamente UN número.")
    print("  • El área de la región debe ser IGUAL a ese número.")
    print("  • Todas las celdas deben pertenecer a una región.")
    print("  • No se permiten superposiciones ni celdas vacías.")
    print("\n" + "─" * 34)
    input("  Presiona Enter para volver al menú... ")

def iniciar_partida():
    """Placeholder para la transición al juego real."""
    limpiar_pantalla()
    mostrar_titulo()
    print("  Preparando tablero...")
    print("  Cargando interfaz de juego...")
    print("\n" + "─" * 34)
    print("  AQUÍ IRÍA LA LÓGICA DEL JUEGO")
    print("  (Tablero, entrada de usuario, validación, etc.)")
    print("\n" + "─" * 34)
    input("  Presiona Enter para volver al menú... ")

def main():
    """Bucle principal de la interfaz."""
    try:
        while True:
            limpiar_pantalla()
            opcion = mostrar_menu()

            if opcion == '1':
                iniciar_partida()
            elif opcion == '2':
                mostrar_instrucciones()
            elif opcion == '3':
                limpiar_pantalla()
                print("  ¡Gracias por jugar Shikaku!  \n")
                sys.exit(0)
            else:
                print("  Opción no válida. Intenta de nuevo.")
                input("  Presiona Enter para continuar... ")
    except KeyboardInterrupt:
        print("\n\n  Interrupción detectada. Saliendo...")
        sys.exit(0)

if __name__ == "__main__":
    main()