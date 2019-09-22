# Python Pyro Assignment 2
### Distributed System TC-ITS 19/20
Rahadian K Putra  
05111640000006  
  
## How-To
### Dependencies Installation
```pip install -r requirements.txt```  

### Run Program
#### Server
```shell script
python PyroFile_Server.py -d DPATH -w -n NAME -h HOST -p PORT

-d, --dpath=path    Required. Root directory to use. Default to '/var/pyrofileserver'
-w, --withns        Use Pyro Nameserver
-n, --name=name     Use Pyro Nameserver naming. Default to 'pyrofileserver'
-h, --host=host     Use Pyro Nameserver host. Default to 'localhost'
-p, --port=port     Use Pyro Nameserver port. Default to 6969
```
#### Client
```shell script
python PyroFile_Client.py -h HOST

-h, --host=uri      Host to use. If not specified, automatically use host in 'pyro_host' file
```
##### Available Commands
```shell script
ls                      Show directory listing
cat FILE                Read a FILE
touch FILE1 [FILE2] ... Create new blank file(s)
rm FILE1 [FILE2] ...    Delete file(s). Support globing
nano FILE               Edit a FILE. Will overwrite content entirely
help                    Print this information
exit                    Exit this prompt
```
I've prepared a test server on URI: `PYRONAME:pyrofileserver@pyradian.me:6969`  
Run below to test:  
```shell script
python PyroFile_Client.py -h 'PYRONAME:pyrofileserver@pyradian.me:6969'
```
