import sys
from enum import Enum

class CommandList() :
    Noun = ('tmp', 'sys', 'system', 'var')
    Verb = ('ch', 'chg', 'change', 'crt', 'create', 'echo', 'get', 'stop')
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
