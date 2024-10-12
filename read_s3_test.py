import boto3
import json
from botocore.exceptions import ClientError
import streamlit as st
from datetime import datetime

# S3 Configuration
s3 = boto3.client('s3',
    aws_access_key_id=st.secrets["aws_credentials"]["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["aws_credentials"]["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["aws_credentials"]["AWS_DEFAULT_REGION"]
)
BUCKET_NAME = 'joke-annotation'

def list_s3_objects():
    """List all objects in the S3 bucket."""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        return response.get('Contents', [])
    except ClientError as e:
        print(f"Error listing objects: {e}")
        return []

def read_s3_object(key):
    """Read and parse a JSON object from S3."""
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except ClientError as e:
        print(f"Error reading object {key}: {e}")
        return None

def main():
    print(f"Listing objects in bucket: {BUCKET_NAME}")
    objects = list_s3_objects()
    
    if not objects:
        print("No objects found in the bucket.")
        return

    print(f"Found {len(objects)} objects:")
    for obj in objects:
        print(f"- {obj['Key']}")
        
        # Read and print the contents of each object
        data = read_s3_object(obj['Key'])
        if data:
            print(f"Contents of {obj['Key']}:")
            print(json.dumps(data, indent=2))
            
            # Convert timestamp to readable format
            if 'timestamp' in data:
                timestamp = datetime.fromtimestamp(data['timestamp'])
                print(f"Timestamp: {timestamp}")
            
            print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
