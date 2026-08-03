import mysql.connector as connection
import pandas as pd

'''
 Simulate the extraction step in an ETL job
'''
def extract_table_from_mysql(table_name, my_sql_connection):
  # Extract data from mysql table
  extraction_query = 'select * from ' + table_name
  df_table_data = pd.read_sql(extraction_query,my_sql_connection)
  return df_table_data

def transform_data_from_table(df_table_data):
  # If the DataFrame is empty, return it as is to avoid errors
  if df_table_data.empty:
    return df_table_data

  # Clean dates - convert to string
  object_cols = df_table_data.select_dtypes(include=['object']).columns

  for column in object_cols:
    # Only attempt to get type if the column has at least one non-null value
    if not df_table_data[column].dropna().empty:
      # Get the type from the first non-null value in the column
      dtype = str(type(df_table_data[column].dropna().iloc[0]))

      if dtype == "<class 'datetime.date'>":
        # Convert to string, handling potential NaT values
        df_table_data[column] = df_table_data[column].map(lambda x: str(x) if pd.notna(x) else x)

  return df_table_data

'''
 Simulate the load step in an ETL job
'''
def load_data_into_bigquery(bq_project_id, dataset,table_name,df_table_data):
  import pandas_gbq as pdbq
  full_table_name_bg = "{}.{}".format(dataset,table_name)
  pdbq.to_gbq(df_table_data,full_table_name_bg,project_id=bq_project_id,
  if_exists='replace')


kwargs = {
 # BigQuery connection details
 'bq_project_id': 'your_project_id',
 'dataset': 'your_dataset_name',
 # MySQL connection details
 'mysql_host': 'your_mysql_host',
 'mysql_user': 'your_mysql_user',
 'mysql_password': 'your_mysql_password',
 'mysql_database': 'your_mysql_database',
 'mysql_port': 25806 # make sure to set the correct port for your MySQL instance
}



def data_pipeline_mysql_to_bq(**kwargs):

  mysql_host = kwargs.get('mysql_host')
  mysql_database = kwargs.get('mysql_database')
  mysql_user = kwargs.get('mysql_user')
  mysql_password = kwargs.get('mysql_password')
  mysql_port = kwargs.get('mysql_port') #  Extract the port

  bq_project_id = kwargs.get('bq_project_id')
  dataset = kwargs.get('dataset')
  mydb = None # Initialize mydb to None
  try:
# Use explicit, clean variable mappings
    mydb = connection.connect(
        host=mysql_host,
        port=mysql_port,              #  2. You must pass the port explicitly
        user=mysql_user,
        password=mysql_password,      #  3. Fixed 'passwd' to 'password'
        database=mysql_database,
        ssl_disabled=False,           #  4. Force SSL compliance for Aiven
        use_pure=True
    )
    print("Successfully connected to OMNI_MANAGEMENT on Aiven!")

    all_tables_query = "Select table_name from information_schema.tables where table_schema = '{}'".format(mysql_database)
    # Removed parse_dates as it's not relevant for a query selecting table names
    df_tables = pd.read_sql(all_tables_query, mydb)

    if df_tables.empty:
      print(f"No tables found in database '{mysql_database}'. Skipping data ingestion.")
      return # Exit the function if no tables are found

    for table in df_tables.TABLE_NAME:
      table_name = table
      # Extract table data from MySQL
      df_table_data = extract_table_from_mysql(table_name, mydb)
      # Transform table data from MySQL
      df_table_data = transform_data_from_table(df_table_data)
      # Load data to BigQuery
      load_data_into_bigquery(bq_project_id,
      dataset,table_name,df_table_data)
      # Show confirmation message
      print("Ingested table {}".format(table_name))
  except Exception as e:
    print(str(e))
  finally:
    if mydb: # Only close if mydb was successfully created
      mydb.close() #close the connection


data_pipeline_mysql_to_bq(**kwargs)