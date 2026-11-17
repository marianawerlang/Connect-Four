
# Trabalho Avaliativo - Jogo Connect Four (Quatro em Linha)
# Alunas:
# - Mariana Werlang Moraes - Matrícula 25204855




# Como extra, implementamos uma lógica adicional para o Computador (Modo Difícil),
# onde ele simula jogadas para tentar vencer ou bloquear o jogador humano.

# Todos os requisitos do jogo foram implementados com sucesso. A lógica
# de gravidade funciona corretamente, bem como a validação de colunas cheias
# e a verificação de vitória (horizontal, vertical e diagonais) ou empate.
# Não houve aspectos que deixaram de funcionar.



import random

# Constantes para evitar números "mágicos" soltos no código e facilitar a leitura
LINHAS = 6
COLUNAS = 7
VAZIO = '.'
JOGADOR_1 = 'X'
JOGADOR_2 = 'O'

def criar_tabuleiro():
    # Raciocínio: Uma lista de listas (matriz) é a melhor forma de representar 
    # um tabuleiro 2D bidimensional na programação estruturada em Python.
    tabuleiro = []
    for _ in range(LINHAS):
        linha = [VAZIO] * COLUNAS
        tabuleiro.append(linha)
    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    # Raciocínio: Exibir o tabuleiro de forma amigável no terminal.
    # O cabeçalho numérico ajuda o jogador humano a saber qual número digitar.
    print() 
    cabecalho = " ".join([str(i) for i in range(COLUNAS)])
    print(cabecalho)
    for linha in tabuleiro:
        print(" ".join(linha))
    print()

def coluna_valida(tabuleiro, col):
    # Raciocínio: Como as peças caem (gravidade), a última posição a ser preenchida
    # em uma coluna é sempre a linha 0 (o topo). Se a linha 0 estiver vazia, a coluna tem espaço.
    return tabuleiro[0][col] == VAZIO

def obter_linha_disponivel(tabuleiro, col):
    # Raciocínio: Para simular a gravidade, precisamos verificar a coluna de baixo para cima.
    # Por isso o 'for' começa na última linha (LINHAS - 1) e vai diminuindo até a linha 0.
    for r in range(LINHAS - 1, -1, -1):
        if tabuleiro[r][col] == VAZIO:
            return r
    return -1

def inserir_peca(tabuleiro, linha, col, peca):
    # Raciocínio: Apenas atualiza a matriz do tabuleiro na posição (linha, coluna)
    # com a peça do jogador da vez ('X' ou 'O').
    tabuleiro[linha][col] = peca

def verificar_vitoria(tabuleiro, peca):
    # Raciocínio: Precisamos checar todas as direções possíveis. 
    # Em vez de olhar o tabuleiro todo para cada direção, limitamos os laços 'for' 
    # (ex: COLUNAS - 3) para evitar erros de "Index Out of Range" ao buscar 4 posições à frente.
    
    # 1. Horizontal
    for c in range(COLUNAS - 3):
        for r in range(LINHAS):
            if tabuleiro[r][c] == peca and tabuleiro[r][c+1] == peca and \
               tabuleiro[r][c+2] == peca and tabuleiro[r][c+3] == peca:
                return True

    # 2. Vertical
    for c in range(COLUNAS):
        for r in range(LINHAS - 3):
            if tabuleiro[r][c] == peca and tabuleiro[r+1][c] == peca and \
               tabuleiro[r+2][c] == peca and tabuleiro[r+3][c] == peca:
                return True

    # 3. Diagonal Positiva (\)
    for c in range(COLUNAS - 3):
        for r in range(LINHAS - 3):
            if tabuleiro[r][c] == peca and tabuleiro[r+1][c+1] == peca and \
               tabuleiro[r+2][c+2] == peca and tabuleiro[r+3][c+3] == peca:
                return True

    # 4. Diagonal Negativa (/)
    for c in range(COLUNAS - 3):
        for r in range(3, LINHAS):
            if tabuleiro[r][c] == peca and tabuleiro[r-1][c+1] == peca and \
               tabuleiro[r-2][c+2] == peca and tabuleiro[r-3][c+3] == peca:
                return True

    return False

def tabuleiro_cheio(tabuleiro):
    # Raciocínio: O jogo empata se ninguém vencer e não houver mais espaços.
    # Novamente, basta verificar se o topo (linha 0) de todas as colunas está ocupado.
    for c in range(COLUNAS):
        if tabuleiro[0][c] == VAZIO:
            return False
    return True

# FUNÇÕES EXTRAS PARA A INTELIGÊNCIA DO COMPUTADOR (MODO DIFÍCIL) 

