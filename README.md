# Ingesting [MapPluto](https://www1.nyc.gov/site/planning/data-maps/open-data/bytes-archive.page?sorts[year]=0) archives into Bigquery

1. /etc/scrape_links.py: scrapes relevant links of the most recent version of each shapefile from each year (2002-2020)
2. Unzip each zipfile to local temporary directory
3. For each year:
    - read shapefile in chunks
    - transform crs to 4326
    - geometry to wkt
4. Load csv into gcloud storage
5. storage -> Bigquery


## TODO:

1. Scrape and load all htm and pdf metadata files into storage
   - see if there is a way to get the metadata into tabular form to load as tables for easier lookups
2. Connect to dbt and start modelling
3. Document code better
4. Find a better way to recursively unzip nested zipfiles from urls
