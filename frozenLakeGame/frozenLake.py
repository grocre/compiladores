import ply.lex as lex
import ply.yacc as yacc
import numpy as np

'''
Introdução:

Este é um trabalho desenvolvido para a disciplina de Compiladores do CEFET-RJ. Foi desenvolvido um jogo utilizando as ferramentas do PLY, uma implementação em Python de ferramentas de parsing tradicionais como o lex e o yacc.

##############################################################################################################################################################################

REGRAS:

1 - O OBJETIVO É COLETAR O TROFEU E SAIR DO LABIRINTO ILESO
2 - O JOGADOR PERDE SE CAIR EM UM BURACO DE GELO
3 - O JOGADOR PERDE SE SAIR DO LAGO SEM O TROFEU
4 - O JOGADOR PERDE SE TENTAR PEGAR O TROFEU EM UM ESTADO ONDE NÃO EXISTE TROFEU

##############################################################################################################################################################################

AÇÕES VÁLIDAS:

START - INICIA O JOGO
MOVE UP, MOVE DOWN, MOVE RIGHT e MOVE LEFT - Movem o player pelo mapa
CATCH - Coleta o prêmio
EXIT - Sai do lago.

##############################################################################################################################################################################

LEGENDA DO MAPA:

S - ESTADO INICIAL/FINAL - start
G - ESTADO OBJETIVO (ONDE CONTEM O PREMIO) - goal
H - ESTADO ONDE HÁ UM BURACO NO LAGO - hole
P - ESTADO ONDE SE ENCONTRA O PLAYER - player
_ - ESTADO NEUTRO

'''

# Tokens da linguagem do CRUD
tokens = ['INICIAR', 'MOVER', 'PEGAR', 'SAIR', 'CIMA', 'BAIXO', 'ESQUERDA', 'DIREITA']

# Regras para os tokens
t_INICIAR = r'START'
t_MOVER = r'MOVE'
t_PEGAR = r'CATCH'
t_SAIR = r'EXIT'
t_CIMA = r'UP'
t_BAIXO = r'DOWN'
t_DIREITA = r'RIGHT'
t_ESQUERDA = r'LEFT'

# geração das matrizes e definição dos obstáculos (de maneira estática)
matriz = np.chararray((5, 5), offset= 1, unicode=True)
action = ""
start_state = (0 , 0)
player_state = [0, 0]
goal_state = (4 , 4)
holes = (
    (2, 3), 
    (3, 4), 
    (1, 4), 
    (2, 0), 
    (3, 1)
)

# Regra para ignorar espaços em branco
t_ignore = ' \t'

# Regra para lidar com erros
def t_error(t):
    print(f'Erro léxico: {t.value[0]}')
    t.lexer.skip(1)\


# Criação do analisador léxico
lexer = lex.lex()

