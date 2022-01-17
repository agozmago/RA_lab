import pygame, sys, csv, pandas as pd
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

clock = pygame.time.Clock()

settings = pd.read_csv('data/settings.csv', index_col=0, squeeze=True)
planets = pd.read_csv('data/planets.csv', index_col=0, comment='#')

images = ['data/textures/milky_way.jpg',
          'data/textures/sun.jpg', 
          'data/textures/mercury.jpg', 
          'data/textures/venus.jpg', 
          'data/textures/earth.jpg', 
          'data/textures/mars.jpg', 
          'data/textures/jupiter.jpg', 
          'data/textures/saturn.jpg', 
          'data/textures/uranus.jpg', 
          'data/textures/neptune.jpg',
          'data/textures/saturn_ring.png']

sphere = gluNewQuadric()
orbit = gluNewQuadric()
ring = gluNewQuadric()


def init_GL():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, (2, 1.5, 1, 0))
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 1))
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)


def load_textures(images):
    textures = glGenTextures(len(images))

    for image, texture in zip(images, textures):
        glBindTexture(GL_TEXTURE_2D, texture)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, 
                          pygame.image.load(image).get_width(), 
                          pygame.image.load(image).get_height(), 
                          GL_RGBA, GL_UNSIGNED_BYTE, 
                          pygame.image.tostring(pygame.image.load(image).convert_alpha(), 'RGBA', True))
    
    return textures


def scene():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, settings['width']/settings['height'], 0.1, 2000.0)
    gluLookAt(settings['eyeX'], settings['eyeY'], settings['eyeZ'], settings['centerX'], settings['centerY'], settings['centerZ'], 0,1,0)
    glMatrixMode(GL_MODELVIEW)


def draw_orbit(planet_name, planet_data, orbit):
    scale = planet_data['orbit_scale']
    glScalef(scale, scale, scale)
    glRotatef(90, 1, 0, 0)
    try:
        gluDisk(orbit, 1-0.02/scale, 1, 500, 1)
    except:
        gluDisk(orbit, 0, 0, 0, 1)
    glLoadIdentity()
            

def draw_planet(planet_name, planet_data, texture):
    global planets

    if planet_name == 'sky' or planet_name == 'sun':
        glDisable(GL_LIGHTING)
    else:
        glEnable(GL_LIGHTING)
        
    glBindTexture(GL_TEXTURE_2D, texture)

    translateX = planet_data['orbit_scale']*sin(radians(planet_data['curr_rev']))
    translateZ = planet_data['orbit_scale']*cos(radians(planet_data['curr_rev']))
    glTranslatef(translateX, 0, translateZ)

    glScalef(planet_data['size_scale'], planet_data['size_scale'], planet_data['size_scale'])

    glRotatef(planet_data['curr_rot'], planet_data['rot_axX'], planet_data['rot_axY'], planet_data['rot_axZ'])
    glRotatef(-90, planet_data['tiltX'], planet_data['tiltY'], planet_data['tiltZ'])

    gluQuadricTexture(sphere, True)
    gluSphere(sphere, 1.0, 64, 16)

    if planet_name == 'saturn':
        glBindTexture(GL_TEXTURE_2D, textures[-1])
        gluQuadricTexture(ring, True)
        gluDisk(ring, 1.3, 2.1, 100, 1)
    
    glLoadIdentity()

    planets.loc[planet_name, 'curr_rev'] += 0.1*planet_data['revolution_step']
    planets.loc[planet_name, 'curr_rot'] += 0.1*planet_data['rotation_step']


def draw(planets, textures):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for planet in planets.iterrows():
        draw_orbit(*planet, orbit)
    
    for planet, texture in zip(planets.iterrows(), textures):
        draw_planet(*planet, texture)
        
    pygame.display.flip()


def keys():
    global settings

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        settings['eyeX'] += (sin(radians(settings['mouseAngleX']))*cos(radians(settings['mouseAngleY'])))
        settings['eyeY'] += sin(radians(settings['mouseAngleY']))
        settings['eyeZ'] += (cos(radians(settings['mouseAngleX']))*cos(radians(settings['mouseAngleY'])))
    elif key[pygame.K_s]:
        settings['eyeX'] -= (sin(radians(settings['mouseAngleX']))*cos(radians(settings['mouseAngleY'])))
        settings['eyeY'] -= sin(radians(settings['mouseAngleY']))
        settings['eyeZ'] -= (cos(radians(settings['mouseAngleX']))*cos(radians(settings['mouseAngleY'])))
    if key[pygame.K_a]:
        settings['eyeX'] += (sin(radians(settings['mouseAngleX']+90)))
        settings['eyeZ'] += (cos(radians(settings['mouseAngleX']+90)))
    elif key[pygame.K_d]:
        settings['eyeX'] += (sin(radians(settings['mouseAngleX']-90)))
        settings['eyeZ'] += (cos(radians(settings['mouseAngleX']-90)))
    
    mouseMove = pygame.mouse.get_rel()
    settings['mouseAngleX'] -= mouseMove[0]/10
    settings['mouseAngleY'] -= mouseMove[1]/10

    settings['centerX'] = settings['eyeX'] + (sin(radians(settings['mouseAngleX']))*cos(radians(settings['mouseAngleY'])))
    settings['centerY'] = settings['eyeY'] + sin(radians(settings['mouseAngleY']))
    settings['centerZ'] = settings['eyeZ'] + (cos(radians(settings['mouseAngleX']))*cos(radians(settings['mouseAngleY'])))
    

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((int(settings['width']), int(settings['height'])), pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.event.set_grab(1)
    pygame.mouse.set_visible(0)
    init_GL()
    textures = load_textures(images)

    while True:
        keys()
        clock.tick(30)
        scene()
        draw(planets, textures)
