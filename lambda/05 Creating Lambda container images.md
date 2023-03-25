# Creating Lambda container images

AWS provides a set of open-source [base images](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-images.html#runtimes-images-lp) that you can use to create your container image. These base images include a runtime interface client to manage the interaction between Lambda and your function code.

## 1. Lambda container images
### 1.1 Image types

You can use an AWS provided base image or an alternative base image, such as **Alpine** or **Debian**. Lambda supports any image that conforms to one of the following image manifest formats:

- Docker image manifest V2, schema 2 (used with Docker version 1.10 and newer)
- Open Container Initiative (OCI) Specifications (v1.0.0 and up)

Lambda supports a maximum uncompressed image size of 10 GB, including all layers.

### 1.2 Container tools

To create your container image, you can use any development tool that supports one of the following container image manifest formats:

- Docker image manifest V2, schema 2 (used with Docker version 1.10 and newer)
- OCI Specifications (v1.0.0 and up)

For example, you can use the Docker CLI to build, test, and deploy your container images.

### 1.3 Container image settings

Lambda supports the following container image settings in the Dockerfile:

- `ENTRYPOINT` – Specifies the absolute path to the entry point of the application.
- `CMD` – Specifies parameters that you want to pass in with `ENTRYPOINT`.
- `WORKDIR` – Specifies the absolute path to the working directory.
- `ENV` – Specifies an environment variable for the Lambda function.

You can specify the container image settings in the Dockerfile when you build your image. You can also override these configurations using the Lambda console or Lambda API. This allows you to deploy multiple functions that deploy the same container image but with different runtime configurations.

## 2. Creating images
### 2.1 Creating images from AWS base images
To build a container image for a new Lambda function, you can start with an AWS base image for Lambda. Lambda provides two types of base images:

- Multi-architecture base image. Specify one of the main image tags (such as `python:3.8`) to choose this type of image.
- Architecture-specific base image.
    Specify an image tag with an architecture suffix. For example, specify `3.9-arm64` to choose the arm64 base image for Python 3.8.

**To create an image from an AWS base image for Lambda**

1. On your local machine, create a project directory for your new function.
2. Create a directory named app in the project directory, and then add your function handler code to the app directory.
3. Use a text editor to create a new Dockerfile.
   The AWS base images provide the following environment variables:

    - LAMBDA_TASK_ROOT=/var/task
    - LAMBDA_RUNTIME_DIR=/var/runtime

    Install any dependencies under the `${LAMBDA_TASK_ROOT}` directory alongside the function handler to ensure that the Lambda runtime can locate them when the function is invoked.

    ```
    FROM public.ecr.aws/lambda/python:3.8

    COPY app.py ${LAMBDA_TASK_ROOT}
    COPY requirements.txt .

    RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

    # Set the CMD to your handler
    CMD [ "app.handler" ]
    ```
4. Build your Docker image with the `docker build` command. Enter a name for the image. The following example names the image `opencv-image`.
    ```
    docker build -t opencv-image .
    ```

5. Start the Docker image with the `docker run` command. For this example, enter `hello-world` as the image name.
    ```
    docker run -p 9000:8080 opencv-image 
    ```
6. (Optional) Test your application locally using the runtime interface emulator. From a new terminal window, post an event to the following endpoint using a curl command:
    ```
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
    ```

### 2.2 Creating images from alternative base images

1. Choose a base image. Lambda supports all Linux distributions, such as Alpine, Debian, and Ubuntu.
2. On your local machine, create a project directory for your new function.
3. Create a directory named **app** in the project directory, and then add your function handler code to the app directory.

4. Use a text editor to create a new Dockerfile with the following configuration:
    - Set the `FROM` property to the URI of the base image.
    - Add instructions to install the runtime interface client.
    - Set the `ENTRYPOINT` property to invoke the runtime interface client.
    - Set the `CMD` argument to specify the Lambda function handler.

    The following example shows a Dockerfile for Python:
    ```
    # Define function directory
    ARG FUNCTION_DIR="/function"

    FROM python:buster as build-image

    # Install aws-lambda-cpp build dependencies
    RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

    # Include global arg in this stage of the build
    ARG FUNCTION_DIR
    # Create function directory
    RUN mkdir -p ${FUNCTION_DIR}

    # Copy function code
    COPY app/* ${FUNCTION_DIR}

    # Install the runtime interface client
    RUN pip install \
            --target ${FUNCTION_DIR} \
            awslambdaric

    # Multi-stage build: grab a fresh copy of the base image
    FROM python:buster

    # Include global arg in this stage of the build
    ARG FUNCTION_DIR
    # Set working directory to function root directory
    WORKDIR ${FUNCTION_DIR}

    # Copy in the build image dependencies
    COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

    ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
    CMD [ "app.handler" ]
    ```

5. Build your Docker image with the docker build command. Enter a name for the image. The following example names the image opencv-image.
    ```
    docker build -t opencv-image .    
    ```
6. (Optional) Test your application locally using the Runtime interface emulator.
    ```
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
    ```
## 3. Upload the image to the Amazon ECR repository
In the following commands, replace `123456789012` with your AWS account ID and set the region value to the region where you want to create the Amazon ECR repository.
1. Authenticate the Docker CLI to your Amazon ECR registry.
    ```
    aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-southeast-1.amazonaws.com    
    ```
2. Create a repository in Amazon ECR using the `create-repository` command.
    ```
    aws ecr create-repository --repository-name opencv-image --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
    ```
3. Tag your image to match your repository name, and deploy the image to Amazon ECR using the docker push command. 
    ```
    docker tag  opencv-image:latest 123456789012.dkr.ecr.ap-southeast-1.amazonaws.com/opencv-image:latest
    docker push 123456789012.dkr.ecr.ap-southeast-1.amazonaws.com/opencv-image:latest       
    ```