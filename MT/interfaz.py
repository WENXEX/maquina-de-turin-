import tkinter as tk
from tkinter import ttk
import subprocess

class InterfazCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Calculadora")
        self.root.geometry("300x400")
        self.root.configure(bg="#2E4053")

        # Título
        self.title_label = tk.Label(root, text="Calculadora", font=("Helvetica", 20, "bold"), bg="#2E4053", fg="#FDFEFE")
        self.title_label.pack(pady=20)

        # Crear botones con estilo
        self.estilo_boton = {'font': ('Helvetica', 14), 'width': 15, 'bg': '#1ABC9C', 'fg': '#FDFEFE'}

        # Crear botón para la suma
        self.btn_suma = tk.Button(root, text="Suma", command=self.ejecutar_suma, **self.estilo_boton)
        self.btn_suma.pack(pady=10)

        # Crear botón para la resta
        self.btn_resta = tk.Button(root, text="Resta", command=self.ejecutar_resta, **self.estilo_boton)
        self.btn_resta.pack(pady=10)

        # Crear botón para la multiplicación
        self.btn_multiplicacion = tk.Button(root, text="Multiplicación", command=self.ejecutar_multiplicacion, **self.estilo_boton)
        self.btn_multiplicacion.pack(pady=10)

        # Crear botón para la división
        self.btn_division = tk.Button(root, text="División", command=self.ejecutar_division, **self.estilo_boton)
        self.btn_division.pack(pady=10)

        # Crear estilo específico para el botón de salir
        estilo_boton_salir = self.estilo_boton.copy()
        estilo_boton_salir['bg'] = '#E74C3C'

        # Crear botón para salir
        self.btn_salir = tk.Button(root, text="Salir", command=root.quit, **estilo_boton_salir)
        self.btn_salir.pack(pady=20)

    def ejecutar_suma(self):
        # Llamar al script suma.py usando subprocess
        subprocess.Popen(['python', 'suma.py'])

    def ejecutar_resta(self):
        # Llamar al script resta.py usando subprocess
        subprocess.Popen(['python', 'resta.py'])

    def ejecutar_multiplicacion(self):
        # Llamar al script multiplicacion.py usando subprocess
        subprocess.Popen(['python', 'multiplicacion.py'])

    def ejecutar_division(self):
        # Llamar al script division.py usando subprocess
        subprocess.Popen(['python', 'division.py'])

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCalculadora(root)
    root.mainloop()
