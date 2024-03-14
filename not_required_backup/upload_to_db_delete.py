import json
import boto3

def upload_to_dynamodb(data, table_name, region_name):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)
    
    for item_data in data:
        put_request = item_data.get('PutRequest')
        if put_request:
            item = put_request.get('Item')
            if item:
                try:
                    table.put_item(Item=item)
                    print(f"Uploaded item: {item}")
                except Exception as e:
                    print(f"Failed to upload item: {item}, Error: {e}")

if __name__ == "__main__":
    json_data = {
        "mig-dev03-connect-p-ssp-extensions": [
            {
                "PutRequest": {
                    "Item": {
                        "Extension": {"S": "29866"},
                        "ExtensionType": {"S": "agent"},
                        "ExtensionTypeValue": {"S": "agent2"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Extension": {"S": "298662"},
                        "ExtensionType": {"S": "agent11"},
                        "ExtensionTypeValue": {"S": "agent21"}
                    }
                }
            }
        ]
    }

    table_name = "mig-dev03-connect-p-ssp-extensions"  # Replace with your DynamoDB table name
    region_name = "us-west-2"  # Replace with your desired AWS region
    
    upload_to_dynamodb(json_data['mig-dev03-connect-p-ssp-extensions'], table_name, region_name)
