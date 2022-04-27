from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.textures import loadTexture
# from modules.gameobject import GameObject
from modules.nave import Nave
import numpy as np
import random

#!-----Variables importantes-----
## Ventana
screenWidth, screenHeight = 1080,720 

## Movimiento
flag_left = False
flag_right = False
flag_up = False
flag_down = False

## Arrays de texturas
player_textures = []
alien_textures_type1 = []
alien_textures_type2 = []
alien_textures_type3 = []
alien_textures_special = []
laser_textures = []
PLAYER_IDLE = 0
PLAYER_RUN = 1

## Elementos de juego
player_Obj = None
alien_Objs = [] #-> Array de instancias Nave para aliens

# Puntuación de jugador
player_score = 0

#!-----Funciones de dibujo-----
def draw_texture(x,y,w,h,frame_to_draw=0): #-> Se usa para dibujar una textura con glBindTexture()
    pin_x_start, pin_x_end = (0,1)
    glBindTexture(GL_TEXTURE_2D, frame_to_draw)
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glVertex2d(x,y+h)
    glEnd()

#Alien
def draw_aliens():
    #TODO Different aliens and stuff zamn
    for i in range(len(alien_Objs)):
        alien_gameObj = alien_Objs[i]
        x,y = alien_gameObj.get_position()
        w,h = alien_gameObj.get_size()
        draw_texture(x,y,w,h,alien_gameObj.get_frame_to_draw())
        
#Dibujar Nave
def draw_nave():
    x,y = player_Obj.get_position()
    w,h = player_Obj.get_size()
    draw_texture(x,y,w,h,player_Obj.get_frame_to_draw())

#TODO Averiguar como disparar el laser desde la clase de Nave
def draw_laser():
    global laser_gameobject
    x,y = laser_gameobject.get_position()
    w,h = laser_gameobject.get_size()
    draw_texture(x,y,w,h,laser_gameobject.get_frame_to_draw())
    

def polygon(aristas, x1, y1, rad, rojo, verde , azul, rotacion):
    PI = 3.141592
    angle = 2*PI/aristas
    glColor3f(rojo, verde, azul)
    glBegin(GL_POLYGON)
    for i in range(aristas):
        x = x1 + rad*np.cos(angle*i+(PI*rotacion))
        y = y1 + rad*np.sin(angle*i+(PI*rotacion))
        glVertex2d(x, y)
    glEnd()
    

def keyPressed ( key, x, y ):
    global flag_left, flag_down, flag_right, flag_up
    if key == b'\x1b':
        glutLeaveMainLoop() 
    if key == b'w':
        flag_up = True
    if key == b's':
        flag_down = True
    if key == b'a':
        flag_left = True
    if key == b'd':
        flag_right = True

def keyUp( key, x, y ):
    global flag_left, flag_down, flag_right, flag_up
    if key == b'w':
        flag_up = False
    if key == b's':
        flag_down = False
    if key == b'a':
        flag_left = False
    if key == b'd':
        flag_right = False



def init():
    glClearColor ( 0.0, 0.0, 0.0, 0.0 )
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

    #!---------------------DIBUJAR AQUI------------------------#
    draw_nave()
    draw_aliens()
    #TODO Workout laser shooting
    # draw_laser()
    #!---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp =0  #Si cualquiera de estas funciones se activa pedimos al glut que "se actualice"


#!-----Timers-------
def timer_move_nave(value):
    global PLAYER_IDLE, PLAYER_RUN
    state = player_Obj.get_state()
    input = 0
    if flag_right: 
        input = 1
        if state != PLAYER_RUN:
            player_Obj.change_state(PLAYER_RUN)     
    elif flag_left:
        input = -1
        if state != PLAYER_RUN:
            player_Obj.change_state(PLAYER_RUN)
    elif flag_up: 
       input = 1
    else: 
        if state != PLAYER_IDLE:
            player_Obj.change_state(PLAYER_IDLE)

    player_Obj.move(input)
    # laser_gameobject.move_laser(input)
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_nave, 1)

def timer_animate_nave(value):
    global player_Obj
    player_Obj.animate()
    glutPostRedisplay()
    glutTimerFunc(150, timer_animate_nave, 1)
    

def timer_create_alien(value):
    global alien_Objs, alien_textures_type1
    coords = [random.randint(0,screenWidth-50), screenHeight-50]
    alien_Objs.append(Nave(coords,1,500,alien_textures_type1, False))
    # alien_Objs.append(GameObject(random.randint(0,screenWidth-40),453,50,50,alien_textures_type1))
    glutPostRedisplay()
    glutTimerFunc (5000, timer_create_alien,1)
     

#!----Main function-----

def main():
    global player_Obj, player_textures
    global alien_textures_type1, alien_textures_type2, alien_textures_type3, alien_textures_special
    global laser_textures

    glutInit ()
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( screenWidth, screenHeight )
    glutInitWindowPosition( 0, 0 )
    
    glutCreateWindow( "Catattack!" )
    glutDisplayFunc (display) #Para dibujar la pantalla
    #glutIdleFunc ( animate ) #Cosas que se ejecutan continuamente
    glutReshapeFunc ( reshape ) #SE EJECUTA CUANDO CAMBIEMOS LA VENTANA
    glutKeyboardFunc( keyPressed ) #Este nos permite manejos de teclado
    glutKeyboardUpFunc(keyUp)  
    init()

    #-> Carga de Recursos
    ##: Texturas de jugador
    player_textures.append([loadTexture('./Resources/naveinput.png')])
    player_textures.append([loadTexture('./Resources/nave3.png'),loadTexture('./Resources/nave2.png'),loadTexture('./Resources/nave.png')])
    player_Obj = Nave([10,10], 10,500,player_textures, True)
     
    ##: Texturas de aliens
    alien_textures_type1.append([loadTexture('./Resources/perro.png')])
    alien_textures_type2.append([loadTexture('./Resources/perro.png')])
    alien_textures_type3.append([loadTexture('./Resources/perro.png')])
    alien_textures_special.append([loadTexture('./Resources/perro.png')])

    ##: Texturas de laser
    laser_textures.append([loadTexture('./Resources/laser.png')])
    player_Obj.set_laser_texture(laser_textures)

    #-> Timers
    timer_move_nave(0)
    timer_animate_nave(0)
    timer_create_alien(0)

    glutMainLoop()

print("Presiona Escape para salir!")
main()
