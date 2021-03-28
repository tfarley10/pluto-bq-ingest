from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import re
import pandas as pd

zip_files = pd.read_csv('./etc/zip_links.csv')


def f_file_name(path: str):
    return path.rsplit("/", 1)[1]


def is_terminal(path: str):
    return bool(re.findall('[.]', path))


def terminal_filter(paths: list):
    return [*filter(is_terminal, paths)]


def make_paths_df(paths: list, year):
    return pd.DataFrame({'file': terminal_filter(paths), 'year': year})


def zip_names(p):
    with urlopen(p.path) as zipresp:
        print(f"downloading {f_file_name(p.path)}")
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            return make_paths_df(zfile.namelist(), p.year)


files = zip_files.apply(zip_names, axis=1)
file_df = pd.concat(files.values.tolist())
file_df.to_csv('./etc/pluto_files_agg.csv', index=False)
