import pandas as pd
import requests
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'),
                         os.getenv('SUPABASE_API_KEY'))

# Function to get ZIP codes for a given city and state using API-Ninjas


def get_zip_codes(city, state):
    print(f"Getting ZIP codes for {city}, {state}")

    headers = {'X-Api-Key': os.getenv('API_NINJAS_API_KEY')}
    try:
        response = requests.get(
            f"https://api.api-ninjas.com/v1/zipcode?city={city}&state={state}", headers=headers)
        # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        return response.json()  # Returns a list of ZIP code entries
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
        return []
    except Exception as err:
        print(f"An error occurred: {err}")
        return []

# Function to insert ZIP codes into the Supabase 'doula_zip' table


def insert_zip_codes(doula_id, zip_codes):
    print(f"Inserting ZIP codes for doula ID: {doula_id}")

    table_name = "doula_zip"
    rows_to_insert = [{'doula_id': doula_id, 'zip': entry['zip_code']}
                      for entry in zip_codes]
    try:
        response = supabase.table(table_name).insert(rows_to_insert).execute()
        # Check for errors - if the response contains an error, it will be raised as an exception
        if 'error' in response:
            raise Exception(response['error'])
        print(f"Successfully inserted ZIP codes for doula ID: {doula_id}")
    except Exception as e:
        print(f"Error inserting data: {e}")


# Fetch the doula data from the Supabase 'doula' table
try:
    doula_data_response = supabase.table("doula").select("*").execute()
    doula_data = pd.DataFrame(doula_data_response.data)
except Exception as e:
    print(f"Failed to fetch doula data: {e}")
    exit()

# Iterate through each doula entry, fetch ZIP codes, and insert into Supabase
for index, row in doula_data.iterrows():
    city_state = row['location'].split(', ')
    if len(city_state) == 2:
        city, state = city_state
        zip_codes = get_zip_codes(city, state.strip())
        if zip_codes:
            insert_zip_codes(row['id'], zip_codes)

# Output the completion of the task
print("Finished inserting ZIP codes into the Supabase 'doula_zip' table.")
