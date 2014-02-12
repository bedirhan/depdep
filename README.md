Depdep is a merciless sentinel which will seek sensitive files containing critical info leaking through your network. Basically, it is a fast and practical sensitive data search tool **maintaining** personal &amp; commercial data privacy for companies and institutions. It can very well be used by auditors making sure that their network doesn't leak any unauthorized non-compliant data through windows &amp; unix/linux shares.

The usage is easy and configurable, however, certain technical knowledge is necessary, such as using linux console, ability of writing and understanding basic regular expressions, etc.

**To-Do List**

* Process using hostname or ip address
* Advanced Logging operations 
* Advanced Debugging operations 
* Detect Linux sharing (NFS)

**Installation**

In order to run depdep succesfully, you have to install some packages. Packages needed to run depdep succesfully are below.

* nmap -> Scan network and detect opened 445/tcp ports
* cifs-utils -> mount windows sharing from linux machine
* mount -> mount and umount operations
* smbclient -> list windows sharing
* samba4-clients -> other operations for listing and accessing windows sharing from linux machine
* findutils -> find command utility
* curl -> upload files to the tika and get results

For this, you can use apt-get. For Kali Linux :

    # apt-get install nmap cifs-utils mount smbclient samba4-clients findutils curl

There is tika binary in the script directory. In order to run tika, java must be installed on system. So you have to setup java related your arch. You can achieve this using apt-get like below;

    # apt-get install openjdk-6-jre-headless:amd64

Then you must download tika from internet and run like below;

    # /usr/bin/java -jar /opt/tika/tika-server-1.4.jar >/dev/null 2>/dev/null &

Also there ise script that can manage tika into the script directoy. Use this script;
    
    # /etc/init.d/tika.sh start
    [+] Tika has been started ...
    
    To see running tika process using ps command,
    # ps -ef | grep java | grep -v grep
    root     13066     1 99 15:52 pts/3    00:00:01 /usr/bin/java -jar /opt/tika/tika-server-1.4.jar
    
After that, you have to configure depdep configuration file to run depdep . Please configure depdep.xml config file before usage.

**Basic Usage**

    # python depdep.py --config config/depdep.xml

When you dont use -w 1 options, depdep search sessions file records history about depdep operation. So if you want to use session file use above. But if you don't want to use session file, use -w 1 option like below.

    # python depdep.py --config config/depdep.xml -w 1

    
    
