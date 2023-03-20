import logging
import boto3
from botocore.exceptions import ClientError
import uuid

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            response = s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        
    except ClientError as e:
        logging.error(e)
        return False
    return response

if __name__ == "__main__":
    bucket_name = create_bucket_name('boto3-')
    region = "ap-southeast-1"

    bucket_response = create_bucket(bucket_name, region)
    if bucket_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Create S3 bucket {bucket_name} success")
