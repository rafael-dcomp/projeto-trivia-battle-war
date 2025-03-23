import pygame

pygame.init()

X = 400

Y = 300

velocidade = 10


janela = pygame.display.set_mode((800,600))

pygame.display.set_caption("Criando um jogo com Python")


janela_aberta = True

while janela_aberta :

    pygame.time.delay(50)

   

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            janela_aberta = False


    comandos = pygame.key.get_pressed()

    if comandos[pygame.K_UP]:

        Y -= velocidade

    if comandos[pygame.K_DOWN]:

        Y += velocidade

    if comandos[pygame.K_RIGHT]:

        X += velocidade

    if comandos[pygame.K_LEFT]:

        X -= velocidade


    janela.fill((0,0,0))


    pygame.draw.circle(janela, (0,255,0),(X,Y),50)

    pygame.display.update()

           

pygame.quit()