# Definição da gramática do jogo
def p_expressao(p):
    '''
        expressao : comando acao
                | comando
                    
    '''
    global matriz
    global action
    global start_state
    global player_state
    global goal_state
    global holes
    global is_with_goal
    is_with_goal = False

    # Comando de Começar
    if p[1] == 'START':

        print(p)
        
        # Grandeza da matriz
        n = 5

        # Definindo o index inicial das linhas da matriz
        row_index = 0
        # Para cada linha na matriz
        for row in matriz:
            # Para cada index de coluna na linha
            for column in range(n):
                # Se a posição for igual ao estado inicial, armazena 'S' na matriz
                if (row_index, column) == start_state:
                    matriz[row_index, column] = 'S'
                # Se a posição for igual a algum buraco no gelo, armazena 'H' na matriz
                elif (row_index, column) in holes:
                    matriz[row_index, column] = "H"
                # Se a posição for igual ao estado objetivo, armazena 'G' na matriz
                elif (row_index, column) == goal_state:
                    matriz[row_index, column] = "G"
                # Se a posição for neutra, armazena '_' na matriz
                else:
                    matriz[row_index, column] = "_"
            # Incrementa o index da linha em questão        
            row_index += 1
        # Print para o usuário final
        print(f'\nS - ESTADO INICIAL/FINAL - start\nG - ESTADO OBJETIVO (ONDE CONTEM O PREMIO) - goal\nH - ESTADO ONDE HÁ UM BURACO NO LAGO - hole\nP - ESTADO ONDE SE ENCONTRA O PLAYER - player\n_ - ESTADO NEUTRO\n\nO estado inicial do seu jogo é o seguinte:\n\n{matriz}\n')
     # Comando de Movimentação
    if p[1] =='MOVE':

        # Mover o jogador para cima
        if p[2] == 'UP':
            # Define action como UP para evitar mensagem de erro ao usuário
            action = p[2]
            player_linha_atual = player_state[0]
            valor_posicao_futura = matriz[player_state[0] - 1, player_state[1]]
            
            if valor_posicao_futura == 'S':

                matriz[player_state[0], player_state[1]] = '_'
                player_state[0] = player_state[0] - 1

            elif player_linha_atual == 0:
                print("\nCuidado, você bateu na parede do lago!\n")

            elif valor_posicao_futura == 'H':
                print('\nAh que pena, você caiu em um buraco! Game over.\n')
            else: 
                matriz[player_state[0], player_state[1]] = valor_posicao_futura
                matriz[player_state[0] - 1, player_state[1]] = 'P'
                player_state[0] = player_state[0] - 1
            print(player_state)
            print(matriz) 
            
        # mover para baixo
        elif p[2] == "DOWN":

            action = p[2]
            player_linha_atual = player_state[0]
            if (player_state[0], player_state[1]) == start_state:
                matriz[player_state[0] + 1, player_state[1]] = 'P'
                player_state[0] = player_state[0] + 1
            elif player_linha_atual == 4:
                print("\nCuidado, você bateu na parede do lago!\n")
            else:
                valor_posicao_futura = matriz[player_state[0] + 1, player_state[1]]
                if valor_posicao_futura == 'H':
                    print('\nAh que pena, você caiu em um buraco! Game over.\n')

                else: 
                    matriz[player_state[0], player_state[1]] = valor_posicao_futura
                    matriz[player_state[0] + 1, player_state[1]] = 'P'
                    player_state[0] = player_state[0] + 1
                print(player_state)
                print(matriz) 

        # mover para a direita
        elif p[2] == "RIGHT":
            action = p[2]

            player_coluna_atual = player_state[1]
            if (player_state[0], player_state[1]) == start_state:
                matriz[player_state[0], player_state[1] + 1] = 'P'
                player_state[1] = player_state[1] + 1
            elif player_coluna_atual == 4:
                print("\nCuidado, você bateu na parede do lago!\n")
            else:
                valor_posicao_futura = matriz[player_state[0], player_state[1] + 1]
                if valor_posicao_futura == 'H':
                    print('\nAh que pena, você caiu em um buraco! Game over.\n')
                elif valor_posicao_futura == 'G':
                    matriz[player_state[0], player_state[1]] = '_'
                    player_state[1] = player_state[1] + 1
                else:
                    matriz[player_state[0], player_state[1]] = valor_posicao_futura
                    matriz[player_state[0], player_state[1] + 1] = 'P'
                    player_state[1] = player_state[1] + 1
            print(player_state)
            print(matriz)     

        # mover para a esquerda
        elif p[2] == "LEFT":
            action = p[2]

            player_coluna_atual = player_state[1]
            if player_coluna_atual == 0:
                print("\nCuidado, você bateu na parede do lago!\n")
            else:
                valor_posicao_futura = matriz[player_state[0], player_state[1] - 1]
                if valor_posicao_futura == 'H':
                    print('\nAh que pena, você caiu em um buraco! Game over.\n')
                elif valor_posicao_futura == 'S':
                    matriz[player_state[0], player_state[1]] = '_'
                    player_state[1] = player_state[1] - 1
                else:
                    matriz[player_state[0], player_state[1]] = valor_posicao_futura
                    matriz[player_state[0], player_state[1] - 1] = 'P'
                    player_state[1] = player_state[1] - 1
            print(player_state)
            print(matriz)      

        elif action == "":
            print("\nVocê precisa inserir um valor válido para o movimento. Exemplo de uso: MOVE UP, MOVE DOWN, MOVE RIGHT and MOVE LEFT\n")
    
    # comando para pegar o goal
    if p[1] == 'CATCH':
        if (player_state[0], player_state[1]) != goal_state: 
            
            if is_with_goal == False:
                print("\nVocê Perdeu! Inicie o jogo novamente digitando START\n")

            else:
                print("\nParabéns! Você coletou o prêmio, agora você deve voltar ao estado inicial e fugir do lago!\n")
        
        else: 
            print("\n{matriz}\n\nVocê coletou a goal. Agora siga até a saída do Lago!! (A saída é localizada no mesmo local que a entrada)\n")

    # comando para sair do lago
    if p[1] == 'EXIT': 
        if (player_state[0], player_state[1]) != start_state: 
                if is_with_goal == False:
                    print("\n Você precisa coletar a goal antes. Game over, rode o comando START para recomeçar.")
                else: 
                    print("Game over. Você precisa retornar a entrada do lago! Rode o comando START para recomeçar")
        else: 
            print("Parabéns, você ganhou!!!") 
                
def p_comando(p):
    '''
        comando : INICIAR 
                | MOVER
                | PEGAR
                | SAIR
    '''
    p[0] = p[1]

def p_acao(p):
    '''
        acao : BAIXO  
            | CIMA
            | DIREITA
            | ESQUERDA
    '''
    p[0] = p[1]

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
