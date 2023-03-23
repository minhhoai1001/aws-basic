# Lambda Layers
## 1. What are Lambda Layers?
Lambda layers provide a convenient way to package libraries and other dependencies that you can use with your Lambda functions. Using layers reduces the size of uploaded deployment archives and makes it faster to deploy your code.

You can use layers only with Lambda functions deployed as a .zip file archive. For functions defined as a container image, you package your preferred runtime and all code dependencies when you create the container.

You can create layers using the Lambda console, the Lambda API, AWS CloudFormation, or the AWS Serverless Application Model (AWS SAM).

## 2. Creating layer content
When you create a layer, you must bundle all its content into a .zip file archive. You upload the .zip file archive to your layer from Amazon Simple Storage Service (Amazon S3) or your local machine. Lambda extracts the layer contents into the /opt directory when setting up the execution environment for the function.
### 2.1 Compiling the .zip file archive for your layer

You build your layer code into a .zip file archive using the same procedure that you would use for a function deployment package. If your layer includes any native code libraries, you must compile and build these libraries using a Linux development machine so that the binaries are compatible with Amazon Linux.

When you create a layer, you can specify whether the layer is compatible with one or both of the instruction set architectures. You may need to set specific compile flags to build a layer that is compatible with the `arm64` architecture.

### 2.2 Including library dependencies in a layer
For each Lambda runtime, the PATH variable includes specific folders in the /opt directory. If you define the same folder structure in your layer .zip file archive, your function code can access the layer content without the need to specify the path.

The following table lists the folder paths that each runtime supports.

|Runtime	|Path|
|-----------|----|
|Node.js|nodejs/node_modules<br> nodejs/node14/node_modules (NODE_PATH)<br>nodejs/node16/node_modules (NODE_PATH)<br>nodejs/node18/node_modules (NODE_PATH)|
|Python|python<br>python/lib/python3.9/site-packages(site directories)|
|Java|java/lib (CLASSPATH)|
|Ruby|ruby/gems/2.7.0 (GEM_PATH) <br>ruby/lib (RUBYLIB)|
|All runtimes|bin (PATH) <br>lib (LD_LIBRARY_PATH)|

### 2.3 Creating layer content with virtual enviroment
Create a folder for your project on your local computer
```
mkdir -p lambda_layer/python/lib/python3.8/site-packages
```

Once the folders are created, create a virtual environment and install the packages you need:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --target lambda_layer/python/lib/python3.8/site-packages
```

Next, change directories into the `lambda_layer` directory and create a zip file containing the contents of that folder:
```
cd lambda_layer
zip -r9 lambda_layer.zip .
```

## 3. Creating a layer
You can create new layers using the Lambda console or the Lambda API.

Layers can have one or more version. When you create a layer, Lambda sets the layer version to version 1. You can configure permissions on an existing layer version, but to update the code or make other configuration changes, you must create a new version of the layer.

**To create a layer (console)**
1. Open the Layers page of the Lambda console.
2. Choose **Create layer**.
3. Under **Layer configuration**, for **Name**, enter a name for your layer.
4. (Optional) For **Description**, enter a description for your layer.
5. To upload your layer code, do one of the following:
    - To upload a .zip file from your computer, choose **Upload a .zip file**. Then, choose **Upload** to select your local .zip file.
    - To upload a file from Amazon S3, choose **Upload a file from Amazon S3**. Then, for **Amazon S3 link URL**, enter a link to the file.
6. (Optional) For **Compatible instruction set architectures**, choose one value or both values.
7. (Optional) For **Compatible runtimes**, choose up to 15 runtimes.
8. (Optional) For **License**, enter any necessary license information.
9. Choose **Create**.

**To create a layer (API)**

To create a layer, use the publish-layer-version command with a name, description, .zip file archive, a list of runtimes and a list of architectures that are compatible with the layer. The runtimes and architecture parameters are optional.

```
aws lambda publish-layer-version --layer-name opencv_layer \
    --description "Opencv 4.7 python" \
    --license-info "MIT" \
    --zip-file fileb://lambda_layer.zip \
    --compatible-runtimes python3.8 \
    --compatible-architectures "x86_64"
```

## 4. Testing the Layer
To test the Lambda Layer, I simply created a new Lambda function and added my layer to it, you can do this by simply clicking on Layers, then click on the custom layer option and select the layer you just deployed to Lambda, at the end, you should see an image below:

![](../imgs/lambda_add_layer.jpg)

Then on the function, I imported numpy
```
import json
import numpy as np

def lambda_handler(event, context):
    # TODO 
    print("Numpy create random number: ", np.random.randint(100))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

Then I tested the function and got the following response
```
Test Event Name
test_opencv

Response
{
  "statusCode": 200,
  "body": "\"Hello from Lambda!\""
}

Function Logs
START RequestId: f02b0b52-9594-40bc-9559-37ddc1cd7e7c Version: $LATEST
Numpy create random number:  82
END RequestId: f02b0b52-9594-40bc-9559-37ddc1cd7e7c
REPORT RequestId: f02b0b52-9594-40bc-9559-37ddc1cd7e7c	Duration: 2.58 ms	Billed Duration: 3 ms	Memory Size: 128 MB	Max Memory Used: 67 MB

Request ID
f02b0b52-9594-40bc-9559-37ddc1cd7e7c
```

Try `import cv2`, we got error `libGL.so.1: cannot open shared object file`
```
Response
{
  "errorMessage": "Unable to import module 'lambda_function': libGL.so.1: cannot open shared object file: No such file or directory",
  "errorType": "Runtime.ImportModuleError",
  "stackTrace": []
}
```

We need install `libgl1-mesa-glx`. Maybe using docker image can help.

## 4. Deleting a layer version
To delete a layer version, use the delete-layer-version command.
```
aws lambda delete-layer-version --layer-name opencv_layer --version-number 1
```
When you delete a layer version, you can no longer configure a Lambda function to use it. However, any function that already uses the version continues to have access to it. Version numbers are never reused for a layer name.

## 5. Configuring layer permissions
By default, a layer that you create is private to your AWS account. However, you can optionally share the layer with other accounts or make it public.

To grant layer-usage permission to another account, add a statement to the layer version's permissions policy using the `add-layer-version-permission` command. In each statement, you can grant permission to a single account, all accounts, or an organization.

```
aws lambda add-layer-version-permission \
--layer-name opencv_layer \
--statement-id xaccount \
--action lambda:GetLayerVersion  \
--principal 111122223333\
--version-number 1 \
--output text
```