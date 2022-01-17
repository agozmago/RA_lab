import random
from pyglet.gl import *


class Particle:
    def __init__(self, image, src, scaling, batch):
        self.rand_x = random.uniform(-1.5, 1.5)
        self.rand_y = random.uniform(-1.5, 1.5)

        self.sprite = pyglet.sprite.Sprite(img=image, x=src[0], y=src[1], batch=batch)
        self.sprite.scale = scaling

    def update(self, direction):
        self.sprite.x = self.sprite.x + self.rand_x + direction[0]
        self.sprite.y = self.sprite.y + self.rand_y + direction[1]

        self.sprite.opacity *= 0.99
        self.sprite.scale *= 0.99
