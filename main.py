import pygame
import config
import os
from sys import exit
from components.ground import Ground
from components.pipe import Pipes
from components.player import Player
from logic.population import Population
import math

pygame.font.init()
MENU_FONT = pygame.font.SysFont('arial', 20, bold=True)
TITLE_FONT = pygame.font.SysFont('arial', 30, bold=True)
SCORE_FONT = pygame.font.SysFont('arial', 25, bold=True) 
GAME_OVER_FONT = pygame.font.SysFont('arial', 40, bold=True)

SESSION_HIGH_SCORE = 0
BEST_MANUAL_SCORE = 0
BEST_AI_SCORE = 0
AI_SESSION_HIGH_SCORE = 0

def get_game_speed(score):
    """
    Returns pipe & ground speed based on player score.
    Keeps difficulty increasing but capped.
    """
    if score < 10:
        return 4   # normal speed
    elif score < 20:
        return 5
    elif score < 30:
        return 6
    elif score < 40:
        return 7
    else:
        return 8   # max speed cap

def get_medal(score):
    if score >= 40:
        return config.MEDAL_PLATINUM
    elif score >= 30:
        return config.MEDAL_GOLD
    elif score >= 20:
        return config.MEDAL_SILVER
    elif score >= 10:
        return config.MEDAL_BRONZE
    return None  # No medal

def draw_window(window, birds, pipes, ground, score, gen=None):
    # 1. Fundal
    window.blit(config.BG_IMG, (0, 0))

    # 2. Tevi
    for pipe in pipes:
        pipe.draw(window)

    # 3. Podea
    ground.draw(window)

    # 4. Pasari
    for bird in birds:
        bird.draw(window)

    # 5. Scor curent
    score_text = SCORE_FONT.render(f"{score}", True, (255, 255, 255))
    score_shadow = SCORE_FONT.render(f"{score}", True, (0, 0, 0))
    
    window.blit(score_shadow, (config.WIN_WIDTH/2 - score_text.get_width()/2 + 2, 52))
    window.blit(score_text, (config.WIN_WIDTH/2 - score_text.get_width()/2, 50))

    if gen:
        gen_text = MENU_FONT.render(f"Gen: {gen}", True, (255, 255, 255))
        window.blit(gen_text, (10, 10))

    pygame.display.update()

