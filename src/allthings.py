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
    phpIndexPath = str(dsl['ConfigurationFiles']['php'])
    phpFileOwner = dsl['PHPConfiguration']['owner']
    phpFileGroup = dsl['PHPConfiguration']['group']
    phpFileMode = dsl['PHPConfiguration']['mode']
    phpTargetPath = '/var/www/html/index.php'
    phpFileConfig = "sudo chmod %s %s; sudo chown %s:%s %s" %(phpFileMode, phpTargetPath, phpFileOwner, phpFileGroup, phpTargetPath)
    InstallPackagesCommand = "sudo apt update -y; sudo apt install -y %s" %(packagesToInstall)
    print("Packages Being Installed If not already %s" %(packagesToInstall))
    print('Making Remote Connection to Install packages')
    stdin, stdout,stderr = ssh_client.exec_command(InstallPackagesCommand)
    stdout = stdout.readlines()
    print(stdout)
    print('Package Install Has Finished')

    sftp = ssh_client.open_sftp()
    defaultSiteConfig = str(dsl['ConfigurationFiles']['defaultSite'])
 
    if 'nginx' in packagesToInstall:
        print('Nginx is installed so checking config')
        sftp.put(phpIndexPath, '/var/www/html/index.php')
        sftp.put(defaultSiteConfig, '/etc/nginx/sites-available/default')

    else:
        print('No Nginx. Move Along. Be About Your Buisness')

    if str(dsl['Install']['RestartWebServices']) == "true":
        print('You selected restart web services. Doing that')
        stdin, stdout,stderr = ssh_client.exec_command("sudo systemctl restart nginx")
        stdout = stdout.readlines()
        print(stdout)
        print('nginx restarted')
    else:
        print("You didn't delcare to restart services")


    stdin, stdout,stderr = ssh_client.exec_command(phpFileConfig)
    stdout = stdout.readlines()
    print(stdout)
    print('File Mode Set On index.php')

def updatePackage():
    tmp = dsl['Install']['PackageInstallation']
    packagesToUpgrade = " ".join(tmp)
    
    UpgradePackagesCommand = "sudo apt upgrade -y; sudo apt upgrade -y %s" %(packagesToUpgrade)
    print('Making Remote Connection to Upgrade Packages')
    stdin, stdout,stderr = ssh_client.exec_command(UpgradePackagesCommand)
    stdout = stdout.readlines()
    print(stdout)
    print('Package Upgrade Has Finished')


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


#TODO 

#Setup SystemCTL Path Watcher HERE:




# Function Calls


installPackage()
removePackage()
updatePackage()
