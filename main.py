import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, randint, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'img')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

back_music = pygame.mixer.music.load(os.path.join(diretorio_sons, 'thriller.mp3'))
pygame.mixer.music.play(-1)

#DECLARANDO ATRIBUTOS
LARGURA = 800
ALTURA = 600
GAME_SPEED = 10
SCROLL = 0
FPS = 60
WAITING = True

screen = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Jackson's Nightmare")

sprite_sheet_mj = pygame.image.load(os.path.join(diretorio_imagens, 'MJ_SpritesSheet.png')).convert_alpha()
sprite_sheet_obs = pygame.image.load(os.path.join(diretorio_imagens, 'Obs_SpritesSheet.png')).convert_alpha()
background = pygame.image.load(os.path.join(diretorio_imagens, 'cemetery_bg.jpeg')).convert()
nuv = pygame.image.load(os.path.join(diretorio_imagens, 'nuvem.png'))

background = pygame.transform.scale(background, (800, 600))
bg_width = background.get_width()

colisao_sound = pygame.mixer.Sound(os.path.join(diretorio_sons, 'ee_hee.mp3'))
colisao_sound.set_volume(0.8)
pontuacao_sound = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
pontuacao_sound.set_volume(0.2)

colidir = False

random_obstacle = choice([0, 1])
random_ground = randint(0,2)
points = 0

class MJ(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.jump_sound = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.jump_sound.set_volume(0.8)
        self.imagens_MJ = []
        for i in range(3):
            img = sprite_sheet_mj.subsurface((i * 200,0), (200,578))
            img = pygame.transform.scale(img, (200//3, 578//3))
            self.imagens_MJ.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_MJ[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, (ALTURA - 100) - ((578//3)//2)
        self.ground_height = (ALTURA - 100) - ((578//3)//2)
        self.jump_height = 150
        self.is_jumping = False

    def jump(self):
        if self.is_jumping == False:
            self.is_jumping = True
            self.jump_sound.play()

    def update(self):
        if self.is_jumping == True:
            if self.rect.y <= self.jump_height:
                self.is_jumping = False
            self.rect.y -= 15
        else:
            if self.rect.y < self.ground_height:
                self.rect.y += 15
            else:
                self.rect.y = self.ground_height
            
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_MJ[int(self.index_lista)]

    def morreu(self):
        self.image = sprite_sheet_mj.subsurface((3 * 200,0), (200,578))
        self.image = pygame.transform.scale(self.image, (200//3, 578//3))

class Nuvens(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = nuv.subsurface((0,0), (667, 374))
        self.image = pygame.transform.scale(self.image, (667//4, 374//4))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(100, 150, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA + randrange(30, 300, 90)
            self.rect.y = randrange(100, 200, 50)
        self.rect.x -= GAME_SPEED


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.i = randint(0,2)
        self.image = sprite_sheet_obs.subsurface((self.i * 220, 0), (220,283))
        self.image = pygame.transform.scale(self.image, (220//3, 283//3))
        self.random = random_obstacle
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA
        self.rect.y = ALTURA - 283//3
        

    def update(self):
        if self.random == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
                self.image = sprite_sheet_obs.subsurface((self.i * 220, 0), (220,283))
                self.image = pygame.transform.scale(self.image, (220//3, 283//3))
            self.rect.x -= GAME_SPEED

    def draw(self):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.width, self.height))

class Morcego(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_obs.subsurface((3 * 220, 0), (220,283))
        self.image = pygame.transform.scale(self.image, (220//3, 283//3))
        self.random = random_obstacle
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 300
        self.rect.x = LARGURA
        
    def update(self):
        if self.random == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= GAME_SPEED

todas_as_sprites = pygame.sprite.Group()

def exibe_texto(msg, tamanho, cor, x, y):
    #Exibe um texto na tela
    fonte = pygame.font.Font('fonts/JejuHallasan-Regular.ttf', tamanho)
    mensagem = f"{msg}"
    texto = fonte.render(mensagem, False, cor)
    texto_rect = texto.get_rect()
    texto_rect.midtop = (x, y)
    screen.blit(texto, texto_rect)

def restart_game():
    global points, GAME_SPEED, colidir, random_obstacle, random_ground, SCROLL
    points = 0
    GAME_SPEED = 10
    colidir = False
    obs.rect.x = LARGURA
    bat.rect.x = LARGURA
    random_obstacle = choice([0, 1])
    random_ground = randint(0,2)
    SCROLL = 0
    mj.is_jumping = False
    mj.rect.y = (ALTURA - 100) - ((578//3)//2)
    pygame.mixer.music.play(-1)

def exibe_menu():
    #Exibe o Menu na tela
    if WAITING == True:
        title_screen = background.subsurface(((200, 0), (400,300)))
        title_screen = pygame.transform.scale(title_screen, (800, 600))
        img_menu = title_screen.get_rect()
        img_menu.midtop = (LARGURA//2, 0)
        screen.blit(title_screen, img_menu)
        exibe_texto(
            "Jackson's Nightmare", 60, ('red'), LARGURA//2, 110
        )
        exibe_texto(
            "Pressione SPACE para iniciar", 30, ('red'), LARGURA//2, 450
        )


def wait_start():
    #Mantem o loop do jogo na tela do menu até que o jogador pressione a tecla ESPACO
    WAITING = True
    while WAITING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WAITING = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    WAITING = False
                    pontuacao_sound.play()

for i in range(3):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

mj = MJ()
todas_as_sprites.add(mj)

bat = Morcego()
todas_as_sprites.add(bat)

obs = Obstacle()
todas_as_sprites.add(obs)

obs_group = pygame.sprite.Group()
obs_group.add(obs, bat)

clock = pygame.time.Clock()

exibe_menu()

pygame.display.flip()
wait_start()
while True:
    clock.tick(FPS)
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and colidir == False:
                    if mj.rect.y != mj.ground_height:
                        pass
                    else: 
                        mj.jump()
                if event.key == pygame.K_r and colidir == True:
                    restart_game()

    if obs.rect.topright[0] <= 0 or bat.rect.topright[0] <= 0:
        random_obstacle = choice([0, 1])
        random_ground = randint(0,2)
        obs.image = sprite_sheet_obs.subsurface((obs.i * 220, 0), (220,283))
        obs.image = pygame.transform.scale(obs.image, (220//3, 283//3))
        obs.i = random_ground
        obs.rect.x = LARGURA
        bat.rect.x = LARGURA
        obs.random = random_obstacle
        bat.random = random_obstacle

    colidiu = pygame.sprite.spritecollide(mj, obs_group, False)
    if colidiu and colidir == False:
        mj.morreu()
        colisao_sound.play()
        pygame.mixer.music.stop()
        colidir = True
        
    for i in range(3):
        screen.blit(background, (i * bg_width + SCROLL, 0))

    if colidir == True:
        exibe_texto("GAME OVER", 70, ('red'), 450, 250)
        exibe_texto("pressione R para reiniciar", 25, ('red'), 485, 320)
    else:
        points += 1
        todas_as_sprites.update()
        exibe_texto(points, 50, ('red'), 720, 30)
        SCROLL -= 4
        if abs(SCROLL) > bg_width:
            SCROLL = 0

    if points % 500 == 0:
        pontuacao_sound.play()
        if GAME_SPEED >= 20:
            GAME_SPEED += 0
        else:
            GAME_SPEED += 0.5

    todas_as_sprites.draw(screen)

    pygame.display.flip()