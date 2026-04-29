import pygame
import sys

# Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 600, 600  # Voltamos ao tamanho original para um visual mais limpo
LINHA_LARGURA = 15
COR_FUNDO = (28, 170, 156)
COR_LINHA = (23, 145, 135)
COR_CIRCULO = (239, 231, 200)
COR_X = (84, 84, 84)
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (30, 30, 30)
COR_BOTAO_HOVER = (50, 50, 50)

# Fontes
FONTE_MSG = pygame.font.SysFont("Arial", 32, bold=True)
FONTE_BOTAO = pygame.font.SysFont("Arial", 24, bold=True)

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha')

# Tabuleiro interno
tabuleiro = [
    [0, 0, 0], 
    [0, 0, 0], 
    [0, 0, 0]
]

# tabuleiro = [[0] * 3 for _ in range(3)] => DA PRA FAZER DESSE JEITO TBM

# Definição do Botão (Centralizado, abaixo da mensagem de fim de jogo)
rect_botao = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 20, 200, 50)

def desenhar_linhas():
    tela.fill(COR_FUNDO)
    # Horizontais
    pygame.draw.line(tela, COR_LINHA, (0, 200), (600, 200), LINHA_LARGURA)
    pygame.draw.line(tela, COR_LINHA, (0, 400), (600, 400), LINHA_LARGURA)
    # Verticais
    pygame.draw.line(tela, COR_LINHA, (200, 0), (200, 600), LINHA_LARGURA)
    pygame.draw.line(tela, COR_LINHA, (400, 0), (400, 600), LINHA_LARGURA)

def desenhar_figuras():
    for linha in range(3):
        for col in range(3):
            centro_x = int(col * 200 + 100)
            centro_y = int(linha * 200 + 100)
            
            if tabuleiro[linha][col] == 1:
                pygame.draw.circle(tela, COR_CIRCULO, (centro_x, centro_y), 60, LINHA_LARGURA)
            elif tabuleiro[linha][col] == 2:
                offset = 55
                pygame.draw.line(tela, COR_X, (centro_x - offset, centro_y + offset), (centro_x + offset, centro_y - offset), LINHA_LARGURA)
                pygame.draw.line(tela, COR_X, (centro_x - offset, centro_y - offset), (centro_x + offset, centro_y + offset), LINHA_LARGURA)

def marcar_quadrado(linha, col, jogador):
    tabuleiro[linha][col] = jogador

def quadrado_disponivel(linha, col):
    return tabuleiro[linha][col] == 0

def tabuleiro_cheio():
    for linha in range(3):
        for col in range(3):
            if tabuleiro[linha][col] == 0:
                return False
    return True

def verificar_vitoria(jogador):
    for i in range(3):
        if tabuleiro[i][0] == jogador and tabuleiro[i][1] == jogador and tabuleiro[i][2] == jogador:
            return True
        if tabuleiro[0][i] == jogador and tabuleiro[1][i] == jogador and tabuleiro[2][i] == jogador:
            return True
    if tabuleiro[0][0] == jogador and tabuleiro[1][1] == jogador and tabuleiro[2][2] == jogador:
            return True
    if tabuleiro[2][0] == jogador and tabuleiro[1][1] == jogador and tabuleiro[0][2] == jogador:
            return True
    return False

def exibir_final(mensagem):
    # Fundo escuro atrás da mensagem
    overlay = pygame.Surface((LARGURA, 200))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, ALTURA // 2 - 100))
    
    # Texto do Resultado
    texto_surf = FONTE_MSG.render(mensagem, True, COR_TEXTO)
    texto_rect = texto_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
    tela.blit(texto_surf, texto_rect)

    # Desenho do Botão "Jogar Novamente"
    mouse_pos = pygame.mouse.get_pos()
    cor_atual = COR_BOTAO_HOVER if rect_botao.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela, cor_atual, rect_botao, border_radius=12)
    
    texto_btn = FONTE_BOTAO.render("Jogar Novamente", True, COR_TEXTO)
    texto_btn_rect = texto_btn.get_rect(center=rect_botao.center)
    tela.blit(texto_btn, texto_btn_rect)

def reiniciar_jogo():
    global jogador, jogo_acabou
    tabuleiro[:] = [[0] * 3 for _ in range(3)]
    jogador = 1
    jogo_acabou = False
    desenhar_linhas()

# Variáveis Iniciais
jogador = 1
jogo_acabou = False
desenhar_linhas()

# Loop Principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # Se o jogo acabou, o clique só serve para o botão de reiniciar
            if jogo_acabou:
                if rect_botao.collidepoint(mouseX, mouseY):
                    reiniciar_jogo()
            else:
                # Clique no tabuleiro
                linha_clicada = int(mouseY // 200)
                coluna_clicada = int(mouseX // 200)

                if quadrado_disponivel(linha_clicada, coluna_clicada):
                    marcar_quadrado(linha_clicada, coluna_clicada, jogador)
                    
                    if verificar_vitoria(jogador):
                        jogo_acabou = True
                    elif tabuleiro_cheio():
                        jogo_acabou = True
                    
                    if not jogo_acabou:
                        jogador = 2 if jogador == 1 else 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reiniciar_jogo()

    # Atualização Visual
    if not jogo_acabou:
        desenhar_figuras()
    else:
        desenhar_figuras() # Garante que a última peça apareça
        if verificar_vitoria(1):
            exibir_final("J1 Ganhou! J2 Perdeu.")
        elif verificar_vitoria(2):
            exibir_final("J2 Ganhou! J1 Perdeu.")
        else:
            exibir_final("Empate! Deu Velha.")

    pygame.display.update()