from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.textures import loadTexture
from modules.gameobject import GameObject
from modules.nave import Nave
from modules.nave import Laser
import numpy as np
import random

#!-----Variables importantes-----
## Ventana
screenWidth, screenHeight = 1080,720 

## Deteccion de teclado
flag_left = False
flag_right = False
flag_up = False
flag_down = False
flag_enter = False

## Menu assets
menu_pug_textures = []
menu_text_img = []
color_1 = [62/255,0/255,74/255]
color_2 = [20/255,3/255,61/255]
min_blue_1, min_blue_2 = True, True #Para crear efecto en degradado

## Arrays de texturas
player_textures = []
alien_textures_type1 = []
alien_textures_type2 = []
alien_textures_type3 = []
alien_textures_special = []
laser_textures = []
laser_textures_type1 = []
PLAYER_IDLE = 0
PLAYER_RUN = 1

## Elementos de juego
menu_pug = None #-> Se usa para instancia GameObject
menu_text = None
player_Obj = None
alien_Objs = [] #-> Array de instancias Nave para aliens
laser_Objs = []
laser_ObjsA = []
alien_gameObj = []

# Puntuación de jugador
player_score = 0
lvl_2_locked = True
lvl_3_locked = True

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

#Menu
def load_menu():
    global  min_blue_1, min_blue_2
    pug_x,pug_y = menu_pug.get_position()
    pug_w,pug_h = menu_pug.get_size()
    text_x,text_y = menu_text.get_position()
    text_w,text_h = menu_text.get_size()
    color_increment = 1/255
    glBindTexture(GL_TEXTURE_2D, 0) #! Importante: si dejamos la textura en 0, podemos dibujar tambien
    #:-----Cuadrilatero degradado
    glBegin(GL_QUADS)
    glColor3f(color_1[0], color_1[1], color_1[2])
    glVertex2d(50,50)
    glColor3f(color_1[0], color_1[1], color_1[2])
    glVertex2d(50,screenHeight-50)
    glColor3f(color_2[0], color_2[1], color_2[2])
    glVertex2d(screenWidth-50,screenHeight-50)
    glColor3f(color_2[0], color_2[1], color_2[2])
    glVertex2d(screenWidth-50,50)
    glEnd()
    glColor3f(1,1,1)

    # Ciclo del degradado
    if min_blue_1:
        if color_1[2] < .90:
            color_1[0] += 0.5/255
            color_1[2] += color_increment
        else: 
            min_blue_1 = False
    else: 
        if color_1[2] >= 74/255:
            color_1[0] -= 0.5/255
            color_1[2] -= color_increment
        else: 
            min_blue_1 = True
    
    if min_blue_2:
        if color_2[2] < .70:
            color_2[0] += color_increment
            color_2[2] += color_increment
        else: 
            min_blue_2 = False
    else: 
        if color_2[2] >= 61/255:
            color_2[0] -= color_increment
            color_2[2] -= color_increment
        else: 
            min_blue_2 = True
    #:-----

    draw_texture(text_x,text_y,text_w,text_h,menu_text.get_frame_to_draw())
    draw_texture(pug_x,pug_y,pug_w,pug_h,menu_pug.get_frame_to_draw())
    

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

def draw_laser():
    global laser_Objs, laser_ObjsA   
    for i in range(len(laser_Objs)):
        laser_gameObj = laser_Objs[i]
        x,y = laser_gameObj.get_position()
        w,h = laser_gameObj.get_size()
        draw_texture(x,y,w,h,laser_gameObj.get_frame_to_draw())
        laser_gameObj.move_laser(1)

    for i in range(len(laser_ObjsA)):
        laser_gameObjA = laser_ObjsA[i]
        x,y = laser_gameObjA.get_position()
        w,h = laser_gameObjA.get_size()
        draw_texture(x,y,w,h,laser_gameObjA.get_frame_to_draw())
        laser_gameObjA.laser_alien()

    

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
    
#!-----Colisiones|Limites-----
#TODO Colisiones para laseres, quitar vida, etc.
def player_collision(): 
    global alien_Objs
    for i in range(len(alien_Objs)):
        if player_Obj.is_collision(alien_Objs[i]):
            alien_Objs.pop(i)
            player_Obj.decrease_hp(1)
            # print(player_Obj.get_hp())
            return

def player_laser_collision():
    global alien_Objs, laser_Objs
    for i in range(len(alien_Objs)):
        for j in range(len(laser_Objs)):
            if laser_Objs[j].is_collision(alien_Objs[i]):

                alien_Objs[i].decrease_hp(laser_Objs[j].get_base_dmg())
                if alien_Objs[i].get_hp() <= 0:
                    alien_Objs.pop(i)

                laser_Objs.pop(j)
                return

def object_out_of_bounds(gameObjectArray = []):
    for i in range(len(gameObjectArray)):
        x,y = gameObjectArray[i].get_position()
        if y > screenHeight:
            if not isinstance(gameObjectArray[i], Nave):
                gameObjectArray.pop(i)
                return
        
        if y <= -25:
            gameObjectArray.pop(i)
            return

# TODO Colisiones de aliens hacia jugador

