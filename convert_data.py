import json

def filter_empty_values(data):
    if isinstance(data, dict):
        filtered_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                filtered_value = filter_empty_values(value)
                if filtered_value:  # Only add non-empty dictionaries
                    filtered_data[key] = filtered_value
            elif value and not value.isspace():  # Check if value is not null or empty
                filtered_data[key] = value
        return filtered_data
    else:
        return data  # Return data unchanged if it's not a dictionary

def convert_to_dynamodb_format(data):
    dynamodb_data = []
    for item in data:
        filtered_item = filter_empty_values(item)
        dynamodb_item = {
            "PutRequest": {
                "Item": {
                    key: {"S": str(value)}  # Convert all values to strings
                    for key, value in filtered_item.items()
                }
            }
        }
        dynamodb_data.append(dynamodb_item)
    return dynamodb_data

# Load input data from JSON file
with open('data.json') as f:
    input_data = json.load(f)

# Ensure input data is a list of dictionaries
if isinstance(input_data, list):
    # Convert data to DynamoDB format
    dynamodb_data = convert_to_dynamodb_format(input_data)

    # Print the DynamoDB formatted data
    print(json.dumps({"migration-table": dynamodb_data}, indent=4))
else:
    print("Input data must be a list of dictionaries.")
