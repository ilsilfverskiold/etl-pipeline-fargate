from helper_functions.bigquery_insert import insert_rows_to_bigquery
from helper_functions.bigquery_query import query_bigquery_table
from helper_functions.transform_data import transform_names

def main():
    """
    Simple ETL Pipeline Template
    This code will execute as follows
    1. Extract: Get Rows with SQL Query for BigQuery - names with "Doe"
    2. Transform: Transform the rows - Change last name from "Doe" to "Das"
    3. Load: Insert new rows to BigQuery table - insert new rows with the last name "Das"

    For this script to execute:
    1) Create a dataset and datatable with a field called name (string).
    2) Change the table_id to your table id.
    3) Insert a few names in the table with Doe in it, i.e. John Doe, Jane Doe.
    4) Create a new service account and grant it BigQuery Job User at the account level.
    4) Make sure you grant your service account permissions at the dataset level as User/Editor. 
    5) Make sure this code has access to the credentials to the service account.
    """

    # Path to your service account credentials file & BigQuery table 
    service_account_json = 'google_credentials.json'
    table_id = "YOUR_TABLE_ID"

    # Extract - Get Rows
    fetched_rows = query_bigquery_table(service_account_json, table_id)

    # Transform - Transform Data
    transformed_rows = transform_names(fetched_rows)

    # Load - Insert Data
    insert_rows_to_bigquery(service_account_json, table_id, transformed_rows)

if __name__ == "__main__":
    main()