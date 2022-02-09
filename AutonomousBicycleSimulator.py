import pygame
import math
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([1600,800])
pygame.display.set_caption("Autonomous Bicycle Model")
done = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
waypoints = []
obstacles = []

def rect(x, y, angle, w, h):
    return [rotate(x, y, angle, -w/2,  h/2),
            rotate(x, y, angle,  w/2,  h/2),
            rotate(x, y, angle,  w/2, -h/2),
            rotate(x, y, angle, -w/2, -h/2)]
def rotate(x, y, angle, px, py):
    x1 = x + px * math.cos(angle) - py * math.sin(angle)
    y1 = y + px * math.sin(angle) + py * math.cos(angle)
    return [x1, y1]


def distanceFUNC(vehicle,waypoint):
    return math.sqrt(abs(waypoint.x - vehicle.x)**2 + abs(waypoint.y - vehicle.y)**2)





class Bike(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3
        self.theta = 0
        self.delta = 0
        self.length = 80
        self.desiredtheta = 0
    def track(self):
        if len(obstacles) == 0:
            self.desiredtheta = math.atan2(-(waypoints[0].y - self.y), waypoints[0].x- self.x)
        else:
            obstaclespresent = False
            for obstacle in obstacles:
                if abs(math.atan2(-(waypoints[0].y - self.y), waypoints[0].x- self.x) - math.atan2(-(obstacle.y - self.y), obstacle.x- self.x)) < .70:
                    obstaclespresent = True
                    if math.atan2(-(waypoints[0].y - self.y), waypoints[0].x- self.x) > math.atan2(-(obstacle.y - self.y), obstacle.x- self.x):
                        self.desiredtheta = math.atan2(-(waypoints[0].y - self.y), waypoints[0].x- self.x) + .70
                    else:
                        self.desiredtheta = math.atan2(-(waypoints[0].y - self.y), waypoints[0].x- self.x) - .70
            if not obstaclespresent:
                self.desiredtheta = math.atan2(-(waypoints[0].y - self.y), waypoints[0].x- self.x)
    def update(self):
        if len(waypoints) > 0:
            
            self.x += self.vel * math.cos(-self.theta - self.delta)
            self.y += self.vel * math.sin(-self.theta - self.delta)
            self.theta += (self.vel / self.length) * math.tan(self.delta)
            
            if self.theta > math.pi:
                self.theta -= 2 * math.pi
            elif self.theta < -math.pi:
                self.theta += 2 * math.pi
            
            self.track()
            if distanceFUNC(self, waypoints[0]) < 100 and distanceFUNC(self, waypoints[0]) > 35:
                if abs(self.desiredtheta - self.theta) > .66:
                    self.delta = 0
                    self.vel = -2
            elif abs(self.desiredtheta - self.theta) >= 3.0:
                if self.desiredtheta - self.theta > 0:
                    self.vel = -2
                    self.delta = .5 
                else:
                    self.vel = -2
                    self.delta = -.5 
            else:
                self.vel = 3
                if self.desiredtheta < self.theta:
                    self.delta = self.desiredtheta - self.theta
                    if self.delta < -.66:
                        self.delta = -.66
                elif self.desiredtheta > self.theta:
                    self.delta = self.desiredtheta - self.theta
                    if self.delta > .66:
                        self.delta = .66
                else:
                    self.delta = 0

            if distanceFUNC(self,waypoints[0]) < 30:
                waypoints.pop(0)
            
    def show_metrics(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
 
        theta = font.render("Vehicle Theta: " + str(self.theta), False, BLACK)
        screen.blit(theta,(0,10))
        delta = font.render("Vehicle Delta: " + str(self.delta), False, BLACK)
        screen.blit(delta,(0,35))
        if len(waypoints) > 0:
            distance = font.render("Distance to point: " + str(distanceFUNC(self, waypoints[0])), False, BLACK)
            screen.blit(distance,(0,60))
            desiredtheta = font.render("Desired Theta: " + str(self.desiredtheta), False, BLACK)
            screen.blit(desiredtheta,(0,85))

    def show_vehicle(self):
        pygame.draw.polygon(screen, BLACK, rect(self.x - (self.length/2) * math.cos(-self.theta),
                                                self.y - (self.length/2) * math.sin(-self.theta),
                                                -self.theta, self.length, 10))
        pygame.draw.polygon(screen, BLUE, rect(self.x - self.length * math.cos(-self.theta),
                                                self.y - self.length * math.sin(-self.theta),
                                                -self.theta, 40, 8))
        pygame.draw.polygon(screen, BLUE, rect(self.x, self.y, -self.delta - self.theta, 40, 8))

class WayPoint(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def show(self):
        pygame.draw.circle(screen,GREEN, (self.x, self.y), 10)


class Obstacle(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def show(self):
        pygame.draw.circle(screen,RED, (self.x, self.y), 20)
#waypoints.append(WayPoint(1500,700))

player = Bike(100,100)


while done == False:

    clock.tick(35 )
    screen.fill((WHITE))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()
        waypoints.append(WayPoint(x,y))
    if pygame.mouse.get_pressed()[2]:
        x,y = pygame.mouse.get_pos()
        obstacles.append(Obstacle(x,y))

    if len(waypoints) > 0:  
        for waypoint in waypoints:
            waypoint.show()
    if len(obstacles) > 0:  
        for obstacle in obstacles:
            obstacle.show()
    player.update()
    player.show_vehicle()
    player.show_metrics()
    
    pygame.display.flip()