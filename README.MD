Note:
=====
Be advised, this is still pretty early.  I'm still hammering out details with the DSL and provider modules (as well as things like whether or not I want to incorporate jinja2)

Command Line:
=============

usage: virt-maker.py [-h] [--file [VMKFILEPATH [VMKFILEPATH ...]]] [--build]
                     [--noop] [--variables [OVERRIDEVARS [OVERRIDEVARS ...]]]
                     [--show-variables] [--show-template]
                     [--input-format INPUT_FORMAT] [--pretty] [--version]

Libvirt based VM builder

optional arguments:
  -h, --help            show this help message and exit
  --file [VMKFILEPATH [VMKFILEPATH ...]], -f [VMKFILEPATH [VMKFILEPATH ...]]
                        VMK build template file
  --build, -b           Build file
  --noop, -n            Displays provider output only
  --variables [OVERRIDEVARS [OVERRIDEVARS ...]]
                        Override input variables on build
  --show-variables      Shows the input variables for a given *.vmk file
  --show-template       Shows the input template for a given *.vmk file
  --input-format INPUT_FORMAT
                        Set the input format (JSON|Key). Default KEY
  --pretty, -p          Displays output in easily readable format
  --version             show program's version number and exit

  
Example:
========
```
#####################################
#                                   #
#     Rundeck server build for      #
# automated test enviroment in APSD #
#                                   #
#####################################

## Example: virt-maker --build --file autotest-rundeck-dev.vmk --variables IPADDR=10.0.0.117 PREFIX=24 GATEWAY=10.0.0.1 HOSTDEV=ens32 DNS1=10.0.0.2 DNS2=10.0.0.1 

##->Variables<-##

## System
OS=centos-6
HOSTNAME=rundeckserver
DOMAIN=local.domain
PASSWORD=


## Networking
IPADDR=10.0.0.100
HOSTDEV=ens2f3
DEVICE=eth0
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
PREFIX=24
GATEWAY=10.0.0.1
DNS1=10.0.0.1
DNS2=8.8.8.8


## Nginx
SSL=ssl
PORT=443
PROXYPORT=4440
SSLCRT=/etc/nginx/ssl/rundeck.crt
SSLKEY=/etc/nginx/ssl/rundeck.key
X509=/C=None/ST=None/O=Local/OU=Domain/CN=local.domain


## Rundeck
RDECKUSER=root: SuperSecretPassword,user,admin,architect,deploy,build
APIUSER=api
APIPASS=apipass
RDECKSSHUSER=root


## Slack
SLACKKEY=1234567/890123456/789012345678901234567
SLACKCHANNEL=#virt-maker-builds



##->Build<-##

@test
which virt-builder


@slack <[SLACKCHANNEL]> <[SLACKKEY]>
Build "<[HOSTNAME]>" Started


## Build base image
@virt-builder <[OS]>
@import <[OS]>.img
@sysprep
@run sed -i s/SELINUX=enforcing/SELINUX=disabled/g /etc/selinux/config
@hostname <[HOSTNAME]>.<[DOMAIN]>
@rootpass <[PASSWORD]>
@run yum clean all
@run yum remove -y cloud*


## Setup network
@file /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
BOOTPROTO=<[BOOTPROTO]>
MTU=1500
ONBOOT=<[ONBOOT]>
TYPE=Ethernet
IPADDR=<[IPADDR]>
PREFIX=<[PREFIX]>
GATEWAY=<[GATEWAY]>
DNS1=<[DNS1]>
DNS2=<[DNS2]>


## Firewall
@run iptables -A INPUT -p tcp -m tcp --dport 22   -j ACCEPT; service iptables save
@run iptables -A INPUT -p tcp -m tcp --dport 80   -j ACCEPT; service iptables save
@run iptables -A INPUT -p tcp -m tcp --dport 443  -j ACCEPT; service iptables save
@run iptables -A INPUT -p tcp -m tcp --dport 4440 -j ACCEPT; service iptables save


## Setup Nginx
@run yum install -y epel-release
@run yum clean all
#@run yum install -y openssl
@run yum install -y nginx

@script
mkdir -p /etc/nginx/ssl
openssl req -x509 -nodes -sha384 -days 3650 -newkey rsa:4096 -keyout '<[SSLKEY]>' -out '<[SSLCRT]>' -subj '<[X509]>'
cat > /etc/nginx/conf.d/10-rundeck.conf << 'EOF'
server {
  listen [::]:80;
  server_name <[HOSTNAME]>.<[DOMAIN]>;
  location / {
    rewrite ^ <[HOSTNAME]>.<[DOMAIN]>$request_uri? permanent;
  }
}
server {
  listen [::]:443;
  server_name <[HOSTNAME]>.<[DOMAIN]>;
  keepalive_timeout 70;
  ssl on;
  ssl_certificate <[SSLCRT]>;
  ssl_certificate_key <[SSLKEY]>;
  access_log /var/log/nginx/access.log  main;
  location / {
    proxy_pass http://127.0.0.1:4440/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size 100M;
  }
}
EOF
@run sed -i s/80/88/g /etc/nginx/nginx.conf
@run rm -f /etc/nginx/conf.d/default.conf
@run chkconfig nginx on


## Setup Rundeck
@run yum install -y java-1.6.0 
@run yum install -y http://repo.rundeck.org/latest.rpm 
@run yum install -y rundeck
@run chkconfig rundeckd on

@file /etc/rundeck/rundeck-config.properties
"loglevel.default=INFO
rundeck.security.useHMacRequestTokens=false
rdeck.base=$base
rss.enabled=$rss
grails.serverURL=https://<[HOSTNAME]>.<[DOMAIN]>
dataSource.dbCreate = update
dataSource.url = jdbc:h2:file:/var/lib/rundeck/data/rundeckdb;MVCC=true

@file /etc/rundeck/framework.properties
framework.server.name = "<[HOSTNAME]>.<[DOMAIN]>"
framework.server.hostname = <[HOSTNAME]>.<[DOMAIN]>
framework.server.port = 4440
framework.server.url = https://<[HOSTNAME]>.<[DOMAIN]>
framework.server.username = <[APIUSER]>
framework.server.password = <[APIPASS]>
rdeck.base=$base
framework.projects.dir=/var/rundeck/projects
framework.etc.dir=/etc/rundeck
framework.var.dir=$base/var
framework.tmp.dir=$base/var/tmp
framework.logs.dir=$base/logs
framework.libext.dir=$base/libext
framework.ssh.keypath = $keypath
framework.ssh.user = <[RDECKSSHUSER]>
framework.ssh.timeout = 0

@file /etc/rundeck/realm.properties
<[RDECKUSER]>
<[APIUSER]>: <[APIPASS]>,user,deploy

@file /etc/rundeck/profile
RDECK_BASE=/var/lib/rundeck
export RDECK_BASE
JAVA_CMD=java
RUNDECK_TEMPDIR=/tmp/rundeck
RDECK_HTTP_PORT=4440
RDECK_HTTPS_PORT=4443
if [ ! -z $JAVA_HOME ]; then
  PATH=$PATH:$JAVA_HOME/bin
  export PATH
  JAVA_CMD=$JAVA_HOME/bin/java
fi
export CLI_CP=$(find /var/lib/rundeck/cli -name \*.jar -printf %p:)
export BOOTSTRAP_CP=$(find /var/lib/rundeck/bootstrap -name \*.jar -printf %p:)
export RDECK_JVM="-Djava.security.auth.login.config=/etc/rundeck/jaas-loginmodule.conf -Drundeck.jetty.connector.forwarded=true -Dloginmodule.name=RDpropertyfilelogin -Drdeck.config=/etc/rundeck -Drdeck.base=/var/lib/rundeck -Drundeck.server.configDir=/etc/rundeck -Dserver.datastore.path=/var/lib/rundeck/data -Drundeck.server.serverDir=/var/lib/rundeck -Drdeck.projects=/var/rundeck/projects -Drdeck.runlogs=/var/lib/rundeck/logs -Drundeck.config.location=/etc/rundeck/rundeck-config.properties -Djava.io.tmpdir=$RUNDECK_TEMPDIR"
RDECK_JVM="$RDECK_JVM -Xmx1024m -Xms256m -XX:MaxPermSize=256m -server"
#export RDECK_JVM="$RDECK_JVM -Drundeck.ssl.config=/etc/rundeck/ssl/ssl.properties -Dserver.https.port=${RDECK_HTTPS_PORT}"
export RDECK_SSL_OPTS="-Djavax.net.ssl.trustStore=/etc/rundeck/ssl/truststore -Djavax.net.ssl.trustStoreType=jks -Djava.protocol.handler.pkgs=com.sun.net.ssl.internal.www.protocol"
if test -t 0 -a -z "$RUNDECK_CLI_TERSE"
then
  RUNDECK_CLI_TERSE=true
  export RUNDECK_CLI_TERSE
fi
if test -n "$JRE_HOME"
then
  unset JRE_HOME
fi
umask 002


## Prepare system for deployment
@export <[HOSTNAME]>.<[DOMAIN]>
@cp <[HOSTNAME]>.<[DOMAIN]> /var/lib/libvirt/images/<[HOSTNAME]>.<[DOMAIN]>
@virsh destroy <[HOSTNAME]>
@virsh undefine <[HOSTNAME]>
@create /var/lib/libvirt/images/<[HOSTNAME]>.<[DOMAIN]>
name=<[HOSTNAME]>
network=type=direct,source=<[HOSTDEV]>,model=virtio
ram=2048


## Post slack message
@slack <[SLACKCHANNEL]> <[SLACKKEY]>
Build "<[HOSTNAME]>" Complete
```