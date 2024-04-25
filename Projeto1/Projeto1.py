#LEIC-A FP 2022  1º Projeto
#Gonçalo Aleixo
#IST1106900

#Exercicio 1

#1.2.1
def limpa_texto(texto: str) -> str: 
    
    '''Esta funcao separa a string em um tuplo em que cada palavra eh um item do duplo, 
    e depois junta-os numa string com um espaço em cada palavra'''
    
    texto_partido = texto.split()
    return(' '.join(texto_partido))


#1.2.2
def corta_texto(texto: str, largura: int) -> str:
    
    '''Esta função recebe uma string e separa em duas partes, na largura e devolve duas 
    strings separadas por uma virgula, na posição da largura indicada, 
    (se n estiver no meio de uma palavra,
    a string é cortada no espaço mais próximo)'''
    
    texto_partido = texto.split()
    res = []    # primeira string, com tamanho n
    res2 = []   # segunda string, sem tamanho máximo (resto da string original)
    
    for palavra in texto_partido:
        if len(palavra) <= largura :
            res.append(palavra) 
            largura = largura -(len(palavra)+1)
        else:
            largura = largura -(len(palavra)+1)
            res2.append(palavra)
            
    return ' '.join(res), ' '.join(res2)


#1.2.3
def insere_espacos(texto: str, largura: int) -> str:
    
    '''Esta função recebe uma string, e vai palavra a palavra adicionar espaços
    até que a string tenha o tamanho da largura, e na ultima palavra não adiciona espaços ah frente
    para a string acabar sempre no final da palavra'''
    
    texto_cortado = texto.split()
    
    # numero de espaços que vão ser preciso de ser inseridos
    letras = len(texto)
    espacos = largura - letras      
    
    if len(texto_cortado) <= 1: 
        return (texto + ' '*espacos)  
    
    # loop de adicionar um espaco por palavra ate nao haver mais espaços para meter
    while espacos > 0:      
        for palavra in texto_cortado:
            if espacos == 0:
                break
            
            indice = texto_cortado.index(palavra)
            
            if not indice == len(texto_cortado)-1  :
                texto_cortado[indice] = palavra + ' '
                espacos -= 1
                
    return ' '.join(texto_cortado)  


#1.2.4   
def justifica_texto (texto: str, largura: int) -> tuple:
    
    '''Esta funcao usa as outras tres funcoes para retornar uma string em um tuple
    em que cada membrodo tuple tenha largura, com excessão do ultimo elemento do tuple
    que apenas vai ter um espaço por palavra sem ter que chegar a largura desejada'''
    
    # prever os diferentes erros
    if not isinstance(largura,int) or not isinstance(texto,str) or len(texto) == 0: 
        raise ValueError('justifica_texto: argumentos invalidos')
    
    texto_cortado = texto.split() 
    
    # este for preve o caso de o numero de caracteres da palavra for superior a largura possivel
    for x in texto_cortado: 
        if len(x) > largura: raise ValueError('justifica_texto: argumentos invalidos')
        
    texto_limpo = limpa_texto(texto)
    texto_partido = []
    
    # este loop vai dividindo a string em elementos de um tuplo
    while True:  
        parte1, parte2 = corta_texto(texto_limpo, largura)
        texto_partido.append(parte1)
        
        if len(parte2) > largura:
            texto_limpo = parte2
            
        else:
            if len(parte2) != 0:   
                texto_partido.append(parte2)
            break   
  
    texto_justificado = [] 
    
    # condição para que o ultimo elemento do tuple não seja preenchico com espaços até ah largura
    for palavra in texto_partido:   
        if texto_partido.index(palavra) == len(texto_partido)-1:
            texto_justificado.append(palavra + ' ' *(largura-len(palavra)))
            
        else:
            texto_justificado.append(insere_espacos(palavra,largura))
        
    return(tuple(texto_justificado))



#Exercicio 2

#2.2.1
def calcula_quocientes(votos: dict, deputados: int) -> dict:
    
    '''Esta função recebe um dicionario e os numeros de deputados e 
    vai devolver os quocientes de cada partido, calculado com o método de Hondt
    (não altera o dicionário inicial)
    '''
    
    if not isinstance(deputados, int):
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    for v in votos.values():
        if not isinstance(v, int) or v <= 0:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    copia = votos.copy()
    for key in copia.keys():
        copia[key] = []

    # calcula os quocientes de votação usando o método de Hondt
    for key, lista in copia.items(): 
        quociente = 1
        for i in range(deputados):
            lista.append(votos[key] / quociente)
            quociente += 1

    return copia


