import pygame
from pygame import *
from math import sin, cos, radians, sqrt

INIT = False
OBS = []
PLANEZ = 0
WIDTH = 0
HEIGHT = 0


objs = []

EMPTY_MATRIX = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

BASE_MATRIX = [
    [1,0,0],
    [0,1,0],
    [0,0,1]
]



def run(baseactions=[], keyactions={}, bg="white", basefps=60, surf=None, drawhidden=False):
    if surf == None:
        surf = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    fps = basefps
    drawhidden = drawhidden

    run = True
    pause = False
    while run:
        if not pause:
            surf.fill(bg)

            for fun in baseactions:
                fun()

            drawall(surf, drawhidden)
                
            pygame.display.update()
            clock.tick(fps)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                for key in keyactions.keys():
                    if event.key == key:
                        keyactions[key]()
                if event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_RIGHT:
                    fps+=10
                elif event.key == pygame.K_LEFT:
                    fps-=10
                elif event.key == pygame.K_o:
                    drawhidden = not drawhidden


def drawall(surf: pygame.Surface, drawhidden=False):
    if drawhidden:
        for obj in objs:
            obj.draw(surf)
    else:
        for obj in objs:
            if not obj.hidden:
                obj.draw(surf)


def getrotation(degrees: float, axis: str) -> list[list[float]]:
    trsf = []
    axis = axis.lower()
    
    if axis == "x":
        trsf = [
        [1, 0, 0],
        [0, cos(radians(degrees)), -sin(radians(degrees))],
        [0, sin(radians(degrees)), cos(radians(degrees))]
        ]
    elif axis == "y":
        trsf = [
        [cos(radians(degrees)), 0, sin(radians(degrees))],
        [0, 1, 0],
        [-sin(radians(degrees)), 0, cos(radians(degrees))]
        ]
    elif axis == "z":
        trsf = [
        [cos(radians(degrees)), -sin(radians(degrees)), 0],
        [sin(radians(degrees)), cos(radians(degrees)), 0],
        [0, 0, 1]
        ]
    else:
        raise ValueError("Inserted axis is not valid")
    
    return trsf


def combinetransformation(trsf: list[list[float]], *trsfs: list[list[float]]) -> list[list[float]]:
    temp = EMPTY_MATRIX
    for tr in trsfs:
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    temp[i][j] += tr[i][k]*trsf[k][j]
        trsf = temp
        temp = EMPTY_MATRIX
    return trsf


def init(size=(600,600), obs=[0,0,800], planez=500):
    global INIT, OBS, PLANEZ, WIDTH, HEIGHT
    INIT = True
    OBS = obs
    PLANEZ = planez
    WIDTH = size[0]
    HEIGHT = size[1]
    pygame.init()


def setobs(vector: list[float]):
    global OBS
    for i in range(3):
        OBS[i] = vector[i]
        
        
def getobs() -> list[float]:
    return OBS
        
        
def setplane(z: float):
    global PLANEZ
    PLANEZ = z
    
    
def getplane() -> float:
    return PLANEZ


def setsize(size: list[int]):
    global WIDTH, HEIGHT
    WIDTH = size[0]
    HEIGHT = size[1]
    
    
def getsize() -> list[int]:
    return [WIDTH, HEIGHT]
    
    
def topygame(vector: list[float]) -> list[float]:
    return [int(vector[0]+WIDTH/2), HEIGHT-int(vector[1]+HEIGHT/2)]



class Dot():
    def __init__(self, pos: list[float], color="black", width=2, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        
        if len(pos) != 3:
            raise ValueError("Dot does not have 3 dimensional coordinates")
        objs.append(self)
        self.pos = list(pos)
        self.color = color
        self.width = width
        self.hidden = hidden
        self.finalpos = topygame(self.project(self.pos, PLANEZ, OBS))
        
    def project(self, vector: list[float], planeZ: float, obs: list[float]) -> list[float]:
        return [((vector[0]-obs[0]) * (obs[2]-planeZ)) / (obs[2]-vector[2]), ((vector[1]-obs[1]) * (obs[2]-planeZ)) / (obs[2]-vector[2])]
    
    def transform(self, transformation: list[list[float]]):
        temp = [0,0,0]
        
        for i in range(3):
            for j in range(3):
                temp[i] += transformation[i][j]*self.pos[j]
                
        self.pos = temp
        self.finalpos = topygame(self.project(self.pos, PLANEZ, OBS))
        
    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, self.color, self.finalpos, self.width)

    def kill(self):
        objs.remove(self)

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

        
        
