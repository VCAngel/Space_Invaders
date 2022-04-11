from turtle import pos

class GameObject: #La razon de todo esto es para representar a mario, enemigos y su comportamiento
    """Clase para objetos como Mario y Goomba """





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