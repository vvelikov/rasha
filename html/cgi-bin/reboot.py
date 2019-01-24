#!/usr/bin/python
import subprocess
command = "sudo reboot -f"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
