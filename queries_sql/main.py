from ply.lex import lex
from ply.yacc import yacc

tokens = ('TABLE', 'COLUMN', 'ALL', 'SELECT', 'FROM')

reserved = {all: r"\*"}


t_ignore = ' \t'

t_TABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_COLUMN = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_ALL = r'\*'
    

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()

def p_expression(p):
    '''
    expression : SELECT term
    
    '''
    # p is a sequence that represents rule contents.
    # 
    # expression : SELECT term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = ('command', p[2], p[1])


def p_term(p):
    '''
    term : factor FROM factor
    '''
    p[0] = ('term', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1] # precedência

def p_factor_table(p):
    '''
    factor : TABLE
    '''
    p[0] = ('table', p[1])

def p_factor_name(p):
    '''
    factor : COLUMN
    '''
    p[0] = ('column', p[1])

def p_factor_all(p):
    '''
    factor : ALL
    '''
    p[0] = ('all', p[1])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('SELECT * FROM tabela1')

# p = ["SELECT", "*", "FROM", "tabela1"]

''''
p[0] = "SELECT"
p[1] = "*"
p[2] = "FROM"
P[3] = "tabela1"

Necessária uma função para tratar o dict

fluxo: 

dict -> compilador -> saida de um .sql -> execução do arquivo de saída

'''
print(ast)


