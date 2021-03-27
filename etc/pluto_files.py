from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import re
import pandas as pd

zip_files = pd.read_csv('./etc/zip_links.csv')

f_file_name = lambda x: x.rsplit("/", 1)[1]
is_terminal = lambda x: bool(re.findall('[.]', x))
terminal_filter = lambda x: [*filter(is_terminal,x)]
file_to_df = lambda files, year: pd.DataFrame({'file': files, 'year': year})


def zip_names(p):
    with urlopen(p.path) as zipresp:
        print(f"downloading {f_file_name(p.path)}")
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            return terminal_filter(zfile.namelist()), p.year

def main(p):
    files, year = zip_names(p)
    return file_to_df(files, year)

files = zip_files.apply(main, axis = 1)
file_df = pd.concat(files.values.tolist())
file_df.to_csv('./etc/pluto_files_agg.csv', index = False)