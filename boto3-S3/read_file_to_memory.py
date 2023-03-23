import io
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_object = s3_resource.Object(S3_BUCKET_NAME, 'README.md')
with io.BytesIO() as f:
    s3_object.download_fileobj(f)
    f.seek(0)
    print(f'Downloaded content:\n{f.read()}')