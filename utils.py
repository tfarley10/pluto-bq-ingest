import os
import pandas as pd
from fiona import open
from time import time
import geopandas as gpd

def get_ext(path):
    return path.rsplit('.', 1)[1].lower()


def list_all_files(filepath, filetypes):
    filetypes = [types.lower() for types in filetypes]
    paths = []
    get_ext = lambda x: x.rsplit('.', 1)[1].lower()
    for root, dirs, files in os.walk(filepath):
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

def read_shapefile(path):
    t0 = time()
    file = file_name(path)
    rows = nrows(path)
    print(f"{file} is  {rows} rows long")
    f = gpd.read_file(path)
    delta = round((time()-t0)/60,2)
    print(f"Reading {file} took {delta} minutes")
    return(f)

"""
    def read_shapefile(self):
        t0 = time()
        if self.chunks == None:
            print(f"{self.filename} is only {self.nrows} rows long, reading all at once")
            f = gpd.read_file(self.path)
            delta = round((time()-t0)/60,2)
            print(f"Reading {self.filename} took {delta} minutes")
            return(f)
        else:
            l = [*map(self.read_chunk, self.chunks)]
            l = pd.concat(l)
            delta = round((time()-t0)/60,2)
            print(f"Reading {self.filename} took {delta} minutes")
            return (l)
"""