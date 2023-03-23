import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_client = boto3.client("s3", region_name=AWS_REGION)
def gen_signed_url(bucket_name, object_name):
    url = s3_client.generate_presigned_url(ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=3600)
    print(url)
gen_signed_url(S3_BUCKET_NAME, 'demo.txt')