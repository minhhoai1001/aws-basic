# The 10-minute EC2 web server
Here’s what you’ll accomplish through the rest of this chapter:
- Launch an EC2 Ubuntu Linux server instance
- Use SSH to connect with your instance
- Use the Ubuntu package manager to install the software packages
it will need to run as a web server
- Create a simple Welcome page for your site

## 2.1 What is EC2, and what does it do?
Elastic Compute Cloud (EC2) is a hugely successful service at the core
of the AWS platform that allows you to effectively rent units of compute
power (EC2 instances), storage space (Elastic Block Store [EBS] volumes, which work like a PC’s hard drive), and network connectivity running in AWS’s vast infrastructure.

## 2.2 Launching an AWS instance
Let’s begin the process of starting up a new virtual Linux server. Why
Linux? Because it can be easily adapted to fill just about any role, and,
in most cases, the OS is available for free.


`Amazon Machine Images`
*An Amazon Machine Image (AMI) is effectively a template that defines the
OS, application, and storage environment for an EC2 instance. AWS provides a couple of dozen official and supported Quick Start AMIs you can use
(including the Ubuntu 16.04 AMI you just selected).
But there are also many hundreds of specialty AMIs available in the AWS
Marketplace. Beyond that, you can easily build your own AMI out of any
instance that you’ve customized to fit your specific needs. I’ll talk a bit about how that works in chapter 12.*

- Step 1: Name and tags
- Step 2: Application and OS Images (Amazon Machine Image): Ubuntu Sercver 20.04 LTS (Free tier aligible).
- Step 3: Instance type: t2.micro (Free tier aligible)
- Step 4: Key pair (login): create new kay pair
- Step 5: Network settings: Create security group. 
    + Allow SSH traffic from Anywhere (0.0.0.0/0). 
    + Allow HTTP traffic from Anywhere (0.0.0.0/0).
- Step 6: Configure storage: 8Gib gp2.
- Step 7: launch instance

## 2.3 Accessing your AWS instance
- Find Public IPv4 address of instance
- SSH to instance
`ssh -i key-gen.pem ubuntu@public_ip`

## 2.4 Building an Ubuntu Linux web server
### 2.4.1 Installing the software
Now you’ll install the three software packages that will power your website. These packages in particular are used
together with Linux so often that the combination has been given its
own acronym—LAMP (Linux, Apache, MySQL, and PHP):
- Apache web server management tool, to point inbound internet
visitors to your website resources
- MySQL database, so any software you’ll use later—including
WordPress—will have a platform on which to build the databases
it needs
- PHP scripting language, also necessary for many applications,
including WordPress
    ```
    sudo apt update
    sudo apt install lamp-server^ -y
    ```
`What? No password?`

*Doesn’t sudo always require you to enter your password? Another question:
just what is your password on this AWS instance?
The short answer: for security reasons, you don’t have a password. The
(slightly) longer answer: if you managed to log in using your unique and
highly secure key pair, you’re assumed to be who you claim.*

### 2.4.2 Creating the website
You’re now ready to write a simple HTML page of your own, using your
favorite text editor. Mine is nano, so the command is as follows:
```
cd /var/www/html
sudo nano index.html
```

Type whatever you want into the editor. Just so you can see how it works,
try adding a little HTML formatting, perhaps something like this:
```
<h1>Welcome!</h1>
We hope you <i>really</i> enjoy your stay here.
```
Open web bowser and anter public ip to see the web site.

**NOTE**
In addition to Terminate, you can also select Stop from the
Instance State menu. As the name suggests, Stop shuts down the EC2
instance but doesn’t destroy it or delete the contents of the EBS volume. You won’t be charged for the instance while it’s stopped, and it
can be restarted again whenever you like, so this can be a nice compromise between choosing Terminate and leaving the instance running.
But when it’s restarted, the instance will be using a different IP
address, which can have an effect on how users or other AWS services
communicate with it.