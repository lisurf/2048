
from random import random
from random import choice

def get_posicoes_vazias(grelha):
#leitura de toda a grelha para obter as posições vazias
    posicoes_vazias = []

    for indice_linha in range(4):
        for indice_coluna in range(4):
            if grelha[indice_linha][indice_coluna] == 0:
                posicao_vazia = (indice_linha, indice_coluna)
                posicoes_vazias.append(posicao_vazia)
    
    return posicoes_vazias


def get_posicao_vazia(grelha):
# escolha de uma das posições vazias
# posicoes_vazias é uma lista de posições vazias

    posicoes_vazias = get_posicoes_vazias(grelha)
    posicao_vazia   = choice(posicoes_vazias)
    return posicao_vazia


def get_2ou4():
# probabilidade de calhar um 2 ou um 4 após cada jogada e no inicio do jogo
    x = random()
    if x > 0.1:
        return 2
    else:
        return 4


def inserir_2ou4(grelha):
# inserção de um 2 ou de um 4 segundo a def get_2ou4, após cada jogada e no inicio do jogo
    dois_ou_quatro = get_2ou4()
    posicoes_vazias = get_posicoes_vazias(grelha)
    posicao_vazia = choice(posicoes_vazias)
    # índices da posição vazia
    indice_linha = posicao_vazia[0]
    indice_coluna = posicao_vazia[1]
    
    grelha[indice_linha][indice_coluna] = dois_ou_quatro
    

def novo_jogo():
# cria um novo jogo com a inserção de 2 números segundo a função inserir_2ou4
    grelha  = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    fim     = False
    vitoria = False
    pontos  = 0
    
    inserir_2ou4(grelha)
    inserir_2ou4(grelha)

    jogo = (grelha, fim, vitoria, pontos)

    return jogo


def mover_esquerda(uma_lista):
# mover todos os valores para a esquerda, mantendo a ordem em que se encontram  
# exemplo : [0, 4, 0, 2] -> [4, 2] -> [4, 2, 0, 0]
    resultado = []

    for indice in range(len(uma_lista)):
        if uma_lista[indice] != 0:
            resultado.append(uma_lista[indice])
                  
    while len(resultado) != len(uma_lista):
        resultado.append(0)

    return resultado


def somar_esquerda(uma_lista):
#se um certo número x, tiver à sua esquerda o mesmo número x, estes são somados, ocupando o indice_linha mais à esquerda

    resultado = []
    
    indice = 0
    pontos = 0

    while indice < len(uma_lista)-1:
        if uma_lista[indice] == uma_lista[indice+1]:
            soma = uma_lista[indice] + uma_lista[indice+1]   # 2 * uma_lista[indice]
            resultado.append(soma)
            indice = indice + 2
            pontos = pontos + soma
        else:
            resultado.append(uma_lista[indice])
            indice = indice +1
# para que o último elemento da lista uma_lista seja processado
    if indice == len(uma_lista)-1:
        resultado.append(uma_lista[indice])

    while len(resultado) != len(uma_lista):
                resultado.append(0)

    return (resultado, pontos)


def atualizar_grelha(grelha_inicial, grelha):
# atualiza a grelha, incluindo novamente a inserção de um 2 ou um 4
    inserir = False
    for il in range(len(grelha)):
        for ic in range(len(grelha[il])):
            if (grelha_inicial[il][ic]) !=(grelha[il][ic]):
                inserir = True

    if inserir == True:
        inserir_2ou4(grelha)


def get_vitoria(grelha):
# considera vitoria quando o jogador atinge 2048 numa das celulas da grelha
    vitoria = False
    for il in range(len(grelha)):
        for ic in range(len(grelha[il])):
            if grelha[il][ic] == 2048:   # >= caso se pretenda que o jogo continue para alem do valor de 2048 
                vitoria = True
    return vitoria


def ha_iguais_adjacentes(grelha):
# verifica se os valores adjacentes nas linhas e nas colunas são iguais
    # por linhas
    ha = False
    for il in range(len(grelha)):
        for ic in range(len(grelha[il]) - 1):
            if (grelha[il][ic] != 0) and (grelha[il][ic] == grelha[il][ic + 1]):
                ha = True
    # por colunas
    for il in range(len(grelha) - 1):
        for ic in range(len(grelha[il])):
            if (grelha[il][ic] !=0) and (grelha[il][ic] == grelha[il + 1][ic]):
                ha = True

    return ha


def get_fim(grelha):
# quando deixarem de existir espaços vazios e não for possível realizar somas, o jogo termina
    fim = False

    posicoes_vazias = get_posicoes_vazias(grelha)
    if (len(posicoes_vazias) == 0) and not ha_iguais_adjacentes(grelha):
        fim = True

    return fim