def main_menu():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(30)
        config.WINDOW.blit(config.BG_IMG, (0,0))
        
        title = TITLE_FONT.render("Flappy AI Project", True, (255, 255, 255))
        title_shadow = TITLE_FONT.render("Flappy AI Project", True, (0, 0, 0))
        
        opt_ai = MENU_FONT.render("Press 'A' for AI", True, (255, 255, 255))
        opt_man = MENU_FONT.render("Press 'M' for Manual", True, (255, 255, 255))
        opt_esc = MENU_FONT.render("ESC to Quit", True, (200, 200, 200))
        
        config.WINDOW.blit(title_shadow, (config.WIN_WIDTH/2 - title.get_width()/2 + 2, 82))
        config.WINDOW.blit(title, (config.WIN_WIDTH/2 - title.get_width()/2, 80))
        
        config.WINDOW.blit(opt_ai, (config.WIN_WIDTH/2 - opt_ai.get_width()/2, 200))
        config.WINDOW.blit(opt_man, (config.WIN_WIDTH/2 - opt_man.get_width()/2, 250))
        config.WINDOW.blit(opt_esc, (config.WIN_WIDTH/2 - opt_esc.get_width()/2, 350))
        
        bird_img = config.BIRD_IMGS[1]
        config.WINDOW.blit(bird_img, (config.WIN_WIDTH/2 - bird_img.get_width()/2, 140))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    run_ai() 
                if event.key == pygame.K_m:
                    run_manual() 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def game_over_screen(current_score):
    global SESSION_HIGH_SCORE

    clock = pygame.time.Clock()

    if current_score > SESSION_HIGH_SCORE:
        SESSION_HIGH_SCORE = current_score
    gameover_img = pygame.image.load(os.path.join("assets", "sprites", "gameover.png")).convert_alpha()
    panel_img = config.SCORE_PANEL

    # Medal
    medal_img = get_medal(current_score)

    # Button dimensions
    button_width = 130
    button_height = 40
    spacing = 20

    # Buttons positions
    play_rect = pygame.Rect(
        config.WIN_WIDTH // 2 - button_width - spacing // 2,
        400,
        button_width,
        button_height
    )

    leaderboard_rect = pygame.Rect(
        config.WIN_WIDTH // 2 + spacing // 2,
        400,
        button_width,
        button_height
    )

    run = True
    while run:
        clock.tick(30)

        mx, my = pygame.mouse.get_pos()

        config.WINDOW.blit(config.BG_IMG, (0, 0))

        config.WINDOW.blit(gameover_img, (config.WIN_WIDTH // 2 - gameover_img.get_width() // 2, 80))

        panel_x = config.WIN_WIDTH // 2 - panel_img.get_width() // 2
        panel_y = 170
        config.WINDOW.blit(panel_img, (panel_x, panel_y))

        if medal_img:
            medal_scaled = pygame.transform.smoothscale(medal_img, (60, 60))
            medal_pos_x = panel_x + 25   # adjust for center
            medal_pos_y = panel_y + 45
            config.WINDOW.blit(medal_scaled, (medal_pos_x, medal_pos_y))

        score_text = MENU_FONT.render(str(current_score), True, (0, 0, 0))
        best_text = MENU_FONT.render(str(SESSION_HIGH_SCORE), True, (0, 0, 0))

        config.WINDOW.blit(score_text, (panel_x + 200, panel_y + 40))
        config.WINDOW.blit(best_text,  (panel_x + 200, panel_y + 80))


        def draw_button(rect, text):
            hovered = rect.collidepoint(mx, my)
            color = (210, 210, 210) if hovered else (240, 240, 240)
            pygame.draw.rect(config.WINDOW, color, rect, border_radius=10)
            pygame.draw.rect(config.WINDOW, (0, 0, 0), rect, 2, border_radius=10)

            label = MENU_FONT.render(text, True, (0, 0, 0))
            config.WINDOW.blit(
                label,
                (rect.x + rect.width//2 - label.get_width()//2,
                 rect.y + rect.height//2 - label.get_height()//2)
            )

        draw_button(play_rect, "PLAY")
        draw_button(leaderboard_rect, "SCORES")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mx, my):
                    start_screen()
                    return
                if leaderboard_rect.collidepoint(mx, my):
                    leaderboard_screen()
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen()
                    return
                if event.key == pygame.K_l:
                    leaderboard_screen()
                    return
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    return



def leaderboard_screen():
    clock = pygame.time.Clock()

    button_width = 120
    button_height = 40
    back_rect = pygame.Rect(
        config.WIN_WIDTH // 2 - button_width // 2,
        440,
        button_width,
        button_height
    )

    run = True
    while run:
        clock.tick(30)
        mx, my = pygame.mouse.get_pos()

        config.WINDOW.blit(config.BG_IMG, (0, 0))

        title = TITLE_FONT.render("LEADERBOARD", True, (255, 255, 255))
        config.WINDOW.blit(
            title,
            (config.WIN_WIDTH // 2 - title.get_width() // 2, 100)
        )

        panel_width = 240
        panel_height = 180
        panel_x = config.WIN_WIDTH // 2 - panel_width // 2
        panel_y = 200

        pygame.draw.rect(config.WINDOW, (245, 245, 245),
                         (panel_x, panel_y, panel_width, panel_height),
                         border_radius=12)

        pygame.draw.rect(config.WINDOW, (0, 0, 0),
                         (panel_x, panel_y, panel_width, panel_height),
                         width=2, border_radius=12)

        manual_text = MENU_FONT.render(
            f"Manual Best: {BEST_MANUAL_SCORE}", True, (0, 0, 0)
        )
        ai_text = MENU_FONT.render(
            f"AI Best: {AI_SESSION_HIGH_SCORE}", True, (0, 0, 0)
        )

        config.WINDOW.blit(
            manual_text,
            (panel_x + panel_width // 2 - manual_text.get_width() // 2, panel_y + 50)
        )
        config.WINDOW.blit(
            ai_text,
            (panel_x + panel_width // 2 - ai_text.get_width() // 2, panel_y + 100)
        )

        hovered = back_rect.collidepoint(mx, my)
        color = (210, 210, 210) if hovered else (240, 240, 240)

        pygame.draw.rect(config.WINDOW, color, back_rect, border_radius=10)
        pygame.draw.rect(config.WINDOW, (0, 0, 0), back_rect, 2, border_radius=10)

        back_label = MENU_FONT.render("BACK", True, (0, 0, 0))
        config.WINDOW.blit(
            back_label,
            (back_rect.x + back_rect.width // 2 - back_label.get_width() // 2,
             back_rect.y + back_rect.height // 2 - back_label.get_height() // 2)
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mx, my):
                    start_screen()
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    return



def start_screen():
    clock = pygame.time.Clock()

    button_width = 200
    button_height = 40
    spacing = 55

    center_x = config.WIN_WIDTH // 2 - button_width // 2
    start_y = 300

    manual_rect = pygame.Rect(center_x, start_y, button_width, button_height)
    ai_rect = pygame.Rect(center_x, start_y + spacing, button_width, button_height)
    leaderboard_rect = pygame.Rect(center_x, start_y + spacing * 2, button_width, button_height)

    bird_img = config.BIRD_IMGS[1]
    bird_x = config.WIN_WIDTH // 2 - bird_img.get_width() // 2
    bird_y_base = 200
    oscillation = 0

    run = True
    while run:
        clock.tick(30)
        oscillation += 0.05
        bird_y = bird_y_base + int(4 * math.sin(oscillation))

        config.WINDOW.blit(config.BG_IMG, (0, 0))

        logo = config.LOGO_IMG
        config.WINDOW.blit(logo, (config.WIN_WIDTH // 2 - logo.get_width() // 2, 80))

        config.WINDOW.blit(bird_img, (bird_x, bird_y))

        mx, my = pygame.mouse.get_pos()

        def draw_button(rect, text):
            is_hovered = rect.collidepoint(mx, my)
            color = (210, 210, 210) if is_hovered else (240, 240, 240)
            pygame.draw.rect(config.WINDOW, color, rect, border_radius=10)
            pygame.draw.rect(config.WINDOW, (0, 0, 0), rect, width=2, border_radius=10)

            label = MENU_FONT.render(text, True, (0, 0, 0))
            config.WINDOW.blit(label, (rect.x + rect.width//2 - label.get_width()//2,
                                       rect.y + rect.height//2 - label.get_height()//2))

        draw_button(manual_rect, "Manual Mode")
        draw_button(ai_rect, "AI Mode")
        draw_button(leaderboard_rect, "Leaderboard")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if manual_rect.collidepoint(mx, my):
                    run_manual()
                if ai_rect.collidepoint(mx, my):
                    run_ai()
                if leaderboard_rect.collidepoint(mx, my):
                    leaderboard_screen()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    run_manual()
                if event.key == pygame.K_a:
                    run_ai()
                if event.key == pygame.K_l:
                    leaderboard_screen()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def run_manual():
    global BEST_MANUAL_SCORE
    bird = Player()
    ground = Ground(config.WIN_WIDTH)
    pipes = []
    score = 0
    clock = pygame.time.Clock()
    run = True
    pipes_spawn_timer = 0

    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.bird_flap()
                if event.key == pygame.K_ESCAPE:
                    return 
        speed = get_game_speed(score)
        ground.update(speed)
        bird.update(ground)

        if pipes_spawn_timer <= 0:
            pipes.append(Pipes(config.WIN_WIDTH + 50,speed))
            pipes_spawn_timer = 45
        pipes_spawn_timer -= 1

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.update(speed)
            
            if pipe.collide(bird):
                config.SOUND_DIE.play()
                if score > BEST_MANUAL_SCORE:
                    BEST_MANUAL_SCORE = score
                game_over_screen(score)
                return 

            if not pipe.passed and pipe.x < bird.rect.x:
                pipe.passed = True
                add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            config.SOUND_SCORE.play()

        for r in rem:
            pipes.remove(r)

        if not bird.alive:
            if score > BEST_MANUAL_SCORE:
                BEST_MANUAL_SCORE = score

            game_over_screen(score)
            return

        draw_window(config.WINDOW, [bird], pipes, ground, score)

def run_ai():
    global BEST_AI_SCORE
    global AI_SESSION_HIGH_SCORE

    if BEST_AI_SCORE>AI_SESSION_HIGH_SCORE:
        AI_SESSION_HIGH_SCORE=BEST_AI_SCORE
    BEST_AI_SCORE = 0
    population = Population(20)
    ground = Ground(config.WIN_WIDTH)
    config.pipes = [] 
    clock = pygame.time.Clock()
    pipes_spawn_timer = 0
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if score > BEST_AI_SCORE:
                        BEST_AI_SCORE = score
                    config.pipes.clear()
                    game_over_screen(BEST_AI_SCORE)
                    return


        speed = get_game_speed(score)
        ground.update(speed)

        if pipes_spawn_timer <= 0:
            config.pipes.append(Pipes(config.WIN_WIDTH + 50,speed))
            pipes_spawn_timer = 50
        pipes_spawn_timer -= 1

        rem = []
        add_pipe = False
        for pipe in config.pipes:
            pipe.update(speed)
            if population.players:
                living_birds = [p for p in population.players if p.alive]
                if living_birds and not pipe.passed and pipe.x < living_birds[0].rect.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            config.SOUND_SCORE.play()

        for r in rem:
            config.pipes.remove(r)

        if not population.extinct():
            population.update_live_players(ground)
        else:
            config.SOUND_DIE.play()
            if score > BEST_AI_SCORE:
                BEST_AI_SCORE = score
            config.pipes.clear()
            population.natural_selection()
            pipes_spawn_timer = 0
            score = 0
        
        live_birds = [p for p in population.players if p.alive]
        draw_window(config.WINDOW, live_birds, config.pipes, ground, score, population.generation)

if __name__ == "__main__":
    start_screen()