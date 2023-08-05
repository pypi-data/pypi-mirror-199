"""
Este es el modulo que incluye la clase de reproductor de musica
"""


class Player:
    """
    Esta clase crea un reproductor de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio como parametro en el constructor

        Parameters:
        song (str): este es un string con el path de la cancion

        Returns:
        int: devuelve 1 si reproducce con exito y 0 en caso de error

        """
        print("reproduciendo cancion")

    def stop(self):
        print("stoping")