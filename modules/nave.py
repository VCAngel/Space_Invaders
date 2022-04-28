from .gameobject import GameObject

# * Clase para crear naves de jugador y aliens
# Hereda de GameObject


class Nave(GameObject):
    """Constructor de Naves

    Parametros: 
        player (boolean): True si la nave es del jugador
        hp (int): Cantidad de golpes que aguanta
        laser_timer (int): Tiempo en ms para intervalos entre cada disparo
    
    No tiene textura por default. Usar método set_laser_texture().
    """

    def __init__(self, coords=[0, 0], hp=1, laser_timer=500, textures=[], is_player=True):
        posX, posY = coords
        super().__init__(posX, posY, (int)(180/4), (int)(196/4), textures)
        self.__is_player = is_player
        self.__hp = hp
        self.__laser_timer = laser_timer
        self.__laser_textures = None
        self.__laser_type = 0

    def get_hp(self):
        return self.__hp
    
    def decrease_hp(self, value):
        self.__hp -= value

    def get_laser_timer(self):
        return self.__laser_timer

    def set_laser_timer(self, laser_timer):
        self.__laser_timer = laser_timer

    def set_laser_type(self, type = 0):
        self.__laser_type = type

    def get_laser_type(self):
        return self.__laser_type


class Laser(GameObject):
    def __init__(self, coords=[0, 0], base_dmg=1, textures=[]):
        posX, posY = coords
        super().__init__(posX, posY, (int)(180/4), (int)(196/4), textures)
        self.__base_dmg = base_dmg

    def get_base_dmg(self):
        return self.__base_dmg