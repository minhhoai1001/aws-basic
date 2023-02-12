# Provisioning a more robust EC2 website
## 3.1 Calculating capacity needs
To make sure your server won’t have to strain its
poor, delicate self, you need to give it enough of these things:
- Processing power-CPU capacity
- Storage space-Hard drive capacity
- System memory-RAM
- Network bandwidth-Maximum amount of data that can be transferred into and out of your infrastructure at a given time

## 3.2 Getting the measure of EC2’s core compute services
### 3.2.1 vCPU
In the Amazon universe, processing power is measured in virtual central processing units (vCPUs). AWS tells you that a single AWS vCPU is
roughly the equivalent of a “1.0-1.2 GHz 2007 Opteron or 2007 Xeon
processor.”

### 3.2.2 EBS
The AWS storage that’s most comparable to the physical hard drive
inside your PC is the EBS volume. Elastic Block Store (EBS) is a vast collection of hundreds of thousands of storage drives kept running in
AWS’s data centers. An EBS volume is a logically defined amount of storage space carved out of that vast storage system that’s been set aside for
an EC2 customer—which would be you.

### 3.2.3 Memory
Memory is memory, no matter where it lives. Because RAM memory is
much more instantly accessible than any other widely available option,
it’s usually used to temporarily store as much system-process and application data as possible. If, for example, serving a single web page to a
single customer requires one tenth of a megabyte (100 KB) of RAM,
you’ll want to make sure you have at least 100 KB times n of the stuff
available, where n is the maximum number of pages you might need to
serve at a single time.

### 3.2.4 Bandwidth
The quality of an EC2 instance’s connectivity to its network is described
as its network performance. For most instance types, the value is Low, Moderate, or High.

The real-world performance you’ll experience will depend on a wide
variety of factors, but it’s been estimated that you’ll get anywhere from 2
to 100 Mbps for Low, 10 to 250 Mbps for Moderate, and 95 to 1000
Mbps for High. Compare those numbers with the amount of data you
expect you’ll need to transfer in and out of your server to keep your
customers happy, to determine what level of network performance to
select.

## 3.3 Choosing the right instance for your project
**EC2 instance type families**
| Type family      | Member types |Focus |
| ----------- | ----------- | ----------- |
| T      | T2       |Baseline general purpose (burstable performance)       |
| M   | M3, M4        |General purpose: balance between compute, memory, and network       |
| C   | C3, C4        | Computer optimized: high-performance processors       |
| X   | X1        |Memory optimized for enterprise-class, in-memory applications       |
| R   | R3, R4        |Memory optimized for memory-intensive applications       |
| P   | P2        |Graphics accelerated for GPU-intensive applications       |
| G   | G2        | Graphics-heavy processing       |
| F   | F1        | Hardware acceleration with field-programmable arrays (FPGAs)       |
| I   | I2, I3        |Storage optimized: very fast storage volumes for efficient I/O operations       |
| D   | D2        | Storage optimized: high disk throughput for very large data stores       |

## 3.4 Adding WordPress
### 3.4.1 Preparing the server
Just so you know
what’s coming, here’s what you’ll do:
1. Install the LAMP server the same way you did in the last chapter
(before you terminated that instance).
2. Create a new database in MySQL for WordPress to use.
3. Download and configure the latest version of WordPress.
4. Copy the WordPress files to your Apache document root directory.
5. Log in to your new WordPress site.

```
$ ssh -i keyname.pem ubuntu@<your-instance-IP-address>
$ sudo apt update
$ sudo apt install lamp-server^ -y
```

### 3.4.2 Preparing MySQL
Use the root user (and the root password that you created and didn’t
forget during the MySQL installation) to log in to the MySQL shell. -u
tells MySQL that you’ll assume the root user, and -p says that you want
to be prompted for your password:
```
mysql -u root -p
mysql> CREATE DATABASE wordpressdb;
mysql> CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'mypassword';
mysql> GRANT ALL PRIVILEGES ON wordpressdb.* To 'wpuser'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> exit
```

### 3.4.3 Downloading and configuring WordPress
 Back in the SSH terminal session, use the wget program to download
WordPress, using the address you copied from the WordPress website:
```
$ wget https://wordpress.org/latest.tar.gz
$ tar xzf latest.tar.gz
```
See the file called wp-config-sample.php? That’s a template you can use
to manage your WordPress configuration. You’ll use cp to create a copy
of that file named wp-config.php (so WordPress will know that this is
the configuration file you want it to use) and then edit its contents:
```
$ cd wordpress
$ cp wp-config-sample.php wp-config.php
$ nano wp-config.php
```

Replace database_name_here with the name you’d
like to give your database, username_here with the wpuser you created
for MySQL, and password_here with that user’s new password, so that
WordPress can successfully log in and manage its database. For the values I used, those lines now look like this:
```
/** The name of the database for WordPress */
define('DB_NAME', 'wordpressdb');
/** MySQL database username */
define('DB_USER', 'wpuser');
/** MySQL database password */
define('DB_PASSWORD', 'mypassword');
```

### 3.4.4 Setting up the WordPress filesystem
If you want to use WordPress to manage all the content on your
domain—perhaps you like the fact that the WordPress ecosystem
includes so many resources for closely integrating content and transaction processing—you should copy all the files in the wordpress directory to Apache’s document root directory. On Ubuntu machines, you’ll
recall, this is /var/www/html/.
```
$ sudo cp -r * /var/www/html
```

### 3.4.5 Testing your application
When that’s done, it’s time to head back to your browser and point it to
your instance’s public IP address (the one you used to SSH in). Just this
once, add the route to the install.php file, where you can create a WordPress admin account. The address will look something like this:
`54.218.241.9/wp-admin/install.php`