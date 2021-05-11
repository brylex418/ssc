# ssc
simple server configurator(ssc) that installs / removes deb packages and configures a webserver.


# Directory Manifest:


### configurations:
This is where a user woud palce config files are defined such as index.php / nginx default site 

### hostconfigs:
This is where a user would define their desired configuration in yml. lemp.yml is the file that defines the deployment of a PHP webserver 

### inventory:
This is where a user would define the inventory of servers to apply this configuration on. There should be one yaml file per server

### src:
This is where the python that does all of the work lives


# Setup:

1. Begin with running bootstrap.sh on your ubuntu system. This script will install the necessary bits and set some aliases to use ssc. 
2. Setup your inventory. Place your SSH credentials inside of a yaml file. Using inventory/host01.yml as an example 

# Running:

Use the below command as a template for how to run ssc. 

```ssc hostconfigs/lemp.yml inventory/host01.yml```

NOTE: Be sure to run ssc with the arguments in the order above.