#2.2.2
def atribui_mandatos(votos: dict, deputados: int) -> list:
    
    '''Esta função recebe um dicionario com os votos num criculo, e o numero de deputados
    e vai retornar uma lista. Esta lista vai ter as letras correspondentes aos partidos
    que obtiveram mandatos, em ordem decrescente
    '''
    
    if not isinstance(deputados, int) or deputados <= 0:
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    quocientes = calcula_quocientes(votos, deputados)
    valores = {}

    # cria uma lista de partidos que terão mandatos
    for partido, qs in quocientes.items():  
        for q in qs:
            if q not in valores:
                valores[q] = []

            valores[q].append(partido)

    # ordenamos a lista com base nos quocientes
    ordenado = sorted(valores.items(), reverse=True)   
    resultado = []
    for v, partidos in ordenado:
        partidos_ordenados = []
        for p in partidos:
            partidos_ordenados.append((votos[p], p))

        partidos_ordenados = sorted(partidos_ordenados)

        for p in partidos_ordenados:
            resultado.append(p[1])

    return resultado[:deputados] 


#2.2.3
def obtem_partidos(info: dict) -> list:
    
    '''Esta função recebe um dicionário com os votos por partidos num circulo eleitoral
    e devolve uma lista com o nome dos partidos por ordem alfabética crescente
    (não altera o dicionario inicial)
    '''
    
    partidos = set()
    for circulo, dados in info.items():
        # valida se esse circulo possui os dados corretos
        if not isinstance(dados, dict):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

        if 'votos' not in dados or not isinstance(dados['votos'], dict) or not dados['votos']:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

        if 'deputados' not in dados:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

        for key in dados:
            if key not in ['deputados', 'votos']:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            
        if not isinstance(circulo,str):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

        # lista os partidos contidos em um dicionário de informações de votos
        for partido in dados['votos'].keys():  
            if not isinstance(partido, str):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")

            partidos.add(partido)  

    return sorted(partidos)


#2.2.4
def obtem_resultado_eleicoes(info: dict) -> list:
    
    '''Esta função usa as outras 3 funções principais, e usa o dicionario com
    a informação das eleições para criar uma lista. Cada elemento da lista eh
    um tuplo com três elementos: o partido, o numero de deputados, e os votos totais
    (lista em ordem crescente, tanto alfabeticamente se o numero de deputados for igual 
    em dois partidos, não altera o dicionario)
    '''
    
    if not info:
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    if not isinstance(info, dict):
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    

    resultados = {}
    for partido in obtem_partidos(info):
        # inicia o dicionário de resultados com valores iguais a zero
        resultados[partido] = {'deputados': 0, 'votos': 0}

    for dados in info.values():
        # calcula os mandatos e adiciona ao resultado
        mandatos = atribui_mandatos(dados['votos'], dados['deputados'])
        for m in mandatos:
            resultados[m]['deputados'] += 1

        # adiciona os votos dessa região ao total de votos do partido
        for partido, votos in dados['votos'].items():
            resultados[partido]['votos'] += votos

    # transforma o resultado em uma lista de tuplos
    resultado_final = []
    for partido, resultado in resultados.items():
        resultado_final.append((partido, resultado['deputados'], resultado['votos']))

    # ordena o resultado com base no número de votos
    ordenado = sorted(resultado_final, key=lambda i: i[2], reverse=True)
    return ordenado



#Exercicio 3

#3.2.1
def produto_interno(vetor1: tuple, vetor2: tuple):
    
    '''Esta função recebe dois tuplos (vetores) e 
    retorna o produto interno dos dois vetores
    '''
    
    # calcula o produto interno de dois vetores
    valores = []
    for x, y in zip(vetor1, vetor2):
        valores.append(float(x) * y)

    # soma todos os valores do vetor
    return sum(valores)


