from functools import partial
from tkinter import *

import parser as pars
import solver as sol

class StartWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Hitori")
        self.window.geometry('300x150')
        self._init_ui()

    def _init_ui(self):
        n_label = Label(self.window, text="Введите размер сетки")
        n_label.grid(column=3, row=5)
        n_entry = Entry(self.window)
        n_entry.grid(column=5, row=5)
        start = Button(self.window, text="Начать", command=lambda: self._start_game(n_entry))
        start.grid(column=7, row=7)

    def _start_game(self, count_entry):
        try:
            count = int(count_entry.get())
            self.window.destroy()
            GameWindow(count)
        except ValueError:
            ErrorWindow("Неверный ввод данных")

    def run(self):
        self.window.mainloop()

class GameWindow:
    def __init__(self, n):
        self.n = n
        self.size_x = 1200
        self.size_y = 800
        self.width_cell = (self.size_x - 200) / n
        self.height_cell = (self.size_y - 200) / n
        self.table = []
        
        self.window = Tk()
        self.window.geometry(f'{self.size_x}x{self.size_y}')
        self._init_ui()
        self.window.mainloop()

    def _init_ui(self):
        text_hello = Label(self.window, text="Введи в клетки цифры и нажми решить", font=("Arial Bold", 16))
        text_hello.place(x=self.size_x / 2, y=25)
        self._create_input_grid()
        solve = Button(self.window, text="Решить", command=self._solve_puzzle)
        solve.place(x=self.size_x - 100, y=self.size_y - 100, width=100, height=25)

    def _create_input_grid(self):
        for x in range(self.n):
            line = []
            for y in range(self.n):
                cell = Entry(self.window)
                self._bind_navigation(cell, x, y)
                line.append(cell)
                cell.place(x=100 + x * self.width_cell, y=100 + y * self.height_cell, 
                          width=self.width_cell, height=self.height_cell)
            self.table.append(line)

    def _bind_navigation(self, cell, x, y):
        cell.bind('<Left>', lambda e: self._move_focus(x-1, y))
        cell.bind('<Right>', lambda e: self._move_focus(x+1, y))
        cell.bind('<Up>', lambda e: self._move_focus(x, y-1))
        cell.bind('<Down>', lambda e: self._move_focus(x, y+1))

    def _move_focus(self, x, y):
        if 0 <= x < self.n and 0 <= y < self.n:
            self.table[x][y].focus_set()

    def _solve_puzzle(self):
        try:
            game_field = pars.get_field_by_gui(self.table)
            self.window.destroy()
            SolutionWindow(game_field, self.n)
        except:
            ErrorWindow("Неверный ввод данных")

class SolutionWindow:
    def __init__(self, game_field, n):
        self.n = n
        self.size_x = 1200
        self.size_y = 800
        self.width_cell = (self.size_x - 200) / n
        self.height_cell = (self.size_y - 200) / n
        self.current_solve = 0
        self.table_gui = []
        
        self.window = Tk()
        self.window.geometry(f'{self.size_x}x{self.size_y}')
        self.window.title("Solve")
        
        self.all_solve = sol.solve(game_field)
        self._init_ui()

    def _init_ui(self):
        self._create_grid()
        if len(self.all_solve) == 0:
            self._show_no_solution()
        else:
            self._show_solution_controls()
            self.window.mainloop()

    def _create_grid(self):
        for x in range(self.n):
            line = []
            for y in range(self.n):
                cell = Label(self.window, text="")
                line.append(cell)
                cell.place(x=100 + x * self.width_cell, y=100 + y * self.height_cell,
                          width=self.width_cell, height=self.height_cell)
            self.table_gui.append(line)

    def _show_no_solution(self):
        text_counter = Label(self.window, text="Решений нет!", font=("Arial Bold", 24))
        text_counter.place(x=self.size_x / 2, y=self.size_y / 2)

    def _show_solution_controls(self):
        if self.current_solve >= len(self.all_solve) or self.current_solve < 0:
            return
            
        text_counter = Label(self.window, 
                           text=f"Номер текущего решения {self.current_solve + 1} из {len(self.all_solve)}")
        text_counter.place(x=self.size_x / 2, y=25)
        
        go_back = Button(self.window, text="Назад", 
                        command=lambda: self._go_to_solution(self.current_solve - 1))
        go_back.place(x=0, y=self.size_y / 2 - 100, width=100, height=25)
        
        go_next = Button(self.window, text="Вперед", 
                        command=lambda: self._go_to_solution(self.current_solve + 1))
        go_next.place(x=self.size_x - 100, y=self.size_y / 2 - 100, width=100, height=25)
        
        self._update_table()
        self.window.bind('<Left>', lambda e: self._go_to_solution(self.current_solve - 1))
        self.window.bind('<Right>', lambda e: self._go_to_solution(self.current_solve + 1))

    def _update_table(self):
        field = self.all_solve[self.current_solve]
        for x in range(self.n):
            for y in range(self.n):
                if field.cells[x][y].value == 1:
                    self.table_gui[x][y].configure(text=field.values[x][y], bg="#000000")
                    continue
                self.table_gui[x][y].configure(text=field.values[x][y], bg="#FFFFFF")

    def _go_to_solution(self, current_solve):
        self.current_solve = current_solve
        self._show_solution_controls()

class ErrorWindow:
    def __init__(self, text):
        window = Tk()
        window.title("Error")
        window.geometry('450x200')
        error_label = Label(window, text=text, font=("Arial Bold", 25), fg="#ff0000")
        error_label.grid(column=5, row=5)

if __name__ == "__main__":
    start_window = StartWindow()
    start_window.run()
