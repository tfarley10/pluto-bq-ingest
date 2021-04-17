import pandas as pd
import geopandas as gpd
from janitor import clean_names
import fiona
from functools import partial
import utils


def filter_pluto(file_list:list) -> list:

    return list(filter(utils.is_pluto_path, file_list))


def make_chunks(path, size=5 * 10 ** 4):

    """
    :param gf_rows: number of rows in spatial data file
    :param size: # of rows to read in each slice
    :return: list of slices that will `chunk` the file read
    """
    df_rows = utils.shapefile_length(path)
    starts = list(range(0, df_rows, size))
    ends = list(range(size, df_rows + size, size))
    slices = [slice(start, end, 1) for start, end in zip(starts, ends)]

    return slices

def read_chunk(path, chunk:slice):

    """

    :param path: path to spatial file
    :return: geodataframe
    """
    name = utils.get_terminal(path)
    print(f'reading from {chunk.start} to {chunk.stop} rows from {name}')
    return gpd.read_file(path, rows=chunk)


def transform_gdf(gdf: gpd.GeoDataFrame):

    print("transforming dataframe")
    transformed = gdf.copy(deep=False)
    print("transforming crs")
    transformed = transformed.to_crs(epsg = 4326)
    transformed['geometry'] = transformed["geometry"].fillna()
    transformed = transformed.clean_names()

    return transformed


def read_transform(path: str, chunk: slice):
    
    chunk_gdf = read_chunk(path, chunk)
    
    return transform_gdf(chunk_gdf)




def agg_from_path(file_path):
    chunks = make_chunks(file_path)
    read_t = [read_transform(path = file_path, chunk = c) for c in chunks]

    return read_t

def agg_from_paths(file_paths:list):
    
    if len(file_paths) == 1:
        out = agg_from_path(file_paths[0])
        out = pd.concat(out, ignore_index = True)
        return out
    else:
        out = [agg_from_path(f) for f in file_paths]
        out = [pd.concat(g) for g in out]
        out = pd.concat(out, ignore_index = True)
        return out
        







