#LEIC-A FP 2022  Projeto 2
#Goncalo Aleixo
#IST1106900


#Funcoes Auxiliares

caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def index_caractere(c: str) -> str:
    return caracteres.index(c)

def caractere_index(i: int) -> int:
    return caracteres[i]


#TAD Gerador
#O tad Gerador eh representado por um dicionario com duas chaves

#Operacoes Basicas

#Construtores
def cria_gerador(b, s):  
    
    '''
    cria_gerador : int x int -> gerador
    Recebe um inteiro b correspondente ao numero de bits
    do gerador e um inteiro positivo s correspondente a seed 
    ou estado inicial,e devolve o gerador (dict) correspondente
    '''
    
    if not isinstance(b, int) or not isinstance(s, int) or b not in (32, 64) or s <= 0 or s > 1000000000:
        raise ValueError('cria_gerador: argumentos invalidos')

    return {'b': b, 's': s}


def cria_copia_gerador(g):
    
    '''
    cria_copia_gerador : gerador -> gerador
    Recebe um gerador e devolve uma copia nova do gerador
    '''
    
    return cria_gerador(g['b'], g['s'])


#Seletor
def obtem_estado(g):
    
    '''
    obtem_estado: gerador -> int
    Devolve o estado atual do gerador g sem o alterar
    '''
    
    return g['s']


#Modificadores
def define_estado(g, s):
    
    '''
    define_estado: gerador x int -> int
    Define o novo valor do estado do gerador g como sendo s, e devolve s (int)
    '''
    
    g['s'] = s
    return s


def atualiza_estado(g):
    
    '''
    atualiza_estado: gerador -> int
    Atualiza o estado do gerador g de acordo com o algoritmo
    xorshift de geracao de numeros pseudoaleatorios, e devolve-o
    '''
    
    s = g['s']

    if g['b'] == 32:
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= (s >> 17) & 0xFFFFFFFF
        s ^= (s << 5) & 0xFFFFFFFF

    elif g['b'] == 64:
        s ^= (s << 13) & 0xFFFFFFFFFFFFFFFF
        s ^= (s >> 7) & 0xFFFFFFFFFFFFFFFF
        s ^= (s << 17) & 0xFFFFFFFFFFFFFFFF

    g['s'] = s
    return s


#Reconhecedor
def eh_gerador(g):
    
    '''
    eh_gerador : universal -> booleano
    Devolve True caso o seu argumento (universal) seja um TAD gerador e
    False caso contrario
    '''
    
    return isinstance(g, dict) and 's' in g and 'b' in g


#Teste
def geradores_iguais(g1, g2):
    
    '''
    geradores_iguais: gerador x gerador -> booleano
    Devolve True apenas se g1 e g2 sao geradores (dict) e sao iguais
    '''
    
    return eh_gerador(g1) and eh_gerador(g2) and g1['s'] == g2['s'] and g1['b'] == g2['b']


#Transformador
def gerador_para_str(g):
    
    '''
    gerador_para_str : gerador -> str
    Devolve a cadeia de carateres que representa o seu argumento
    '''
    
    return 'xorshift' + str(g['b']) + '(s=' + str(g['s']) + ')'


#Funcoes Alto Nivel
def gera_numero_aleatorio(g, n):
    
    '''
    gera_numero_aleatorio: gerador x int -> int
    Atualiza o estado do gerador g (dict) e devolve um numero
    aleatorio no intervalo [1, n] obtido a partir do novo estado s (int) de g 
    como 1 + resto da divisao inteira de g por n
    '''
    atualiza_estado(g)
    return 1 + (obtem_estado(g) % n)


def gera_carater_aleatorio(g, c):
    
    '''
    gera_carater_aleatorio: gerador x str -> str
    Atualiza o estado do gerador g e devolve um carateraleatorio no 
    intervalo entre A e o carater maiusculo c. Este e obtido a partir
    do novo estado s de g como o carater na posicao mod(s, l) da cadeia 
    de carateresde tamanho l formada por todos os carateres entre A e c
    '''
    
    n = gera_numero_aleatorio(g, caracteres.index(c) + 1)
    return caracteres[n - 1]


