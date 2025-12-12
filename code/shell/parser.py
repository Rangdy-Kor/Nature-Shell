from .constants import CommandList

class Logic:
    @staticmethod
    def tokenize(code):
        tokens = []
        in_string = False
        current_token = ""
        i = 0
        delimiters = ['(', ')', '{', '}', '>', '<', '=', '!']
        
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
            
            if char in ('>', '<', '=', '!') and i + 1 < len(code) and code[i+1] == '=':
                if current_token:
                    tokens.append(('WORD', current_token))
                    current_token = ""
                tokens.append(('OPERATOR', char + '='))
                i += 2
                continue

            if char in delimiters:
                if current_token:
                    tokens.append(('WORD', current_token))
                    current_token = ""
                tokens.append((char, char))
                i += 1
                continue

            if char.isspace():
                if current_token:
                    tokens.append(('WORD', current_token))
                    current_token = ""
                i += 1
                continue
            
            current_token += char
            i += 1
        
        if current_token:
            tokens.append(('WORD', current_token))

        final_tokens = []
        for token_type, value in tokens:
            if token_type == 'STRING':
                final_tokens.append(('STRING', value))
            
            elif value.startswith('"') and value.endswith('"'):
                final_tokens.append(('STRING', value[1:-1]))
            
            elif value.startswith('$'):
                final_tokens.append(('VARIABLE', value))
            
            elif value.startswith('-'):
                if value in CommandList.Prep or value in ['-if', '-else', '-and', '-or', '-not']:
                    final_tokens.append(('PREPOSITION', value))
                else:
                    final_tokens.append(('WORD', value))
            
            elif ':' in value:
                parts = value.split(':', 1)
                noun_part = parts[0]
                
                if noun_part in CommandList.Noun:
                    final_tokens.append(('NOUN', noun_part))
                    if len(parts) > 1:
                        final_tokens.append(('ADJECTIVE', parts[1]))
                else:
                    final_tokens.append(('WORD', value))
            
            elif value in CommandList.Verb:
                final_tokens.append(('VERB', value))
            
            elif value in CommandList.Noun:
                final_tokens.append(('NOUN', value))
            
            elif token_type == 'OPERATOR' or value in ['>', '<', '==', '!=', '>=', '<=']:
                final_tokens.append(('OPERATOR', value))
            
            elif value in ['(', ')', '{', '}']:
                final_tokens.append((value, value))
            
            else:
                final_tokens.append(('WORD', value))

        return final_tokens
    
    @staticmethod
    def extract_block(tokens, start_idx):
        # { }로 묶인 블록을 추출하는 함수
        if start_idx >= len(tokens) or tokens[start_idx][0] != '{':
            return [], start_idx
        
        depth = 0
        block_tokens = []
        i = start_idx
        
        while i < len(tokens):
            token_type, value = tokens[i]
            
            if token_type == '{':
                depth += 1
                if depth > 1:
                    block_tokens.append(tokens[i])
            elif token_type == '}':
                depth -= 1
                if depth == 0:
                    return block_tokens, i
                else:
                    block_tokens.append(tokens[i])
            else:
                if depth > 0:
                    block_tokens.append(tokens[i])
            
            i += 1
        
        raise ValueError("Unclosed block: missing }")
    
    @staticmethod
    def split_commands(block_tokens):
        # 블록 안의 토큰들을 개별 명령어로 나누기
        commands = []
        current_command = []
        
        for token in block_tokens:
            token_type, value = token
            
            if token_type == 'NOUN' and current_command:
                commands.append(current_command)
                current_command = [token]
            else:
                current_command.append(token)
        
        if current_command:
            commands.append(current_command)
        
        return commands

    @staticmethod
    def parse(tokens):
        if not tokens:
            return None

        # -if 찾기
        if_idx = -1
        for i, token in enumerate(tokens):
            if token[0] == 'PREPOSITION' and token[1] == '-if':
                if_idx = i
                break

        # 조건문 처리
        if if_idx != -1:
            ast = {
                'type': 'conditional',
                'condition': None,
                'if_block': [],
                'else_block': []
            }
            
            condition_part = tokens[:if_idx]
            ast['condition'] = condition_part
            
            rest = tokens[if_idx + 1:]
            
            if not rest:
                return ast
            
            if rest[0][0] == '{':
                try:
                    block_tokens, end_idx = Logic.extract_block(rest, 0)
                    commands = Logic.split_commands(block_tokens)
                    
                    ast['if_block'] = []
                    for cmd_tokens in commands:
                        cmd_str = " ".join([val for typ, val in cmd_tokens])
                        ast['if_block'].append(cmd_str)
                    
                except ValueError as e:
                    print(f"Block parsing error: {e}")
                    return None
            else:
                cmd_str = " ".join([val for typ, val in rest])
                ast['if_block'] = [cmd_str]
            
            return ast
        
        # 일반 명령어 처리
        else:
            ast = {
                'type': 'command',
                'noun': None,
                'adjective': None,  #  형용사 필드 추가
                'verb': None,
                'args': [],
                'prep': None
            }
            
            pos = 0
            
            #  명사 읽기
            if pos < len(tokens) and tokens[pos][0] == 'NOUN':
                ast['noun'] = tokens[pos][1]
                pos += 1
            else:
                return None
            
            #  형용사 읽기 (있으면)
            if pos < len(tokens) and tokens[pos][0] == 'ADJECTIVE':
                ast['adjective'] = tokens[pos][1]
                pos += 1
            
            #  동사 읽기
            if pos < len(tokens) and tokens[pos][0] == 'VERB':
                ast['verb'] = tokens[pos][1]
                pos += 1

            #  나머지 인수들
            while pos < len(tokens):
                token_type, value = tokens[pos]
                if token_type == 'PREPOSITION':
                    ast['prep'] = value
                    ast['args'].extend([t[1] for t in tokens[pos+1:]])
                    break
                else:
                    ast['args'].append(value)
                pos += 1
                
            return ast