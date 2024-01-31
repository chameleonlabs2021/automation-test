import csv
import json

# Path to the JSON file
json_file_path = 'products/AutoInsurance/policy/exposures/vehicle/exposure.json'

try:
    # Open and load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

except FileNotFoundError:
    print(f"Error: The file at {json_file_path} was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: The file at {json_file_path} is not a valid JSON file.")
    exit()

# Function to process each field into a list of CSV rows
def process_field(field):
    # Select only the required fields
    row = {k: field[k] for k in ('name', 'title', 'width', 'type', 'values') if k in field}
    # Check if field type is 'select' and format values as a JSON string
    if row.get('type') == 'select' and 'values' in row:
        row['values'] = json.dumps(row['values'])
    # Initialize list of rows
    rows = [row]
    return rows

# Process each field and flatten the list of rows
rows = [row for field in data['fields'] for row in process_field(field)]

# Writing to csv
csv_file = 'vehicle_fields.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'title', 'width', 'type', 'values'])
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV file '{csv_file}' created successfully.")
