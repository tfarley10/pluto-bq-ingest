from utils import read_shapefile
import pandas as pd
from shapely import wkt
from janitor import clean_names


class PlutoYear:

    def __init__(self, shape_paths):


        pluto_filter = lambda x: ('unclipped' not in x) and ('mappluto' in x)
        shape_paths = list(filter(pluto_filter, shape_paths))


        print("aggregating shapefiles")
        if len(shape_paths) > 1:
            d = [read_shapefile(f) for f in shape_paths]
            d = pd.concat(d)
        else:
            d = read_shapefile(shape_paths[0])

        print("filling nulls geometries with empty polygons")
        d['geometry'] = d['geometry'].fillna()
        
        

        print("converting coordinate reference system to ESPG:4326")
        d = d.to_crs({'init': "EPSG:4326"})

        print("making well known text representation out of geometries")
        wkt_geom = d['geometry'].apply(lambda x: wkt.dumps(x))
        d = pd.DataFrame(d)
        d = d.drop(columns=['geometry'])
        d['wkt_geom'] = wkt_geom
        print("cleaning column names")
        d = d.clean_names()
        self.wkt_file = d
