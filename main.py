import tkinter as tk
from colorama import  init , Fore
from vista.ventana_principal import VentanaPrincipal
from  reproductor.audio import Reproductor



if __name__ == "__main__":
    root = tk.Tk()
    init()

    reproductor = Reproductor()
    
    print(Fore.GREEN+"Empezando ejecución")
    app = VentanaPrincipal(master=root, rep=reproductor)
    root.title("Reproductor Lorito")
    # root.configure(bg="white")   
    app.mainloop()
    print(Fore.RED+"Termino la ejecución")