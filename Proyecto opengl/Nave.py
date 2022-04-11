from glob import glob
from pickle import FALSE
from turtle import circle
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.textures import loadTexture

w,h= 500,500
#Texturas chidas de la nave
texture_nave = 0

#Dibujar Nave
def draw_nave():
    global texture_nave
    glBindTexture(GL_TEXTURE_2D, texture_nave)
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(-90+250,-96+250)
    glTexCoord2f(1,0)
    glVertex2d(90+250,-96+250)
    glTexCoord2f(1,1)
    glVertex2d(90+250,96+250)
    glTexCoord2f(0,1)
    glVertex2d(-90+250,96+250)
    glEnd()

def keyPressed ( key, x, y ):
    if key == b'\x1b':
        glutLeaveMainLoop()
    
    
def keyUp(key, x, y):
    xKeyup = 0

def init():
    glClearColor ( 1.0, 1.0, 1.0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def reshape(width, height):
    global w, h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def display():
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
    draw_nave()



    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp =0  #Si cualquiera de estas funciones se activa pedimos al glut que "se actualice"

def main():
    global texture_nave
    glutInit (  )
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( w, h )
    glutInitWindowPosition( 0, 0 )
    
    glutCreateWindow( "Ventana de PyOpenGL" )
    glutDisplayFunc (display) #Para dibujar la pantalla
    #glutIdleFunc ( animate ) #Cosas que se ejecutan continuamente
    glutReshapeFunc ( reshape ) #SE EJECUTA CUANDO CAMBIEMOS LA VENTANA
    glutKeyboardFunc( keyPressed ) #Esye nos permite manejos de teclado

    glutKeyboardUpFunc(keyUp)  
    init()
    
    #Cargar textura
    texture_nave = loadTexture('Resources/nave.png')

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()