import button
import pygame
import math

pygame.init()

# set window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit")

start_img = pygame.image.load('start-button.png')
start_button = button.Button(320, 320, start_img, 0.3)

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (100, 98, 101)
WHITE = (255, 255, 255)
DARK_RED = (128, 0, 0)
BROWN = (210,105,30)
LIGHT_BLUE = (0,191,255)
DARK_BLUE = (72,61,139)

FONT = pygame.font.SysFont("comicsans", 16)

# planet initialization
class Planet:

    # astronomical unit
    AU = 149.6e6 * 1000

    # gravitational constant
    G = 6.67428e-11

    # 1 AU = 100 pixel
    # or scale 50 / AU
    SCALE = 250 / AU

    # 1 day
    TIMESTEP = 3600*24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    # scaling distance and center
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        

        # drawing orbit
        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # drawing planet
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # displaying distance to sun
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2,y - distance_text.get_width() / 2))

    # moving planets
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance
        
        # straight force
        force = self.G * self.mass * other.mass / distance**2

        # angle
        theta = math.atan2(distance_y, distance_x)

        # x,y force
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    # forces of other planets
    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # velocity F = m * a -> a = F / m
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # update with velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    while run:
        WIN.fill(BLACK)
        if start_button.draw(WIN):
            play()

        # exit window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    

# main loop
def play():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)  # or diameter 5
    sun.sun = True  

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23) # or diameter 3
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24) # or diameter 7
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24) # or diameter 8
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23) # or diameter 4
    mars.y_vel = 24.077 * 1000

    # second stage
    jupiter = Planet(5.203 * Planet.AU, 0, 88, DARK_RED, 1.90 * 10**27)
    jupiter.y_vel = 13.1 * 1000

    saturn = Planet(9.539 * Planet.AU, 0, 74, BROWN, 5.69 * 10**26)
    saturn.y_vel = 9.7 * 1000

    uranus = Planet(19.18 * Planet.AU, 0, 32, LIGHT_BLUE, 8.68 * 10*25)
    uranus.y_vel = 6.8 * 1000

    neptune = Planet(30.06 * Planet.AU, 0, 30, DARK_BLUE, 1.02 * 10**26)
    neptune.y_vel = 5.4 * 1000

    planets1 = [sun, mercury, venus, earth, mars]
    planets2 = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:

        # max 60 fps
        clock.tick(60)

        # black background
        WIN.fill(BLACK)

        # exit window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # draw planets1 or planets 2
        for planet in planets1:
            planet.update_position(planets1)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()