#TAD Coordenada
#O TAD Coordeanda eh representado por um dicionario com duas chaves

#Operacoes Basicas

#Construtor
def cria_coordenada(col, lin):
    
    '''
    cria_coordenada: str x int -> coordenada
    Recebe os valores correspondentes ah coluna col e
    linha lin e devolve a coordenada correspondente (dict)
    '''
    
    if not isinstance(col, str) or not isinstance(lin,
                                                  int) or lin > 99 or lin <= 0 or col not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        raise ValueError('cria_coordenada: argumentos invalidos')

    return {'col': col, 'lin': lin}


#Seletores
def obtem_coluna(c):
    
    '''
    obtem_coluna: coordenada -> str
    Devolve a coluna col da coordenada c
    '''
    
    return c['col']

def obtem_linha(c):
    
    '''
    obtem_linha: coordenada -> int
    Devolve a linha lin da coordenada c
    '''
    
    return c['lin']


#Reconhecedor
def eh_coordenada(c):
    
    '''
    eh_coordenada: universal -> booleano
    Devolve True caso o seu argumento (universal) seja um TAD 
    coordenada e False caso contrario
    '''
    
    return isinstance(c, dict) and 'lin' in c and 'col' in c


#Teste
def coordenadas_iguais(c1, c2):
    
    '''
    coordenadas_iguais: coordenada x coordenada -> booleano
    Devolve True apenas se c1 e c2 sao coordenadas e
    sao iguais.
    '''
    
    return eh_coordenada(c1) and eh_coordenada(c2) and c1['col'] == c2['col'] and c1['lin'] == c2['lin']


#Transformadores
def coordenada_para_str(c):
    
    '''
    coordenada_para_str : coordenada -> str
    Devolve a cadeia de carateres que representa o seu argumento
    '''
    
    return '{}{:02d}'.format(c['col'], c['lin'])


def str_para_coordenada(s):
    
    '''
    str_para_coordenada: str -> coordenada
    Devolve a coordenada reapresentada pelo seu argumento
    '''
    
    if not isinstance(s, str) or len(s) != 3:
        raise ValueError('str_para_coordenada: argumentos invalidos')

    try:
        return cria_coordenada(s[0], int(s[1:]))
    except ValueError:
        raise ValueError('str_para_coordenada: argumentos invalidos')


#Funcoes Alto Nivel
def obtem_coordenadas_vizinhas(c):
    
    '''
    obtem_coordenadas_vizinhas: coordenada -> tuplo
    Devolve um tuplo com as coordenadas vizinhas a
    coordenada c, comecando pela coordenada na diagonal 
    acima-esquerda de c e seguindo no sentido horario

    '''
    
    col_index = caracteres.index(obtem_coluna(c))
    modificadores = [
        (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)
    ]

    coordenadas = []
    for m in modificadores:
        col = col_index + m[1]
        lin = obtem_linha(c) + m[0]
        if col >= 0 and lin > 0 and col < len(caracteres) and col < 26 and lin < 100:
            cv = cria_coordenada(caracteres[col], lin)
            coordenadas.append(cv)

    return tuple(coordenadas)


def obtem_coordenada_aleatoria(c, g):
    
    '''
    obtem_coordenada_aleatoria: coordenada x gerador -> coordenada
    Recebe uma coordenada c e um TAD gerador g, e devolve uma 
    coordenada gerada aleatoriamente em que c define a maior 
    coluna e maior linha possiveis
    '''
    
    col = obtem_coluna(c)
    lin = obtem_linha(c)

    return cria_coordenada(gera_carater_aleatorio(g, col), gera_numero_aleatorio(g, lin))


