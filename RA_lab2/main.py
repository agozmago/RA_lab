from pyglet.gl import *
from pyglet.window import key
from particle import Particle


window = pyglet.window.Window(width=1024, height=480, config=pyglet.gl.Config(double_buffer=True))


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(interval):
    global particle_list, particles_in_batch

    for particle in particle_list:
        particle.update(direction)

        if alpha_threshold > particle.sprite.opacity:
            particle_list.remove(particle)

    for new_particle in range(particles_in_batch):
        particle_list.append(Particle(image=image, src=src, scaling=0.15, batch=batch))


@window.event
def on_key_press(symbol, modifiers):
    global src, direction, particles_in_batch, alpha_threshold

    if symbol == key.N:
        particles_in_batch += 1
    elif symbol == key.M:
        particles_in_batch -= 1
    particles_in_batch = max(0, min(10, particles_in_batch))

    if symbol == key.W:
        src[1] += 10
    elif symbol == key.A:
        src[0] -= 10
    elif symbol == key.S:
        src[1] -= 10
    elif symbol == key.D:
        src[0] += 10
    src[0] = max(0, min(1024, src[0]))
    src[1] = max(0, min(480, src[1]))

    if symbol == key.X:
        alpha_threshold -= 25
    elif symbol == key.Y:
        alpha_threshold += 25
    alpha_threshold = max(0, min(255, alpha_threshold))

    if symbol == key.NUM_1:
        direction[0] -= 5
        direction[1] -= 5
    elif symbol == key.NUM_2:
        direction[1] -= 5
    elif symbol == key.NUM_3:
        direction[0] += 5
        direction[1] -= 5
    elif symbol == key.NUM_4:
        direction[0] -= 5
    elif symbol == key.NUM_6:
        direction[0] += 5
    elif symbol == key.NUM_7:
        direction[0] -= 5
        direction[1] += 5
    elif symbol == key.NUM_8:
        direction[1] += 5
    elif symbol == key.NUM_9:
        direction[0] += 5
        direction[1] += 5
    direction[0] = max(-50, min(50, direction[0]))
    direction[1] = max(-255, min(255, direction[1]))


if __name__ == "__main__":
    direction = [0, 0]
    src = [1024//2, 480//2]

    image = pyglet.image.load("explosion.bmp")
    batch = pyglet.graphics.Batch()

    particles_in_batch = 2
    particle_list = []
    alpha_threshold = 20

    pyglet.clock.schedule_interval(update, interval=1/60)
    pyglet.app.run()
