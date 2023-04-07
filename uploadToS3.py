import boto3
import json
import os
from botocore.exceptions import ClientError
import requests

# Note that this script assumes that the the S3 bucket has already been created on AWS.
# Hence, this script does not atempt to creata a new S3 bucket or check if one exists.

# Define the S3 bucket name and region as well as path to download images to locally
S3_BUCKET_NAME = 'devins-big-s3-bucket'
S3_REGION = 'us-east-1'
IMG_PATH = './Images/'
HTTP_200 = 200

# Access an enpoint and dowload an image from there into a specified local directory
def dowload_images_from_endpoint(fileNameWithPath, img_url):
    # Access the endpoint the image is hosted on
    response = requests.get(img_url)

    # Download the image if the endpoint was successfully accessed
    if response.status_code == HTTP_200:
        with open(fileNameWithPath, 'wb') as handler:
            handler.write(response.content)
            handler.close()

# Upload inamge from local directory to an existing S3 bucket
def upload_to_s3(fileNameWithPath, fileName, img_url):
    try:
        s3.upload_file(fileNameWithPath, S3_BUCKET_NAME, fileName)
        print(f"Image: '{img_url}'\nUploaded to S3 bucket: '{S3_BUCKET_NAME}'\n File name: '{fileName}'.\n")
    except ClientError as e:
        print(f"Error uploading image '{img_url}' to S3 bucket '{S3_BUCKET_NAME}': {e}")
    


# Create an S3 client
s3 = boto3.client('s3', region_name = S3_REGION)

# Load data from a1.json into the table
with open('a1.json', 'r') as file:
    data = json.load(file)
    
    for item in data['songs']:
        title = item['title']
        artist = item['artist']
        year = item['year']
        web_url = item['web_url']
        img_url = item['img_url']

        fileName = title + "-" + artist + ".jpg"
        fileNameWithPath = os.path.join(IMG_PATH, fileName)

        dowload_images_from_endpoint(fileNameWithPath, img_url)
        upload_to_s3(fileNameWithPath, fileName, img_url)


