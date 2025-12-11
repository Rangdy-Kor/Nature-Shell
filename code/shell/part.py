from list import CommandList

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
