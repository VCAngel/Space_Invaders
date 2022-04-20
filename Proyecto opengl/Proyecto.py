from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

#Datos Globales
width = 640
height = 480
x = 500
y = 300

dots = []  #Coordenadas de las estrellas de fondo
for i in range(100):
    dots.append([np.random.randint(0,width),np.random.randint(0,height)])

ships = []  #Coordenadas del centro de la nave, su tamaño y el color
for i in range(10):
    r= np.random.randint(20,80)
    ships.append([np.random.randint(r,width-r),np.random.randint(r,height-r),r, np.random.random(),np.random.random(),np.random.random()])


def poligonoxd(pc,xy,R,l,c1,c2,c3):
    angle = 2*3.141592/l
    glBegin(GL_POLYGON)
    glColor(c1,c2,c3)
    for i in range(l):
        x = pc + R*np.cos(angle*i)
        y = xy + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()


def space_noise():
    glColor3f(1,1,1)
    glBegin(GL_POINTS)
    for i in range(200):
        glVertex2d(np.random.randint(0,width),np.random.randint(0,height))
    glEnd()


def iterate():
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,width,0,height,0,1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    #DIBUJAR
    space_noise()
    poligonoxd(620,470,70,15,1,1,1)
    glutSwapBuffers()
    





def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width,height)
    glutInitWindowPosition(x,y)
    window= glutCreateWindow("Ventana con OpenGL")
    glutDisplayFunc(showScreen) 
    glutIdleFunc(showScreen)
    glutMainLoop()


main()
    