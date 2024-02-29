from google.cloud import bigquery

def query_bigquery_table(service_account_json, table_id):
    """
    Query data from a BigQuery table.
    """

    query = f"""
        SELECT name, transform_name
        FROM `{table_id}`
        WHERE name LIKE '%Doe%'
    """

    # Authenticate
    client = bigquery.Client.from_service_account_json(service_account_json)

    # Run the query
    query_job = client.query(query)

    # Collect and return the results
    results = query_job.result()

    return results