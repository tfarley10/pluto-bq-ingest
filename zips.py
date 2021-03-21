from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from tempfile import mkdtemp
from utils import list_all_files
import os



def temp_sub(file):

    """Makes a subdirectory in the existing temporary directory to unzip a file"""

    new_dir = file.strip('.zip')
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_dir = mkdtemp(dir = new_dir)
    return(new_dir)

def dir_dic(zip_list):

    """Creates tmp directories for zipfiles, creates dictionary for zipfile -> directory"""
    zip_dir = [temp_sub(x) for x in zip_list]
    zip_dict = dict(zip(zip_list, zip_dir))
    return(zip_dict)

def unzip_child(zip_list):
    
    zip_dict = dir_dic(zip_list)

    for file, dir in zip_dict.items():
        with ZipFile(file) as zfile:
            print("Unzipping children")
            zfile.extractall(dir)

def unzip_to_temp(zipurl):

    """

    :param zipurl: url of MapPluto Zip file
    :return: temporary directory of unzipped shapefiles
    """

    dir = mkdtemp()

    with urlopen(zipurl) as zipresp:
        print(f"Downloading ZIPFile {zipurl}")
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            print("Unzipping file")
            zfile.extractall(dir)

    # does the shapefile contain more zipfiles?
    child_zips = list_all_files(dir, ['zip'])
    if len(child_zips) >0:
        unzip_child(child_zips)

    return(dir)
    



