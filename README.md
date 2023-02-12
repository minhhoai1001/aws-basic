# Learn Amazon Web Services in a Month of Luches

![](imgs/aws.jpg)

How AWS data and security services are used to help an EC2 compute instance deliver its network-facing
application:
1. VPCs encompass all the AWS resources in an application deployment.
2. There are two kinds of subnets: private and public. They can be located in separate availability
zones and are used to manage and, where needed, isolate resources.
3. Security groups’ rules control the movement of data between resources.
4. The EC2 Amazon Machine Image (AMI) acts as a template for replicating precise operating system environments.
5. The Simple Storage Service (S3) bucket can store and deliver data for both backup and delivery
to users.
. Elastic Block Store (EBS) volumes act as data volumes (like hard drives) for an instance.
7. The auto scaler permits automatic provisioning of greater (or fewer) instances to meet changing
demands on an application.
8. The load balancer routes traffic among multiple servers to ensure the smoothest and most efficient user experience.

## Content
As you can see from the table of contents, I’ve divided the book’s chapters into three sections: the core toolset (chapters 2–12), high availability (chapters 13–17), and brief introductions to some of the AWS
services and functionality that didn’t fit into the book’s other sections
(chapters 18–20):
- Chapter 1 introduces the cloud, the space within it that AWS
inhabits, and, in broad terms, the kinds of things you can accomplish there.
- Chapter 2 is a quick-start project in which you’ll launch an actual
virtual machine on AWS EC2, serving a simple web server to the
internet.
- Chapter 3 demonstrates capacity-analysis techniques and adds
WordPress to your EC2 server.
- Chapter 4 introduces managed-database hosting on Amazon’s
Relational Database Service (RDS).
- Chapter 5 shows you how to register and administer DNS domains
and routing policies using Route 53.
- Chapter 6 addresses cheap, reliable, fast data storage using Simple
Storage Service (S3).
- Chapter 7 demonstrates a couple of approaches to using S3 for
system and archive backups.
- Chapter 8 turns your attention to security through the IAM service.
- Chapter 9 shows how you can (and must) work with AWS tools to
estimate and model the true costs of your projects.
- Chapter 10 demonstrates the far-reaching value of applying
resource tags.
- Chapter 11 promotes regular, smart monitoring of your resources
through CloudWatch.
- Chapter 12 introduces you to administering AWS resources
through the AWS command-line interface (CLI).
- Chapter 13 discusses elasticity and scalability as they relate to virtual servers.
- Chapter 14 addresses organizing your infrastructure within VPCs
and availability zones to enhance their reliability.
- Chapter 15 covers load balancing as a tool for intelligently directing client traffic among multiple servers.
- Chapter 16 shows how auto scaling can be used to automatically
manage changes in user demand and server health.
- Chapter 17 describes how the CloudFront content-delivery network can be used to reduce latency for geographically dispersed
users.
- Chapter 18 illustrates the use of various tools to permit hybrid
local/cloud solutions.
- Chapter 19 discusses some AWS cloud-automation tools (specifically, Elastic Beanstalk, ECS, and Lambda).
- Chapter 20 briefly surveys some of the AWS tools I couldn’t properly cover in the book.
- Chapter 21 says, “Goodbye—it’s been great spending time with
you!”

## About the author
David Clinton is a system administrator, teacher, and writer. He has
administered, written about, and created training materials for many
important technology subjects including Linux systems, cloud computing (AWS in particular), and container technologies like Docker. Many
of his video training courses can be found on Pluralsight.com, and links
to his other books (on Linux administration and server virtualization)
can be found at https://bootstrap-it.com.