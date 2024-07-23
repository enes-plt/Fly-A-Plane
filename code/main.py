import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        # Initialize the pygame library
        pygame.init()
        
        # Set up the game display window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Fly A Plane')
        
        # Set up the game clock to manage frame rate
        self.clock = pygame.time.Clock()
        
        # Flag to indicate if the game is active or not
        self.active = True

        # Create sprite groups to manage all game sprites and collision sprites separately
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Calculate the scale factor for resizing sprites based on the background image height
        bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # Set up the background and ground sprites, and add them to the appropriate sprite groups
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        
        # Initialize the plane sprite and add it to the all_sprites group
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.8)

        # Set up a custom event for obstacle spawning, with a timer interval of 1400 milliseconds
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Load the font for displaying the score
        self.font = pygame.font.Font('../graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0  # Initialize the score
        self.start_offset = 0  # Initialize the start offset for score calculation

        # Load the menu image for displaying when the game is not active
        self.menu_surface = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Load and play background music on a loop
        self.music = pygame.mixer.Sound('../sounds/music.wav')
        self.music.play(loops = -1)

    def collisions(self):
        # Check for collisions between the plane and collision sprites
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            # If a collision is detected, remove all obstacle sprites and deactivate the game
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False  # Deactivate the game
            self.plane.kill()  # Remove the plane sprite

    def display_score(self):
        # Display the current score on the screen
        if self.active:
            # Calculate the score based on the time elapsed since the game started
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10  # Position the score at the top of the screen
        else:
            # Position the score in the center of the screen when the game is not active
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        # Render the score text and blit it to the display surface
        score_surface = self.font.render(str(self.score), True, 'black')
        score_rect = score_surface.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surface, score_rect)

    def run(self):
        last_time = time.time()  # Get the current time
        while True:
            # Calculate the time elapsed since the last frame
            dt = time.time() - last_time
            last_time = time.time()

            # Handle events such as quitting the game or mouse button presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()  # Make the plane jump if the game is active
                    else:
                        # Restart the game if it is not active
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.8)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                # Spawn obstacles at regular intervals if the game is active
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            # Clear the display surface
            self.display_surface.fill('black')
            
            # Update and draw all sprites
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            
            # Display the current score
            self.display_score()

            # Check for collisions if the game is active
            if self.active: 
                self.collisions()
            else:
                # Display the menu screen if the game is not active
                self.display_surface.blit(self.menu_surface, self.menu_rect)

            # Update the display and manage the frame rate
            pygame.display.update()
            self.clock.tick(FRAMERATE)

# Entry point of the game
if __name__== '__main__':
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game
