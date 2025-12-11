import sys
from list import CommandList, ErrorCode
from part import Logic

class ShellApp:
    def __init__(self):
        self.is_running = True
        self.var_dic = {}

    def _echo(self, text):
        sys.stdout.write(text + "\n")

    def _execute_command(self, command: str):
        command = command.strip()

        if not command:
            return

        tokens = Logic.tokenize(command)
        cmd = Logic.parse(tokens)

        if cmd['noun'] == CommandList.Index('noun', 'tmp'):
            if not cmd['verb'] :
                ErrorCode.PartOfSpeech_Missing.ErrorCodePrint()
            elif cmd['verb'] == CommandList.Index('verb', 'echo'):
                if cmd['args'] :
                    output = []
                    for arg in cmd['args']:
                        if arg.startswith('$'):
                            var_name = arg[1:]
                            output.append(str(self.var_dic.get(var_name, arg)))
                        else:
                            output.append(arg)
                    sys.stdout.write(" ".join(output) + "\n")
                else :
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint()
            else :
                ErrorCode.UNKNOWS_COMMAND.ErrorCodePrint()
        
        elif cmd['noun'] == CommandList.Index('noun', 'sys') or cmd['noun'] == CommandList.Index('noun', 'system'):
            if not cmd['verb'] :
                ErrorCode.PartOfSpeech_Missing.ErrorCodePrint()
            elif cmd['verb'] == CommandList.Index('verb', 'stop'):
                if not cmd['args'] :
                    sys.stdout.write("Shut down the system... \n")
                    self.is_running = False
                else:
                    ErrorCode.PARAMETER_UNKNOWN.ErrorCodePrint()
            else :
                ErrorCode.UNKNOWS_COMMAND.ErrorCodePrint()

        elif cmd['noun'] == CommandList.Index('noun', 'var'):
            if not cmd['verb'] :
                ErrorCode.PartOfSpeech_Missing.ErrorCodePrint()
            elif cmd['verb'] == CommandList.Index('verb', 'crt') or cmd['verb'] == CommandList.Index('verb', 'create'):
                if len(cmd['args']) >= 1 and cmd['args'][0].startswith('$'):
                    var_name = cmd['args'][0][1:]
                    value = None

                    if cmd['prep'] == '-in' and len(cmd['args']) >= 2:
                        value = cmd['args'][1]
                    self.var_dic[var_name] = value
                else:
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint()

            elif cmd['verb'] in (CommandList.Index('verb', 'ch'), CommandList.Index('verb', 'chg'), CommandList.Index('verb', 'change')) :
                if len(cmd['args']) >= 2 and cmd['args'][0].startswith('$') and cmd['prep'] == '-in':
                    var_name = cmd['args'][0][1:]
                    if var_name in self.var_dic:
                        self.var_dic[var_name] = cmd['args'][1]
                    else:
                        ErrorCode.UNDECLARED_VARIABLE.ErrorCodePrint()
                else:
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint()

            elif cmd['verb'] == CommandList.Index('verb', 'get') :
                if len(cmd['args']) == 1 and cmd['args'][0].startswith('$') :
                    var_name = cmd['args'][0][1:]
                    if var_name in self.var_dic:
                        sys.stdout.write(f'${var_name}: {self.var_dic[var_name]}\n')
                    else:
                        ErrorCode.UNDECLARED_VARIABLE.ErrorCodePrint()
                else:
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint()

            else :
                ErrorCode.UNKNOWS_COMMAND.ErrorCodePrint()
        
        else :
            ErrorCode.UNKNOWS_COMMAND.ErrorCodePrint()

    def run(self):
        while self.is_running:
            sys.stdout.write("\n>>> ")
            try:
                command = sys.stdin.readline()
                if not command:
                     raise EOFError 

                self._execute_command(command.strip())
            except EOFError:
                sys.stdout.write("\nShut down the system... \n")
                self.is_running = False
            except Exception as e:
                import traceback
                traceback.print_exc(file=sys.stderr)
                sys.stderr.write(f"An unexpected error occurred: {e}\n")
                ErrorCode.UNKNOWN_ERROR.ErrorCodePrint()

if __name__ == "__main__":
    app = ShellApp()
    app.run()