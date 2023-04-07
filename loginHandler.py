import json
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'login'

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        if event['path'] == '/login':
            return handle_login(json.loads(event['body']))
        elif event['path'] == '/register':
            return handle_register(json.loads(event['body']))
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Invalid path.')
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid httpMethod.')
        }

def handle_login(request_data):
    email = request_data.get('email')
    password = request_data.get('password')

    # Making sure user and pasword have both been entered.
    if not email or not password:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing email or password.')
        }


    # Retreiving the user from the database.
    user = get_user_by_email(email)

    # Validating entered details and giving generic error message if incorrect.
    if not user:
        return {
            'statusCode': 404,
            'body': json.dumps('Incorrect email address or password.')
        }

    if password != user['password']:
        return {
            'statusCode': 401,
            'body': json.dumps('Incorrect email address or password.')
        }

    # Allowing the user to login if credentials are correct.
    return {
        'statusCode': 200,
        'body': json.dumps('Login successful.')
    }

def handle_register(request_data):
    email = request_data.get('email')
    user_name = request_data.get('user_name')
    password = request_data.get('password')

    # Making sure something has been entered for all required fields .
    if not email or not user_name or not password:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing email, username, or password.')
        }

    # Making sure the email address is not already in use.
    user = get_user_by_email(email)
    if user:
        return {
            'statusCode': 400,
            'body': json.dumps('Email already exists.')
        }

    # Adding user details to the database.
    put_user(email, user_name, password)

    return {
        'statusCode': 200,
        'body': json.dumps('Signup successful.')
    }

# Get user from database. 
def get_user_by_email(email):
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={'email': email})
    return response.get('Item')

# Insert new entry in the database.
def put_user(email, user_name, password):
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={'email': email, 'user_name': user_name, 'password': password})
