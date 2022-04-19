import sys, pygame, math
import numpy as np

class ImproperUse(Exception):
    pass

if len(sys.argv) == 1:
    BkgImage = False
elif len(sys.argv) == 2:
    BkgImage = True
else:
    raise ImproperUse("Improper use of arguments, please use: Micr0Desmos.py [image]")
    

pygame.init()
pygame.font.init()

size = width, height = 1080, 1080
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
purple = 255, 0, 255
blue = 0, 0, 255
green = 0, 255, 0

screen = pygame.display.set_mode(size)

if BkgImage:
    backgroundimg = pygame.image.load(sys.argv[1])
    backgroundimg = pygame.transform.scale(backgroundimg, size)
    imgrect = backgroundimg.get_rect()

def CalcFormulas(points, lines):
    pointsDes = []
    for point in points:
        if point != None:
            pointsDes.append((point[0],-point[1]))
        else:
            pointsDes.append(point)
    outputString = ""

    for line in lines:
        if pointsDes[line[0]] != None and pointsDes[line[1]] != None:
            vertical = False
            try:
                slope = (pointsDes[line[0]][1] - pointsDes[line[1]][1])/(pointsDes[line[0]][0] - pointsDes[line[1]][0])
            except ZeroDivisionError:
                vertical = True
                yvalues = (pointsDes[line[0]][1],pointsDes[line[1]][1])
                string = "x="+str(pointsDes[line[0]][0])+"\\left\\{"+str(min(yvalues))+"<y<"+str(max(yvalues))+"\\right\\}"
            if not vertical:
                offset = pointsDes[line[0]][1] - pointsDes[line[0]][0]*slope
                xvalues = (pointsDes[line[0]][0],pointsDes[line[1]][0])
                string = "y="+str(slope)+"x+"+str(offset)+"\\left\\{"+str(min(xvalues))+"<x<"+str(max(xvalues))+"\\right\\}"
            outputString+=string+"\n"

    for curve in curves:
        if pointsDes[curve[0]] != None and pointsDes[curve[1]] != None and pointsDes[curve[2]] != None:
            string = "\\left(\\left(1-t\\right)\\left(\\left(1-t\\right)("+str(pointsDes[curve[0]][0])+")+t("+str(pointsDes[curve[1]][0])+")\\right)+t\\left(\\left(1-t\\right)("+str(pointsDes[curve[1]][0])+")+t("+str(pointsDes[curve[2]][0])+")\\right),\\left(1-t\\right)\\left(\\left(1-t\\right)("+str(pointsDes[curve[0]][1])+")+t("+str(pointsDes[curve[1]][1])+")\\right)+t\\left(\\left(1-t\\right)("+str(pointsDes[curve[1]][1])+")+t("+str(pointsDes[curve[2]][1])+")\\right)\\right)"
            outputString+=string+"\n"
    print(outputString)
    
    for elipse in elipses:
        if pointsDes[elipse[0]] != None and pointsDes[elipse[1]] != None:
            a = (pointsDes[elipse[0]][0]-pointsDes[elipse[1]][0])/2
            b = (pointsDes[elipse[0]][1]-pointsDes[elipse[1]][1])/2
            h = (pointsDes[elipse[0]][0]+pointsDes[elipse[1]][0])/2
            k = (pointsDes[elipse[0]][1]+pointsDes[elipse[1]][1])/2
            string = "\\frac{\\left(x-("+str(h)+")\\right)^{2}}{("+str(a)+")^{2}}+\\frac{\\left(y-("+str(k)+")\\right)^{2}}{("+str(b)+")^{2}}=1"
            outputString+=string+"\n"
    print(outputString)

myfont = pygame.font.SysFont('Comic Sans MS', 30)


points = []
lines = []
curves = []
elipses = []

curveCount = 0
elipseCount = 0

mouse_pos = (size[0]/2,size[1]/2)

pygame.mouse.set_visible(False)

