def transform_names(rows):
    """
    Transform 'Doe' to 'Das' in the names from the fetched rows.
    """
    transformed_rows = []
    for row in rows:
        new_name = row['name'].replace('Doe', 'Das')
        transformed_row = {'name': new_name, 'transform_name': row['transform_name']}
        transformed_rows.append(transformed_row)
    return transformed_rows