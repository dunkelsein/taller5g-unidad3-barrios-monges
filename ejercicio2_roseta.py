# ejercicio2_roseta.py
# Generador de rosetas geométricas mediante el algoritmo de Bresenham

from PIL import Image
import math
import colorsys

# -----------------------------------------------------------------------------
# Algoritmo de Bresenham visto en clase 
# -----------------------------------------------------------------------------
def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una línea usando el algoritmo de Bresenham para cualquier octante."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color

        if x == x1 and y == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

# -----------------------------------------------------------------------------
# Funciones auxiliares y de generación
# -----------------------------------------------------------------------------
def generar_puntos_circulo(cx, cy, radio, n):
    """
    Devuelve una lista de n puntos (x, y) equiespaciados sobre una circunferencia imaginaria.
    """
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos

def calcular_color_gradiente(angulo_promedio):
    """
    Calcula un color RGB dinámico en base al ángulo de la línea usando HSV.
    Esto genera un gradiente cromático suave a lo largo de toda la roseta.
    """
    # Normalizar el ángulo en el rango [0.0, 1.0]
    hue = (angulo_promedio % (2 * math.pi)) / (2 * math.pi)
    # Convertir HSV a RGB (Saturación=0.85, Valor=0.95 para colores vivos)
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 0.95)
    return (int(r * 255), int(g * 255), int(b * 255))

def dibujar_roseta(pixels, puntos, ancho, alto, paso=1):
    """
    Conecta pares de puntos en la circunferencia aplicando un gradiente cromático.
    - paso=1: Conecta TODOS los pares (roseta completa).
    - paso>1: Conecta con saltos entre puntos (extensión voluntaria).
    """
    n = len(puntos)
    cx, cy = ancho // 2, alto // 2
    
    for i in range(n):
        # Si paso == 1, j recorre todos los puntos desde i+1 (matriz completa)
        # Si paso > 1, conecta i con (i + paso) % n
        rango_j = range(i + 1, n) if paso == 1 else [(i + paso) % n]
        
        for j in rango_j:
            if paso > 1 and i > j:
                continue  # Evitar trazar la misma línea dos veces en el modo con salto
                
            p1, p2 = puntos[i], puntos[j]
            
            # Ángulo de la línea respecto al centro para el cálculo del gradiente
            dx = (p1[0] + p2[0]) / 2 - cx
            dy = (p1[1] + p2[1]) / 2 - cy
            angulo_linea = math.atan2(dy, dx)
            
            color = calcular_color_gradiente(angulo_linea)
            
            bresenham(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)

# -----------------------------------------------------------------------------
# Programa Principal
# -----------------------------------------------------------------------------
def main():
    ancho, alto = 700, 700
    cx, cy = 350, 350
    radio = 300
    
    variantes = [12, 24, 36]
    
    for n in variantes:
        # Lienzo en fondo negro para resaltar el gradiente
        img = Image.new("RGB", (ancho, alto), (10, 10, 15))
        pixels = img.load()
        
        puntos = generar_puntos_circulo(cx, cy, radio, n)
        dibujar_roseta(pixels, puntos, ancho, alto, paso=1)
        
        nombre_salida = f"roseta_{n}.png"
        img.save(nombre_salida)
        print(f"✓ Roseta N={n} guardada como: {nombre_salida}")
        
        if n == 24:
            img.save("roseta.png")
            print("✓ Copia principal guardada como: roseta.png")

    # 2. Extensiones voluntarias 
    # Cuarta roseta con N=48 conectando puntos no adyacentes (saltando de a 7 puntos)
    print("\n[Extensión] Generando cuarta roseta con salto de puntos no adyacentes...")
    img_ext = Image.new("RGB", (ancho, alto), (5, 5, 12))
    pixels_ext = img_ext.load()
    
    puntos_ext = generar_puntos_circulo(cx, cy, radio, n=48)
    dibujar_roseta(pixels_ext, puntos_ext, ancho, alto, paso=7)
    
    img_ext.save("roseta_salto_48.png")
    print("✓ Roseta especial guardada como: roseta_salto_48.png")

if __name__ == "__main__":
    main()