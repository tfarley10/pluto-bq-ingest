from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from tempfile import mkdtemp
from utils import list_all_files
import os



def temp_sub(file):
    new_dir = file.strip('.zip')
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_dir = mkdtemp(dir = new_dir)
    return(new_dir)

def dir_dic(zip_list):
    zip_dir = [temp_sub(x) for x in zip_list]
    foo = dict(zip(zip_list, zip_dir))
    return(foo)

def unzip_child(zip_list):
    
    bar = dir_dic(zip_list)

    for x, y in bar.items():
        with ZipFile(x) as zfile:
            print("Unzipping children")
            zfile.extractall(y)

def unzip_to_temp(zipurl):

    dir = mkdtemp()

    with urlopen(zipurl) as zipresp:
        print(f"Downloading ZIPFile {zipurl}")
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            print("Unzipping file")
            zfile.extractall(dir)
    child_zips = list_all_files(dir, ['zip'])
    if len(child_zips) >0:
        unzip_child(child_zips)

    return(dir)
    

"""
    shapes = list_all_files(dir, ['shp'])
    clipped_only = lambda x: x.lower('(?!.*unclipped)'
    shapes = re.findall('(?!.*unclipped)')
    metadata = list_all_files(dir, ['pdf', 'htm'])
"""



