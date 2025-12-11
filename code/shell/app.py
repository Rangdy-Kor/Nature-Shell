# 모듈 불러오기
import sys
from .constants import CommandList, ErrorCode
from .parser import Logic

class ShellApp:
    # 변수 초기화
    def __init__(self):
        self.is_running = True
        self.var_dic = {}

    # 조건식을 평가하여 True/False를 반환하는 함수
    def _evaluate_condition(self, condition_tokens):
        # 조건에 아무것도 없다면 False를 반환
        if not condition_tokens:
            return False

		# Python이 이해 가능한 조건식 문자열 만들기
        eval_string = ""
        
		# 토큰을 하나하나 읽어가며 문자열을 완성
        for token_type, value in condition_tokens:
            
			# 변수인 경우 실제 값으로 변환
            if token_type == 'VARIABLE':
                var_name = value[1:]
                var_value = self.var_dic.get(var_name)
                
				# 변수가 없을 시 에러
                if var_value is None:
                    ErrorCode.UNDECLARED_VARIABLE.ErrorCodePrint()
                    return False
                
				# 문자열이면 따옴표 추가, 숫자면 그대로
                if isinstance(var_value, str):
                    eval_string += f'"{var_value}" '
                else:
                    eval_string += f'{var_value} '
                    
			# 변수가 아닌 경우, Shell 연산자를 Python의 그것으로 변환
            else:
                op_map = {'-and': 'and', '-or': 'or', '-not': 'not'}
                eval_string += f'{op_map.get(value, value)} '
        
        try:
            return eval(eval_string)
        except Exception as e:
            sys.stderr.write(f"Error evaluating condition: {e}\n")
            return False

    def _execute_command(self, command: str):
        command = command.strip()

        if not command:
            return

        tokens = Logic.tokenize(command)
        cmd = Logic.parse(tokens)

        if not cmd:
            return
        
        if cmd.get('type') == 'conditional':
            if self._evaluate_condition(cmd.get('condition')):
                if cmd.get('if_block'):
                    self._execute_command(cmd['if_block'])
            else:
                if cmd.get('else_block'):
                    self._execute_command(cmd['else_block'])
            return

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
                        raw_value = cmd['args'][1]
                        try:
                            value = int(raw_value)
                        except ValueError:
                            value = raw_value
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