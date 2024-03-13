import json

# Read the JSON data from data.json
with open('data.json', 'r') as f:
    data = json.load(f)

# Extract items from the JSON data
items = data['Items']

# Transform items into the expected format
request_items = {}
table_name = 'migration-table'
request_items[table_name] = []

for item in items:
    put_request = {
        'PutRequest': {
            'Item': {}
        }
    }

    for key, value in item.items():
        attribute_name = list(value.keys())[0]  # Extract the attribute name
        attribute_value = list(value.values())[0]  # Extract the attribute value
        put_request['PutRequest']['Item'][key] = {attribute_name: attribute_value}

    request_items[table_name].append(put_request)

# Generate the final JSON data
final_data = json.dumps(request_items, indent=4)

# Write the final JSON data to a new file
with open('batch_write_data.json', 'w') as f:
    f.write(final_data)

print("Conversion completed. Output saved to batch_write_data.json")
