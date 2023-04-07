import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb')
TABLE_MUSIC = 'music'
TABLE_LOGIN = 'login'


# Override the default JSON encoder to handle Decimal types.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

# Hander for POST and PATCH calls made to the /home page.
def lambda_handler(event, context):
    # POST request made during a query and also to get the user's username with their login email address.
    if event['httpMethod'] == 'POST':
        request_data = json.loads(event['body'])
        
        # The request data will contain a title, artist, or year for a query being run.
        if 'title' in request_data or 'artist' in request_data or 'year' in request_data:
            email = request_data.get('email')
            if email:
                return handle_search_songs(request_data, email)
            else:
                return get_response_body(400, "Email is required for search.")
        
        # The request data will contain an email address for a user's login.
        else:
            email = None
            try:
                email = json.loads(event['body'])['email']
                user = get_user_by_email(email)
    
                subscribed_songs = handle_get_subscribed_songs(user)
    
                return { 
                        'statusCode':200, 
                        'headers' : {
                            "Access-Control-Allow-Origin" : "*",
                            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,PATCH",
                            "Access-Control-Allow-Headers" : "Access-Control-Allows-Headers, Access-Control-Allow-Origin, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
                            },
                        'body':json.dumps({
                            'user_name' : user['user_name'], 
                            'subscribed_songs': subscribed_songs
                            }) 
                }
            except Exception as e:
                print(f"EXCEPTION: {e}. No email address used for login")
    
    # PATCH request made to subscribe or unsubscribe to a song.
    elif event['httpMethod'] == 'PATCH':
        if json.loads(event['body'])['action'] == 'subscribe':
            return handle_subscriptions(json.loads(event['body']), 'subscribe')
        
        elif json.loads(event['body'])['action'] == 'unsubscribe':
            return handle_subscriptions(json.loads(event['body']), 'unsubscribe')
        
    else:
        return get_response_body(405, "Invalid HTTP method.")
    

# Handles the subscribe and unsubscribe actions.
def handle_subscriptions(request_data, action):
    email = request_data.get('email')
    song_name = request_data.get('song_name')

    if not email or not song_name:
        return get_response_body(400, "Bad Request: Missing username or song name.")

    user = get_user_by_email(email)

    if not user:
        return get_response_body(400, "Bad Request: User not found.")

    if action == 'subscribe':
        add_song_to_user(user, song_name)
    elif action == 'unsubscribe':
        remove_song_from_user(user, song_name)

    return get_response_body(200, "Song added successfully.")


# Getting th existing list of subscribed songs for a user and adding a new song to it if it is not already there.
def add_song_to_user(user, song_name):
    user_email = user['email']
    subscribed_songs = user.get('subscribed_songs', [])
    if song_name not in subscribed_songs:
        subscribed_songs.append(song_name)
        update_user_songs(user_email, subscribed_songs)

# Getting the existing list of subscribed songs for a user and removing a song from it.
def remove_song_from_user(user, song_name):
    user_email = user['email']
    subscribed_songs = user.get('subscribed_songs', [])
    if song_name in subscribed_songs:
        subscribed_songs.remove(song_name)
        update_user_songs(user_email, subscribed_songs)

# Updates the subscribed songs list for a user in the login table.
def update_user_songs(email, subscribed_songs):
    table = dynamodb.Table(TABLE_LOGIN)
    table.update_item(
        Key={'email': email},
        UpdateExpression='SET subscribed_songs = :subscribed_songs',
        ExpressionAttributeValues={':subscribed_songs': subscribed_songs}
    )

# Uses the email address to return the respective row of data from the login table.
def get_user_by_email(email):
    table = dynamodb.Table(TABLE_LOGIN)
    response = table.get_item(Key={'email': email})
    return response.get('Item')

# Returns a response body with a particular status code and message.
def get_response_body(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,PATCH",
            "Access-Control-Allow-Headers": "Access-Control-Allows-Headers, Access-Control-Allow-Origin, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        },
        'body': json.dumps(message)
    }

# Finds songs a user has subscribed to in the login table.
# Looks for these songs in the music table.
# Returns all songs
def handle_get_subscribed_songs(user):
    subscribed_songs = user.get('subscribed_songs', [])
    table = dynamodb.Table(TABLE_MUSIC)

    songs = []

    # For each song a user has subscribed to, get the song from the music table using the title and artist. 
    for sub_song in subscribed_songs:
        title, artist = sub_song.split('-')
        response = table.get_item(Key={'title': title, 'artist': artist})

        if response.get('Item'):
            songs.append(response['Item'])
    
    # Convert the year to an integer.
    for song in songs:
        song['year'] = int(song['year'])

    return songs


# Handles the search for songs (the query)
def handle_search_songs(request_data, email):
    if not request_data:
        return {
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,PATCH",
                "Access-Control-Allow-Headers": "Access-Control-Allows-Headers, Access-Control-Allow-Origin, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
            },
            'body': json.dumps([])
        }

    title = request_data.get('title')
    artist = request_data.get('artist')
    year = request_data.get('year')

    if not title and not artist and not year:
        return get_response_body(400, "Please provide at least one of the following attributes: title, artist, or year.")

    table = dynamodb.Table(TABLE_MUSIC)
    filters = []

    # Add the filters to the query only if the respective attribute is provided during the  search.
    if title:
        filters.append("contains(#title, :title)")
    if artist:
        filters.append("contains(#artist, :artist)")
    if year:
        filters.append("#year = :year")

    # Create the filter expression using the AND operator.
    filter_expression = ' AND '.join(filters)

    # Create the expression attribute values only if the respective attribute is provided during the search.
    expression_attribute_values = {}
    if title:
        expression_attribute_values[':title'] = title
    if artist:
        expression_attribute_values[':artist'] = artist
    if year:
        expression_attribute_values[':year'] = decimal.Decimal(year)

    # Create the expression attribute names only if the respective attribute is provided during the search.
    expression_attribute_names = {}
    if title:
        expression_attribute_names["#title"] = "title"
    if artist:
        expression_attribute_names["#artist"] = "artist"
    if year:
        expression_attribute_names["#year"] = "year"

    # Perform the scan operation on the music table.
    if filter_expression:
        response = table.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
    else:
        response = table.scan()

    # Get user's subscribed songs
    user = get_user_by_email(email)
    subscribed_songs = set(user.get('subscribed_songs', []))

    # Filter out subscribed songs from search results
    filtered_items = [item for item in response['Items'] if f"{item['title']}-{item['artist']}" not in subscribed_songs]

    #  Return the search results.
    if filtered_items:
        for item in filtered_items:
            item['year'] = int(item['year'])  # Convert decimal to integer
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,PATCH",
                "Access-Control-Allow-Headers": "Access-Control-Allows-Headers, Access-Control-Allow-Origin, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
            },
            'body': json.dumps(filtered_items, cls=DecimalEncoder)
        }
    else:
        return get_response_body(404, "No search results found.")