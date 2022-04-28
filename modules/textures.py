from math import pi
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import sys

#------------------TEXTURA----------------------
def loadTexture ( fileName ):
    image = Image.open( fileName )
    width = image.size[0]
    height = image.size[1]
    rgb = False
    try:
        image = image.tobytes ( "raw", "RGBA", 0, -1 )  #La traduce a bytes, y manejamos un canal RGBA
    except:
        rgb = True
        image = image.tobytes ( "raw", "RGB", 0, -1 ) 

    texture = glGenTextures ( 1 ) #Generamos un ID de textura y le decimos que nada mas 1 
    
    glBindTexture ( GL_TEXTURE_2D, texture ) # 2d texture (x and y size)
    #glPixelStorei ( GL_UNPACK_ALIGNMENT,1 )
    glTexParameterf ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT ) #Si se pasa el tamaño del objeto al de la textura repetimos
    glTexParameterf ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameteri ( GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR )
    glTexParameteri ( GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR )
    if not rgb:
        gluBuild2DMipmaps ( GL_TEXTURE_2D, 4, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image ) #Asigna la imagen al id texture para relacionar la imagen que se carga
    else: 
        gluBuild2DMipmaps ( GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE, image ) #Asigna la imagen al id texture para relacionar la imagen que se carga
    #El 4 implica el número de canales Rojo, Verde, Azul y Alpha
    return texture