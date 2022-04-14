from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.textures import loadTexture
from modules.gameobject import GameObject

w,h= 500,500


#Movimiento
flag_left = False
flag_right = False
flag_up = False
flag_down = False

#Texturas chidas de la nave
NAVE_IDLE = 0
NAVE_RUN = 1
texture_nave = []

#Elemento de nave
nave_gameobject = GameObject()

#Dibujar Nave
def draw_nave():
    global nave_gameobject
    x,y = nave_gameobject.get_position()
    w,h = nave_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if nave_gameobject.is_mirrored() else (0,1) # Posiblemente lo quite xd
    glBindTexture(GL_TEXTURE_2D, nave_gameobject.get_frame_to_draw()) #Apartir de aqui dibujamos al mario
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

def keyUp(key, x, y):
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

    #---------------------DIBUJAR AQUI------------------------#
    draw_nave()

    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp =0  #Si cualquiera de estas funciones se activa pedimos al glut que "se actualice"


#---Timers----
def timer_move_nave(value):
    global nave_gameobject, flag_left, flag_right
    global NAVE_IDLE, NAVE_RUN
    state = nave_gameobject.get_state
    input = 0
    if flag_right: 
        input = 1
        if state != NAVE_RUN:
            nave_gameobject.change_state(NAVE_RUN)
        if nave_gameobject.is_mirrored():  #Posiblemente se pueda quitar
            nave_gameobject.set_mirror(False) #Quitar
    elif flag_left:
        input = -1
        if state != NAVE_RUN:
            nave_gameobject.change_state(NAVE_RUN)
        if not nave_gameobject.is_mirrored():  #Quitar
            nave_gameobject.set_mirror(True)    #Quitar
    else: 
        if state != NAVE_IDLE:
            nave_gameobject.change_state(NAVE_IDLE)

    nave_gameobject.move(input)
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_nave, 1)

def timer_animate_nave(value):
    global nave_gameobject
    nave_gameobject.animate()
    glutPostRedisplay()
    glutTimerFunc(150, timer_animate_nave, 1)

#------------

def main():
    global texture_nave, nave_gameobject
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

    texture_nave.append([loadTexture('Resources/naveinput.png')])
    texture_nave.append([loadTexture('Resources/nave3.png'),loadTexture('Resources/nave2.png'),loadTexture('Resources/nave.png')])
    nave_gameobject = GameObject(250,250,(int)(180/4),(int)(196/4),texture_nave)
     
    timer_move_nave(0)
    timer_animate_nave(0)

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()