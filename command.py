import sys
from enum import Enum

class CommandList() :
    Noun = ('tmp', 'sys', 'system', 'var')
    Verb = ('ch', 'change', 'crt', 'create', 'echo', 'get', 'stop')
    Prep = ('-in')
    
    @staticmethod
    def Index(key, ele) :
        if key == 'noun' :
            return CommandList.Noun[CommandList.Noun.index(ele)]
        elif key == 'verb' :
            return CommandList.Verb[CommandList.Verb.index(ele)]

class ErrorCode (Enum):
    SUCCESS = ('0', 'Successfully executed') 
    UNKNOWN_ERROR = ('-1', 'Unknown error')

    UNKNOWS_COMMAND = ('1-1', 'Unknown command has been entered')

    PartOfSpeech_Missing = ('2-1', 'Required part of speech is missing')

    PARAMETER_MISSING = ('3-1', 'Required parameter is missing')
    PARAMETER_UNKNOWN = ('3-2', 'Unknown parameter has been entered')

    UNDECLARED_VARIABLE = ('4-1', 'This is an undeclared variable')

    def __init__ (self, code, description) :
        self.code = code
        self.description = description

    def ErrorCodePrint (self) :
        sys.stderr.write(f"ErrorCode {self.code}: {self.description}\n")

class Logic:
    @staticmethod
    def tokenize(code):
        tokens = []
        in_string = False
        current_token = ""
        i = 0
        
        while i < len(code):
            char = code[i]
            if char == '"':
                if in_string:
                    tokens.append(('STRING', current_token))
                    current_token = ""
                    in_string = False
                else:
                    in_string = True
                i += 1
                continue
            
            if in_string:
                current_token += char
                i += 1
                continue
            
            if char in (' ', '\t', '\n'):
                if current_token:
                    if current_token.startswith('-'):
                        tokens.append(('PREPOSITION', current_token))
                    elif current_token.startswith('$'):
                        tokens.append(('VARIABLE', current_token))
                    else:
                        tokens.append(('WORD', current_token))
                    current_token = ""
                i += 1
                continue
            
            current_token += char
            i += 1
        
        if current_token:
            if in_string:
                raise ValueError("Unclosed string")
            if current_token.startswith('-'):
                tokens.append(('PREPOSITION', current_token))
            elif current_token.startswith('$'):
                tokens.append(('VARIABLE', current_token))
            else:
                tokens.append(('WORD', current_token))
        
        return tokens
    
    @staticmethod
    def parse(tokens):
        ast = {
            'noun': None,
            'verb': None,
            'args': [],
            'prep' : None
        }
        
        if tokens:
            ast['noun'] = tokens[0][1]
        
        if len(tokens) > 1:
            ast['verb'] = tokens[1][1]
            
            if len(tokens) > 2:
                for token in tokens[2:]:
                    if token[0] == 'PREPOSITION' and token[1] in CommandList.Prep:
                        ast['prep'] = token[1]
                    else:
                        ast['args'].append(token[1])
        return ast

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

            elif cmd['verb'] in (CommandList.Index('verb', 'ch'), CommandList.Index('verb', 'change')):
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