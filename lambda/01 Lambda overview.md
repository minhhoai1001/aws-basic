# AWS Lambda
##  1. What is AWS Lambda?
AWS Lambda is a service which performs serverless computing, which involves computing without any server. The code is executed based on the response of events in AWS services such as adding/removing files in S3 bucket, updating Amazon dynamo dB tables, HTTP request from Amazon API gateway etc.

## 2. How AWS Lambda Works?
The block diagram that explains the working of AWS Lambda in five easy steps is shown below.
![](./imgs/aws_lambda_block_diagram.jpg)

**Step 1** − Upload AWS lambda code in any of languages AWS lambda supports, that is NodeJS, Java, Python, C# and Go.

**Step 2** − These are few AWS services on which AWS lambda can be triggered.

**Step 3** − AWS Lambda which has the upload code and the event details on which the trigger has occurred. For example, event from Amazon S3, Amazon API Gateway, Dynamo dB, Amazon SNS, Amazon Kinesis, CloudFront, Amazon SES, CloudTrail, mobile app etc.

**Step 4** − Executes AWS Lambda Code only when triggered by AWS services under the scenarios such as:

- User uploads files in S3 bucket
- http get/post endpoint URL is hit
- data is added/updated/deleted in dynamo dB tables
- push notification
- data streams collection
- hosting of website
- email sending
- mobile app, etc.

**Step 5** − Remember that AWS charges only when the AWS lambda code executes, and not otherwise.

### 2.1 Advantages of using AWS Lambda
AWS Lambda offers multiple benefits when you are working on it. This section discusses them in detail

**Ease of working with code**

AWS Lambda gives you the infrastructure to upload your code. It takes care of maintaining the code and triggers the code whenever the required event happens. It allows you to choose the memory and the timeout required for the code.

AWS Lambda can also execute parallel requests as per the event triggers.

**Log Provision**

AWS Lambda gives the details of number of times a code was executed and time taken for execution, the memory consumed etc. AWS CloudWatch collects all the logs, which helps in understanding the execution flow and in the debugging of the code.

**Billing based on Usage**

AWS Lambda billing is done on memory usage, request made and the execution, which is billed in increments of minimum 100ms. So for a 500ms execution, the billing will be after every 100ms. If you specify your AWS lambda code to be executed in 500ms and the time taken to execute is just 200ms, AWS will bill you only for the time taken, that is 200ms of execution instead of 500ms. AWS always charges for the execution time used. You need not pay if the function is not executed.

**Multi Language Support**

AWS Lambda supports popular languages such as Node. js, Python, Java, C# and Go. These are widely used languages and any developer will find it easy to write code for AWS Lambda.

**Ease of code authoring and deploying**

There are many options available for Lambda for authoring and deploying code. For writing your code, you can use AWS online editor, Visual Studio IDE, or Eclipse IDE. It also has support for serverless framework which makes writing and deploying of AWS Lambda code easy. Besides AWS console, we have AWS-cli to create and deploy code.

**Other features**

You can use AWS Lambda for free by getting a login to AWS free tier. It gives you service for free for 1 year. Take a look at the free services offered by AWS free tier.

### 2.2 Disadvantages of using AWS Lambda
In spite of many advantages, AWS Lambda possesses the following disadvantages:

- It is not suitable for small projects.

- You need to carefully analyze your code and decide the memory and timeout. Incase if your function needs more time than what is allocated, it will get terminated as per the timeout specified on it and the code will not be fully executed.

- Since AWS Lambda relies completely on AWS for the infrastructure, you cannot install anything additional software if your code demands it.

### 2.3 Events that Trigger AWS Lambda
The events can trigger AWS Lambda are as follows −

- Entry into a S3 object
- Insertion, updation and deletion of data in Dynamo DB table
- Push notifications from SNS
- GET/POST calls to API Gateway
- Headers modification at viewer or origin request/response in CloudFront
- Log entries in AWS Kinesis data stream
- Log history in CloudTrail