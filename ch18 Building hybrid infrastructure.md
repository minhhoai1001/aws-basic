# Building hybrid infrastructure
## 18.1 Why go hybrid?
Cloud computing is definitely not a zero-sum game. There’s nothing
wrong with deploying your resources both locally and on AWS. In fact,
there’s no law preventing you from using multiple cloud providers at
the same time. The trick is properly coordinating the administration of
remote infrastructure. You’ll learn about some pretty powerful coordination tools as you move through this chapter. But first, just why would you want to split things up? Here are some possibilities:
- *Staged migrations*—Even if you understand the value proposition of
AWS, it will often be impractical to shift all the pieces of a complicated operation into the cloud at once. It sometimes makes sense to move things over in stages. You might begin by transferring a few databases to RDS or moving backup archives to S3. 
- *Using existing infrastructure and skills*—If you’ve recently invested in
a rack of high-performance servers, now is probably not the best
time to send them off to a landfill. Ditto the six months of training
your junior sysadmins just completed. But that doesn’t mean you
can’t plan (and upgrade your skills) for the future while moving
what can be easily moved.
- *Regulatory and compliance restrictions*—Although this happens less
and less, some deployments may, due to security concerns, require
specialized local care and handling.
- *Costs of data transfer*—For some businesses, migrating server workloads to the cloud is a no-brainer, but finding a way to upload a few dozen terabytes of back-end data can be complicated. Even if
you’re lucky enough to have a gigabyte internet connection, that
doesn’t mean you’ll get anything like those speeds for real-world
uploads. Do the math: a 10 TB archive sent at a rate of 500 Mbps
will take close to 48 hours—and probably severely limit everyone
else’s internet use for the duration. That’s assuming you’re getting
500 Mbps. The more common rate of 25 Mbps would take well
over a month. I’ll talk about some interesting alternatives in the
next section.

## 18.2 Hybrid storage solutions
### 18.2.1 S3 and Glacier
If all you’re looking for is a place to store moderate amounts of easily
accessible data, then S3 is probably where you want to put it. Do your
saved archives lose their relevance over time? Once your files are safely
parked in S3, it’s trivial to arrange for them to be automatically transitioned between S3 and the much cheaper **Glacier** storage service.

### 18.2.2 AWS Storage Gateway
If backups are critical to your operations but making the connection with off-site storage is a problem, why not pretend that everything’s in the same room? **AWS Storage Gateway**, which makes a living
by imitating on-premises storage devices, can simplify the process.
Once you’ve installed the Storage Gateway as a virtual machine on a
local server, it can be mounted as a compatible storage device—including as an iSCSI device (iSCSI is a common standard for managing data
transfers). That means it can present itself to your local infrastructure
exactly the way your legacy hardware did, while, in reality, its data is
stored in the AWS cloud.
![](imgs/Storage-Gateway.png)

### 18.2.3 AWS Snowball
Don’t have three years to wait, but still want to move large volumes of
data to AWS? Consider having Amazon send you a petabyte-sized physical storage device: you can load your data onto it and then ship it back.
This service is called Snowball, and the device comes with 256-bit
encryption and multiple layers of security and tracking features to protect it through its journey back to AWS.

Assuming you’re in a location where the **Snowball** service is available
(consult AWS documentation for details), the entire process can take
less than a week, and it will end up a great deal cheaper than the cost of
bandwidth for an upload. Snowball can also be used in the other direction: if your local system fails, and you need to retrieve a huge data
backup from S3, you can order an export.

## 18.3 Hybrid connectivity
### 18.3.1 AWS Direct Connect
**Direct Connect** is built on a pool of third-party providers, each of which can create and maintain a fast, dedicated network connection between your office or data center and your AWS-based resources. Companies called AWS Partner Network (APN) Technology and Consulting Partners are available to help you establish connections to Amazon’s Direct Connect locations.

### 18.3.2 The hardware virtual private gateway
Even if your internet connection is already fast and reliable enough for
the things you’re doing, you may be uncomfortable sending your private data across an unprotected public network like the internet. A
common solution involves creating a tunneled connection using a special virtual private network (VPN) to connect your local servers to the
resources you have running within an **AWS Virtual Private Cloud** (VPC).

### 18.3.3 AWS Directory Service
Securing your hybrid infrastructure involves more than just ensuring that the network connections are strong enough to keep bad guys on the internet from eavesdropping on your data transfers. You’ll probably also want to manage the way your users authenticate themselves to gain legitimate access. After all, there’s no point in securing the network and then turning around and letting everyone in through the front door. But creating a new authentication system in addition to whatever you’re using on the rest of your company’s networks can introduce some serious pain into the process.

The &&AWS Directory Service** allows close integration between any existing local Microsoft Active
Directory (or AD-compatible) system and AWS resources. This can permit system-wide deployment of features like Kerberos-based single signon, RADIUS-based multi-factor authentication, and LDAP.

## 18.4 Disaster recovery
Even if you decide to keep every last byte of your live deployments offcloud and local, there’s still plenty of value to be found in using AWS as part of your disaster-recovery plan. You do have a disaster-recover plan,
right? I mean the kind of plan that includes clear and realistic recoverytime objectives (the maximum amount of time you can tolerate a service outage) and recovery-point objectives (the maximum amount of transaction
data loss you can tolerate). You obviously want to be able to return your
application and its data to a fully functioning state as quickly as possible.

- The *pilot-light model*, where you keep a synchronized, constantly
updated copy of your back-end database running on AWS RDS.
The goal is that, should your local servers fail, the RDS database
can be used to instantly “ignite the furnace” by restoring up-todate application data to freshly launched, prebuilt AWS-based
AMIs. All you’ll need to do is redirect your DNS records away from
your local infrastructure to your AWS VPC so users are sent to the
new servers.
- The *warm-standby model*, where you run a full-tiered copy of your
actual application but, to save costs, in a scaled-down version. If
the local resources fail, pointing your DNS traffic to AWS will automatically cause your auto scaler to quickly increase capacity to
meet demand. This can be more expensive to maintain than a
pilot-light infrastructure, but you get quicker recovery as a return
on your extra investment.

## 18.5 The Amazon EC2 Systems Manager
EC2 Systems Manager is essentially a collection of administration tools that were recently added to the EC2 family. It’s an AWS in-house answer to an entire class of third-party provisioning tools like Puppet and Chef, to Linux-based cron jobs, and to first-party tools like a keyboard and a wall full of monitors.

The EC2 Systems Manager tools provide one-stop, centralized control
over all of your Linux and Windows instances, allowing you to schedule
software and OS updates, run regularly scheduled or one-off scripts
(both Linux and PowerShell), and apply updates to underlying AMIs.

## 18.6 VMware integration
As of this writing, VMware Cloud on AWS (an AWS/VMware partnership) is in a prerelease stage called Technology Preview. The idea is that
you’ll be able to use the tried and tested VMware administration software to manage not only resources in your local environment, the way
you always have, but AWS instances as well. In a way, this is the Amazon
EC2 Systems Manager in reverse. The key advantage is that your team’s
hard-earned VMware skills and existing VMware infrastructure need
not be abandoned as you move to the cloud.