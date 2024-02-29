from google.cloud import bigquery

def insert_rows_to_bigquery(service_account_json, table_id, rows_to_insert):
    """
    Inserts rows into a BigQuery table.
    """

    # Authenticate
    client = bigquery.Client.from_service_account_json(service_account_json)

    # Insert rows
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")