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

        # 명령어가 비어있으면 그대로 종료
        if not command:
            return

        tokens = Logic.tokenize(command) # 명령어를 토큰화
        cmd = Logic.parse(tokens) # 토큰을 파싱하여 딕셔너리 생성

        # 구문 해석 실패 시 그대로 종료
        if not cmd:
            return
        
        # 조건문 실행
        if cmd.get('type') == 'conditional':
            if self._evaluate_condition(cmd.get('condition')): # 조건식 평가
                if cmd.get('if_block'):
                    self._execute_command(cmd['if_block']) # 조건이 참일 경우 if_block 실행
            else:
                if cmd.get('else_block'):
                    self._execute_command(cmd['else_block']) # 조건이 거짓일 경우 else_block 실행
            return

        # 임시 명사 처리
        if cmd['noun'] == CommandList.Index('noun', 'tmp'):
            if not cmd['verb'] :
                ErrorCode.PartOfSpeech_Missing.ErrorCodePrint()
            elif cmd['verb'] == CommandList.Index('verb', 'echo'): # echo 명령어 처리
                if cmd['args'] :
                    output = []
                    for arg in cmd['args']:
                        if arg.startswith('$'): # 인수가 변수인 경우
                            var_name = arg[1:]
                            # 변수 딕셔너리에서 값을 가져오고, 값이 없으면 그대로 사용
                            output.append(str(self.var_dic.get(var_name, arg)))
                        else:
                            output.append(arg) # 변수가 아니면 인수를 그대로 사용
                    sys.stdout.write(" ".join(output) + "\n") # 모든 인수를 공백으로 연결하여 출력
                else :
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint() # 인수가 없는 경우
            else :
                ErrorCode.UNKNOWS_COMMAND.ErrorCodePrint() # 알 수 없는 동사 에러
        
        # 시스템 명령어 처리
        elif cmd['noun'] == CommandList.Index('noun', 'sys') or cmd['noun'] == CommandList.Index('noun', 'system'):
            if not cmd['verb'] :
                ErrorCode.PartOfSpeech_Missing.ErrorCodePrint()
            elif cmd['verb'] == CommandList.Index('verb', 'stop'): # stop 명령어 처리
                if not cmd['args'] :
                    sys.stdout.write("Shut down the system... \n")
                    self.is_running = False # 쉘 실행 변수를 False로 설정하여 종료 준비
                else:
                    ErrorCode.PARAMETER_UNKNOWN.ErrorCodePrint() # 인수가 있는 경우 에러
            else :
                ErrorCode.UNKNOWS_COMMAND.ErrorCodePrint()

        # 변수 명령어 처리
        elif cmd['noun'] == CommandList.Index('noun', 'var'):
            if not cmd['verb'] :
                ErrorCode.PartOfSpeech_Missing.ErrorCodePrint()
            # create 명령어 처리 
            elif cmd['verb'] == CommandList.Index('verb', 'crt') or cmd['verb'] == CommandList.Index('verb', 'create'):
                # 인수가 1개 이상이고 첫 번째 인수가 변수인 경우
                if len(cmd['args']) >= 1 and cmd['args'][0].startswith('$'):
                    var_name = cmd['args'][0][1:]
                    value = None

                    # -in 전치사와 두 번째 인수가 있는 경우 값 할당
                    if cmd['prep'] == '-in' and len(cmd['args']) >= 2:
                        raw_value = cmd['args'][1]
                        try:
                            value = int(raw_value)
                        except ValueError:
                            value = raw_value
                    self.var_dic[var_name] = value
                else:
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint()

            # change 명령어 처리
            elif cmd['verb'] in (CommandList.Index('verb', 'ch'), CommandList.Index('verb', 'chg'), CommandList.Index('verb', 'change')) :
                # 인수가 2개 이상이고 첫 번째 인수가 변수이며, -in 전치사가 있는 경우
                if len(cmd['args']) >= 2 and cmd['args'][0].startswith('$') and cmd['prep'] == '-in':
                    var_name = cmd['args'][0][1:]
                    if var_name in self.var_dic:
                        self.var_dic[var_name] = cmd['args'][1]
                    else:
                        ErrorCode.UNDECLARED_VARIABLE.ErrorCodePrint()
                else:
                    ErrorCode.PARAMETER_MISSING.ErrorCodePrint()

            # get 명령어 처리
            elif cmd['verb'] == CommandList.Index('verb', 'get') :
                # 인수가 1개이고 변수인 경우
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
        while self.is_running: # self.is_running이 True인 동안 반복
            sys.stdout.write("\n>>> ") # 사용자에게 입력 대기 프롬프트 출력
            try:
                command = sys.stdin.readline() # 표준 입력(키보드)에서 한 줄 읽기
                if not command:
                     raise EOFError # 입력이 없으면 EOFError 발생

                self._execute_command(command.strip()) # 읽은 명령어를 앞뒤 공백 제거 후 실행
            except EOFError:
                sys.stdout.write("\nShut down the system... \n") # EOFError 발생 시 종료 메시지 출력 후 실행 플래그 False로 설정
                self.is_running = False
            except Exception as e:
                import traceback
                traceback.print_exc(file=sys.stderr) # 예외 발생 시 스택 추적 정보를 stderr에 출력
                sys.stderr.write(f"An unexpected error occurred: {e}\n") # 예상치 못한 오류 메시지 출력
                ErrorCode.UNKNOWN_ERROR.ErrorCodePrint() # 일반적인 알 수 없는 오류 코드 출력

# 스크립트가 직접 실행될 때
if __name__ == "__main__":
    sys.stdout.write("Shell starting...\n")
    app = ShellApp()
    sys.stdout.write("Shell started.\n")
    app.run()