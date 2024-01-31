import random
import string
import json

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_number(min_value, max_value):
    return random.randint(min_value, max_value)

def generate_random_data(field):
    field_type = field.get("type")
    
    if field_type == "select":
        values = field.get("values", [])
        if values:
            return random.choice(values)
    elif field_type == "string":
        length = field.get("length", 10)
        return generate_random_string(length)
    elif field_type == "number":
        min_value = field.get("min_value", 0)
        max_value = field.get("max_value", 100)
        return generate_random_number(min_value, max_value)
    elif field_type == "group":
        num_repeats = field.get("maximum", 1)
        sub_fields = field.get("fields", [])
        group_data = []
        for _ in range(num_repeats):
            sub_data = {}
            for sub_field in sub_fields:
                sub_field_name = sub_field["name"]
                sub_data[sub_field_name] = generate_random_data(sub_field)
            group_data.append(sub_data)
        return group_data
    
    return None  # Handle unknown field types

def generate_random_data_for_fields(fields):
    data = {}
    for field in fields:
        field_name = field["name"]
        data[field_name] = generate_random_data(field)
    return data


def create_multiple_policyholders(session, num_policyholders):
    sandbox_url = config['sandbox_url']
    policyholder_information_list = []
    policyholder_values_list = datagen()
    print("policyholder_values_list", policyholder_values_list)

    for policyholder_values in policyholder_values_list[:num_policyholders]:
        if isinstance(policyholder_values, dict) and 'values' in policyholder_values:
            correct_structure = {
                "values": policyholder_values['values'],
                "completed": True
            }

            response = session.post(f'{sandbox_url}/policyholder/create', json=correct_structure)
            policyholder_information = response.json()
            policyholder_information_list.append(policyholder_information)
        else:
            print(f'Invalid policyholder structure: {policyholder_values}')

    print(f'Created {len(policyholder_information_list)} policyholders')
    return policyholder_information_list

# Read the JSON schema from a file
json_file_path = "products/AutoInsurance/policy/policy.json"  # Replace with the actual file path
with open(json_file_path, 'r') as json_file:
    json_schema = json.load(json_file)

# Generate random data based on the schema
dummy_data = generate_random_data_for_fields(json_schema["fields"])
print("dummy_data:", dummy_data)
