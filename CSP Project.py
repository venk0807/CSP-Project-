import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
# comment 
# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 49, 237)
RED = (188, 39, 50)
GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 18)

# Define the Planet class
class Planet:
    # Constants for the simulation
    AU = 146.6e6 * 1000
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU  # Scale for visualization
    TIMESTEP = 3600 * 24  # Time step for simulation (1 day)

    # Initialize the planet object
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        # Properties related to orbiting
        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        # Initial velocity components
        self.x_vel = 0
        self.y_vel = 0

    # Draw the planet on the window
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw orbit path if available
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2)) 
                     

        # Draw the planet as a circle
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    # Calculate gravitational attraction between planets
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance_sq = distance_x ** 2 + distance_y ** 2  # Squared distance
        
        if other.sun: 
            self.distance_to_sun = math.sqrt(distance_sq)  # Store distance to the sun
            
        force = self.G * self.mass * other.mass / distance_sq
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force 
        force_y = math.sin(theta) * force 
        return force_x, force_y
    
    # Update the position of the planet based on gravitational forces
    def update_position(self, planets):
        total_fx = total_fy = 0 
        for planet in planets: 
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocity and position
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP 
        self.y += self.y_vel * self.TIMESTEP 
        self.orbit.append((self.x, self.y))

# Main function for running the simulation
def main():
    run = True 
    clock = pygame.time.Clock()

    # Create Sun and planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30) 
    sun.sun = True 

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 0.30 * 10**24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    # Main game loop
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # key to add a new planet
                    try:
                        weight = float(input("Enter the weight of the new planet: ")) 
                        speed = float(input("Enter the speed of the new planet: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue  # Skip adding the planet and continue the loop

                    new_planet = Planet(0, 0, 10, (255, 255, 255), weight)
                    new_planet.x_vel = speed
                    planets.append(new_planet)

        # Update and draw each planet
        for planet in planets: 
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
        
    pygame.quit()

# Start the simulation
main()
