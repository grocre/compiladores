from ply.lex import lex
from ply.yacc import yacc

token = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'NAME', 'NUMBER' )

t_ignore = ' \t'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN =r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_number(t): 
    r'\d+'
    t.value = int(t.value)
    return t

def t_ignore_newline(t): 
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()

def p_expression(p): 
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p): 
    p[0] = p[1]

def p_term(p):
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p): 
    p[0] = p[1]

def p_factor_number(p):
    p[0] = ('number', p[1])

def p_factor_name(p):
    p[0] = ('name', p[1])

def p_factor_unary(p):
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

parser = yacc()

ast = parser.parse('3 * 3 + 4 * (5 - x)')
print(ast)