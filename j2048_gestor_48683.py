
from random import randint
from random import seed

numero  = None
amigos  = None
grelha  = None
jogadas = None
pontos  = None
semente = None

def get_numero(linha):
# obtem o numero de aluno do jogador
    numero = linha[7:-1]

    print('numero = "' + numero + '"')

    return numero


def get_amigos(linha):
# obtem os amigos de um jogador, fazendo a contacgem do m3esmo a parti das virgulas,
# e verifica se o numero de amigos está entre 2 e 5
    amigos = linha[7:-1]

    print('amigos = "' + amigos + '"')

# contar vírgulas
    n_virgulas = 0
    for letra in amigos:
        if letra == ',':
            n_virgulas = n_virgulas + 1

    n_amigos = n_virgulas + 1

    if (n_amigos < 2) or (n_amigos > 5):
        print('Número de amigos = ' + str(n_amigos))
        print('O número de amigos é INVÁLIDO. Tem que estar entre 2 e 5.')
        print('A sua entrada no ranking vai ser REJEITADA.')

    return amigos


def le_identificacao():
# lê o ficheiro identificacao.txt do qual obtem a identificação do jogador
    global numero
    global amigos

    ficheiro = open('identificacao.txt', 'r')

    linha1 = ficheiro.readline()
    print(linha1)
    linha2 = ficheiro.readline()
    print(linha2)

    ficheiro.close()

    numero = get_numero(linha1)
    amigos = get_amigos(linha2)


def inicializa_semente(semente_a_usar):
# gera uma nova semente de jogo
    global semente
    if semente_a_usar == None:
        semente_a_usar = randint(1, 1000)
    seed(semente_a_usar)
    semente = semente_a_usar


def regista_grelha_inicial(g11, g12, g13, g14,
                           g21, g22, g23, g24,
                           g31, g32, g33, g34,
                           g41, g42, g43, g44):

    global grelha
    global jogadas
    global pontos

    grelha = [[g11, g12, g13, g14],
             [g21, g22, g23, g24],
             [g31, g32, g33, g34],
             [g41, g42, g43, g44]]

# inicialização das restantes variáveis globais
    jogadas = ''
    pontos = None


def regista_jogada(letra):
# adiciona uma nova jogada
    global jogadas

    jogadas = jogadas + letra


def regista_pontos(p):
# atualiza os pontos
    global pontos

    pontos = p


def regista_ranking():
# regista o ranking no url http://beleza2.ddns.net/api/submit_2048
    import urllib.request
    import json

    mensagem = None
    try:

        request_data = {'numero': numero, 'amigos': amigos,
                        'jogadas': jogadas, 'pontos': pontos,
                        'semente': semente}
        json_request_data = json.dumps(request_data)

        url = 'http://beleza2.ddns.net/api/submit_2048'

        req = urllib.request.Request(
            url = url,
            data = bytes(json_request_data.encode('utf-8')),
            method = 'POST')
        req.add_header('Content-type', 'application/json; charset=UTF-8')

        resp = urllib.request.urlopen(req)
        response_data = json.loads(resp.read().decode('utf-8'))
        resp.close()
        mensagem = response_data['mensagem_cloud']

    except Exception as err:
        mensagem = 'Não foi possível registar a pontuação no ranking.\n'
        mensagem = mensagem + str(err)

    return mensagem

def escreve_registo():
# exporta o registo para um fifcheiro em formato txt.
    nome_ficheiro = numero + '.' + str(pontos)

    ficheiro = open(nome_ficheiro, 'w')

    ficheiro.write('numero=' + numero + '\n')
    ficheiro.write('amigos=' + amigos + '\n')
    ficheiro.write('grelha_inicial=' + str(grelha) + '\n')
    ficheiro.write('jogadas=' + jogadas + '\n')
    ficheiro.write('pontos=' + str(pontos) + '\n')
    ficheiro.write('semente=' + str(semente) + '\n')
    
    ficheiro.close()

    mensagem_cloud = regista_ranking()

    return mensagem_cloud
