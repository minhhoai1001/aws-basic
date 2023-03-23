import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)

def enable_version(bucket_name):
    versioning = s3_resource.BucketVersioning(bucket_name)
    versioning.enable()
    print(f'S3 Bucket versioning: {versioning.status}')

enable_version(S3_BUCKET_NAME)