import tkinter as tk
from tkinter import messagebox, PhotoImage
import os

class TuringMachine:
    def __init__(self, tape, transitions, initial_state, accept_state):
        self.original_tape = list(tape)
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_state = accept_state
        self.reset()

    def reset(self):
        self.tape = [' '] * 2 + self.original_tape[:] + [' '] * 2
        self.head = 2  # Iniciar después de los primeros dos espacios en blanco
        self.state = self.initial_state
        self.history = []
        self.instantaneous_description = []
        self.add_instantaneous_description()
        self.advance_successful = True

    def step(self):
        if self.head < 0:
            self.head = 0
            self.tape.insert(0, ' ')
        if self.head >= len(self.tape):
            self.tape.append(' ')

        symbol = self.tape[self.head]
        if (self.state, symbol) in self.transitions:
            self.history.append((self.state, self.head, list(self.tape)))
            next_state, write_symbol, direction = self.transitions[(self.state, symbol)]
            self.tape[self.head] = write_symbol
            self.state = next_state
            self.head += 1 if direction == 'R' else -1
            self.advance_successful = True
            self.add_instantaneous_description()
            return True, f"({self.state}, {symbol}) -> ({next_state}, {write_symbol}, {direction})"
        else:
            self.advance_successful = False
            return False, f"No hay transición para: ({self.state}, {symbol})"

    def run(self):
        actions = []
        while self.state != self.accept_state:
            step_result, action = self.step()
            actions.append(action)
            if not step_result:
                break
        return actions

    def is_accepted(self):
        return self.state == self.accept_state

    def undo(self):
        if self.history:
            self.state, self.head, self.tape = self.history.pop()
            self.instantaneous_description.pop()
            self.advance_successful = True

    def add_instantaneous_description(self):
        left_tape = ''.join('B' if x == ' ' else x for x in self.tape[:self.head])
        right_tape = ''.join('B' if x == ' ' else x for x in self.tape[self.head + 1:])
        current_symbol = self.tape[self.head]
        state_text = f"({self.state})"
        description = f"{left_tape}{state_text}{current_symbol}{right_tape}"
        self.instantaneous_description.append(description)

