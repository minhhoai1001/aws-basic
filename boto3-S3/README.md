# Boto3 S3
**Boto3** is the name of the Python SDK for AWS. It allows you to directly create, update, and delete AWS resources from your Python scripts.

With the Boto3 S3 client and resources, you can perform various operations using Amazon S3 API, such as creating and managing buckets, uploading and downloading objects, setting permissions on buckets and objects, and more. You can also use the Boto3 S3 client to manage metadata associated with your Amazon S3 resources.

## 1. Installation

To install Boto3 on your computer, go to your terminal and run the following:
```
pip install boto3
```
You’ve got the SDK. But, you won’t be able to use it right now, because it doesn’t know which AWS account it should connect to.

To make it run against your AWS account, you’ll need to provide some valid credentials. If you already have an IAM user that has **full permissions to S3**, you can use those user’s credentials (their access key and their secret access key) without needing to create a new user. Otherwise, the easiest way to do this is to create a new AWS user and then store the new credentials.

To create a new user, go to your AWS account, then go to **Services** and select **IAM**. Then choose **Users** and click on **Add user**.

After created account, download `user_accessKeys.csv`

Now that you have your new user, create a new file, `~/.aws/credentials`:
```
touch ~/.aws/credentials
```
Open the file `user_accessKeys.csv` and paste the structure below. Fill in the placeholders with the new user credentials you have downloaded:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```
Save the file.

Now that you have set up these credentials, you have a default profile, which will be used by Boto3 to interact with your AWS account.

There is one more configuration to set up: the default region that Boto3 should interact with.

Create a new file, ~/.aws/config:
```
touch ~/.aws/config
```
Add the following and replace the placeholder with the region you have copied:
```
[default]
region = YOUR_PREFERRED_REGION
```

## 2. Client Versus Resource

At its core, all that Boto3 does is call AWS APIs on your behalf. For the majority of the AWS services, Boto3 offers two distinct ways of accessing these abstracted APIs:

- **Client**: low-level service access
- **Resource**: higher-level object-oriented service access

You can use either to interact with S3.

To connect to the low-level client interface, you must use Boto3’s `client()`. You then pass in the name of the service you want to connect to, in this case, s3:

```
import boto3
s3_client = boto3.client('s3')
```
To connect to the high-level interface, you’ll follow a similar approach, but use resource():
```
import boto3
s3_resource = boto3.resource('s3')
```

## 2. Amazon S3 buckets

### 2.1 Creating a Bucket
To create one programmatically, you must first choose a name for your bucket. Remember that this name must be unique throughout the whole AWS platform, as bucket names are DNS compliant. If you try to create a bucket, but another user has already claimed your desired bucket name, your code will fail. Instead of success, you will see the following error: `botocore.errorfactory.BucketAlreadyExists`.

You can increase your chance of success when creating your bucket by picking a random name. You can generate your own function that does that for you. In this implementation, you’ll see how using the `uuid` module will help you achieve that. A UUID4’s string representation is 36 characters long (including hyphens), and you can add a prefix to specify what each bucket is for.

Here’s a way you can achieve that:
```
import uuid
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])
```