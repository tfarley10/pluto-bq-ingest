import pandas as pd
from utils import list_all_files
from google.cloud import storage
import etc.secret
from zips import unzip_to_temp
from pluto_year import PlutoYear
from shutil import rmtree
import os

client = storage.Client()
bucket = client.bucket('raw-pluto')

zip_links = pd.read_csv('./etc/zip_links.csv').loc[16:]

for index, row in zip_links.iterrows():



    print(f"make blob for {row.year}.csv")
    blob = bucket.blob(f"{row.year}.csv")
    dir = unzip_to_temp(row.path)
    shapes = list_all_files(dir, ['shp'])
    print("make pluto-year objects")
    py = PlutoYear(shapes)
    print("save py obj to tmp_data.csv")
    py.wkt_file.to_csv('tmp_data.csv', index = False)
    print("clean tmp dir")
    rmtree(dir)
    blob.upload_from_filename('./tmp_data.csv')
    os.remove('tmp_data.csv')


if __name__ == '__main__':
    pass