#3.2.2
def verifica_convergencia(A: tuple, c: tuple, x: tuple, precisao: float) -> bool:
    
    '''Esta função recebe uma matriz A, um vetor x, e o resultado c (constantes) (tudo em tuplos)
    A função retorna True se o erro absoluto for menor que a precisão, e false caso contrário
    '''
    
    # verifica se há convergência na solução x
    for linha in A:
        resultado = 0
        for i, n in enumerate(linha):
            resultado += n * x[i]

        # pega o valor de c usando o index atual da linha e valida com o resultado obtido em x
        erro = abs(resultado - c[A.index(linha)])
        if erro > precisao:
            return False

    return True


#3.2.3
def retira_zeros_diagonal(A: tuple, c: tuple) -> tuple:
    
    '''Esta função transforma a matriz introduzida, numa matriz reordenada de forma
    a que não existam zeros na diagonal, procurando linha a linha, e os valores de c 
    tambem sao reordenados na mesma sequência que a matriz A
    '''
    
    # reordena uma matriz de forma que não fiquem zeros em diagonal
    resultado = list(A)

    for i in range(len(resultado)):
        if resultado[i][i] == 0:
            for j in range(len(resultado)):
                if resultado[j][i] != 0 and resultado[i][j] != 0:
                    vi = resultado[i]
                    vj = resultado[j]
                    resultado[i] = vj
                    resultado[j] = vi
                    break

    novo_c = []
    for linha in resultado:
        novo_c.append(c[A.index(linha)])

    return tuple(resultado), tuple(novo_c)


#3.2.4
def eh_diagonal_dominante(A: tuple) -> tuple:
    
    '''Esta função recebe uma matriz quadrada formada por tuplos(linhas)
    e retorna True se for uma matriz diagonal dominante (para todas as 
    linhas da matriz, o módulo do valor da matriz na diagonal é maior 
    que a soma dos módulos de todos os demais valores (não-diagonais) daquela linha)
    '''
    
    if not isinstance(A, (list, tuple)) or not len(A):
        raise ValueError('resolve_sistema: argumentos invalidos')

    for linha in A:
        if not isinstance(linha, (list, tuple)):
            raise ValueError('resolve_sistema: argumentos invalidos')

        for numero in linha:
            if not isinstance(numero, (int, float)):
                raise ValueError('resolve_sistema: argumentos invalidos')

    formato = A[0]
    for linha in A:
        if len(linha) != len(formato):
            raise ValueError('resolve_sistema: argumentos invalidos')

    # verifica se uma matriz é diagonal dominante
    tamanho = len(A)
    for i in range(tamanho):
        soma = 0
        for j in range(tamanho):
            soma += abs(A[i][j])

        soma -= abs(A[i][i])
        if abs(A[i][i]) < soma:
            return False

    return True

#funcao auxiliar
def zeros(tamanho: tuple) -> list:
    
    # cria uma matriz, de tamanho definido, preenchida com zeros
    x = []
    for i in range(tamanho):
        x.append(0)

    return x

#3.2.5
def resolve_sistema(A: tuple, c: tuple, precisao: float) -> tuple:
    
    '''Esta função usa as outras 4 funções principais, (+1 auxiliar) e 
    recebe uma matriz A, um vetor x, e o resultado c (constantes).
    Vai retornar um tuplo que é solução do sistema aplicando o método de Jacobi
    (Inicialmente todas as variáveis do sistema     valem 0)
    '''

    if not isinstance(precisao, (float, int)) or precisao <= 0:
        raise ValueError('resolve_sistema: argumentos invalidos')

    if not isinstance(c, (list, tuple)) or len(A) == 0 or len(A[0]) != len(c):
        raise ValueError('resolve_sistema: argumentos invalidos')

    if len(A) != len(c):
        raise ValueError('resolve_sistema: argumentos invalidos')

    for n in c:
        if not isinstance(n, (float, int)):
            raise ValueError('resolve_sistema: argumentos invalidos')

    A, c = retira_zeros_diagonal(A, c)
    x = zeros(len(c))

    for i in range(1000000):
        novo_x = x.copy()

        for i in range(len(A)):
            s1 = produto_interno(A[i][:i], x[:i])
            s2 = produto_interno(A[i][i + 1:], x[i + 1:])
            novo_x[i] = (c[i] - s1 - s2) / A[i][i]
            if novo_x[i] == novo_x[i - 1]:
                break

        x = novo_x
        if verifica_convergencia(A, c, x, precisao):
            break

    # retorna o último valor com convergência
    return x











    
        

    
