import pygame, random

pygame.init()


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the monsters")

# Set FPS
FPS = 60
clock = pygame.time.Clock()


# Define Classed
class Game():
    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        self.next_level_sound = pygame.mixer.Sound("assets/next_level.wav")

        self.font = pygame.font.Font("assets/Abrushow.ttf", 24)

        # Set images
        blue_monster_img = pygame.image.load("assets/blue_monster.png")
        green_monster_img = pygame.image.load("assets/green_monster.png")
        purple_monster_img = pygame.image.load("assets/purple_monster.png")
        yellow_monster_img = pygame.image.load("assets/yellow_monster.png")
        self.target_monster_images = [blue_monster_img, green_monster_img,purple_monster_img, yellow_monster_img]

        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.y = 30

    def updete(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        # check for collision
        self.check_collisions()

    def draw(self):
        WHITE = (255, 255, 255)
        BLUE = (21, 177, 234)
        GREEN = (88, 200, 49)
        PURPLE = (227, 72, 242)
        YELLOW = (242, 155, 21)

        # Add the monster color to the list WHERE index of the color MATCHES with monster_image
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # Set text
        catch_text = self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH //2
        catch_rect.top = 5

        score_text = self.font.render("Score " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Lives " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Current round " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round Time: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warps_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warps_rect = warps_text.get_rect()
        warps_rect.topright = (WINDOW_WIDTH - 10, 35)

        # Blit the HUD
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warps_text, warps_rect)

        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH//2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)


    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        if collided_monster:
            if collided_monster.type == self.target_monster_type:
                self.score += self.round_number
                collided_monster.remove(self.monster_group)
                if self.monster_group:
                    # There more monster to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    # the round is over
                    self.player.reset()
                    self.start_new_round()
            # Collide wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -= 1

                if self.player.lives <= 0:
                    self.pause_game("Score :"+ str(self.score), "Press 'Enter' to restart thr game ")
                    self.reset_game()
                self.player.reset()


    def start_new_round(self):
        # Provide score bonus based on timeing
        self.score += int(100*self.round_number/ (1 + self.round_time))

        # Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        # Remove remaining monsters
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        # Add monster to monster group
        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                                           self.target_monster_images[0], 0))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[1], 1))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[2], 2))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[3], 3))

        # Choose a new target
        self.choose_new_target()
        self.next_level_sound.play()


    def choose_new_target(self):
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        global running

        main_text = self.font.render(main_text, True, (255, 255, 255))
        main_text_rect = main_text.get_rect()
        main_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        sub_text = self.font.render(sub_text, True, (255, 255, 255))
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        display_surface.fill((0, 0, 0))
        display_surface.blit(main_text, main_text_rect)
        display_surface.blit(sub_text, sub_text_rect)

        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def reset_game(self):
        self.score = 0
        self.round_number = 0
        self.player.lives = 4
        self.player.warps = 1
        self.player.reset()

        self.start_new_round()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

        self.velocity = 8
        self.lives = 4
        self.warps = 1

        self.catch_sound = pygame.mixer.Sound("assets/catch.wav")
        self.die_sound = pygame.mixer.Sound("assets/die.wav")
        self.warp_sound = pygame.mixer.Sound("assets/warp.wav")

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity

    def warp(self):
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT



class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

        #monster type will be an int 0 - blue, 1 - green, 2 - purple, 3 - yellow
        self.type = monster_type

        # Set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)

    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # Bounce from the edges
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy = -1 * self.dy


# cREATE PLAYER GROUP and obj
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

# Create a monster group
my_monster_group = pygame.sprite.Group()

# test_monster = Monster(500, 500, pygame.image.load("assets/green_monster.png"), 1)
# my_monster_group.add(test_monster)
# test_monster2 = Monster(200, 200, pygame.image.load("assets/blue_monster.png"), 1)
# my_monster_group.add(test_monster2)

# Create a game obj
my_game = Game(my_player, my_monster_group)
my_game.pause_game("Catch the monster of the right color. Press Spacebar to teleport to a safe zone",
                   "Press Enter to start the Game")
my_game.start_new_round()


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player wants to warp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()

    # Fill display
    display_surface.fill((0, 0, 0))


    # Update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    # update Game
    my_game.updete()
    my_game.draw()

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()