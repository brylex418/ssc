import os
import yaml
import paramiko
import sys


# DSL YAML

with open(sys.argv[1]) as file:
        dsl = yaml.safe_load(file)

# Host YAML BELOW

with open(sys.argv[2]) as file:
        hosts = yaml.safe_load(file)

#HOST Variables

host = hosts['host']
username = hosts['username']
password = hosts['password']


# SSH Client Variables

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host,username=username,password=password)


# function to iterate through packages to perform apt installs

def installPackage():
    
    tmp  = dsl['Install']['PackageInstallation']
    packagesToInstall = " ".join(tmp)

    InstallPackagesCommand = "sudo apt install -y %s" %(packagesToInstall)
    apacheConfiguration = "cd /etc/apache2/sites-available; sed 's|/var/www/html/index.html|/var/www/html/index.php|' 000-default.conf; sudo systemctl restart apache2"
    print('Making Remote Connection to Install packages')
    stdin, stdout,stderr = ssh_client.exec_command(InstallPackagesCommand)
    stdout = stdout.readlines()
    print(stdout)
    print('Package Install Has Finished')

    sftp = ssh_client.open_sftp()
    phpConfigPath = str(dsl['ConfigurationFiles']['php'])

#TODO 

Need to further automate the creation of Apache and serving PHP FILES
https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-16-04



    if 'libapache2-mod-php' in packagesToInstall:
        print('Apache is installed so configuring it')
        print('Copying Up To Date PHP Configuration')
        sftp.put(phpConfigPath, '/var/www/html/index.php')

    stdin, stdout,stderr = ssh_client.exec_command(apacheConfiguration)
    stdout = stdout.readlines()
    print(stdout)



# function to iterate through packages to perform apt removes

def removePackage():
    tmp = dsl['Remove']['PackageRemoval']
    packagesToRemove = " ".join(tmp)

    RemovePackagesCommand = "sudo apt remove -y %s" %(packagesToRemove)

    print('Making Remote Connection To Remove packages')
    stdin, stdout,stderr = ssh_client.exec_command(RemovePackagesCommand)
    stdout = stdout.readlines()
    print(stdout)
    print('Package Removal Has Finished')

#def scpFiles():
#
#    sftp = ssh_client.open_sftp()
#    phpConfigPath = dsl['ConfigurationFiles']['php'] 
#    sftp.put(phpConfigPath, '/var/www/html/index.php')
#    sftp.close()

#TODO 

Setup SystemCTL Path Watcher HERE:




# Function Calls


installPackage()
removePackage()

# function to iterate through packages to perform apt removes

#def removePackage(packages):
#    for package in packagesToRemove:
#        os.system("sudo apt remove -y " + str(packagesToRemove))

# Loads the yml file

#with open('/home/ubuntu/cm/templates/onefile.yml') as file:
#    result =yaml.safe_load(file)

#Formats the List of packages and sets vars

#space = " "

#InstallPacks = result['Install']['PackageInstallation']
#packagesToInstall = space.join(InstallPacks)

#RemovePacks = result['Remove']['PackageRemoval']
#packagesToRemove = space.join(RemovePacks)


#Runs any Installs and removes

#print('Beginning The Server Configurator!!')
#print('Get READY TO BE CONFIGURED!')

#InstallPackagesCommand = "sudo apt install -y %s;ls -lah" %(packagesToInstall)

#RemovePackagesCommand = "sudo apt remove -y %s;ls -lah" %(packagesToRemove)

#stdin, stdout,stderr = ssh_client.exec_command(InstallPackagesCommand)
#stdout = stdout.readlines()
#stdeout = "".join(stdout)
#print(stdout)
#print('Package Installation Phase has finished')

#removePackage(packagesToRemove)

