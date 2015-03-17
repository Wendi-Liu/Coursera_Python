# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
CW = 0.1
CCW = -CW
ON = True
OFF = False
ship_acc = 0.15
friction = 0.01
missile_speed = 3
speed_increment = 0.01
lives = 3
score = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# helper functions to process group of sprites
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        if not sprite.update():
            sprite_group.remove(sprite)
        
def group_collide(sprite_group, other_object): #rock/ship collide
    for sprite in set(sprite_group):
        if sprite.collide(other_object):
            sprite_group.discard(sprite)
            an_explosion = Sprite(sprite.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            return True
    return False

def group_group_collide(sprite_group, other_group): #rock/missile collide
    num = len(sprite_group)
    for other_sprite in set(other_group):
        if group_collide(sprite_group, other_sprite):
            other_group.discard(other_sprite)
    return num - len(sprite_group)
                        


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, angle_vel, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_angle_vel(self):
        return self.angle_vel
    
    def draw(self, canvas):
        canvas.draw_image(ship_image, (self.image_center[0] + self.thrust * self.image_size[0], self.image_center[1]),
                          self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] = (self.vel[0] + self.thrust * ship_acc * angle_to_vector(self.angle)[0]) * ( 1 - friction)
        self.vel[1] = (self.vel[1] + self.thrust * ship_acc * angle_to_vector(self.angle)[1]) * ( 1 - friction)
        self.angle += self.angle_vel
        
    def rotate(self, delta_vel):
        self.angle_vel += delta_vel
      
    def flip_thrust(self, state):
        self.thrust = state
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        missile_pos = (self.pos[0] + angle_to_vector(self.angle)[0] * self.image_size[0] / 2, self.pos[1] + angle_to_vector(self.angle)[1] * self.image_size[0] / 2)
        missile_vel = (self.vel[0] + angle_to_vector(self.angle)[0] * missile_speed, self.vel[1] + angle_to_vector(self.angle)[1] * missile_speed)
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.speed = math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, (self.image_center[0] + self.age * self.image_size[0], self.image_center[1]),
                              self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age > self.lifespan:
            return False
        else:
            return True
        
    def increment_speed(self, par):
        self.vel[0] += par * speed_increment * self.vel[0] / self.speed
        self.vel[1] += par * speed_increment * self.vel[1] / self.speed

    def collide(self, other_object):
        other_pos = other_object.get_position()
        other_radius = other_object.get_radius()
        if dist(self.pos, other_pos) < self.radius + other_radius:
            return True
        else:
            return False

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()        
            
def draw(canvas):
    global time
    global score, lives, started
    global my_ship, rock_group, missile_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw and update ship and sprites
    my_ship.draw(canvas)    
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # draw user interface
    if group_collide(rock_group, my_ship):
        lives -= 1
    gain = group_group_collide(rock_group, missile_group)
    if gain != 0:
        for rock in rock_group:
            rock.increment_speed(gain)
    score += gain
    canvas.draw_text("lives = " + str(lives), (WIDTH / 30, HEIGHT / 15), 30, 'White')
    canvas.draw_text("score = " + str(score), (24 * WIDTH / 30, HEIGHT / 15), 30, 'White')
    
    if lives == 0: # restart if live runs out
        started = False
        angle_vel = my_ship.get_angle_vel()
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, angle_vel, ship_image, ship_info)
        for rock in set(rock_group):
            rock_group.remove(rock)
        for missile in set(missile_group):
            missile_group.remove(missile)
        lives = 3
        score = 0
        soundtrack.rewind()
        
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
def key_down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.rotate(CCW)
    if key == simplegui.KEY_MAP['right']:
        my_ship.rotate(CW)
    if key == simplegui.KEY_MAP['up']:
        my_ship.flip_thrust(ON)
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def key_up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.rotate(CW)
    if key == simplegui.KEY_MAP['right']:
        my_ship.rotate(CCW)
    if key == simplegui.KEY_MAP['up']:
        my_ship.flip_thrust(OFF)
            
# timer handler that spawns a rock    
def rock_spawner():
    if len(rock_group) <= 12 and started:
        while True:
            size = asteroid_info.get_size()
            pos = (random.randrange(size[0], WIDTH - size[0]), random.randrange(size[1], WIDTH - size[1]))
            vel = (random.randrange(-1, 3, 2) * random.random(), random.randrange(-1, 3, 2) * random.random())
            angle_vel = 0.1 * random.randrange(-1, 3, 2) * random.random()
            a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
            if not a_rock.collide(my_ship): #make sure the newly added rock isn't on top of our ship
                break
        rock_group.add(a_rock)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()


# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
