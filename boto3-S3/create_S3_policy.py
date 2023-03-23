import json
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_client = boto3.client("s3", region_name=AWS_REGION)
BUCKET_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "s3:*"
            ],
            "Resource": [
                f"arn:aws:s3:::{S3_BUCKET_NAME}/*",
                f"arn:aws:s3:::{S3_BUCKET_NAME}"
            ],
            "Effect": "Deny",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                },
                "NumericLessThan": {
                    "s3:TlsVersion": 1.2
                }
            }
        }
    ]
}
policy_document = json.dumps(BUCKET_POLICY)
s3_client.put_bucket_policy(Bucket=S3_BUCKET_NAME, Policy=policy_document)
print('Bucket Policy has been set up')