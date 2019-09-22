# Python Pyro Assignment 2  
## How-To
### Dependencies Installation
```shell script
pip install -r requirements.txt
```  

### Run Program
#### Server
```shell script
python PyroFile_Server.py -d DPATH -w -n NAME -h HOST -p PORT

Options:
-d DPATH, --dpath=DPATH   Required. Root directory to use
-w, --withns              Use Pyro Nameserver
-n NAME, --name=NAME      Use Pyro Nameserver naming. Default to 'pyrofileserver'
-h HOST, --host=HOST      Use Pyro Nameserver host. Default to 'localhost'
-p PORT, --port=PORT      Use Pyro Nameserver port. Default to 6969
```
If you prefer to use Pyro NameServer, you have to start the service first.
```shell script
pyro4-ns -n HOST -p PORT

Options:
-n HOST, --host=HOST  hostname to bind server on
-p PORT, --port=PORT  port to bind server on (0=random)
```
#### Client
```shell script
python PyroFile_Client.py -h HOST

Options:
-h HOST, --host=HOST      Host to use. If not specified, automatically use host in 'pyro_host' file
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