#TAD Parcela
#O TAD Parcela eh representado por um dicionario 

#Operacoes Basicas

#Construtores
def cria_parcela():
    
    '''
    cria_parcela: {} -> parcela
    Devolve uma parcela tapada sem mina escondida
    '''
    
    return {'estado': 'tapada', 'minada': False}


def cria_copia_parcela(p):
    
    '''
    cria_copia_parcela: parcela -> parcela
    Recebe uma parcela p e devolve uma nova copia da parcela
    '''
    
    return p.copy()

#Modificadores
def limpa_parcela(p):
    
    '''
    limpa_parcela: parcela -> parcela
    Modifica destrutivamente a parcela p modificando o seu estado 
    para limpa, e devolve a propria parcela
    '''
    
    p['estado'] = 'limpa'
    return p


def marca_parcela(p):
    
    '''
    marca_parcela: parcela -> parcela
    Modifica destrutivamente a parcela p modificando o seu estado
    para marcada com uma bandeira, e devolve a propria parcela
    '''
    
    p['estado'] = 'marcada'
    return p


def desmarca_parcela(p):
    
    '''
    desmarca_parcela: parcela -> parcela
    Modifica destrutivamente a parcela p modificando o seu
    estado para tapada, e devolve a propria parcela
    '''
    
    p['estado'] = 'tapada'
    return p


def esconde_mina(p):
    
    '''
    esconde mina: parcela -> parcela
    Modifica destrutivamente a parcela p escondendo uma mina
    na parcela, e devolve a propria parcela.
    '''
    
    p['minada'] = True
    return p


#Reconhecedores
def eh_parcela(p):
    
    '''
    eh_parcela: universal -> booleano
    Devolve True caso o seu argumento seja um TAD parcela e
    False caso contrario
    '''
    
    return isinstance(p, dict) and 'estado' in p and 'minada' in p


def eh_parcela_tapada(p):
    
    '''
    eh_parcela_tapada: parcela -> booleano
    Devolve True caso a parcela p se encontre tapada e False
    caso contrario.
    '''
    
    return eh_parcela(p) and p['estado'] == 'tapada'


def eh_parcela_marcada(p):
    
    '''
    eh_parcela_marcada: parcela -> booleano
    Devolve True caso a parcela p se encontre marcada
    com uma bandeira e False caso contrario.

    '''
    
    return eh_parcela(p) and p['estado'] == 'marcada'


def eh_parcela_limpa(p):
    
    '''
    eh_parcela_limpa: parcela -> booleano
    Devolve True caso a parcela p se encontre limpa e False
    caso contrario
    '''
    
    return eh_parcela(p) and p['estado'] == 'limpa'


def eh_parcela_minada(p):
    
    '''
    eh_parcela_minada: parcela -> booleano
    Devolve True caso a parcela p esconda uma mina e
    False caso contrario 
    '''
    return eh_parcela(p) and p['minada']

#Teste
def parcelas_iguais(p1, p2):

    '''
    parcelas_iguais: parcela x parcela -> booleano
    Devolve True apenas se p1 e p2 sao parcelas e sao iguais.
    '''

    return eh_parcela(p1) and eh_parcela(p2) and p1['estado'] == p2['estado'] and p1['minada'] == p2['minada']


#transformadores
def parcela_para_str(p):

    '''
    parcela_para_str : parcela -> str
    Devolve a cadeia de caracteres que representa a parcela
    em funcao do seu estado: parcelas tapadas (#), parcelas marcadas (@),
    parcelas limpas sem mina (?) e parcelas limpas com mina (X).
    '''
    
    if p['estado'] == 'tapada':
        return '#'

    if p['estado'] == 'limpa':
        if p['minada']:
            return 'X'
        else:
            return '?'

    if p['estado'] == 'marcada':
        return '@'


