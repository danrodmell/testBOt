from pyoso import Client
import os

os.environ["OSO_API_KEY"] = os.getenv("OSO_API_KEY", "")
client = Client()

# Probe artifacts_v1 for available columns
def get_columns(table):
    query = f"SELECT * FROM {table} LIMIT 1"
    df = client.to_pandas(query)
    return list(df.columns)

if __name__ == "__main__":
    tables = ["artifacts_v1", "projects_v1"]
    for table in tables:
        try:
            cols = get_columns(table)
            print(f"Columns in {table}: {cols}")
        except Exception as e:
            print(f"Could not get columns for {table}: {e}")