def simular_jogada_vitoria(tabuleiro, col, peca):
    # Raciocínio: Esta função permite que o computador "pense" no futuro.
    # Ele coloca a peça temporariamente em uma coluna, verifica se essa jogada 
    # resulta em vitória e, logo em seguida, apaga a peça (desfaz a jogada).
    linha = obter_linha_disponivel(tabuleiro, col)
    inserir_peca(tabuleiro, linha, col, peca)
    venceu = verificar_vitoria(tabuleiro, peca)
    inserir_peca(tabuleiro, linha, col, VAZIO) # Desfaz a jogada para não afetar o jogo real
    return venceu

def jogada_inteligente(tabuleiro, peca_pc, peca_humano):
    # Raciocínio da Inteligência: É uma árvore de decisão de 3 passos:
    # 1º - Ataque: Simula jogar em todas as colunas para ver se ganha o jogo agora. Se sim, joga lá.
    # 2º - Defesa: Se não pode ganhar agora, simula as jogadas do Humano. Se o humano for ganhar na próxima, bloqueia a jogada.
    # 3º - Estratégia/Aleatório: Se não há ataque ou defesa urgente, tenta jogar no meio (onde há mais chances de criar diagonais) ou joga aleatoriamente.
    colunas_validas = [c for c in range(COLUNAS) if coluna_valida(tabuleiro, c)]

    # Passo 1: Ataque
    for col in colunas_validas:
        if simular_jogada_vitoria(tabuleiro, col, peca_pc):
            return col

    # Passo 2: Defesa
    for col in colunas_validas:
        if simular_jogada_vitoria(tabuleiro, col, peca_humano):
            return col

    # Passo 3: Padrão (Prioriza o centro ou escolhe aleatório)
    coluna_central = COLUNAS // 2
    if coluna_central in colunas_validas:
        if random.random() < 0.6: 
            return coluna_central

    return random.choice(colunas_validas)


def main():
    # Raciocínio: Função principal para organizar o fluxo do jogo, inicializar variáveis
    # e gerenciar o loop (while) de turnos.
    print("--- CONNECT FOUR (LIG 4) ---")
    print("Escolha o modo de jogo:")
    print("1 - Humano x Humano")
    print("2 - Humano x Computador (Fácil - Aleatório)")
    print("3 - Humano x Computador (Difícil - Inteligente)")
    
    modo = ""
    while modo not in ['1', '2', '3']:
        modo = input("Digite 1, 2 ou 3: ")

    jogar_contra_computador_facil = (modo == '2')
    jogar_contra_computador_dificil = (modo == '3')
    
    tabuleiro = criar_tabuleiro()
    jogo_ativo = True
    turno = 0 # Usamos 0 para X e 1 para O. Ajuda a alternar os jogadores usando modulação (%).

    imprimir_tabuleiro(tabuleiro)

    while jogo_ativo:
        # Define qual é o jogador da vez
        if turno == 0:
            peca = JOGADOR_1
            nome_jogador = "Jogador 1 (X)"
        else:
            peca = JOGADOR_2
            if jogar_contra_computador_facil or jogar_contra_computador_dificil:
                nome_jogador = "Computador (O)"
            else:
                nome_jogador = "Jogador 2 (O)"

        # Coleta a jogada do Computador (turno 1)
        if turno == 1 and (jogar_contra_computador_facil or jogar_contra_computador_dificil):
            if jogar_contra_computador_dificil:
                col = jogada_inteligente(tabuleiro, JOGADOR_2, JOGADOR_1)
            else:
                # O computador fácil escolhe apenas entre colunas que não estão cheias
                colunas_validas = [c for c in range(COLUNAS) if coluna_valida(tabuleiro, c)]
                col = random.choice(colunas_validas)
            
            print(f"\nO {nome_jogador} escolheu a coluna {col}.")
        else:
            # Coleta a jogada do Humano com tratamento de erros (try/except)
            try:
                col = int(input(f"\n{nome_jogador}, escolha a coluna (0-6): "))
                if col < 0 or col > 6:
                    print("Erro: Coluna inválida. Digite um número entre 0 e 6.")
                    continue
                if not coluna_valida(tabuleiro, col):
                    print("Erro: Coluna cheia! Por favor, escolha outra coluna.")
                    continue
            except ValueError:
                print("Erro: Entrada inválida. Digite um número inteiro.")
                continue

        # Insere a peça usando a lógica de gravidade e exibe
        linha = obter_linha_disponivel(tabuleiro, col)
        inserir_peca(tabuleiro, linha, col, peca)
        imprimir_tabuleiro(tabuleiro)

        # Checa se o jogo acabou nesta jogada (Vitória ou Empate)
        if verificar_vitoria(tabuleiro, peca):
            print(f"Vitória! O {nome_jogador} venceu a partida!")
            jogo_ativo = False
        elif tabuleiro_cheio(tabuleiro):
            print("Empate! O tabuleiro encheu e nenhum jogador venceu.")
            jogo_ativo = False

        # Alterna o turno (0 vira 1, 1 vira 0)
        turno = (turno + 1) % 2

if __name__ == "__main__":
    main()