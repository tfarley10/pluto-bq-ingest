import os
import pandas as pd
from fiona import open
from time import time
import geopandas as gpd

def get_ext(path):
    return path.rsplit('.', 1)[1].lower()


def list_all_files(dir:str, filetypes:list):

    """

    :param dir: directory to walk
    :param filetypes: list of filetypes that should be returned (eg. [pdf,htm])
    :return: list of paths to files specified by filetypes
    """

    filetypes = [types.lower() for types in filetypes]
    paths = []
    get_ext = lambda x: x.rsplit('.', 1)[1].lower()
    for root, dirs, files in os.walk(dir):
        for file in files:
            if get_ext(file) in filetypes:
                paths.append(os.path.join(root, file))
    paths = [p.lower() for p in paths]
    return (paths)


def get_terminal_path(df:pd.DataFrame, col_name:str):
     return df[col_name].str.rsplit('/', n = 1, expand = True).loc[:,1]

def nrows(path):
    return len(open(path))

def file_name(path):
    return path.rsplit('/',1)[1]


def make_chunks(gf_rows, size=5 * 10 ** 4):

    """

    :param gf_rows: number of rows in spatial data file
    :param size: # of rows to read in each slice
    :return: list of slices that will `chunk` the file read
    """
    starts = list(range(0, gf_rows, size))
    ends = list(range(size, gf_rows + size, size))
    slices = [slice(start, end, 1) for start, end in zip(starts, ends)]
    return (slices)


def read_chunks(path):

    """

    :param path: path to spatial file
    :return: geodataframe
    """
    with open(path) as g:
        rows = len(g)

    chunks = make_chunks(rows)
    name = file_name(path)

    for c in chunks:
        print(f'reading from {c.start} to {c.stop} rows from {name}')
        d = [gpd.read_file(path, rows=c)]
    d = pd.concat(d)
    return (d)

def read_shapefile(path):
    t0 = time()
    file = file_name(path)
    rows = nrows(path)
    print(f"{file} is  {rows} rows long")
    f = gpd.read_file(path)
    delta = round((time()-t0)/60,2)
    print(f"Reading {file} took {delta} minutes")
    return(f)

