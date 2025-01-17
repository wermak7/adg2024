# Zadanie 13 
# Funkcja losowania stratyfikowanego

import geopandas as gpd
from shapely.geometry import Point

def sample_strata(vector_path, n):
    gdf = gpd.read_file(vector_path)
    sampled_points = []

    for _, row in gdf.iterrows():
        polygon = row.geometry
        bbox = polygon.bounds

        for _ in range(n):
            while True:
                x = random.uniform(bbox[0], bbox[2])
                y = random.uniform(bbox[1], bbox[3])
                point = Point(x, y)
                if polygon.contains(point):
                    sampled_points.append(point)
                    break

    sampled_gdf = gpd.GeoDataFrame(geometry=sampled_points, crs=gdf.crs)
    return sampled_gdf

result = sample_strata("C:/Users/weron/Documents/algorytmy/powiaty.gpkg", 5)
result.to_file("C:/Users/weron/Documents/algorytmy/wynik_stratyfikowane.gpkg", driver="GPKG")

