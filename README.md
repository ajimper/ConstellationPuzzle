# ConstellationPuzzle

Generador de piezas de rompecabezas de constelaciones basado en la proyección **Gnomónica** (tangente plana) para minimizar la deformación local y facilitar el encaje de las piezas.

## Características

- **Proyección Gnomónica**: Centrada en cada constelación para mantener líneas rectas y escala uniforme.
- **Máscaras de la IAU**: Cada pieza está recortada exactamente por los límites oficiales de la Unión Astronómica Internacional.
- **Contenido Astronómico**:
  - Estrellas hasta magnitud 6.0 con nombres para las más brillantes.
  - Objetos de cielo profundo (DSOs) notables.
  - Vía Láctea sombreada.
  - Eclíptica, Ecuador y Polos identificados.
- **Formato**: Genera imágenes GIF de alta resolución (1024x1024).

## Requisitos

```bash
pip install starplot cartopy pillow ibis-framework shapely
```

## Uso

Ejecuta el script principal para generar las piezas:

```bash
python generate_puzzle.py
```

Las piezas se guardarán en la carpeta `constellations/`.

---
Proyecto diseñado para entrenamiento educativo en el reconocimiento de constelaciones.
