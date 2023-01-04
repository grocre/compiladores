import ply.lex as lex
import ply.yacc as yacc
import sqlite3
import json
import subprocess

db = ""
database = ""
client = ""

# Tokens da linguagem do CRUD
tokens = ['CRIAR', 'DATABASE', 'TABELA_DE_EXEMPLO', 'ALL', 'INSERIR',
          'LER', 'ATUALIZAR', 'DELETAR', 'COLECAO', 'ID', 'VALOR', "QUERY"]

# Regras para os tokens
t_CRIAR = r'criar'
t_ALL = r'\*'
t_DATABASE = r'database'
t_INSERIR = r'inserir'
t_LER = r'ler'
t_ATUALIZAR = r'atualizar'
t_DELETAR = r'deletar'
t_COLECAO = r'colecao'
t_ID = r'id'
t_QUERY = r'query'
t_TABELA_DE_EXEMPLO = r'tabela-de-exemplo'

# Regra para reconhecimento de strings


def t_VALOR(t):
    r'".*"'
    t.value = t.value[1:-1]
    return t


def t_COLUNA(t):
    r'".*"'
    t.value = t.value[:]
    return t


# Regra para ignorar espaços em branco
t_ignore = ' \t'

# Regra para lidar com erros


def t_error(t):
    print(f'Erro léxico: {t.value[0]}')
    t.lexer.skip(1)


# Criação do analisador léxico
lexer = lex.lex()

# Definição da gramática da linguagem do CRUD


def p_crud(p):
    '''sql : CRIAR DATABASE VALOR
            | CRIAR TABELA_DE_EXEMPLO
            | INSERIR VALOR
            | LER COLECAO VALOR
            | LER COLECAO ID VALOR
            | LER COLECAO QUERY VALOR
            | ATUALIZAR COLECAO ID VALOR
            | ATUALIZAR COLECAO QUERY VALOR
            | DELETAR COLECAO VALOR
            | DELETAR COLECAO ID VALOR
            | DELETAR COLECAO QUERY VALOR
            '''
    global db
    global database
    global client

    if p[1] == 'criar' and p[2] == 'database':
        print(f'Criando banco {p[3]} no SQlite3')
        conn = sqlite3.connect(f'{p[3]}.db')
        db = conn
        database = p[3]
    elif p[1] == 'criar' and p[2] == 'tabela-de-exemplo':
        if database == '':
            print('Precisa criar um banco de dados primeiro. Use a seguinte expressao para realizar essa operacao: criar database "nome do banco"')
        else:
            print(f'Criando tabela de exemplo no banco de dados {database}')
            conn = sqlite3.connect(f'{database}.db')
            cursor = conn.cursor()
            cursor.execute("""
                            CREATE TABLE clientes (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    nome TEXT NOT NULL,
                                    idade INTEGER,
                                    cpf     VARCHAR(11) NOT NULL,
                                    email TEXT NOT NULL,
                                    fone TEXT,
                                    cidade TEXT,
                                    uf VARCHAR(2) NOT NULL,
                                    criado_em DATE NOT NULL
                            );
                            """)
            print('Tabela criada com sucesso.')
            print(subprocess.run(['sqlite3', 'compiladores.db', "'PRAGMA table_info(clientes)'"], capture_output=True))
    elif db == "":
        print('Banco de dados ainda não foi criado, usar: criar database "nome do banco"')
    elif p[1] == 'inserir':
        doc = json.loads(p[2].split(".")[1])
        print(
            f'Inserindo documento no banco de dados {database} na coluna {p[2].split(".")[0]}')
        db[p[2].split(".")[0]].insert_one(doc)
    elif p[1] == 'ler':
        if len(p) > 4:
            if p[3] == 'id':
                s = p[4].split(".")
                print(f'Lendo documento com ID {s[1]} na coleção {s[0]}')
                result = db[s[0]].find_one({"_id": ObjectId(s[1])})
                if result != None:
                    print(result)
                else:
                    print(
                        f"Nenhum item foi encontrado na coleção {s[0]} com ID = {s[1]}")
            elif p[3] == 'query':
                s = p[4].split(".")
                print(
                    f'Lendo todos os documento que satisfazem a QUERY: {s[1]} na coleção {s[0]}')
                doc = json.loads(s[1])
                resp = db[s[0]].find(doc)
                cont = 0
                for item in resp:
                    print(item)
                    cont += 1
                if cont == 0:
                    print(
                        f"Nenhum item foi encontrado na coleção {s[0]} com query: {s[1]}")
        else:
            print(f'Lendo todos os documentos na coleção {p[3]}')
            resp = db[p[3]].find()
            cont = 0
            for item in resp:
                print(item)
                cont += 1
            if cont == 0:
                print(f"Nenhum item foi encontrado na coleção {p[3]}")

    elif p[1] == 'atualizar':
        if p[3] == 'id':
            s = p[4].split(".")
            print(
                f'Atualizando documento com ID {s[1]} na coleção {s[0]} com o novo valor {s[2]}')
            update = json.loads(s[2])
            result = db[s[0]].update_one(
                {"_id": ObjectId(s[1])}, {"$set": update})

        elif p[3] == 'query':
            s = p[4].split(".")
            print(
                f'Atualizando todos os documento que satisfazem a QUERY: {s[1]} na coleção {s[0]} com o novo valor {s[2]}')
            query = json.loads(s[1])
            update = json.loads(s[2])
            result = db[s[0]].update_many(query, {"$set": update})

    elif p[1] == 'deletar':
        if len(p) > 4:
            if p[3] == 'id':
                s = p[4].split(".")
                print(f'Deletando documento com ID {s[1]} na coleção {s[0]}')
                result = db[s[0]].delete_one({"_id": ObjectId(s[1])})

            elif p[3] == 'query':
                s = p[4].split(".")
                print(
                    f'Deletando todos os documento que satisfazem a QUERY: {s[1]} na coleção {s[0]}')
                query = json.loads(s[1])
                result = db[s[0]].delete_many(query)
        else:
            print(f'Deletando todos os documentos na coleção {p[3]}')
            result = db[p[3]].delete_many({})


def p_error(p):
    print(f'Erro sintático: {p}')


# Criação do analisador sintático
parser = yacc.yacc()

while True:
    try:
        s = input('')
    except EOFError:
        break

    result = parser.parse(s)
