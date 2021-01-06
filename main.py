from colorama import  init , Fore
from vista.ventana_principal import VentanaPrincipal



if __name__ == "__main__":

    init()
    print(Fore.GREEN+"Empezando ejecución")
    ar = VentanaPrincipal()
    print(Fore.RED+"Termino la ejecución")
    