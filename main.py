import pygame
import sys
import random


def draw_base():
    screen.blit(base, (base_position, 520))
    screen.blit(base, (base_position + 360, 520))


def moving_background():
    screen.blit(background, (background_position, 0))
    screen.blit(background, (background_position + 360, 0))


def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe - 600))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 650:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def collution(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_position * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_fonts.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(180, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_fonts.render(f'score {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(180, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_fonts.render(f'high score {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(130, 500))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

# setting up display
screen = pygame.display.set_mode((360, 640))
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('owl.png')
pygame.display.set_icon(icon)
game_fonts = pygame.font.Font('04B_19.ttf', 40)
clock = pygame.time.Clock()

# loading background, base & game surface images
background = pygame.image.load('bg_n.png').convert()
base = pygame.image.load('base.png').convert()
game_over_suraface = pygame.image.load('message.png').convert_alpha()
game_over_rect = game_over_suraface.get_rect(center=(190, 280))

# game sounds
point_sound = pygame.mixer.Sound('sfx_point.wav')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
flap_sound = pygame.mixer.Sound('sfx_wing.wav')

# Bird flap animation
bird_downflap = pygame.transform.scale2x(pygame.image.load('redbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('redbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('redbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 320))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Generating pipes
pipe_surface = pygame.image.load('pipe-red.png')
pipe_list = []
SPANWPIPE = pygame.USEREVENT
pygame.time.set_timer(SPANWPIPE, 1200)
pipe_height = [350, 400, 550]

# Game variables
gravity = 0.25
bird_position = 0
base_position = 0
background_position = 0
game_active = True
score = 0
score_sound_countdown = 100
high_score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                bird_position = -10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 320)
                score = 0

        if event.type == SPANWPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

                bird_surface, bird_rect = bird_animation()

    # reducing 1px at a time from left to right
    base_position -= 1
    background_position -= 1

    # Animating background
    moving_background()
    if background_position <= -360:
        background_position = 0

    # Animating base
    draw_base()
    if base_position <= -360:
        base_position = 0
    if game_active:
        # Bird Moveent
        bird_position += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_position
        screen.blit(rotated_bird, bird_rect)
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = collution(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            point_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_suraface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    pygame.display.update()
    clock.tick(120)
