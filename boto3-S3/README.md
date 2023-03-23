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

![](https://editor.analyticsvidhya.com/uploads/20077boto3%20resource%20client.png)

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

## 3. Amazon S3 buckets

### 3.1 Creating a Bucket
To create one programmatically, you must first choose a name for your bucket. Remember that this name must be unique throughout the whole AWS platform, as bucket names are DNS compliant. If you try to create a bucket, but another user has already claimed your desired bucket name, your code will fail. Instead of success, you will see the following error: `botocore.errorfactory.BucketAlreadyExists`.

You can increase your chance of success when creating your bucket by picking a random name. You can generate your own function that does that for you. In this implementation, you’ll see how using the `uuid` module will help you achieve that. A UUID4’s string representation is 36 characters long (including hyphens), and you can add a prefix to specify what each bucket is for.

Here’s a way you can achieve that:
```
import uuid
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])
```

Boto3 will create the session from your credentials. You just need to take the region and pass it to `create_bucket()` as its `LocationConstraint` configuration. Here’s how to do that:

```
def create_bucket(bucket_name, region=None):
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
```

### 3.2 Upload file to S3 Bucket
The Boto3 library has two ways for uploading files and objects into an S3 Bucket:

- `upload_file()` method allows you to upload a file from the file system
- `upload_fileobj()` method allows you to write access and upload a file binary object data

**Uploading a file to S3 Bucket**

The `upload_file()` method requires the following arguments:

- `file_name` – filename on the local filesystem
- `bucket_name` – the name of the S3 bucket
- `object_name` – the name of the uploaded file (usually equal to the file_name)

```
#!/usr/bin/env python3
import pathlib
import boto3

BASE_DIR = pathlib.Path(__file__).parent.resolve()
AWS_REGION = "us-east-2"
S3_BUCKET_NAME = "hands-on-cloud-demo-bucket"
s3_client = boto3.client("s3", region_name=AWS_REGION)
def upload_files(file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name.split("/)[-1]
    s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    print(f"'{file_name}' has been uploaded to '{S3_BUCKET_NAME}'")
upload_files(f"{BASE_DIR}/files/demo.txt", S3_BUCKET_NAME)
```

You can use S3 Server-Side Encryption (SSE-S3) encryption to protect your data from users access in Amazon S3. We will use server-side encryption, which uses the AES-256 algorithm:

**Generated file object data to S3 Bucket**

If you need to upload file like object data to the Amazon S3 Bucket, you can use the `upload_fileobj()` method. This method might be useful when you need to generate file content in memory (example) and then upload it to S3 without saving it on the file system.

>**Note**: the `upload_fileobj()` method requires opening a file in **binary mode**.

Here’s an example of uploading a generated file to the S3 Bucket:
```
import io
import boto3
AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_client = boto3.client("s3", region_name=AWS_REGION)

def upload_generated_file_object(bucket, object_name):
    with io.BytesIO() as f:
        f.write(b'First line.\n')
        f.write(b'Second line.\n')
        f.seek(0)
        s3_client.upload_fileobj(f, bucket, object_name)

        print(f"Generated has been uploaded to '{bucket}'")

upload_generated_file_object(S3_BUCKET_NAME, 'test/generated_file.txt')
```

### 3.3 List all S3 Bucket
There are two ways of listing all the buckets of the Amazon S3 Buckets:

- `list_buckets()` method of the client resource
- `all()` method of the S3 buckets resource

**Listing S3 Buckets using Boto3 client**
```
import boto3

# Retrieve the list of existing buckets
AWS_REGION = "ap-southeast-1"
s3 = boto3.client('s3', region_name=AWS_REGION)
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
```

**Listing S3 Buckets using Boto3 resource**
```
import boto3

AWS_REGION = "ap-southeast-1"
resource = boto3.resource("s3", region_name=AWS_REGION)
iterator = resource.buckets.all()
print("Listing Amazon S3 Buckets:")
for bucket in iterator:
    print(f"-- {bucket.name}")
```
**Filtering results of S3 list operation**

If you need to get a list of S3 objects whose keys are starting from a specific prefix, you can use the .`filter()` method to do this:

```
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)

print('Listing Amazon S3 Bucket objects/files:')
for obj in s3_bucket.objects.filter(Prefix='RE'):
    print(f'-- {obj.key}')
```

### 3.4 Download file from S3 Bucket
**Download file to local**

You can use the `download_file()` method to download the S3 object to your local file system

```
import boto3
AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_object = s3_resource.Object(S3_BUCKET_NAME, 'README.md')
s3_object.download_file('/tmp/README.md')
print('S3 object download complete')
```

**Read files from the S3 bucket into memory**
```
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
```

### 3.5 Delete S3 Bucket
There are two possible ways of deletingAmazon S3 Bucket using the Boto3 library:

- `delete_bucket()` method of the S3 client
- `delete()` method of the S3.Bucket resource

**Deleting S3 Buckets using Boto3 client**

```
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

client = boto3.client("s3", region_name=AWS_REGION)
client.delete_bucket(Bucket=S3_BUCKET_NAME)
print("Amazon S3 Bucket has been deleted")
```

**Deleting non-empty S3 Bucket**

To delete an S3 Bucket using the Boto3 library, you must clean up the S3 Bucket. Otherwise, the Boto3 library will raise the BucketNotEmpty exception to the specified bucket, which is a non empty bucket. The cleanup operation requires deleting all existing versioned bucket like S3 Bucket objects and their versions:

```
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)

def cleanup_s3_bucket():
    # Deleting objects
    for s3_object in s3_bucket.objects.all():
        s3_object.delete()
    # Deleting objects versions if S3 versioning enabled
    for s3_object_ver in s3_bucket.object_versions.all():
        s3_object_ver.delete()
    print("S3 Bucket cleaned up")
    
cleanup_s3_bucket()
s3_bucket.delete()
print("S3 Bucket deleted")
```

### 3.6 Copy and remane file object

There’s no single API call to rename an S3 object. So, to rename an S3 object, you need to copy it to a new object with a new name and then delete the old object:

```
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
rename_s3_object(S3_BUCKET_NAME, 'demo.txt', 'new_demo.txt')
```

### 3.7 Create S3 Bucket Policy
To specify requirements, conditions, or restrictions for accessing the Amazon S3 Bucket, you have to use Amazon S3 Bucket Policies. Here’s an example of the [Amazon S3 Bucket Policy to enforce HTTPS (TLS) connections to the S3 bucket](https://hands-on.cloud/terraform-how-to-enforce-tls-https-for-aws-s3-bucket/#policy-to-enforce-tls-https-for-aws-s3-bucket).

**Delete S3 Bucket Policy**

To delete the S3 Bucket Policy, you can use the `delete_bucket_policy()` method of the S3 client:
```
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_client = boto3.client("s3", region_name=AWS_REGION)
s3_client.delete_bucket_policy(Bucket=S3_BUCKET_NAME)
print('Bucket Policy has been deleted')
```

### 3.8 Generate S3 presigned URL
If you need to share files from a non-public Amazon S3 Bucket without granting access to AWS APIs to the final user, you can create a [pre-signed URL](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html#) to the Bucket Object:

```
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
```

The S3 client’s `generate_presigned_url()` method accepts the following parameters:

- `ClientMethod` (string) — The Boto3 S3 client method to presign for
- `Params` (dict) — The parameters need to be passed to the ClientMethod
- `ExpiresIn` (int) — The number of seconds the presigned URL is valid for. By default, the presigned URL expires in an hour (3600 seconds)
- `HttpMethod` (string) — The HTTP method to use for the generated URL. By default, the HTTP method is whatever is used in the method’s model

### 3.9 Enable S3 Bucket versioning
S3 Bucket versioning allows you to keep track of the S3 Bucket object’s versions and its latest version over time. Also, it safeguards against accidental object deletion of a currently existing object. Boto3 will retrieve the most recent version of a versioned object on request. When a new version of an object is added, the enabled versioning object takes up the storage size of the original file versions added together; i.e., a 2MB file with 5 versions will take up 10MB of space in the storage class.

To enable versioning for the S3 Bucket, you need to use the `enable_version()` method:

```
import boto3

AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "boto3-818f5862-ac4a-4706-a922-0e260c10a891"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)

def enable_version(bucket_name):
    versioning = s3_resource.BucketVersioning(bucket_name)
    versioning.enable()
    print(f'S3 Bucket versioning: {versioning.status}')

enable_version(S3_BUCKET_NAME)
```