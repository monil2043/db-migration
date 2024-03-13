import json

def transform_item(item):
    dynamodb_item = {}
    for key, value in item.items():
        if isinstance(value, dict) and 'S' in value:
            dynamodb_item[key] = value['S']
        elif isinstance(value, dict) and 'M' in value:
            sub_item = transform_item(value['M'])
            dynamodb_item[key] = sub_item
    return dynamodb_item

def convert_to_dynamodb_format(data):
    dynamodb_data = []
    for item in data['Items']:
        dynamodb_item = transform_item(item)
        dynamodb_data.append({
            'PutRequest': {
                'Item': dynamodb_item
            }
        })
    return dynamodb_data

# Load input data from JSON file
with open('data.json') as f:
    input_data = json.load(f)

# Convert data to DynamoDB format
dynamodb_data = convert_to_dynamodb_format(input_data)

# Write the DynamoDB formatted data to batch_write_data.json file
with open('batch_write_data.json', 'w') as outfile:
    json.dump({'migration-table': dynamodb_data}, outfile, indent=4)
