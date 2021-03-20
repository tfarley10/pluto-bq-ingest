import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
import pandas as pd
import os

"""
This creates zip_links.csv which scrapes all MapPluto links from 
BytesofBigApple Archives then filters for the most recent version from 
each MapPluto release
"""



# make request, parse links
archive_link = 'https://www1.nyc.gov/site/planning/data-maps/open-data/bytes-archive.page?sorts[year]=0'
h = httplib2.Http()
status, response = h.request(archive_link)
a_tags = BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a'))
links = [link['href'] for link in a_tags if link.has_attr('href')]


# filter links
reg_mappluto = '^(?=.*mappluto)'# contains mappluto
reg_not_fgdb = '(?!.*fgdb)' # is not fgdb
reg_zipfile = '.*(\.zip)$' # is a zipfile
reg_pluto_shapes = re.compile(reg_mappluto + reg_not_fgdb + reg_zipfile)
pluto_zips = [link for link in links if reg_pluto_shapes.findall(link)]

# extracting year, version from path
reg_year = 'pluto_([\d]{2})'
reg_version = 'v*([\d]+)?_*([\d])?'
reg_year_version = re.compile(reg_year + reg_version)
year_version = [re.findall(reg_year_version, link) for link in pluto_zips]
yv_list = [list(tup) for file in year_version for tup in file] # list of tuples to list of lists

# years
years = [int('20'+i[0]) for i in yv_list]

# parse versions
version = ['.'.join(list(i[1:])) for i in yv_list]
version_to_float = lambda x: 1.0 if x == '.'  else float(x)
versions_numeric = [*map(version_to_float, version)]

# to df, get latest version
df = pd.DataFrame({'path': pluto_zips,'year':years, 'version': versions_numeric})
df = df.iloc[df.groupby(['year'])['version'].agg(pd.Series.idxmax)]
path_prefix = 'https://www1.nyc.gov'
df['path'] = path_prefix + df['path']

out_path = os.getcwd() + '/data/zip_links.csv'

df.to_csv(out_path, index = False)