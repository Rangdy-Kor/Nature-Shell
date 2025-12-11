import sys
sys.stdout.write("Importing modules...\n")

import shell.command as cmd
import time as tm
sys.stdout.write("Imported modules.\n")

sys.stdout.write("Shell starting...\n")

app = cmd.ShellApp()
sys.stdout.write("Shell started.\n")
app.run()