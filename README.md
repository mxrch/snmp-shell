# SNMP Shell
### Shell Simulation over Net-SNMP with extend functionality

Here is a preview :\
\
![Screenshot](https://user-images.githubusercontent.com/17338428/86642223-083ac100-bfdc-11ea-85da-2cece511534d.PNG)

## Description
If your target has a **Net-SNMP** instance with the **"extend"** functionality, and you got a **SNMP community string** which gives you **write access**, you can use this tool to automate the process of sending commands with the SNMP RCE.\
\
The tool automatically put you in your path to **simulate a real shell**.\
You can also use all the commands you can imagine, apart those requiring a fully interactive shell (MySQL, Vim, Nano, etc.)\
*Not compatible Windows, sorry.*

## Installation (Linux)
```bash
sudo apt install snmp snmp-mibs-downloader rlwrap -y
git clone https://github.com/mxrch/snmp-shell
cd snmp-shell
sudo python3 -m pip install -r requirements.txt
```

## Usage
```bash
$ rlwrap python shell.py <IP> -c <community string>
```

## Help
If you need to send longer strings, like your SSH public key, please use the `legacy.py` version.\
The characters limit to send is short (SNMP Limitation).\
*Tips : use a `ed25519` SSH publickey, not a `RSA` one, it's shorter.*

```
Usage: shell.py [OPTIONS] IP

  Simulates a terminal over Net-SNMP "extend" functionality. Be sure your
  SNMP Community String has write access.

Options:
  -c, --communitystring TEXT  Community string for SNMP
  -v, --version TEXT          SNMP version (1/2c/3)
  -ss, --snmpset TEXT         Path for the snmpset binary
  -sw, --snmpwalk TEXT        Path for the snmpwalk binary
  -h, --help                  Show this message and exit.
```

*****
## References
https://mogwailabs.de/blog/2019/10/abusing-linux-snmp-for-rce/