#Funcoes Alto Nivel
def alterna_bandeira(p):
    
    '''
    alterna_bandeira: parcela -> booleano
    Recebe uma parcela p e modifica-a destrutivamente da seguinte
    forma: desmarca se estiver marcada e marca se estiver tapada, devolvendo True.
    Em qualquer outro caso, nao modifica a parcela e devolve False
    '''
    
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True

    return False



#TAD Campo
#O TAD Campo eh representado por um dicionario 

#Operacoes Basicas

#Construtor
def cria_campo(c, l):

    '''
    cria_campo: str x int -> campo
    Recebe uma cadeia de carateres e um inteiro correspondentes
    ah ultima coluna e ah ultima linha de um campo de minas, 
    e devolve o campo do tamanho pretendido formado por parcelas tapadas sem minas
    '''

    if not isinstance(c, str) or not isinstance(l, int) or c not in caracteres or l > 99 or l <= 0:
        raise ValueError('cria_campo: argumentos invalidos')

    matriz = []
    for lin in range(l):
        linha = []
        for col in range(index_caractere(c) + 1):
            linha.append(cria_parcela())

        matriz.append(linha)

    return matriz


def cria_copia_campo(m):

    '''
    cria_copia_campo: campo -> campo
    Recebe um campo e devolve uma nova copia do campo. 
    '''
    copia_campo = []
    for elemento in range(len(m)):
        m[elemento] = m[elemento].copy()                        #Troquei aqui
    return copia_campo


#Seletores
def obtem_ultima_coluna(m):

    '''
    obtem_ultima_coluna: campo -> str
    Devolve a cadeia de caracteres que corresponde ah
    ultima coluna do campo de minas.
    '''

    return caractere_index(len(m[0]) - 1)


def obtem_ultima_linha(m):
    
    '''
    obtem_ultima_linha: campo -> int
    Devolve o valor inteiro que corresponde ah ultima linha
    do campo de minas.
    '''

    return len(m)


def obtem_parcela(m, c):
    
    '''
    obtem_parcela: campo x coordenada -> parcela
    Devolve a parcela do campo m que se encontra na coordenada c.
    '''
    
    col = index_caractere(obtem_coluna(c))
    lin = obtem_linha(c) - 1
    return m[lin][col]


def obtem_coordenadas(m, s):

    '''
    obtem_coordenadas: campo x str -> tuplo
    Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente de 
    esquerda a direita e de cima a baixo das parcelasdependendo do valor 
    de s: 'limpas' para as parcelas limpas, 'tapadas' para as parcelas tapadas,
    'marcadas' para as parcelas marcadas, e minadas para as parcelas que escondem minas.
    '''

    coordenadas = []
    for l, lin in enumerate(m):
        for c, col in enumerate(lin):
            coord = cria_coordenada(caractere_index(c), l + 1)
            p = obtem_parcela(m, coord)

            if (s == 'tapada' or s == 'tapadas') and eh_parcela_tapada(p):
                coordenadas.append(coord)

            if (s == 'limpa' or s == 'limpas') and eh_parcela_limpa(p):
                coordenadas.append(coord)

            if (s == 'marcada' or s == 'marcadas') and eh_parcela_marcada(p):
                coordenadas.append(coord)

            if (s == 'minada' or s == 'minadas') and eh_parcela_minada(p):
                coordenadas.append(coord)

    return tuple(coordenadas)

#Reconhecedor
def eh_coordenada_do_campo(m, c):
    
    '''
    eh_coordenada_do_campo: campo x coordenada -> booleano
    Devolve True se c eh uma coordenada valida dentro do campo m. 
    '''

    if index_caractere(obtem_coluna(c)) > index_caractere(obtem_ultima_coluna(m)):
        return False

    if obtem_linha(c) > obtem_ultima_linha(m):
        return False

    return True

