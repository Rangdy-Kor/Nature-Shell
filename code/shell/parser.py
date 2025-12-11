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
                if value in CommandList.Prep or value in ['-if', '-else']:
                    final_tokens.append(('PREPOSITION', value))
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
    def parse(tokens):
        if not tokens:
            return None

        if_idx = -1
        for i, token in enumerate(tokens):
            if token[0] == 'PREPOSITION' and token[1] == '-if':
                if_idx = i
                break

        if if_idx != -1:
            ast = {'type': 'conditional', 'condition': None, 'if_block': None, 'else_block': None}
            condition_part = tokens[:if_idx]
            command_part = tokens[if_idx+1:]

            ast['condition'] = condition_part
            ast['if_block'] = " ".join([val for typ, val in command_part]) # 임시 구현

            return ast
        else:
            ast = {'type': 'command', 'noun': None, 'verb': None, 'adjective': None, 'args': [], 'prep': None, 'value': None}
            if tokens[0][0] == 'NOUN':
                ast['noun'] = tokens[0][1]
            else:
                return None

            pos = 1
            if len(tokens) > 1 and tokens[1][0] == 'VERB':
                ast['verb'] = tokens[1][1]
                pos = 2

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
