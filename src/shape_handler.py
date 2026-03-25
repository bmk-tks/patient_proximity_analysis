"""
shape_handler.py
Reads shapefiles and converts to GeoJSON for visualization
"""
import os
import geopandas as gpd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GEO_DIR = os.path.join(DATA_DIR, "geo")


def convert_shapefile_to_geojson(shp_folder, output_name):
    """
    Read a shapefile folder and convert to GeoJSON.
    
    Args:
        shp_folder: Path to folder containing .shp file
        output_name: Name for output .geojson file (without extension)
    
    Returns:
        Path to saved GeoJSON file
    """
    shp_files = [f for f in os.listdir(shp_folder) if f.endswith(".shp")]
    
    if not shp_files:
        raise FileNotFoundError(f"No .shp file found in {shp_folder}")
    
    shp_path = os.path.join(shp_folder, shp_files[0])
    gdf = gpd.read_file(shp_path)
    geojson = gdf.to_json()
    
    os.makedirs(GEO_DIR, exist_ok=True)
    output_path = os.path.join(GEO_DIR, f"{output_name}.geojson")
    
    with open(output_path, "w") as f:
        f.write(geojson)
    
    print(f"Converted {shp_path} -> {output_path}")
    print(f"   Features: {len(gdf)}")
    
    return output_path, geojson


def load_district_boundary():
    """Load Telangana 33 district boundary"""
    district_folder = os.path.join(GEO_DIR, "TS_District_Boundary_33")
    return convert_shapefile_to_geojson(district_folder, "telangana_districts")


def load_mandal_boundary():
    """Load Telangana 621 mandal boundary"""
    mandal_folder = os.path.join(GEO_DIR, "TS_Mandal_Boundary_621")
    return convert_shapefile_to_geojson(mandal_folder, "telangana_mandals")


if __name__ == "__main__":
    print("=== Converting District Boundary ===")
    dist_path, dist_geojson = load_district_boundary()
    
    print("\n=== Converting Mandal Boundary ===")
    mandal_path, mandal_geojson = load_mandal_boundary()