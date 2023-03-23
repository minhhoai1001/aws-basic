import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)

print('Listing Amazon S3 Bucket objects/files:')
for obj in s3_bucket.objects.filter(Prefix='RE'):
    print(f'-- {obj.key}')