while 1:
    mouseUp = False
    mouseDown = False
    deletepoint = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouseUp = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                CalcFormulas(points, lines)
            if event.key == pygame.K_z:
                deletepoint = True
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_artificial = mouse_pos
    
    keys=pygame.key.get_pressed()

    
    linear = False
    if keys[pygame.K_x] and len(points) >= 1:
        linear = True
    else:
        if keys[pygame.K_c] and curveCount == 0:
            curveCount = 3
        else:
            if keys[pygame.K_v] and elipseCount == 0:
                elipseCount = 2

    snap = False
    if keys[pygame.K_LSHIFT]:
        snap = True

    try:
        if snap or deletepoint:
            mouse_x, mouse_y = mouse_pos
            mindist = width
            closestPoint = points[0]
            for point in points:
                if point != None:
                    dist = math.sqrt(abs(point[0]-mouse_x)**2+abs(point[1]-mouse_y)**2)
                    if dist < mindist:
                        mindist = dist
                        closestPoint = point
            mouse_pos_artificial = closestPoint
    except IndexError:
        pass
    
    if deletepoint:
        for point in points:
            if point == mouse_pos_artificial:
                index = points.index(point)
                points[index] = None
                for line in lines:
                    for pointl in line:
                        if pointl == index:
                            lines.remove(line)
                for curve in curves:
                    for pointc in curve:
                        if pointc == index:
                            curves.remove(curve)
                for elipse in elipses:
                    for pointe in elipse:
                        if pointe == index:
                            elipses.remove(elipse)

    if mouseUp:
        points.append(mouse_pos_artificial)
        if linear:
            lines.append((len(points)-2,len(points)-1))
        if curveCount == 3:
            curves.append((len(points)-1,len(points)+1,len(points)))
        if curveCount > 0:
            curveCount-=1
        if elipseCount == 2:
            elipses.append((len(points)-1,len(points)))
        if elipseCount > 0:
            elipseCount-=1

    screen.fill(white)
    if BkgImage:
        screen.blit(backgroundimg, imgrect)
    
    lenpoints = len(points)

    try:
        for line in lines:
            if points[line[0]] != None and points[line[1]] != None:
                pygame.draw.line(screen, blue, points[line[0]], points[line[1]])
    except IndexError:
        pass
    
    if linear:
        try:
            pygame.draw.line(screen, blue, points[-1], mouse_pos_artificial)
        except IndexError:
            pass

    try:
        for curve in curves:
            if curveCount == 1 and curve == curves[-1]:
                for t in np.arange(0, 1, 0.005):
                    px = points[curve[0]][0]*(1-t)**2 + 2*(1-t)*t*mouse_pos_artificial[0] + points[curve[2]][0]*t**2
                    py = points[curve[0]][1]*(1-t)**2 + 2*(1-t)*t*mouse_pos_artificial[1] + points[curve[2]][1]*t**2       
                    pygame.draw.rect(screen, green, (px, py, 2, 2))
            else:
                for t in np.arange(0, 1, 0.005):
                    px = points[curve[0]][0]*(1-t)**2 + 2*(1-t)*t*points[curve[1]][0] + points[curve[2]][0]*t**2
                    py = points[curve[0]][1]*(1-t)**2 + 2*(1-t)*t*points[curve[1]][1] + points[curve[2]][1]*t**2       
                    pygame.draw.rect(screen, green, (px, py, 2, 2))    
    except IndexError:
        pass
    try:
        for elipse in elipses:
            if elipseCount == 1 and elipse == elipses[-1]:
                if mouse_pos_artificial[0]-points[elipse[0]][0] <= 0 and mouse_pos_artificial[1]-points[elipse[0]][1] <= 0:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0]-abs(mouse_pos_artificial[0]-points[elipse[0]][0]), points[elipse[0]][1]-abs(mouse_pos_artificial[1]-points[elipse[0]][1]), abs(mouse_pos_artificial[0]-points[elipse[0]][0]), abs(mouse_pos_artificial[1]-points[elipse[0]][1])), width=1)
                elif mouse_pos_artificial[0]-points[elipse[0]][0] <= 0:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0]-abs(mouse_pos_artificial[0]-points[elipse[0]][0]), points[elipse[0]][1], abs(mouse_pos_artificial[0]-points[elipse[0]][0]), abs(mouse_pos_artificial[1]-points[elipse[0]][1])), width=1)
                elif mouse_pos_artificial[1]-points[elipse[0]][1] <= 0:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0], points[elipse[0]][1]-abs(mouse_pos_artificial[1]-points[elipse[0]][1]), abs(mouse_pos_artificial[0]-points[elipse[0]][0]), abs(mouse_pos_artificial[1]-points[elipse[0]][1])), width=1)
                else:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0], points[elipse[0]][1], abs(mouse_pos_artificial[0]-points[elipse[0]][0]), abs(mouse_pos_artificial[1]-points[elipse[0]][1])), width=1)
            else:
                if points[elipse[1]][0]-points[elipse[0]][0] <= 0 and points[elipse[1]][1]-points[elipse[0]][1] <= 0:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0]-abs(points[elipse[1]][0]-points[elipse[0]][0]), points[elipse[0]][1]-abs(points[elipse[1]][1]-points[elipse[0]][1]), abs(points[elipse[1]][0]-points[elipse[0]][0]), abs(points[elipse[1]][1]-points[elipse[0]][1])), width=1)
                elif points[elipse[1]][0]-points[elipse[0]][0] <= 0:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0]-abs(points[elipse[1]][0]-points[elipse[0]][0]), points[elipse[0]][1], abs(points[elipse[1]][0]-points[elipse[0]][0]), abs(points[elipse[1]][1]-points[elipse[0]][1])), width=1)
                elif points[elipse[1]][1]-points[elipse[0]][1] <= 0:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0], points[elipse[0]][1]-abs(points[elipse[1]][1]-points[elipse[0]][1]), abs(points[elipse[1]][0]-points[elipse[0]][0]), abs(points[elipse[1]][1]-points[elipse[0]][1])), width=1)
                else:
                    pygame.draw.ellipse(screen, blue, (points[elipse[0]][0], points[elipse[0]][1], abs(points[elipse[1]][0]-points[elipse[0]][0]), abs(points[elipse[1]][1]-points[elipse[0]][1])), width=1)   
    except IndexError:
        pass

    for point in points:
        if point != None:
            pygame.draw.circle(screen,red,point,3)

    pygame.draw.circle(screen,green,mouse_pos_artificial,4)
    if curveCount >= 1:
        pygame.draw.circle(screen,purple,mouse_pos,4)
    elif elipseCount >= 1:
        pygame.draw.circle(screen,blue,mouse_pos,4)
    else:
        pygame.draw.circle(screen,black,mouse_pos,4)
    
    textsurface = myfont.render(str(len(curves)+len(lines)), False, (0, 0, 0))
    screen.blit(textsurface,(0,0))

    pygame.display.flip()