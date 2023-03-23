import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
def rename_s3_object(bucket_name, old_name, new_name):
    old_s3_object = s3_resource.Object(bucket_name, old_name)
    new_s3_object = s3_resource.Object(bucket_name, new_name)
    
    new_s3_object.copy_from(
        CopySource=f'{bucket_name}/{old_name}'
    )
    old_s3_object.delete()
    print(f'{bucket_name}/{old_name} -> {bucket_name}/{new_name}')

rename_s3_object(S3_BUCKET_NAME, 'generated_file.txt', 'demo.txt')