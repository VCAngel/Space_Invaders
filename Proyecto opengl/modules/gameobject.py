class GameObject:
    """ Clases para la nave y aliens"""
    __position = {'x': 0, 'y':0} # Maneje posicion
    __size = {'x': 0, 'y':0} # Maneje tamaño
    animator = [] #Lista bidimensional con los Frames del objeto
    __index_state = 0 # Estado del pesonaje a animar
    __latest_frame = 0 #Frame a dibujar
    __mirror = False #No creo que sea necesario ya que la imagen se ve igual de derecha e izquierda xD

    def __init__(self, x=0, y=0, w=0, h=0, frames = []):
        self.__position['x'] = x
        self.__position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h
        self.animator = frames
        

    def move(self, input):
        '''input:
        1.- Mover hacia la derecja
        0.- No se mueve
        -1.- Mover hacia la izquierda'''
        self.__position['x'] += input

    def change_state(self,index):
        if index >= len(self.animator):
            raise Exception('El indice esta fuera del limite pemitido.')
        self.__index_state = index
        self.__latest_frame = 0

    def get_state(self):
        return self.__index_state

    def animate(self):
        if len(self.animator[self.__index_state]) == 1:
            return #Si solo hay un frame no hay que hacer nada pero si hay mas de uno tenemos que ciclarlo
        self.__latest_frame = 0 if self.__latest_frame >= (len(self.animator[self.__index_state]) - 1) else self.__latest_frame + 1 #si existe mas de un frame del estado 

    def get_frame_to_draw(self):
        return self.animator[self.__index_state][self.__latest_frame]
         #Esto regresa la imagen que se quiere dibujar 
    
    def get_position(self):
        return self.__position['x'], self.__position['y']

    def get_size(self):
        return self.__size['x'], self.__size['y']

    def set_mirror(self, value):
        self.__mirror = value

    def is_mirrored(self):
        return self.__mirror
