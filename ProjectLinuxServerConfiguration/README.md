## PROJECT SPECIFICATION

### Linux Server Configuration

##### i. The IP address and SSH port so your server can be accessed by the reviewer.
  `ssh grader@13.236.165.218 -p 2200 -i ~/.ssh/grader_key`
  
##### ii. The complete URL to your hosted web application.
  `http://13.236.165.218.xip.io/`
  
##### iii. A summary of software you installed and configuration changes made.
  Software and packages installed:
```
pip
git
apache2
libapache2-mod-wsgi
postgresql
psycopg2
sqlalchemy
oauth2client
httplib2
json
requests
flask
```
  1. Creation of Amazon Lightsail server
  2. Adjusting server ports for SSH on 2200, NTP on 123 and HTTP on 80
  3. Lock down SSH daemon
  4. Install webserver components and test wsgi on apache2
  5. Create PostresSQL user and database ready for app use
  6. Deploy GIT repostory and adjust code/permissions/config for apache2
  7. Setup grader for udacity
  
  (please see setup details below for more detail)
    
##### iv. A list of any third-party resources you made use of to complete this project.
  Amazon Lightsail  
  bootstrapcdn.com (fontawesome.com)  

*** 

## Detailed setup instructions

### Create web server on Amazon Lightsail

Navigate: https://lightsail.aws.amazon.com/ls/webapp/home/instances  
Select a platform->Linux/Unix  
Select a blueprint->OS Only->Ubuntu 16.04 LTS  
Create instance  
Click the instance when state change to Running  
Select Networking tab and add the following:  
```
    SSH TCP 22
    HTTP	TCP	80
    Custom	UDP	123
    Custom	TCP	2200
```
Return to the Connect tab and the bottom of the page retreive your default private key from the Account page  

### Setup ssh access and security of the instance

`ssh ubuntu@<lightsailIP> -p 22 -i <yourLightsailDefaultKey>.pem`  
`sudo apt update`  
`sudo apt upgrade`  
`sudo vi /etc/ssh/sshd_config`  
Change Port 22 -> Port 2200  
Check that PasswordAuthentication No  
Check that PermitRootLogin no  
`sudo service sshd restart`  
`exit`  
`ssh ubuntu@<lightsailIP> -p 2200 -i <yourLightsailDefaultKey>.pem`  
`sudo ufw default deny incoming`  
`sudo ufw default allow outgoing`  
`sudo ufw allow 2200/tcp`  
`sudo ufw allow www`  
`sudo ufw allow ntp`  
`sudo ufw deny 22`  
`sudo ufw enable`  
`sudo ufw status`  
```
Status: active

To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123                        ALLOW       Anywhere
22                         DENY        Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123 (v6)                   ALLOW       Anywhere (v6)
22 (v6)                    DENY        Anywhere (v6)
```
`exit`  
`ssh ubuntu@<lightsailIP> -p 2200 -i <yourLightsailDefaultKey>.pem`  
`sudo dpkg-reconfigure tzdata`  
Select None of the above -> UTC  
`sudo apt-get install git apache2 postgresql libapache2-mod-wsgi`  

### Apache2 testing:

`sudo vi /etc/apache2/sites-enabled/000-default.conf`  
Add at end of <VirtualHost> block:  
`WSGIScriptAlias / /var/www/html/myapp.wsgi`  
`sudo apache2ctl restart`  
`cd /var/www/html/`  
`nano myapp.wsgi`  
```
def application(environ, start_response):
    status = '200 OK'
    output = 'Hello Udacity!'

    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
```
Navigate to: http://<lightsailIP>/myapp.wsgi  
Verify page is loaded with "Hello Udacity!"  
Return to Amazon Lightsail instance and delete the Networking->Firewall->SSH 22 Rule  

### Setup SQL database:

`sudo su - postgres`  
`psql`  
```
CREATE ROLE catalog WITH LOGIN;
ALTER ROLE catalog CREATEDB;
\password catalog
\du
\q
```
`exit`  
`sudo adduser catalog`  
`sudo usermod -aG sudo grader`  
^ OR \  
`sudo visudo`  
`catalog ALL=(ALL:ALL) ALL`  
`sudo su - catalog`  
`sudo -l`  
`createdb catalog`  
`psql`  
```
\l
\q
```
`vi /etc/postgresql/9.5/main/pg_hba.conf`  

```
local   all             postgres                                peer
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
exit
```

### Deploy GIT Project

Clone GIT project to ~  
Create the directory /var/www/catalog  
Copy the repository catalog/ directory to /var/www/catalog  
So the result is /var/www/catalog/catalog/<project files>  
`sudo a2enmod wsgi`  

`sudo chown -R ubuntu:ubuntu /var/www/catalog`  
`cd /var/www/catalog/catalog`  
`mv project.py __init__.py`  
`vi __init__.py`  
Replace app.run(host='0.0.0.0', port=8000) -> app.run()  

`vi /etc/apache2/sites-available/catalog.conf`  

```
<VirtualHost *:80>
                ServerName 13.236.165.218.xip.io
                ServerAdmin anthony.owen@gmail.com
                WSGIScriptAlias / /var/www/catalog/catalog.wsgi
                <Directory /var/www/catalog/catalog/>
                        Order allow,deny
                        Allow from all
                        Options -Indexes
                </Directory>
                Alias /static /var/www/catalog/catalog/static
                <Directory /var/www/catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                        Options -Indexes
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

`sudo a2ensite catalog`  
`sudo service apache2 reload`  

`vi /var/www/catalog/catalog.wsgi`  
```
activate_this = '/var/www/catalog/catalog/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog")
sys.path.insert(0,"/var/www/catalog/catalog")

from catalog import app as application
application.secret_key = '12345'
````

Update all code to use postgredb: __init__.py, database_setup.py & database_init.py  
`engine = create_engine('postgresql://catalog:<PASSWORD>@localhost/catalog')`  

`a2dissite 000-default.conf`  
`sudo service apache2 reload`  

`sudo chown -R www-data:www-data /var/www/catalog/`  

# Setup Udacity grader account

setup grader:  
`sudo adduser grader`  
`sudo usermod -aG sudo grader`  
^ OR \  
`sudo visudo`  
`grader ALL=(ALL:ALL) ALL`  
`touch ~/.ssh/authorized_keys`  
`chmod 700 ~/.ssh`  
`chmod 644 ~/.ssh/authorized_keys`  
`nano ~/.ssh/authorized_keys`  

On your local machine:  
`ssh-keygen grader_key`  
`cat ~/.ssh/grader_key.pub`  
Paste the key contents into the authorized_keys file in the grader account on the server.  

Test connection:  
`ssh grader@13.236.165.218 -p 2200 -i ~/.ssh/grader_key`  
