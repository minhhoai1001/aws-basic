import pathlib
import boto3

BASE_DIR = pathlib.Path(__file__).parent.resolve()
AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_client = boto3.client("s3", region_name=AWS_REGION)

def upload_files(file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name.split("/")[-1]
    s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    print(f"'{file_name}' has been uploaded to '{bucket}'")


upload_files(f"{BASE_DIR}/README.md", S3_BUCKET_NAME, "README.md", args={'ServerSideEncryption': 'AES256'})