#!-----Eventos de teclado------

def keyPressed ( key, x, y ):
    global flag_left, flag_down, flag_right, flag_up, flag_enter
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
    if key == b'\x0D':
        flag_enter = True

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
    if not flag_enter:
        load_menu()
    else:
        draw_laser()
        draw_nave()
        draw_aliens()
    #!---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp =0  #Si cualquiera de estas funciones se activa pedimos al glut que "se actualice"


#!-----Timers-------    
def timer_move_nave(value):
    if flag_enter:
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
        else: 
            if state != PLAYER_IDLE:
                player_Obj.change_state(PLAYER_IDLE)

        player_Obj.move(input, screenWidth)
    
    player_collision()
    player_laser_collision()
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_nave, 1)


def timer_animate_nave(value):
    global player_Obj
    player_Obj.animate()
    glutPostRedisplay()
    glutTimerFunc(150, timer_animate_nave, 1)
    

def timer_create_lvl_1(value):
    global lvl_2_locked, lvl_3_locked
    if flag_enter:
        global alien_Objs
        coords = [random.randint(0,screenWidth-50), screenHeight+80]
        alien_Objs.append(Nave(coords,1,500,alien_textures_type1, False))

        #TODO if score >= 250: correr lvl 2 aliens timer
        if player_score >= 250 and lvl_2_locked:
            lvl_2_locked = False
            timer_create_lvl_2(0)

        #TODO if score >= 1000: correr lvl 3 aliens timer
        if player_score >= 1000 and lvl_3_locked:
            lvl_3_locked = False
            timer_create_lvl_3(0)

    glutPostRedisplay()
    glutTimerFunc (2000, timer_create_lvl_1,1)

def timer_create_lvl_2(value):
    global alien_Objs
    coords = [random.randint(0,screenWidth-50), screenHeight+80]
    alien_Objs.append(Nave(coords,2,333, alien_textures_type2,False))

    glutPostRedisplay()
    glutTimerFunc (5000, timer_create_lvl_2,1)

def timer_create_lvl_3(value):
    global alien_Objs
    coords = [random.randint(0,screenWidth-50), screenHeight+80]
    alien_Objs.append(Nave(coords,2,1000, alien_textures_type3,False))

    glutPostRedisplay()
    glutTimerFunc (7000, timer_create_lvl_3,1)


def timer_move_alien(value):
    global alien_Objs
    for alien in alien_Objs:
        alien.alien_move()
        
    object_out_of_bounds(alien_Objs)
    glutTimerFunc (20, timer_move_alien, 1)

def timer_laserAlien(value):
    global laser_ObjsA
    for alien in alien_Objs:
        x,y = alien.get_position()
        laser_ObjsA.append(Laser([x,y],1,laser_textures_type1))

    for laser in laser_ObjsA:
        laser.laser_alien()
    glutTimerFunc (2000, timer_laserAlien, 1)

def timer_laser (value):
    global laser_Objs
    if flag_enter:
        global laser_Objs
        x,y = player_Obj.get_position()
        input = 0
        if flag_up: 
            input = 1
            laser_Objs.append(Laser([x,y],1,laser_textures))

        #-> Mueve cada laser en laser_Objs
        for laser in laser_Objs:
            laser.move_laser(input)

    object_out_of_bounds(laser_Objs)
    glutTimerFunc(500,timer_laser,1)
     

#!----Main function-----

def main():
    global menu_pug, menu_text
    global player_Obj, player_textures
    global alien_textures_type1, alien_textures_type2, alien_textures_type3, alien_textures_special
    global laser_textures
    global laser_textures_type1
    

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
    ##: Texturas de menu
    menu_pug_textures.append([loadTexture('./Resources/perro.png')])
    menu_pug = GameObject((screenWidth+100)-(screenWidth/2),-50,screenWidth/2,screenHeight-100,menu_pug_textures)
    menu_text_img.append([loadTexture('./Resources/menu.png')])
    menu_text = GameObject(100,100, 600, 500, menu_text_img)

    ##: Texturas de jugador
    player_textures.append([loadTexture('./Resources/naveinput.png')])
    player_textures.append([loadTexture('./Resources/nave3.png'),loadTexture('./Resources/nave2.png'),loadTexture('./Resources/nave.png')])
    player_Obj = Nave([screenWidth/2,30], 10,500,player_textures, True)
     
    ##: Texturas de aliens
    alien_textures_type1.append([loadTexture('./Resources/gataliens/aliencat.png')])
    alien_textures_type2.append([loadTexture('./Resources/gataliens/aliencatblue.png')])
    alien_textures_type3.append([loadTexture('./Resources/gataliens/aliencatyellow.png')])

    ##: Texturas de laser
    laser_textures.append([loadTexture('./Resources/gataliens/lazerred.png')])
    laser_textures_type1.append([loadTexture('./Resources/gataliens/lazeralien.png')])

    #-> Timers
    timer_move_nave(0)
    timer_animate_nave(0)
    timer_create_lvl_1(0)
    timer_move_alien(0)
    timer_laser(0)
    timer_laserAlien(0)

    glutMainLoop()

print("Presiona Escape para salir!")
main()
