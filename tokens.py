TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_IDENTIFIER  = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_EOF = "EOF"
TT_AND = "AND"
TT_OR = "OR"
TT_NOT = "NOT"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"
TT_COLON = "COLON"
TT_COMMA = "COMMA"
TT_STRING = "STRING"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"
TT_DOT = "DOT"

KEYWORDS = [
    "let",
    "if",
    "elif",
    "else",
    "for",
    "to",
    "step",
    "while",
    "and",
    "or",
    "not",
    "fun",
    "return",
    "skip",
    "stop"
]

class Token:
    def __init__(self,type_,value=None,pos_start=None,pos_end=None):
        self.type = type_
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start
            self.pos_end= pos_start.copy()
            self.pos_end.advance()
            
        if pos_end:
            self.pos_end = pos_end
            
    def matches(self,type_,value=None):
        return self.type == type_ and self.value == value
        
    def __repr__(self) -> str:
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"