class RelativeDot(Dot):
    def __init__(self, center: list[float], vector: list[float], color="black", width=2, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        
        if len(vector) != 3 or len(center) != 3:
            raise ValueError("Dot does not have 3 dimensional coordinates")
        objs.append(self)
        self.center = list(center)
        self.vector = list(vector)
        self.color = color
        self.width = width
        self.hidden = hidden
        
        self.updatefinalpos()

    def changecenterip(self, newcenter: list[float]):
        for i in range(3):
            self.vector[i] += newcenter[i]-self.center[i]
        self.center = newcenter
        
    def updatefinalpos(self):
        self.finalpos = topygame(self.project([self.center[i]+self.vector[i] for i in range(3)], PLANEZ, OBS))
        
    def transform(self, transformation):
        temp = [0,0,0]
        
        for i in range(3):
            for j in range(3):
                temp[i] += transformation[i][j]*self.vector[j]
                
        self.vector = temp
        self.updatefinalpos()
        


class Line():
    def __init__(self, dot1: Dot, dot2: Dot, width=1, color="black", hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        objs.append(self)
        self.vertices = [dot1, dot2]
        self.width = width
        self.color = color
        self.hidden = hidden
        
    def draw(self, surf: pygame.Surface):
        pygame.draw.line(surf, self.color, self.vertices[0].finalpos, self.vertices[1].finalpos, self.width)

    def kill(self):
        objs.remove(self)
    
    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False
        
        
class Polyhedron():
    def __init__(self, reldots: list[RelativeDot], lines: list[Line], center: list[float], dotcolor="", linecolor="", dotwidth=2, linewidth=1, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        
        self.dots = reldots
        self.lines = lines
        self.center = center
        self.dotcolor = dotcolor
        self.linecolor = linecolor
        self.dotwidth = dotwidth
        self.linewidth = linewidth
        self.hidden = hidden
        
        if dotcolor:
            for i in range(len(self.dots)):
                self.dots[i].color = self.dotcolor
                self.dots[i].width = self.dotwidth
                
        if linecolor:
            for i in range(len(self.lines)):
                self.lines[i].color = self.linecolor
                self.lines[i].width = self.linewidth
                
        if hidden:
            for i in range(len(self.dots)):
                self.dots[i].hidden = self.hidden
                
            for i in range(len(self.lines)):
                self.lines[i].hidden = self.hidden
                
                
        
    def setcenter(self, center: list[float]):
        self.center = center
        
    def getcenter(self) -> list[float]:
        return self.center
    
    def move(self, vector: list[float]):
        for i in range(3):
            self.center[i] += vector[i]
            
        for j in range(len(self.dots)):
            self.dots[j].center = self.center
            self.dots[j].updatefinalpos()

    def rotate(self, spd: float, axis: str):
        trsf = getrotation(spd, axis)
        self.relativetransform(trsf)

    def revolve(self, spd: float, axis: str):
        trsf = getrotation(spd, axis)
        self.absolutetransform(trsf)
            
    def relativetransform(self, transformation: list[list[float]]):
        for dot in self.dots:
            dot.transform(transformation)
            
    def absolutetransform(self, transformation: list[list[float]]):
        temp = [0,0,0]
        
        for i in range(3):
            for j in range(3):
                temp[i] += transformation[i][j]*self.center[j]
                
        self.center = temp
        
        for i in range(len(self.dots)):
            self.dots[i].center = self.center
            self.dots[i].updatefinalpos()
            
    def scale(self, factors: list[float]):
        if type(factors) == float:
            factors = [factors for i in range(3)]
            
        trsf = [
            [factors[0],0,0],
            [0,factors[1],0],
            [0,0,factors[2]]
        ]
        self.relativetransform(trsf)
        
            
    def draw(self, surf: pygame.Surface):
        for dot in self.dots:
            dot.draw(surf)
            
        for line in self.lines:
            line.draw(surf)
    
    def hide(self):
        for dot in self.dots:
            dot.hidden = True
        for line in self.lines:
            line.hidden = True
        self.hidden = True

    def show(self):
        for dot in self.dots:
            dot.hidden = False
        for line in self.lines:
            line.hidden = False
        self.hidden = False
            


# TODO: possibly add analogic sphere
class Sphere(Polyhedron):
    def __init__(self, center: list[float], r: float, dotcolor="black", linecolor="black", dotwidth=2, linewidth=1, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")

        self.dots = [
            RelativeDot(center,(r,0,0)),
            RelativeDot(center,(cos(radians(30))*r,0,-sin(radians(30))*r)),
            RelativeDot(center,(cos(radians(60))*r,0,-sin(radians(60))*r)),
            RelativeDot(center,(0,0,-r)),
            RelativeDot(center,(cos(radians(120))*r,0,-sin(radians(120))*r)),
            RelativeDot(center,(cos(radians(150))*r,0,-sin(radians(150))*r)),
            RelativeDot(center,(-r,0,0)),
            RelativeDot(center,(cos(radians(210))*r,0,-sin(radians(210))*r)),
            RelativeDot(center,(cos(radians(240))*r,0,-sin(radians(240))*r)),
            RelativeDot(center,(0,0,r)),
            RelativeDot(center,(cos(radians(300))*r,0,-sin(radians(300))*r)),
            RelativeDot(center,(cos(radians(330))*r,0,-sin(radians(330))*r)),

            RelativeDot(center,(0,r,0)),
            RelativeDot(center,(0,cos(radians(30))*r,sin(radians(30))*r)),
            RelativeDot(center,(0,cos(radians(60))*r,sin(radians(60))*r)),
            RelativeDot(center,(0,0,r)),
            RelativeDot(center,(0,cos(radians(120))*r,sin(radians(120))*r)),
            RelativeDot(center,(0,cos(radians(150))*r,sin(radians(150))*r)),
            RelativeDot(center,(0,-r,0)),
            RelativeDot(center,(0,cos(radians(210))*r,sin(radians(210))*r)),
            RelativeDot(center,(0,cos(radians(240))*r,sin(radians(240))*r)),
            RelativeDot(center,(0,0,-r)),
            RelativeDot(center,(0,cos(radians(300))*r,sin(radians(300))*r)),
            RelativeDot(center,(0,cos(radians(330))*r,sin(radians(330))*r)),

            RelativeDot(center,(r,0,0)),
            RelativeDot(center,(cos(radians(30))*r,sin(radians(30))*r,0)),
            RelativeDot(center,(cos(radians(60))*r,sin(radians(60))*r,0)),
            RelativeDot(center,(0,r,0)),
            RelativeDot(center,(cos(radians(120))*r,sin(radians(120))*r,0)),
            RelativeDot(center,(cos(radians(150))*r,sin(radians(150))*r,0)),
            RelativeDot(center,(-r,0,0)),
            RelativeDot(center,(cos(radians(210))*r,sin(radians(210))*r,0)),
            RelativeDot(center,(cos(radians(240))*r,sin(radians(240))*r,0)),
            RelativeDot(center,(0,-r,0)),
            RelativeDot(center,(cos(radians(300))*r,sin(radians(300))*r,0)),
            RelativeDot(center,(cos(radians(330))*r,sin(radians(330))*r,0)),
        ]
        
        self.lines = [
            Line(self.dots[11], self.dots[0]),
            Line(self.dots[0], self.dots[1]),
            Line(self.dots[1], self.dots[2]),
            Line(self.dots[2], self.dots[3]),
            Line(self.dots[3], self.dots[4]),
            Line(self.dots[4], self.dots[5]),
            Line(self.dots[5], self.dots[6]),
            Line(self.dots[6], self.dots[7]),
            Line(self.dots[7], self.dots[8]),
            Line(self.dots[8], self.dots[9]),
            Line(self.dots[9], self.dots[10]),
            Line(self.dots[10], self.dots[11]),

            Line(self.dots[23], self.dots[12]),
            Line(self.dots[12], self.dots[13]),
            Line(self.dots[13], self.dots[14]),
            Line(self.dots[14], self.dots[15]),
            Line(self.dots[15], self.dots[16]),
            Line(self.dots[16], self.dots[17]),
            Line(self.dots[17], self.dots[18]),
            Line(self.dots[18], self.dots[19]),
            Line(self.dots[19], self.dots[20]),
            Line(self.dots[20], self.dots[21]),
            Line(self.dots[21], self.dots[22]),
            Line(self.dots[22], self.dots[23]),

            Line(self.dots[35], self.dots[24]),
            Line(self.dots[24], self.dots[25]),
            Line(self.dots[25], self.dots[26]),
            Line(self.dots[26], self.dots[27]),
            Line(self.dots[27], self.dots[28]),
            Line(self.dots[28], self.dots[29]),
            Line(self.dots[29], self.dots[30]),
            Line(self.dots[30], self.dots[31]),
            Line(self.dots[31], self.dots[32]),
            Line(self.dots[32], self.dots[33]),
            Line(self.dots[33], self.dots[34]),
            Line(self.dots[34], self.dots[35]),
        ]
        
        super().__init__(self.dots, self.lines, center, dotcolor, linecolor, dotwidth, linewidth, hidden)
            
            
            
class Cube(Polyhedron):
    def __init__(self, center: list[float], size: float, dotcolor="black", linecolor="black", dotwidth=2, linewidth=1, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        
        self.dots = [
            RelativeDot(center,(size/2,size/2,size/2)),
            RelativeDot(center,(-size/2,size/2,size/2)),
            RelativeDot(center,(size/2,-size/2,size/2)),
            RelativeDot(center,(-size/2,-size/2,size/2)),
            RelativeDot(center,(size/2,size/2,-size/2)),
            RelativeDot(center,(-size/2,size/2,-size/2)),
            RelativeDot(center,(size/2,-size/2,-size/2)),
            RelativeDot(center,(-size/2,-size/2,-size/2))
        ]
        
        self.lines = [
            Line(self.dots[0], self.dots[4]),
            Line(self.dots[1], self.dots[5]),
            Line(self.dots[2], self.dots[6]),
            Line(self.dots[3], self.dots[7]),
            Line(self.dots[0], self.dots[1]),
            Line(self.dots[2], self.dots[3]),
            Line(self.dots[4], self.dots[5]),
            Line(self.dots[6], self.dots[7]),
            Line(self.dots[0], self.dots[2]),
            Line(self.dots[1], self.dots[3]),
            Line(self.dots[4], self.dots[6]),
            Line(self.dots[5], self.dots[7])
        ]
        
        super().__init__(self.dots, self.lines, center, dotcolor, linecolor, dotwidth, linewidth, hidden)

        

# TODO: make this actually regular
class Tetrahedron(Polyhedron):
    def __init__(self, center: list[float], size: float, dotcolor="black", linecolor="black", dotwidth=2, linewidth=1, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        
        sqrt2 = sqrt(2)
        self.dots = [
            RelativeDot(center,(size,0,-1/sqrt2)),
            RelativeDot(center,(-size,0,-1/sqrt2)),
            RelativeDot(center,(0,size,1/sqrt2)),
            RelativeDot(center,(0,-size,1/sqrt2)),
        ]
        
        self.lines = [
            Line(self.dots[0], self.dots[1]),
            Line(self.dots[0], self.dots[2]),
            Line(self.dots[0], self.dots[3]),
            Line(self.dots[1], self.dots[2]),
            Line(self.dots[1], self.dots[3]),
            Line(self.dots[2], self.dots[3]),
        ]
        
        super().__init__(self.dots, self.lines, center, dotcolor, linecolor, dotwidth, linewidth, hidden)


class Cylinder(Polyhedron):
    def __init__(self, center: list[float], r: float, height: float, dotcolor="black", linecolor="black", dotwidth=2, linewidth=1, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")
        
        self.dots = [
            RelativeDot(center,(r,height/2,0)),
            RelativeDot(center,(cos(radians(30))*r,height/2,-sin(radians(30))*r)),
            RelativeDot(center,(cos(radians(60))*r,height/2,-sin(radians(60))*r)),
            RelativeDot(center,(0,height/2,-r)),
            RelativeDot(center,(cos(radians(120))*r,height/2,-sin(radians(120))*r)),
            RelativeDot(center,(cos(radians(150))*r,height/2,-sin(radians(150))*r)),
            RelativeDot(center,(-r,height/2,0)),
            RelativeDot(center,(cos(radians(210))*r,height/2,-sin(radians(210))*r)),
            RelativeDot(center,(cos(radians(240))*r,height/2,-sin(radians(240))*r)),
            RelativeDot(center,(0,height/2,r)),
            RelativeDot(center,(cos(radians(300))*r,height/2,-sin(radians(300))*r)),
            RelativeDot(center,(cos(radians(330))*r,height/2,-sin(radians(330))*r)),

            RelativeDot(center,(r,-height/2,0)),
            RelativeDot(center,(cos(radians(30))*r,-height/2,-sin(radians(30))*r)),
            RelativeDot(center,(cos(radians(60))*r,-height/2,-sin(radians(60))*r)),
            RelativeDot(center,(0,-height/2,-r)),
            RelativeDot(center,(cos(radians(120))*r,-height/2,-sin(radians(120))*r)),
            RelativeDot(center,(cos(radians(150))*r,-height/2,-sin(radians(150))*r)),
            RelativeDot(center,(-r,-height/2,0)),
            RelativeDot(center,(cos(radians(210))*r,-height/2,-sin(radians(210))*r)),
            RelativeDot(center,(cos(radians(240))*r,-height/2,-sin(radians(240))*r)),
            RelativeDot(center,(0,-height/2,r)),
            RelativeDot(center,(cos(radians(300))*r,-height/2,-sin(radians(300))*r)),
            RelativeDot(center,(cos(radians(330))*r,-height/2,-sin(radians(330))*r))
        ]

        self.lines = [
            Line(self.dots[11], self.dots[0]),
            Line(self.dots[0], self.dots[1]),
            Line(self.dots[1], self.dots[2]),
            Line(self.dots[2], self.dots[3]),
            Line(self.dots[3], self.dots[4]),
            Line(self.dots[4], self.dots[5]),
            Line(self.dots[5], self.dots[6]),
            Line(self.dots[6], self.dots[7]),
            Line(self.dots[7], self.dots[8]),
            Line(self.dots[8], self.dots[9]),
            Line(self.dots[9], self.dots[10]),
            Line(self.dots[10], self.dots[11]),

            Line(self.dots[23], self.dots[12]),
            Line(self.dots[12], self.dots[13]),
            Line(self.dots[13], self.dots[14]),
            Line(self.dots[14], self.dots[15]),
            Line(self.dots[15], self.dots[16]),
            Line(self.dots[16], self.dots[17]),
            Line(self.dots[17], self.dots[18]),
            Line(self.dots[18], self.dots[19]),
            Line(self.dots[19], self.dots[20]),
            Line(self.dots[20], self.dots[21]),
            Line(self.dots[21], self.dots[22]),
            Line(self.dots[22], self.dots[23]),

            Line(self.dots[0], self.dots[12]),
            Line(self.dots[1], self.dots[13]),
            Line(self.dots[2], self.dots[14]),
            Line(self.dots[3], self.dots[15]),
            Line(self.dots[4], self.dots[16]),
            Line(self.dots[5], self.dots[17]),
            Line(self.dots[6], self.dots[18]),
            Line(self.dots[7], self.dots[19]),
            Line(self.dots[8], self.dots[20]),
            Line(self.dots[9], self.dots[21]),
            Line(self.dots[10], self.dots[22]),
            Line(self.dots[11], self.dots[23]),
        ]

        super().__init__(self.dots, self.lines, center, dotcolor, linecolor, dotwidth, linewidth, hidden)


class Parallelopiped(Polyhedron):
    def __init__(self, center: list[float], sizes: list[float], dotcolor="black", linecolor="black", dotwidth=2, linewidth=1, hidden=False):
        if not INIT:
            raise PermissionError("Module was not initialized correctly")

        self.dots = [
            RelativeDot(center,(sizes[0]/2,sizes[1]/2,sizes[2]/2)),
            RelativeDot(center,(-sizes[0]/2,sizes[1]/2,sizes[2]/2)),
            RelativeDot(center,(sizes[0]/2,-sizes[1]/2,sizes[2]/2)),
            RelativeDot(center,(-sizes[0]/2,-sizes[1]/2,sizes[2]/2)),
            RelativeDot(center,(sizes[0]/2,sizes[1]/2,-sizes[2]/2)),
            RelativeDot(center,(-sizes[0]/2,sizes[1]/2,-sizes[2]/2)),
            RelativeDot(center,(sizes[0]/2,-sizes[1]/2,-sizes[2]/2)),
            RelativeDot(center,(-sizes[0]/2,-sizes[1]/2,-sizes[2]/2))
        ]
        
        self.lines = [
            Line(self.dots[0], self.dots[4]),
            Line(self.dots[1], self.dots[5]),
            Line(self.dots[2], self.dots[6]),
            Line(self.dots[3], self.dots[7]),
            Line(self.dots[0], self.dots[1]),
            Line(self.dots[2], self.dots[3]),
            Line(self.dots[4], self.dots[5]),
            Line(self.dots[6], self.dots[7]),
            Line(self.dots[0], self.dots[2]),
            Line(self.dots[1], self.dots[3]),
            Line(self.dots[4], self.dots[6]),
            Line(self.dots[5], self.dots[7])
        ]

        super().__init__(self.dots, self.lines, center, dotcolor, linecolor, dotwidth, linewidth, hidden)


def combinepoly(center: list[float], *polys: Polyhedron) -> Polyhedron:
    dots = []
    lines = []

    for poly in polys:
        for dot in poly.dots:
            dot.changecenterip(center)
            dots.append(dot)
        for line in poly.lines:
            lines.append(line)
        del poly

    return Polyhedron(dots, lines, center)
