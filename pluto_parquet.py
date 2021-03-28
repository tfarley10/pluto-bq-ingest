import pandas as pd
import geopandas as gpd
from janitor import clean_names
import fiona
from functools import partial


def clipped(path: str):
    return ('unclipped' not in path) and ('mappluto' in path)


def filter_clipped(path_list: list):
    return list(filter(clipped, path_list))


def nrows(path):
    return len(fiona.open(path))


def make_chunks(path, size=5 * 10 ** 4):

    """
    :param gf_rows: number of rows in spatial data file
    :param size: # of rows to read in each slice
    :return: list of slices that will `chunk` the file read
    """
    df_rows = nrows(path)
    starts = list(range(0, df_rows, size))
    ends = list(range(size, df_rows + size, size))
    slices = [slice(start, end, 1) for start, end in zip(starts, ends)]
    return slices


def file_name(path):
    return path.rsplit('/',1)[1]


def read_chunk(path, chunk:slice):

    """

    :param path: path to spatial file
    :return: geodataframe
    """
    name = file_name(path)
    print(f'reading from {chunk.start} to {chunk.stop} rows from {name}')
    return gpd.read_file(path, rows=chunk)


def transform_gdf(gdf: gpd.GeoDataFrame):

    print("transforming dataframe")
    transformed = gdf.copy(deep=False)
    transformed = transformed.to_crs({'init': "ESPG: 4326"})
    transformed['geometry'] = transformed["geometry"].fillna()
    transformed = transformed.clean_names()

    return transformed


def read_transform(path: str, chunk: slice):
    chunk_gdf = read_chunk(path, chunk)
    return transform_gdf(chunk_gdf)


def agg_from_path(path):
    chunks = make_chunks(path)
    read_t = partial(read_transform, path=path)

    return pd.concat(list(map(read_t, chunks)))







