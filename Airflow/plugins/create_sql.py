import json 


def json_to_sql(json_path, sql_path, p_key, table_name):
    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Open the SQL file to write the insert statements
    with open(sql_path, 'w') as sql_file:
        for record in data:
            columns = ', '.join(record.keys())
            values =  ', '.join([
            f"'{str(value).replace("'", "''")}'" if isinstance(value, str) else 
            'NULL' if value is None else 
            str(value)
            for value in record.values()
        ])
            sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) ON CONFLICT ({p_key}) DO NOTHING;\n"
            sql_file.write(sql_statement)