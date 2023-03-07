# Another way to play: the command-line interface
## 12.1 What is the AWS CLI?
The AWS CLI is a set of commands that can run in a command-line
terminal. When the CLI is invoked by the prefix `aws`, the subsequent
characters are subjected to special rules of interpretation.

![](imgs/aws_cli.jpg)

## 12.2 Why use a CLI?
We can comfortable configuring, launching, and
stopping resources from the browser AWS Console.

Of course, there are also sophisticated third-party configuration management packages like Puppet, Vagrant, and Chef that can be integrated directly into your AWS account and provide similar functionality.
But at their core, they’re also scripts, relying on structures and logic
that are similar to what you’ll find in the AWS CLI. Exploring complex
scripting is beyond the scope of this book, but I’ll show you the basics
that should get you most of the way there.

## 12.3 Installing the AWS CLI
I’ll walk you through the largely
straightforward steps to get the package running on Windows, Linux,
and macOS, using both native installation techniques and the pip
software-management system used for Python packages.

### 12.3.1 Installing with a Windows MSI file
You can download the MSI installer file for [64-bit machines](https://s3.amazonaws.com/aws-cli/AWSCLI64.msi) and [32-bit machines](https://s3.amazonaws.com/aws-cli/AWSCLI32.msi)

### 12.3.2 Installing on Linux
Most Linux package managers offer a quick installation option for the
AWS CLI, cleverly called awscli. For Ubuntu or** Debian-based** systems,
use apt:
```
$ sudo apt install awscli
```
The same applies to distributions that use yum, like **CentOS** and **Fedora**:
```
$ sudo yum install awscli
```

### 12.3.3 Installing using Python pip (all OSs)
|OS| Install AWS CLI| Upgrade AWS CLI|
|--|----------------|----------------|
|Windows| pip install awscli| pip install --upgrade awscli|
|Linux| sudo pip install awscli |sudo pip install --upgrade awscli|
|macOS| sudo pip install awscli --ignore-installed six |sudo pip install --upgrade awscli|

You only need to add
the `--ignore-installed six` argument on macOS if you run into trouble installing on El Capitan.

## 12.4 Configuring the AWS CLI
Before you can add your security credentials to the CLI configuration,
you need to head back to the AWS Console to create a set of credentials
to add.  From any page in the Console, click the drop-down menu
header at upper right with your account name on it, and then click the
My Security Credentials link. If you didn’t lock down your root account
and replace it with an IAM user back in chapter 8.

To set things up, open a terminal on your local machine and run aws
configure from the command line. You’ll be asked for your access key
ID, your secret access key, the AWS region you’d like to make the
default, and the format you’d like to use for output.

```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: ap-southeast-1
Default output format [None]:
```

### 12.4.1 Choosing an output format
The output format you choose will largely depend on the kind of data
you’re likely to be generating and viewing and the size of the terminal
window you’ll be using to view it. Your three choices are JSON (enter
**json**), table (**table**), or plain text (**text**). All you need to do to modify
your settings is run aws configure again and enter new values only for
those elements you want to change. This way, you can easily switch back
and forth between formats.

### 12.4.2 Working with multiple AWS profiles
You may find yourself with separate AWS accounts for work and personal use. This can complicate things when you’re trying to access
accounts from the command line. Fortunately, the CLI allows you to
configure multiple accounts and specify the one you’re targeting along
with each subsequent command.
Run aws configure followed by the `--profile` argument and the
name you’d like to use for the new profile. I gave the name testaccount in this example:
```
$ aws configure --profile test-account
```
## 12.5 Using the help 
Type `aws help` to open an overview of the AWS CLI environment that includes commandline options and a helpful list of all the AWS services that the CLI can manage:
```
$ aws help
```
There are currently more than 75 of those services, so I won’t list them
all here. But knowing the name of the service you’re after can get you
more-specific help. For instance, running aws iam help shows a document that explains what IAM is and how it works, and then lists all the available commands that can be used against it:
```
$ aws iam help
```
When you run that yourself, you’ll see that one of those commands is
add-user-to-group. This tells you that, if you want to add an existing
IAM user to an existing IAM group, you type aws iam add-user-togroup. But how do you tell AWS which user and which group you’re
thinking about? If you’re not sure of the exact syntax, add the command name to the string before the help command, like this:
```
$ aws iam add-user-to-group help
```

The help file you’re shown includes this example command line, which
adds the user Bob to the Admins group (assuming you have a user
named Bob and a group named Admins):
```
$ aws iam add-user-to-group --user-name Bob --group-name Admins
```

## 12.6 Using the CLI to administer your AWS account resources
Let’s try performing a few real tasks through the CLI. aws s3 ls lists all
the S3 buckets in your account.
```
$ aws s3 
>> 2023-03-07 20:51:55 wordpress-hoai
```

### 12.6.1 Launching a new EC2 instance using the CLI
Suppose you need to double your EC2 capacity. You’d like to make a
perfect copy of your existing instance so you can launch a second one.
You can replicate a running instance and use it to create an Amazon
Machine Image (AMI) that you can then select for new instances.
![](imgs/aws_AMI.jpg)

The following command includes the AMI ID of my Apache/WordPress
web server image. It will launch a brand-new instance that’s an exact
replica of the original instance I used to create the image:
```
$ aws ec2 run-instances --image-id ami-05c8486d62efc5d07 \
--count 1 --instance-type t2.micro \
--key-name aws-month-lunches --security-group-ids sg-0365d403830f778ab
```

Let’s go through that one step at a time:
- `aws ec2 run-instances` runs a new instance whose details will follow.
- `--image-id ami-05c8486d62efc5d07` identifies the AMI’s ID of Ubuntu 20.04. You can get this
information from the AMI page of the EC2 dashboard, or from the
CLI using `aws ec2 describe-images --owners self`. 
- `--count 1` says to launch only one instance of this image.
- `--instance-type t2.micro` is the instance type.
- `--key-name aws-month-lunches` is the name of the key pair you’ll use to access
the instance once it’s running. This example uses plural—a keyname example from a previous chapter.
- `--security-groups sg-0365d403830f778ab` is the name of the existing security group you’ll use; you can find it using `aws ec2 describe-security-groups`. The ID displayed here is unique to the group in
my account’s VPC. You’ll need to use a group ID from your own account.

Terminate instances
```
$ aws ec2 terminate-instances --instance-ids i-06eebc46d9201804d
```