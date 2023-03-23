# Lambda Layers
## 1. What are Lambda Layers?
Lambda layers provide a convenient way to package libraries and other dependencies that you can use with your Lambda functions. Using layers reduces the size of uploaded deployment archives and makes it faster to deploy your code.

You can use layers only with Lambda functions deployed as a .zip file archive. For functions defined as a container image, you package your preferred runtime and all code dependencies when you create the container.

You can create layers using the Lambda console, the Lambda API, AWS CloudFormation, or the AWS Serverless Application Model (AWS SAM).

## 2. Create Lambda layer
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