def esquerda(jogo):
# uma jogada para a esquerda implica: um movimento (neste caso esquerda), uma soma (caso exista), atualiza a grelha,
# confirma se o jogador obteve vitoria, e returna o jogo atualizado com inserção de um 2 ou um 4
    (grelha, fim, vitoria, pontos) = jogo

    grelha_atualizada = []
    for linha in grelha:
        linha1 = mover_esquerda(linha)
        (linha2, pontos_a_somar) = somar_esquerda(linha1)
        grelha_atualizada.append(linha2)
        pontos = pontos + pontos_a_somar

    atualizar_grelha(grelha, grelha_atualizada)

    if vitoria == False:
        vitoria = get_vitoria(grelha_atualizada)

    fim = get_fim(grelha_atualizada)
    
    jogo_atualizado = (grelha_atualizada, fim, vitoria, pontos)

    return jogo_atualizado


def reverter_linha(linha):
# recebe uma linha e retorna a mesma com as posições revertidas
    linha_revertida = []

    for i in range(len(linha)):
        linha_revertida.append(linha[len(linha) - i - 1])

    return linha_revertida


reverter_linha = reverter_linha


def reverte_linhas(grelha):
# recebe a grelha, e reverte cada uma das linhas
    grelha_revertida = []

    for linha in grelha:
        linha_revertida = reverter_linha(linha)
        grelha_revertida.append(linha_revertida)

    return grelha_revertida


def get_coluna(matriz, indice_coluna):
# retorna uma coluna da matriz com um dado indice
    coluna = []

    for l in range(len(matriz)):
        coluna.append(matriz[l][indice_coluna])

    return coluna
	

def trocar_linhas_com_colunas(matriz):
# (transposição de uma matriz) para que o codigo da função esquerda possa ser reutilizado nas restantes direções
    resultado          = []
    n_linhas_resultado = len(matriz[0])
    
    for il in range(n_linhas_resultado):
        resultado.append(get_coluna(matriz, il))

    return resultado


def print_matriz(matriz):
# imprime a matriz  
    for linha in matriz:
        print(linha)


    print_matriz(grelha)
    

def direita(jogo):
# uma jogada para a direita implica: reverter as linhas da grelha, jogar para a esquerda e volta a reverter as linhas,
# equilvalente a jogar para a direita, uma soma (caso exista), atualiza a grelha,
# confirma se o jogador obteve vitoria, e returna o jogo atualizado com inserção de um 2 ou um 4
    (grelha, fim, vitoria, pontos) = jogo
    grelha_revertida = reverte_linhas(grelha)
    jogo_revertido = (grelha_revertida, fim, vitoria, pontos)
    jogo_revertido_atualizado = esquerda(jogo_revertido)
    (grelha, fim, vitoria, pontos) = jogo_revertido_atualizado
    grelha_revertida = reverte_linhas(grelha)
    jogo_atualizado = (grelha_revertida, fim, vitoria, pontos)

    return jogo_atualizado


def acima(jogo):
# uma jogada para cima implica: transpor as linhas da grelha, jogar para a esquerda e volta a transpor as linhas,
# equilvalente a jogar para cima, uma soma (caso exista), atualiza a grelha,
# confirma se o jogador obteve vitoria, e returna o jogo atualizado com inserção de um 2 ou um 4    
    (grelha, fim, vitoria, pontos) = jogo
    grelha_transposta = trocar_linhas_com_colunas(grelha)
    jogo_transposto = (grelha_transposta, fim, vitoria, pontos)
    jogo_transposto_atualizado = esquerda(jogo_transposto)
    (grelha, fim, vitoria, pontos) = jogo_transposto_atualizado
    grelha_transposta = trocar_linhas_com_colunas(grelha)
    jogo_atualizado = (grelha_transposta, fim, vitoria, pontos)

    return jogo_atualizado


def abaixo(jogo):
# uma jogada para baixo implica: transpor as linhas da grelha, jogar para a direita e volta a transpor as linhas,
# equilvalente a jogar para baixo, uma soma (caso exista), atualiza a grelha,
# confirma se o jogador obteve vitoria, e returna o jogo atualizado com inserção de um 2 ou um 4    
    (grelha, fim, vitoria, pontos) = jogo
    grelha_transposta = trocar_linhas_com_colunas(grelha)
    jogo_transposto = (grelha_transposta, fim, vitoria, pontos)
    jogo_transposto_atualizado = direita(jogo_transposto)
    (grelha, fim, vitoria, pontos) = jogo_transposto_atualizado
    grelha_transposta = trocar_linhas_com_colunas(grelha)
    jogo_atualizado = (grelha_transposta, fim, vitoria, pontos)

    return jogo_atualizado


def valor (jogo, linha, coluna):
# retorna o valor de uma certa posição da grelha
    grelha = jogo[0]

    v = grelha[linha - 1][coluna - 1]
    # a contagem começa no 0, -1+1=0
    return v


def terminou(jogo):
# returna o elemento fim da estrutura jogo
    return jogo[1]


def ganhou_ou_perdeu(jogo):
# returna o elemento ganhou_pu_perdeu da estrutura jogo    
    return jogo[2]


def pontuacao(jogo):
# returna o elemento pontuacao da estrutura jogo
    return jogo[3]
