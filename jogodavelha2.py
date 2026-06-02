import pygame
import sys

# Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 600, 600
LINHA_LARGURA = 15
COR_FUNDO = (28, 170, 156)
COR_LINHA = (23, 145, 135)
COR_CIRCULO = (255, 215, 0) # Amarelo Ouro
COR_X = (0, 0, 0)            # MUDADO: X padrão agora é totalmente preto
COR_X_SUMIR = (180, 195, 190) # MUDADO: X que vai sumir agora é um cinza claro adaptado ao fundo
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (30, 30, 30)
COR_BOTAO_HOVER = (50, 50, 50)

# Fontes
FONTE_MSG = pygame.font.SysFont("Arial", 32, bold=True)
FONTE_BOTAO = pygame.font.SysFont("Arial", 24, bold=True)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha Infinito')

# Estado do Jogo
tabuleiro = [[0 for _ in range(3)] for _ in range(3)]
pecas_j1 = [] 
pecas_j2 = []
jogador = 1
jogo_acabou = False
rect_botao = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 20, 200, 50)

def desenhar_linhas():
    tela.fill(COR_FUNDO)
    pygame.draw.line(tela, COR_LINHA, (0, 200), (600, 200), LINHA_LARGURA)
    pygame.draw.line(tela, COR_LINHA, (0, 400), (600, 400), LINHA_LARGURA)
    pygame.draw.line(tela, COR_LINHA, (200, 0), (200, 600), LINHA_LARGURA)
    pygame.draw.line(tela, COR_LINHA, (400, 0), (400, 600), LINHA_LARGURA)

def desenhar_figuras():
    for linha in range(3):
        for col in range(3):
            centro_x, centro_y = col * 200 + 100, linha * 200 + 100
            
            if tabuleiro[linha][col] == 1:
                # Efeito visual: se for a peça que vai sumir, fica mais escura
                cor = (180, 150, 0) if len(pecas_j1) == 3 and (linha, col) == pecas_j1[0] else COR_CIRCULO
                pygame.draw.circle(tela, cor, (centro_x, centro_y), 60, LINHA_LARGURA)
            elif tabuleiro[linha][col] == 2:
                # MUDADO: Lógica de cor do X (Preto padrão vs Cinza para sumir)
                cor = COR_X_SUMIR if len(pecas_j2) == 3 and (linha, col) == pecas_j2[0] else COR_X
                offset = 55
                pygame.draw.line(tela, cor, (centro_x - offset, centro_y + offset), (centro_x + offset, centro_y - offset), LINHA_LARGURA)
                pygame.draw.line(tela, cor, (centro_x - offset, centro_y - offset), (centro_x + offset, centro_y + offset), LINHA_LARGURA)

def verificar_vitoria(j):
    for i in range(3):
        if all([tabuleiro[i][c] == j for c in range(3)]): return True
        if all([tabuleiro[r][i] == j for r in range(3)]): return True
    if tabuleiro[0][0] == j and tabuleiro[1][1] == j and tabuleiro[2][2] == j: return True
    if tabuleiro[0][2] == j and tabuleiro[1][1] == j and tabuleiro[2][0] == j: return True
    return False

def exibir_final(mensagem):
    overlay = pygame.Surface((LARGURA, 200))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, ALTURA // 2 - 100))
    
    texto_surf = FONTE_MSG.render(mensagem, True, COR_TEXTO)
    texto_rect = texto_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
    tela.blit(texto_surf, texto_rect)

    mouse_pos = pygame.mouse.get_pos()
    cor_atual = COR_BOTAO_HOVER if rect_botao.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela, cor_atual, rect_botao, border_radius=12)
    
    texto_btn = FONTE_BOTAO.render("Jogar Novamente", True, COR_TEXTO)
    texto_btn_rect = texto_btn.get_rect(center=rect_botao.center)
    tela.blit(texto_btn, texto_btn_rect)

def reiniciar_jogo():
    global jogador, jogo_acabou, tabuleiro, pecas_j1, pecas_j2
    tabuleiro = [[0 for _ in range(3)] for _ in range(3)]
    pecas_j1, pecas_j2 = [], []
    jogador = 1
    jogo_acabou = False

# Loop Principal
while True:
    desenhar_linhas()
    desenhar_figuras()
    
    if jogo_acabou:
        vencedor = "J1 Ganhou! J2 Perdeu." if verificar_vitoria(1) else "J2 Ganhou! J1 Perdeu."
        exibir_final(vencedor)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if jogo_acabou:
                if rect_botao.collidepoint(mx, my):
                    reiniciar_jogo()
            else:
                linha, col = my // 200, mx // 200
                if tabuleiro[linha][col] == 0:
                    lista_atual = pecas_j1 if jogador == 1 else pecas_j2
                    
                    if len(lista_atual) == 3:
                        r_lin, r_col = lista_atual.pop(0)
                        tabuleiro[r_lin][r_col] = 0
                    
                    tabuleiro[linha][col] = jogador
                    lista_atual.append((linha, col))

                    if verificar_vitoria(jogador):
                        jogo_acabou = True
                    else:
                        jogador = 2 if jogador == 1 else 1

    pygame.display.update()