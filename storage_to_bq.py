from google.cloud import storage
from google.cloud import bigquery
import etc.secret
from google.cloud.exceptions import NotFound

storage_client = storage.Client()
bq_client = bigquery.Client()


pluto_bucket = 'raw-pluto'
blobs = storage_client.list_blobs(pluto_bucket)
pluto_blob = [blob.name for blob in blobs]


table_id = ['pluto-panel.raw.pluto_' + x.strip('.csv') for x in pluto_blob]
uri = ['gs://raw-pluto/'+ x for x in pluto_blob]
storage_bq_map = dict(zip(uri, table_id))


def load_from_uri(uri, table_id):
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV)

    try:
        bq_client.get_table(table_id)
        print(f"table {table_id} already exists")
    except NotFound:
        load_job = bq_client.load_table_from_uri(
            uri, table_id, job_config=job_config)  # Make an API request.
        load_job.result()  # Waits for the job to complete.
        destination_table = bq_client.get_table(table_id)
        print(f"Loaded {destination_table.num_rows} rows to {table_id}.")

for uri, table in storage_bq_map.items():
    load_from_uri(uri = uri, table_id = table)