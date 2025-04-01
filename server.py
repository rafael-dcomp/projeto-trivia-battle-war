
from sys import exit
from pygame.locals import *
import pygame
import os
from time import sleep
import asyncio
import websockets
import json


questions = [
    {
        "question": "Qual é a capital da França?",
        "options": ["Londres", "Berlim", "Paris", "Madri"],
        "answer": 2
    },
    {
        "question": "Qual é a soma de 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": 1
    },
    {
        "question": "Qual é o maior planeta do sistema solar?",
        "options": ["Terra", "Marte", "Júpiter", "Saturno"],
        "answer": 2
    }
]

# Variáveis do jogo
current_question = 0
score = 0


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
img = pygame.image.load("TelaPerguntas.png")
img = pygame.transform.scale(img, (1200, 675))
background = pygame.image.load("TBW.png")
background = pygame.transform.scale(background, (1200, 675))

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


# Variáveis
connected_clients = set()
salas = {}

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
bt_voltar = Button(10, 10, jg_voltar)


def multiplayer():

    # Criação da Entrada de Texto
    cod_entrada = pygame.Rect(500, 385, 200, 40)
    codigo = ""
    status = False

    var = True
    while var:
        # Tela Estática
        tela.blit(background, (0, 0))

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

    def draw_question(question_data):
        tela.blit(img, (0, 0))
        if bt_voltar.draw(tela):
            main_menu()
        question_text = font.render(question_data["question"], True, BLACK)
        tela.blit(question_text, (450, 150))

        for i, option in enumerate(question_data["options"]):
            option_text = font.render(f"{i + 1}. {option}", True, BLACK)
            tela.blit(option_text, (450, 200 + i * 40))

        pygame.display.flip()

    def winner():
        tela.blit(img, (0, 0))

        if bt_voltar.draw(tela):
            main_menu()
        question_text = font.render(
            "Fim de Jogo, Sua Pontuação foi de: " + str(score) + "/" + str(len(questions)), True, BLACK)
        tela.blit(question_text, (350, 150))
        pygame.display.flip()
        sleep(3)
        main_menu()

    def main():
        global current_question, score

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        answer = event.key - pygame.K_1
                        if answer == questions[current_question]["answer"]:
                            score += 1
                        current_question += 1

                        if current_question >= len(questions):
                            current_question = 0
                            winner()

            draw_question(questions[current_question])
    main()


def sair_jogo():
    exit()


def main_menu():  # TELA INICIAL DO JOGO
    var = True
    while var:
        # Tela Estática
        tela.blit(background, (0, 0))

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