#Seletor
def obtem_numero_minas_vizinhas(m, c):
    
    '''
    obtem_numero_minas_vizinhas: campo x coordenada -> int
    Devolve o numero de parcelas vizinhas
    da parcela na coordenada c que escondem uma mina
    '''
    
    total = 0
    for cv in obtem_coordenadas_vizinhas(c):
        if not eh_coordenada_do_campo(m, cv):
            continue

        p = obtem_parcela(m, cv)
        if eh_parcela_minada(p):
            total += 1

    return total

#Reconhecedor
def eh_campo(m):

    '''
    eh_campo: universal -> booleano
    Devolve True caso o seu argumento seja um TAD campo e
    False caso contrario
    '''

    return isinstance(m, list) and len(m) > 0 and isinstance(m[0], list) and eh_parcela(m[0][0])


#Teste
def campos_iguais(m1, m2):

    '''
    campos_iguais: campo x campo -> booleano
    Devolve True apenas se m1 e m2 forem campos e forem iguais
    '''

    return eh_campo(m1) and eh_campo(m2) and m1 == m2


#Transformador
def campo_para_str(m):

    '''
    campo_para_str : campo -> str
    Devolve uma cadeia de caracteres que representa o campo de minas
    '''
    
    campo = []

    caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    primeira_coluna = caracteres[:caracteres.index(obtem_ultima_coluna(m)) + 1]
    campo.append('   ' + primeira_coluna)

    tracos = '-' * len(primeira_coluna)
    campo.append('  +' + tracos + '+')

    for i, lin in enumerate(m):
        colunas = ''
        for j, p in enumerate(lin):
            if eh_parcela_limpa(p) and not eh_parcela_minada(p):
                c = cria_coordenada(caractere_index(j), i + 1)
                colunas += str(obtem_numero_minas_vizinhas(m, c)).replace('0', ' ')
            else:
                colunas += parcela_para_str(p)

        campo.append('{:02d}|{}|'.format(i + 1, colunas))
        i += 1

    campo.append('  +' + tracos + '+')
    return '\n'.join(campo)


#Funcoes Alto Nivel
def coloca_minas(m, c, g, n):

    '''
    coloca_minas: campo x coordenada x gerador x int -> campo
    Modifica destrutivamente o campo m escondendo n minas em parcelas dentro do campo. 
    As n coordenadas sao geradas em sequencia utilizando o gerador g, de modo a que 
    nao coincidam com a coordenada c nem com nenhuma parcela vizinha desta, n
    em se sobreponham com minas colocadas anteriormente.
    '''

    minadas = 0

    proibidas = []
    if c is not None:
        proibidas += list(obtem_coordenadas_vizinhas(c))
        proibidas.append(c)

    while minadas < n:
        col = gera_carater_aleatorio(g, obtem_ultima_coluna(m))
        lin = gera_numero_aleatorio(g, obtem_ultima_linha(m))

        cg = cria_coordenada(col, lin)
        if not eh_coordenada_do_campo(m, cg):
            continue

        proibida = False
        for cp in proibidas:
            if coordenadas_iguais(cg, cp):
                proibida = True

        if proibida:
            continue

        p = obtem_parcela(m, cg)
        if eh_parcela_minada(p):
            continue

        esconde_mina(p)
        minadas += 1

    return m


def limpa_campo(m, c):

    '''
    limpa_campo: campo x coordenada -> campo
    Modifica destrutivamente o campo limpando a parcela na coordenada c, devolvendo-o. 
    Se nao houver nenhuma mina vizinha escondida, limpa iterativamente todas as parcelas 
    vizinhas tapadas. 
    '''
    p = obtem_parcela(m, c)
    if eh_parcela_limpa(p):
        return m

    limpa_parcela(p)
    if eh_parcela_minada(obtem_parcela(m, c)) or obtem_numero_minas_vizinhas(m, c) > 0:
        return m

    for cv in obtem_coordenadas_vizinhas(c):
        if eh_coordenada_do_campo(m, cv):
            pv = obtem_parcela(m, cv)
            if not eh_parcela_minada(pv) and eh_parcela_tapada(pv):
                limpa_campo(m, cv)

    return m


