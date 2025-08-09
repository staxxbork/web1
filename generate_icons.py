import os
import cairosvg

def generate_pwa_icons():
    """Genera íconos de diferentes tamaños para la PWA a partir del SVG base."""
    # Asegúrate de que el directorio de imágenes existe
    os.makedirs('static/images', exist_ok=True)
    
    # Tamaños de íconos requeridos para PWA
    icon_sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Ruta al archivo SVG original
    svg_path = 'static/images/icon.svg'
    
    if not os.path.exists(svg_path):
        print(f"Error: No se encontró el archivo SVG en {svg_path}")
        return
    
    # Generar cada tamaño de ícono
    for size in icon_sizes:
        output_path = f'static/images/icon-{size}.png'
        try:
            cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=size, output_height=size)
            print(f"Generado: {output_path}")
        except Exception as e:
            print(f"Error al generar {output_path}: {e}")

if __name__ == "__main__":
    print("Generando íconos para la PWA...")
    generate_pwa_icons()
    print("Proceso completado.")