import json
import boto3

def upload_to_dynamodb(json_file_path, table_name, region_name):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)
    
    with open(json_file_path) as f:
        data = json.load(f)
    
    for item in data['migration-table']:
        try:
            table.put_item(Item=item['PutRequest']['Item'])
            print(f"Uploaded item: {item['PutRequest']['Item']}")
        except Exception as e:
            print(f"Failed to upload item: {item['PutRequest']['Item']}, Error: {e}")

if __name__ == "__main__":
    json_file_path = "basic_table.json"  # Replace with the path to your JSON file
    table_name = "migration-table"  # Replace with your DynamoDB table name
    region_name = "us-west-2"  # Replace with your desired AWS region
    
    upload_to_dynamodb(json_file_path, table_name, region_name)
