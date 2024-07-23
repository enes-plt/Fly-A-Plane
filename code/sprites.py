import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        # Load background image and scale it based on the scale factor
        bg_image = pygame.image.load('../graphics/environment/background.png').convert()
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        # Create a surface that is twice the width of the full-sized image for seamless scrolling
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        # Set the rect and initial position of the background
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        # Move the background to the left to create a scrolling effect
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            # Reset the position to create an infinite scrolling effect
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        # Load and scale the ground image
        ground_surface = pygame.image.load('../graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surface, pygame.math.Vector2(ground_surface.get_size()) * scale_factor)

        # Set the rect and initial position of the ground
        self.rect = self.image.get_rect(bottomleft = (0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Create a mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # Move the ground to the left to create a scrolling effect
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            # Reset the position to create an infinite scrolling effect
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # Import and scale the frames for plane animation
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # Set the rect and initial position of the plane
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20 , WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Initialize movement variables
        self.gravity = 600
        self.direction = 0

        # Create a mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

        # Load and set the volume for the jump sound
        self.jump_sound = pygame.mixer.Sound('../sounds/jump.wav')
        self.jump_sound.set_volume(0.3)

    def import_frames(self, scale_factor):
        # Load and scale the frames for the plane animation
        self.frames = []
        for i in range(3):
            surface = pygame.image.load(f'../graphics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        # Apply gravity to the plane, making it fall over time
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        # Make the plane jump by setting a negative direction value
        self.jump_sound.play()
        self.direction = -400

    def animate(self, dt):
        # Animate the plane by cycling through the frames
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        # Rotate the plane based on its direction for a realistic effect
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # Update the plane's position, animation, and rotation
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        # Randomly choose the orientation (up or down) of the obstacle
        orientation = choice(('up', 'down'))
        
        # Load and scale the obstacle image
        surface = pygame.image.load(f'../graphics/obstacles/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)

        # Set the initial position of the obstacle based on its orientation
        x = WINDOW_WIDTH + randint(40, 100)
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Create a mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # Move the obstacle to the left
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            # Remove the obstacle when it goes off-screen
            self.kill()
