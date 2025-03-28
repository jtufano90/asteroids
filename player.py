import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.direction = 0
        self.timer = 0

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        #pygame.draw.polygon(self.image,(255, 255, 255), [(15, 0), (0, 30), (30, 30)])

        self.rect = self.image.get_rect()
        self.rect.center = (self.position.x, self.position.y)

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def rotate(self, dt):
       self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.timer > 0:
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        self.rect.center = (self.position.x, self.position.y)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        velocity = pygame.Vector2(0, 1)
        velocity = velocity.rotate(self.rotation)
        velocity *= PLAYER_SHOOT_SPEED
        shot.velocity = velocity
        self.timer = PLAYER_SHOOT_COOLDOWN

        return shot