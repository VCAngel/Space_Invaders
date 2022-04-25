from gameobject import GameObject

# * Clase para crear naves de jugador y aliens
# Hereda de GameObject
class Nave(GameObject):
    def __init__(self, player=True, hp=3, laser_timer=500):
        """Constructor de Naves

        Parametros: 
        player (boolean): True si la nave es del jugador
        hp (int): Cantidad de golpes que aguanta
        laser_timer (int): Tiempo en ms para intervalos entre cada disparo
        """
        super().__init__(player, hp, laser_timer)
        self.__player = player
        self.__hp = hp
        self.__laser_timer = laser_timer

    def get_hp(self):
        return self.__hp

    def set_hp(self, hp):
        self.__hp = hp

    def get_laser_timer(self):
        return self.__laser_timer

    def set_laser_timer(self, laser_timer):
        self.__laser_timer = laser_timer

    def shoot(self):
        print('Shoot!')