class TuringMachineGUI(tk.Tk):
    def __init__(self, tm):
        super().__init__()
        self.tm = tm
        self.configure(bg="white")

        canvas = tk.Canvas(self, bg="white")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.image_tabla = PhotoImage(file="multiplicacion/tabla.png")
        self.image_tabla = self.image_tabla.subsample(3) 
        self.image_tabla_label = tk.Label(self, image=self.image_tabla)
        self.image_tabla_label.pack(side=tk.TOP, pady=20)

        self.image_q0 = PhotoImage(file="multiplicacion/QINI.png")
        self.image_q0 = self.image_q0.subsample(4)
        self.image_label = tk.Label(self, image=self.image_q0)
        self.image_label.pack(side=tk.TOP, pady=2)

        self.initialize_ui()

    def initialize_ui(self):
        self.entry_label1 = tk.Label(self.scrollable_frame, text="Primer número:", font=('Courier', 14))
        self.entry_label1.pack()
        self.entry1 = tk.Entry(self.scrollable_frame, font=('Courier', 14))
        self.entry1.pack(pady=10)

        self.entry_label2 = tk.Label(self.scrollable_frame, text="Segundo número:", font=('Courier', 14))
        self.entry_label2.pack()
        self.entry2 = tk.Entry(self.scrollable_frame, font=('Courier', 14))
        self.entry2.pack(pady=10)

        self.submit_button = tk.Button(self.scrollable_frame, text="Enviar", command=self.submit)
        self.submit_button.pack(pady=10)

        self.canvas = tk.Canvas(self.scrollable_frame, width=1000, height=150)
        self.canvas.pack(pady=20)

        self.status_display = tk.Label(self.scrollable_frame, font=('Courier', 14))
        self.status_display.pack()

        self.action_display = tk.Label(self.scrollable_frame, font=('Courier', 14))
        self.action_display.pack()

        self.instantaneous_descriptions = tk.Label(self.scrollable_frame, width=100, height=5, font=('Courier', 12), wraplength=1000, anchor="w", justify="left")
        self.instantaneous_descriptions.pack(pady=20)

        self.button_frame = tk.Frame(self.scrollable_frame)
        self.button_frame.pack(pady=10)

        self.step_button = tk.Button(self.button_frame, text="Siguiente", command=self.step)
        self.step_button.grid(row=0, column=0, padx=10)

        self.run_button = tk.Button(self.button_frame, text="Ejecutar", command=self.run)
        self.run_button.grid(row=0, column=1, padx=10)

        self.undo_button = tk.Button(self.button_frame, text="Atrás", command=self.undo)
        self.undo_button.grid(row=0, column=2, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reiniciar", command=self.reset)
        self.reset_button.grid(row=0, column=3, padx=10)

    def draw_tape(self):
        self.canvas.delete("all")
        tape_length = len(self.tm.tape)
        rect_size = 40
        offset = (1000 - (tape_length * rect_size)) // 2

        for i in range(tape_length):
            x0 = offset + i * rect_size
            y0 = 20
            x1 = x0 + rect_size
            y1 = y0 + rect_size

            color = "white"
            if i == self.tm.head:
                color = "green" if self.tm.advance_successful else "red"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.canvas.create_text(x0 + rect_size // 2, y0 + rect_size // 2, text='B' if self.tm.tape[i] == ' ' else self.tm.tape[i], font=('Courier', 18))

        head_pos = offset + self.tm.head * rect_size
        self.canvas.create_text(head_pos + rect_size // 2, y1 + 20, text="^", font=('Courier', 18))
        self.canvas.create_text(head_pos + rect_size // 2, y1 + 40, text=f"Estado: {self.tm.state}", font=('Courier', 14))

    def update_display(self, action=""):
        self.update_image()
        self.update_tabla_image()
        self.draw_tape()
        self.status_display.config(text=f"Estado: {self.tm.state}")
        self.action_display.config(text=f"Transiciones: {action}")
        self.instantaneous_descriptions.config(text=" ˫ ".join(self.tm.instantaneous_description))

    def update_image(self):
        current_state = self.tm.state
        tape_color = "V"

        if current_state == 'q0':
            image_path = f"multiplicacion/Q0{tape_color}.png"
        elif current_state == 'q1':
            image_path = f"multiplicacion/Q1{tape_color}.png"
        elif current_state == 'q2':
            image_path = f"multiplicacion/Q2{tape_color}.png"
        elif current_state == 'q3':
            image_path = f"multiplicacion/Q3{tape_color}.png"
        elif current_state == 'q4':
            image_path = f"multiplicacion/Q4{tape_color}.png"
        elif current_state == 'q5':
            image_path = f"multiplicacion/Q5{tape_color}.png"
        elif current_state == 'q6':
            image_path = f"multiplicacion/Q6{tape_color}.png"
        elif current_state == 'q7':
            image_path = f"multiplicacion/Q7{tape_color}.png"
        elif current_state == 'q8':
            image_path = f"multiplicacion/Q8{tape_color}.png"
        elif current_state == 'q9':
            image_path = f"multiplicacion/Q9{tape_color}.png"
        elif current_state == 'q10':
            image_path = f"multiplicacion/Q10{tape_color}.png"
        elif current_state == 'q11':
            image_path = f"multiplicacion/Q11{tape_color}.png"
        elif current_state == 'q12':
            image_path = f"multiplicacion/Q12{tape_color}.png"
        else: 
            return

        new_image = PhotoImage(file=image_path)
        new_image = new_image.subsample(2)
        self.image_label.configure(image=new_image)
        self.image_label.image = new_image

    def update_tabla_image(self):
        current_state = self.tm.state
        if self.tm.head < len(self.tm.tape):
            current_symbol = self.tm.tape[self.tm.head]
        
       

    def submit(self):
        number1 = self.entry1.get()
        number2 = self.entry2.get()

        if not number1.isdigit() or not number2.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese solo números naturales.")
            return

        number1 = int(number1)
        number2 = int(number2)

        tape_input = "1" * number1 + "0" + "1" * number2
        self.tm.original_tape = list(tape_input)
        self.reset()

    def step(self):
        if self.tm.state == self.tm.accept_state:
            result = self.tm.tape.count('1')
            messagebox.showinfo("Resultado", f"Cadena aceptada. Resultado de la suma: {result}")
        else:
            step_result, action = self.tm.step()
            self.update_display(action)
            if not step_result:
                messagebox.showinfo("Resultado", "Cadena rechazada")

    def run(self):
        actions = self.tm.run()
        for action in actions:
            self.update_display(action)
        if self.tm.is_accepted():
            result = self.tm.tape.count('1')
            messagebox.showinfo("Resultado", f"Cadena aceptada. Resultado de la suma: {result}")
        else:
            messagebox.showinfo("Resultado", "Cadena rechazada")

    def undo(self):
        self.tm.undo()
        self.update_display()

    def reset(self):
        self.tm.reset()
        self.update_display()


transitions = {
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q1', '0', 'L'),
    ('q1', 'X'): ('q1', 'X', 'R'),
    ('q1', '1'): ('q1', 'X', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),
    ('q2', '1'): ('q3', '1', 'R'),
    ('q3', 'Z'): ('q3', 'Z', 'R'),
    ('q3', 'Y'): ('q3', 'Y', 'R'),
    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', ' '): ('q4', ' ', 'L'),
    ('q4', 'Y'): ('q4', 'Y', 'L'),
    ('q4', 'Z'): ('q4', 'Z', 'L'),
    ('q4', '1'): ('q5', 'Y', 'R'),
    ('q5', 'Y'): ('q5', 'Y', 'R'),
    ('q5', 'Z'): ('q5', 'Z', 'R'),
    ('q5', ' '): ('q6', 'Z', 'L'),
    ('q6', 'Y'): ('q6', 'Y', 'L'),
    ('q6', 'Z'): ('q6', 'Z', 'L'),
    ('q6', '0'): ('q7', '0', 'R'),
    ('q7', 'Y'): ('q7', '1', 'R'),
    ('q6', '1'): ('q5', 'Y', 'R'),
    ('q7', 'Z'): ('q8', 'Z', 'L'),
    ('q8', '1'): ('q8', '1', 'L'),
    ('q8', '0'): ('q9', '0', 'L'),
    ('q9', 'X'): ('q9', 'X', 'L'),
    ('q9', '1'): ('q10', 'X', 'R'),
    ('q10', 'X'): ('q10', 'X', 'R'),
    ('q10', '0'): ('q3', '0', 'R'),
    ('q9', ' '): ('q11', ' ', 'R'),
    ('q11', 'X'): ('q11', ' ', 'R'),
    ('q11', 'Y'): ('q11', ' ', 'R'),
    ('q11', '1'): ('q11', ' ', 'R'),
    ('q11', '0'): ('q11', ' ', 'R'),
    ('q11', 'Z'): ('q11', '1', 'R'),
    ('q11', ' '): ('q12', ' ', 'R'),
    
    
    
}
initial_state = 'q0'
accept_state = 'q12'

# Crear la máquina de Turing con una cadena vacía inicialmente
tm = TuringMachine("", transitions, initial_state, accept_state)

# Crear y ejecutar la interfaz gráfica
app = TuringMachineGUI(tm)
app.mainloop()
