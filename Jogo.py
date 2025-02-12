import pygame
from pygame.locals import *
from moviepy import VideoFileClip
from sys import exit
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import pandas as pd


pygame.init()

font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Proporção de Tela e Nome da Janela
largura = 1200
altura = 675
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Trivia Battle War")

# Video rodando
img_fundo = VideoFileClip("tela_de_fundo.mp4")
duracao_vid = img_fundo.duration

# MUSICA DE FUNDO DO JOGO
musica_de_fundo = pygame.mixer.music.load("Spektrem - Shine [NCS Release].mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Classe Para os Botões


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # Pegar posição do mouse#Pegar posição do mouse
        mouse_pos = pygame.mouse.get_pos()

        # Checar se um botão foi clicado ou se o mouse está sobre
        if self.rect.collidepoint(mouse_pos):
            # Clique do mouse esquerdo
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # Reseta o Botão para clicar novamente
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# IMAGENS Botões DO MENU
jg_local = pygame.image.load('jogo_local.png').convert_alpha()
jg_multiplayer = pygame.image.load('multiplayer.png').convert_alpha()
jg_config = pygame.image.load('config.png').convert_alpha()
jg_exit = pygame.image.load('sair_do_jogo.png').convert_alpha()

# BOtÃO VOLTAR
jg_voltar = pygame.image.load('voltar.png').convert_alpha()

# IMAGENS BOTÕES MULTIPLAYERS
jg_entrar_sala = pygame.image.load('entrar_sala.png').convert_alpha()
jg_criar_sala = pygame.image.load('criar_sala.png').convert_alpha()

# Botões Menu
bt_local = Button(450, 200, jg_local)
bt_mult = Button(450, 300, jg_multiplayer)
bt_config = Button(450, 400, jg_config)
bt_exit = Button(450, 500, jg_exit)

# Botões MultiPlayer
bt_criar_sala = Button(450, 200, jg_criar_sala)
bt_entrar_sala = Button(450, 450, jg_entrar_sala)

# Botão VOLTAR
bt_voltar = Button(10, 50, jg_voltar)


def multiplayer():
    # Criação da Entrada de Texto
    cod_entrada = pygame.Rect(500, 385, 200, 40)
    codigo = ""
    status = False

    var = True
    while var:
        # Roda o VIdeo de Fundo em loop
        vid_loop = (pygame.time.get_ticks()/1000.0) % duracao_vid
        inicio_vid = img_fundo.get_frame(vid_loop)
        player = pygame.surfarray.make_surface(inicio_vid.swapaxes(0, 1))
        tela.blit(player, (0, 0))

        # Ativa Botões do Multiplayer
        bt_criar_sala.draw(tela)
        bt_entrar_sala.draw(tela)
        if bt_voltar.draw(tela):
            main_menu()

        # Ativa Entrada de Texto
        entrada_txt = font.render("Código da Sala:", True, BLACK)
        tela.blit(entrada_txt, (500, 350))
        color = BLACK if status else GRAY
        pygame.draw.rect(tela, color, cod_entrada, 2)
        # Exibir txt
        txt = font.render(codigo, True, BLACK)
        tela.blit(txt, (cod_entrada.x + 10, cod_entrada.y + 5))

        # Looping do Jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                var = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                status = cod_entrada.collidepoint(event.pos)
            elif event.type == pygame.KEYDOWN and status:
                if event.key == pygame.K_BACKSPACE:
                    codigo = codigo[:-1]  # Apaga um caractere
                elif event.key == pygame.K_RETURN:
                    print(f"Texto digitado: {codigo}")  # Exibe no console
                else:
                    codigo += event.unicode  # Adiciona a tecla digitada ao texto
        pygame.display.update()


def play_local():
    df = pd.read_excel('perguntas_multipla_escolha_atualizado.xlsx')
    perguntas = df.sample(n=15).values.tolist()

    # Criando Janela
    janela = tk.Tk()
    janela.title("Quiz Local")
    janela.geometry("1200x695")

    # Cores da Janela
    background_color = "#ECECEC"
    txt_color = "333333"
    bt_color = "#4CAF50"
    bt_txt_color = "#FFFFFF"

    janela.config(bg=background_color)
    janela.option_add('*Font', 'Arial')

    # Imagem Central Quiz
    img_quiz = PhotoImage(file='icons8-quiz-100.png')
    img_label = tk.Label(janela, image=img_quiz, bg=background_color)
    img_label.pack(pady=10)

    # Labels e Botões
    question_lbl = tk.Label(
        janela, text="PERGUNTA1 TESTE FEITA COM SUCESSO?", font="Arial")
    question_lbl.pack(pady=20)

    resposta = tk.IntVar()

    opc1 = tk.Button(janela, text="RESPOSTA ALTERNATIVA 1", width=30, bg=bt_color,
                     fg=bt_txt_color, state=tk.DISABLED, font="Arial")
    opc1.pack(pady=10)

    opc2 = tk.Button(janela, text="RESPOSTA ALTERNATIVA 2", width=30, bg=bt_color,
                     fg=bt_txt_color, state=tk.DISABLED, font="Arial")
    opc2.pack(pady=10)

    opc3 = tk.Button(janela, text="RESPOSTA ALTERNATIVA 3", width=30, bg=bt_color,
                     fg=bt_txt_color, state=tk.DISABLED, font="Arial")
    opc3.pack(pady=10)

    opc4 = tk.Button(janela, text="RESPOSTA ALTERNATIVA 4", width=30, bg=bt_color,
                     fg=bt_txt_color, state=tk.DISABLED, font="Arial")
    opc4.pack(pady=10)

    opc5 = tk.Button(janela, text="RESPOSTA ALTERNATIVA 5", width=30, bg=bt_color,
                     fg=bt_txt_color, state=tk.DISABLED, font="Arial")
    opc5.pack(pady=10)

    janela.mainloop()


def sair_jogo():
    exit()


def main_menu():  # TELA INICIAL DO JOGO
    var = True
    while var:
        # Roda o VIdeo de Fundo em loop
        vid_loop = (pygame.time.get_ticks()/1000.0) % duracao_vid
        inicio_vid = img_fundo.get_frame(vid_loop)
        player = pygame.surfarray.make_surface(inicio_vid.swapaxes(0, 1))
        tela.blit(player, (0, 0))

        # Ativar Visualização dos Botões
        if bt_local.draw(tela):
            play_local()
        if bt_mult.draw(tela):
            multiplayer()
        bt_config.draw(tela)
        if bt_exit.draw(tela):
            sair_jogo()

        # Looping do Jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                var = False
                pygame.quit()
                exit()

        pygame.display.update()


main_menu()
