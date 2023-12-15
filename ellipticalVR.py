# env : python 3.10.11 vpython 7.6.4
import math
from vpython import *
from socket import *
# from visual import sphere, box, curve, helix, cylinder , color , scene , rate
# from math import pi , cos , sin , asin


#######make figure#######
scene.x, scene.y = 1,1
scene.width = 1140
scene.height = 380
scene.background = color.white
autoscale = 0

#initial condition
r1 = 0.085 #crank radius OB (m)
r2 = 0.32 #OC (m)
point_radius = r1 / 6 # point radiuspoint_radius
dt = 0.01
dtime = 0.01 #a = a0+wt
seta0 = 0 #initial crank angle
n = 2  
omiga = 1 #w
seta = seta0 + omiga * dtime # crank angle
#point
pointa = sphere(pos = vector(0, 0, 0), radius = point_radius, color = color.black, visible = 0) #original point (x,y,z) point radius
pointb = sphere(pos = vector(-r1 * cos(seta), r1 * sin(seta), 0), radius = point_radius, color = color.black) #point on the circle , seta is the crank angle
# pointc = sphere(pos=(r2*cos(asin(r1*sin(seta)/r2))+r1*cos(seta),0,0),radius=point_radius,color=color
# .red) #point on the slider
pointc = sphere(pos = vector(-r1 * cos(seta) + sqrt(math.pow(r1,2) * math.pow(cos(seta), 2) - (math.pow(r1, 2) - math.pow(r2, 2))), 0, 0), radius = point_radius, color = color.black) #point on the slider

#link
#lineab = curve(pos = [vector(pointa.pos), vector(pointb.pos)], radius = point_radius / 2, color = color.gray(0.5)) #OB link
linebc = curve(pos = [vector(pointb.pos), vector(pointc.pos)], radius = point_radius / 2, color = color.gray(0.5)) #OC link

#slider
box1 = box(pos = vector(pointc.pos.x + r1 / 3, pointc.pos.y, - r1 / 1.5 / 2), length = r1 / 1.5, height = r1 / 1.5, width = r1 / 1.5, color = color.gray(0.5), visible = 1)

#background
table = cylinder(pos = vector(0, 0, -0.1), axis = vector(0, 0, -0.1), radius = 0.14, color = color.gray(0.5))

v1 = vec(pointb.pos.x * 0.2 + pointc.pos.x * 0.8, pointb.pos.y * 0.2 + pointc.pos.y * 0.8, 0 + point_radius / 2)

point_foot = sphere(pos = v1, radius = point_radius * 0.7, color = color.blue)

trace = curve(v1, radius = point_radius / 4, color = color.red)

dt = 1/100

#####TCP transmit initial set#######
serverName = '172.22.11.2'
serverPort = 1236
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#######loop#######
while True:

    rate(1/dt) 
    
    # print(seta)
    # if seta >= 2*pi:
    #    break
    #seta = float(input())

    # get radian
    modifiedSentence = clientSocket.recv(1024)
    seta = float(modifiedSentence[4:modifiedSentence.find('\x00',12)])

    #seta = seta0 + omiga * dtime
    pointb.pos = vec(-r1 * cos(seta), r1 * sin(seta), 0) # update point B
    pointc.pos = vec(-r1 * cos(seta) + sqrt(math.pow(r1, 2) * math.pow(cos(seta), 2) - (math.pow(r1, 2) - math.pow(r2, 2))), 0, 0) #update point C

    #lineab.modify(1, pos = pointb.pos)
    linebc.modify(0, pos = pointb.pos)
    linebc.modify(1, pos = pointc.pos)

    box1.pos = vec(pointc.pos.x + r1 / 3, pointc.pos.y, pointc.pos.z)
    v2 = vec(pointb.pos.x * 0.2 + pointc.pos.x * 0.8, pointb.pos.y * 0.2 + pointc.pos.y * 0.8, 0 + point_radius / 2)
    point_foot.pos = v2;

    if seta < 3.142 * 2: 
        trace.append(v2)

    dtime += dt  # time update