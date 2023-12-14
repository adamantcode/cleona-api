import pandas as pd
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'),
                         os.getenv('SUPABASE_API_KEY'))

# Path to the CSV file
csv_file_path = 'doula.csv'

# Read the CSV data into a DataFrame
doula_data = pd.read_csv(csv_file_path)

# Replace NaN values with empty strings
doula_data.fillna('', inplace=True)

# Define the column mapping from the screenshot (assuming the order is the same as the CSV)
supabase_columns = [
    'profile_image_URL', 'name', 'location', 'service_range', 'website',
    'phone', 'birth_fee', 'birth_doula_experience', 'doula_training', 'type_of_practice',
    'clients_per_month', 'home_births', 'college_education', 'special_services_offered',
    'languages_spoken', 'fee_detail', 'birth_center_births', 'hospital_births_desc',
    'birth_center_births_desc', 'home_births_desc', 'postpartum_rate', 'postpartum_doula_experience',
    'certifications', 'volunteer_or_advocacy_work', 'service_area', 'hospital_births'
]

# Assign the new column names to the DataFrame
doula_data.columns = supabase_columns
doula_data = doula_data.drop('volunteer_or_advocacy_work', axis=1)


def insert_data(df, table_name):
    # Convert DataFrame to a list of dictionaries for insertion
    records = df.to_dict(orient='records')

    # Insert the records into the table
    response = supabase.table(table_name).insert(records).execute()

    # Check for errors
    if response.get('error'):
        print(f"Error inserting data: {response['error']}")
    else:
        print(
            f"Successfully inserted {len(response.data)} records into the '{table_name}' table.")


# Table name in Supabase
table_name = "doula"

# Call the function to insert the data into Supabase
insert_data(doula_data, table_name)
