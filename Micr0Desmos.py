import sys, pygame, math

pygame.init()

size = width, height = 1080, 1080
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0

screen = pygame.display.set_mode(size)

backgroundimg = pygame.image.load("/home/micr0byte/Downloads/Rhombicosidodecahedron.jpg")
imgrect = backgroundimg.get_rect()

def CalcFormulas(points, lines):
    pointsDes = []
    for point in points:
        pointsDes.append((point[0],-point[1]))
    outputString = ""
    for line in lines:
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
    print(outputString)

points = []
lines = []

while 1:
    mouseUp = False
    mouseDown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouseUp = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                CalcFormulas(points, lines)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_artificial = mouse_pos

    keys=pygame.key.get_pressed()

    connect = False
    if keys[pygame.K_c]:
        connect = True

    snap = False
    if keys[pygame.K_LSHIFT]:
        snap = True

    if snap:
        mouse_x, mouse_y = mouse_pos
        mindist = width
        closestPoint = points[0]
        for point in points:
            dist = math.sqrt(abs(point[0]-mouse_x)**2+abs(point[1]-mouse_y)**2)
            if dist < mindist:
                mindist = dist
                closestPoint = point
        mouse_pos_artificial = closestPoint

    if mouseUp:
        points.append(mouse_pos_artificial)
        if connect:
            lines.append((len(points)-2,len(points)-1))

    screen.fill(white)
    screen.blit(backgroundimg, imgrect)

    
    lenpoints = len(points)

    try:
        for line in lines:
            pygame.draw.line(screen, blue, points[line[0]], points[line[1]])
    except IndexError:
        pass
    
    if connect:
        try:
            pygame.draw.line(screen, blue, points[-1], mouse_pos_artificial)
        except IndexError:
            pass
    
    for point in points:
        pygame.draw.circle(screen,red,point,3)

    pygame.draw.circle(screen,green,mouse_pos_artificial,4)
    pygame.draw.circle(screen,black,mouse_pos,4)
    

    pygame.display.flip()