#Funcoes Auxiliares/Adicionais

def mostrar_campo(m, n):

    '''
    mostrar_campo : campo x int -> str
    Eh uma funcao basica que calcula o numero de bandeiras colocadas, formata e faz o print do campo.
    '''

    bandeiras = obtem_coordenadas(m, 'marcada')
    print('   [Bandeiras ' + str(len(bandeiras)) + '/' + str(n) + ']')
    print(campo_para_str(m))


def jogo_ganho(m):

    '''
    jogo_ganho : campo -> booleano
    Eh uma funcao auxiliar que recebe um campo do jogo das minas e devolve
    True se todas as parcelas sem minas se encontram limpas, ou False caso contrario
    '''

    if not eh_campo(m):
        raise ValueError('turno_jogador: argumentos invalidos')

    if len(obtem_coordenadas(m,'minadas')) == len(obtem_coordenadas(m,'tapadas')) + len(obtem_coordenadas(m,'marcadas')):
        return True
    #for c in obtem_coordenadas(m, 'tapada'):
    #    p = obtem_parcela(m, c)
     #   if not eh_parcela_minada(p):                                                                                                       #troquei aqui
      #      return False

    return False


def escolher_coordenada(m):

    '''
    escolher_coordenada : campo -> coordenada
    Esta funcao pede uma coordenada pelo input(), e valida se eh uma coordenada valida.
    '''
    
    while True:
        coord = input('Escolha uma coordenada:').upper()

        try:
            c = str_para_coordenada(coord)
        except ValueError:
            continue

        if not eh_coordenada_do_campo(m, c):
            continue

        return c


def turno_jogador(m, inicio=False):

    '''
    turno_jogador: campo -> booleano
    Eh uma funcao auxiliar que recebe um campo de minas e oferece ao jogador a opcao de 
    escolher uma acao e uma coordenada. A funcao modifica destrutivamente
    o campo de acordo com acao escolhida, devolvendo False caso o jogador tenha limpo
    uma parcela que continha uma mina, ou True caso contrario. 
    '''
    
    if not eh_campo(m):
        raise ValueError('turno_jogador: argumentos invalidos')

    while True:
        if not inicio:
            acao = input('Escolha uma ação, [L]impar ou [M]arcar:').upper()
        else:
            acao = 'L'

        if acao == 'L' or acao == 'M':
            c = escolher_coordenada(m)
            p = obtem_parcela(m, c)

            if acao == 'L':
                limpa_campo(m, c)
                return not eh_parcela_minada(p)
            elif acao == 'M':
                alterna_bandeira(p)
                return True

            break


def minas(c, l, n, d, s):

    '''
    minas: str x int x int x int x int -> booleano
    Eh a funcao principal que permite jogar ao jogo das minas. A funcao
    recebe uma cadeia de carateres e 4 valores inteiros correspondentes, respetivamente, a:
    ultima coluna c; ultima linha l; numero de parcelas com minas n; dimensao do gerador
    de numeros d; e estado inicial ou seed s para a geracao de numeros aleatorios
    '''

    for i in [l, n, d, s]:
        if not isinstance(i, int):
            raise ValueError('minas: argumentos invalidos')

    if not isinstance(c, str) or c not in caracteres or l > 99 or n <= 1 or n > (l * index_caractere(c)) or \
            d not in [32, 64] or s < 1:
        raise ValueError('minas: argumentos invalidos')

    m = cria_campo(c, l)
    g = cria_gerador(d, s)

    # primeiro turno
    mostrar_campo(m, n)
    c = escolher_coordenada(m)
    coloca_minas(m, c, g, n)
    limpa_campo(m, c)

    while True:
        mostrar_campo(m, n)

        if jogo_ganho(m):
            print('VITORIA!!!')
            return True

        if not turno_jogador(m):
            mostrar_campo(m, n)
            print('BOOOOOOOM!!!')
            return False
        

