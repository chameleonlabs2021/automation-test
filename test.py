from faker import Faker
import json
import random
# Create an instance of the Faker class
fake = Faker()


def json_generator(input_file, output_file):
       state_code_random_choice =""
       with open(input_file, 'r') as f:
        data = json.load(f)
        random_data = {}
        for key, value in data.items():
            if isinstance(value, list) and value:
                choice = random.choice(value)
                # random_data[key] = choice
                if "state" in key and not state_code_random_choice:
                    state_code_random_choice = choice
                    random_data[key] = state_code_random_choice
                elif "state" in key and state_code_random_choice:
                    random_data[key] = state_code_random_choice
                else:
                    random_data[key] = choice
                    pass
            else:
                random_data[key] = value
        
        with open(output_file, 'w') as f:
            json.dump(random_data, f, indent=4)


input_file = 'master_json_file.json'
output_file = 'Random_data.json'

json_generator(input_file,output_file)

# states = [ "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
#         "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
#         "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
#     ]
# print(len(states))