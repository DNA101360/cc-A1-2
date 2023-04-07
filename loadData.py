import boto3
import json
import time

# Define the AWS region and DynamoDB table name
REGION = 'us-east-1'
TABLE_NAME = 'music'

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name = REGION)

# Define the table schema and attributes
table_schema = {
    'AttributeDefinitions': [
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'artist',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'title',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'artist',
            'KeyType': 'RANGE'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
    'TableName': TABLE_NAME
}

# Create the table in DynamoDB if one does not already exist
try:
    dynamodb.create_table(**table_schema)
    print(f'Table {TABLE_NAME} created successfully')
    
    # Giving time for the table to be created
    time.sleep(10)

except dynamodb.exceptions.ResourceInUseException:
    print(f'Table {TABLE_NAME} already exists')


# Load data from a1.json into the table
with open('a1.json', 'r') as file:
    data = json.load(file)
    
    for item in data['songs']:
        title = item['title']
        artist = item['artist']
        year = item['year']
        web_url = item['web_url']
        img_url = item['img_url']

        # Add the item to the DynamoDB table
        dynamodb.put_item(
            TableName = TABLE_NAME,
            Item={
                'title': {'S': title},
                'artist': {'S': artist},
                'year': {'N': str(year)},
                'web_url': {'S': web_url},
                'img_url': {'S': img_url},
            }
        )