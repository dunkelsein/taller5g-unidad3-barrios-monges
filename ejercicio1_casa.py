# ejercicio1_casa.py
# Composicion geométrica de una casa utilizando el algoritmo DDA

from PIL import Image
import math

# -----------------------------------------------------------------------------
# Algoritmo DDA visto en clase 
# -----------------------------------------------------------------------------
def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una linea usando el algoritmo DDA."""
    dx, dy = x1 - x0, y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:
        return
    x_inc, y_inc = dx / pasos, dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc

# -----------------------------------------------------------------------------
# Funciones modulares para cada elemento geométrico
# -----------------------------------------------------------------------------
def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """
    Dibuja un rectangulo uniendo sus cuatro vértices (4 líneas DDA).
    (x0, y0) es la esquina superior izquierda, (x1, y1) la inferior derecha.
    """
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)  # Lado superior
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)  # Lado derecho
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)  # Lado inferior
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)  # Lado izquierdo

def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """
    Dibuja un triángulo conectando los tres vértices pasados como tuplas (3 líneas DDA).
    """
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)

def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """
    Dibuja un sol proyectando n_rayos mediante coordenadas polares desde un punto central (cx, cy).
    """
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x_fin = cx + int(radio * math.cos(angulo))
        y_fin = cy + int(radio * math.sin(angulo))
        dda(pixels, cx, cy, x_fin, y_fin, color, ancho, alto)

def dibujar_piso(pixels, y_piso, color, ancho, alto):
    """
    Traza una línea horizontal que atraviesa toda la imagen horizontalmente.
    """
    dda(pixels, 0, y_piso, ancho - 1, y_piso, color, ancho, alto)

def dibujar_humo(pixels, x_inicio, y_inicio, color, ancho, alto):
    """
    [Extensión voluntaria] Traza curvas/zigs en forma de humo saliendo de la chimenea.
    """
    # Primera espiral/onda de humo
    dda(pixels, x_inicio, y_inicio, x_inicio - 10, y_inicio - 25, color, ancho, alto)
    dda(pixels, x_inicio - 10, y_inicio - 25, x_inicio + 15, y_inicio - 50, color, ancho, alto)
    dda(pixels, x_inicio + 15, y_inicio - 50, x_inicio - 5, y_inicio - 75, color, ancho, alto)
    
    # Segunda onda de humo desplazada
    dda(pixels, x_inicio + 10, y_inicio, x_inicio + 25, y_inicio - 20, color, ancho, alto)
    dda(pixels, x_inicio + 25, y_inicio - 20, x_inicio + 5, y_inicio - 45, color, ancho, alto)

# -----------------------------------------------------------------------------
# Programa Principal
# -----------------------------------------------------------------------------
def main():
    ancho, alto = 600, 500
    
    # Lienzo con fondo azul cielo claro
    color_cielo = (200, 230, 255)
    imagen = Image.new("RGB", (ancho, alto), color_cielo)
    pixels = imagen.load()

    # Definicion de la paleta de colores 
    COLOR_PISO = (34, 139, 34)       # Verde pasto
    COLOR_CUERPO = (139, 69, 19)     # Marron madera
    COLOR_TECHO = (178, 34, 34)      # Rojo teja
    COLOR_PUERTA = (101, 67, 33)     # Marrón oscuro
    COLOR_VENTANAS = (30, 144, 255)  # Azul cristal
    COLOR_SOL = (255, 140, 0)        # Naranja radiante
    COLOR_HUMO = (128, 128, 128)     # Gris humo

    # 1. Línea de piso
    y_piso = 420
    dibujar_piso(pixels, y_piso, COLOR_PISO, ancho, alto)

    # 2. Cuerpo de la casa (Rectángulo principal)
    # Vértices: (150, 220) hasta (450, 420)
    dibujar_rectangulo(pixels, 150, 220, 450, y_piso, COLOR_CUERPO, ancho, alto)

    # 3. Techo de la casa (Triángulo)
    p_cumbre = (300, 100)
    p_alero_izq = (120, 220)
    p_alero_der = (480, 220)
    dibujar_triangulo(pixels, p_cumbre, p_alero_izq, p_alero_der, COLOR_TECHO, ancho, alto)

    # [Extensión] Chimenea sobre el techo
    # Chimenea compuesta por 3 líneas (rectángulo abierto en base)
    dda(pixels, 390, 160, 390, 110, COLOR_CUERPO, ancho, alto)
    dda(pixels, 390, 110, 420, 110, COLOR_CUERPO, ancho, alto)
    dda(pixels, 420, 110, 420, 183, COLOR_CUERPO, ancho, alto)
    # Humo saliendo de la chimenea
    dibujar_humo(pixels, 405, 110, COLOR_HUMO, ancho, alto)

    # 4. Puerta rectangular
    dibujar_rectangulo(pixels, 270, 300, 330, y_piso, COLOR_PUERTA, ancho, alto)

    # 5. Dos ventanas cuadradas (8 líneas en total)
    # Ventana izquierda
    dibujar_rectangulo(pixels, 180, 260, 240, 320, COLOR_VENTANAS, ancho, alto)
    # Ventana derecha
    dibujar_rectangulo(pixels, 360, 260, 420, 320, COLOR_VENTANAS, ancho, alto)

    # 6. Sol en esquina superior (al menos 8 líneas irradiando desde el centro)
    dibujar_sol(pixels, cx=90, cy=90, radio=60, n_rayos=12, color=COLOR_SOL, ancho=ancho, alto=alto)

    # Guardar imagen final
    imagen.save("casa.png")
    print("✓ Imagen generada con éxito: casa.png")

if __name__ == "__main__":
    main()