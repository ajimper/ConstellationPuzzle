import os
import starplot
from starplot.styles import PlotStyle
from starplot.projections import ProjectionBase, CenterRADEC
from starplot.data import constellations, catalogs
import cartopy.crs as ccrs
from ibis import _ as ibis_table
from PIL import Image
import numpy as np
from shapely.geometry import MultiPolygon, Polygon

# 1. Extensión para Proyección Gnomónica
class Gnomonic(ProjectionBase, CenterRADEC):
    _ccrs = ccrs.Gnomonic

# 2. Configuración de Escala Uniforme
RESOLUTION = 1024
MARGIN_DEGREES = 20
SCALE = 1.0

def generate_constellation_piece(iau_id, name_es, ra_d, dec_d, boundary_geom, output_dir="constellations"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Estilo base
    style = PlotStyle()
    style.background_color = "#ffffff"
    style.star.marker.color = "#000000"
    style.constellation_lines.color = "#444444"
    style.constellation_labels.font_color = "#000000"
    style.milky_way.fill_color = "#cccccc"
    style.milky_way.alpha = 0.4
    style.ecliptic.line.color = "#ff0000"
    style.celestial_equator.line.color = "#0000ff"
    
    try:
        # Asegurar que la geometría sea válida para starplot clip_path
        p = starplot.MapPlot(
            projection=Gnomonic(center_ra=ra_d, center_dec=dec_d),
            ra_min=ra_d - MARGIN_DEGREES,
            ra_max=ra_d + MARGIN_DEGREES,
            dec_min=dec_d - MARGIN_DEGREES,
            dec_max=dec_d + MARGIN_DEGREES,
            style=style,
            resolution=RESOLUTION,
            clip_path=boundary_geom,
            scale=SCALE
        )

        p.milky_way()
        p.stars(where=[ibis_table.magnitude < 6.0], where_labels=[ibis_table.magnitude < 3.0])
        p.constellations()
        p.dsos(where=[ibis_table.magnitude < 7.0])
        p.gridlines(labels=True)
        p.ecliptic()
        p.celestial_equator()
        
        temp_png = os.path.join(output_dir, f"{iau_id}.png")
        p.export(temp_png)
        
        with Image.open(temp_png) as img:
            img.save(os.path.join(output_dir, f"{iau_id}.gif"))
        
        os.remove(temp_png)
        print(f"Pieza generada: {name_es} ({iau_id})")
        return True
    except Exception as e:
        print(f"Error en {iau_id}: {e}")
        return False

if __name__ == "__main__":
    c_table = constellations.table(catalogs.CONSTELLATIONS_IAU, "es")
    all_constellations = c_table.execute()
    
    print(f"Iniciando generación de piezas...")
    target_ids = ["ori", "uma", "cru", "sco", "cyg", "leo", "cas", "lyr", "per", "aur"]
    
    for _, row in all_constellations.iterrows():
        if row['iau_id'] in target_ids:
            generate_constellation_piece(
                row['iau_id'], 
                row['name'], 
                row['ra'], 
                row['dec'], 
                row['boundary']
            )
