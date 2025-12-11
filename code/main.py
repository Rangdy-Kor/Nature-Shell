# 모듈 불러오기
import sys
sys.stdout.write("Importing modules...\n")

import shell.app as cmd
import time as tm
sys.stdout.write("Imported modules.\n")

# 스크립트 실행
sys.stdout.write("Shell starting...\n")

app = cmd.ShellApp()
sys.stdout.write("Shell started.\n")
app.run()