from functools import partial
from tkinter import *

import parser as pars
import solver as sol


class gui_builder:
    def __init__(self, n):
        self.current_solve = 0
        self.window = Tk()
        self.n = n
        self.size_x = 1200
        self.size_y = 800
        self.width_cell = (size_x - 200) / n
        self.height_cell = (size_y - 200) / n
        self.table = []
        self.all_solve = []

    def create_start_menu(self):
        self.window.geometry(f'{self.size_x}x{self.size_y}')
        text_hello = Label(self.window, text="Введи в клетки цифры и нажми решить", font=("Arial Bold", 16))
        text_hello.place(x=self.size_x / 2, y=25)
        table = []
        for x in range(self.n):
            line = []
            for y in range(self.n):
                cell = Entry(self.window)
                line.append(cell)
                cell.place(x=100 + x * self.width_cell, y=100 + y * self.height_cell, width=self.width_cell,
                           height=self.height_cell)
            table.append(line)
        pars.get_field_by_gui(table)
        solve = Button(self.window, text="Решить", command=partial(self.solve_in_gui, table))
        solve.place(x=self.size_x - 100, y=self.size_y - 100, width=100, height=25)

    def solve_in_gui(self, input_table):
        self.window = Tk()
        self.window.geometry(f'{self.size_x}x{self.size_y}')
        self.window.title("Solve")
        self.create_table()
        try:
            game_field = pars.get_field_by_gui(input_table)
        except:
            create_error_window("Неверный ввод данных")
            return
        self.all_solve = sol.solve(game_field)
        if len(self.all_solve) == 0:
            self.create_no_solve_window()
        self.create_solve_window()

    def create_table(self):
        table = []
        for x in range(self.n):
            line = []
            for y in range(self.n):
                cell = Label(self.window, text="")
                line.append(cell)
                cell.place(x=100 + x * self.width_cell, y=100 + y * self.height_cell, width=self.width_cell,
                           height=self.height_cell)
            table.append(line)
        self.table = table

    def update_table(self):
        field = self.all_solve[self.current_solve]
        for x in range(self.n):
            for y in range(self.n):
                if field[x][y].value == 0:
                    self.table[x][y].configure(text=field[x][y].value, bg="#000000")
                    continue
                self.table[x][y].configure(text=field[x][y].value, bg="#FFFFFF")

    def create_no_solve_window(self):
        text_counter = Label(self.window,
                             text=f"Решений нет!",
                             font=("Arial Bold", 24))
        text_counter.place(x=self.size_x / 2, y=self.size_y / 2)

    def create_solve_window(self):
        if self.current_solve >= len(self.all_solve) or self.current_solve < 0:
            return
        text_counter = Label(self.window,
                             text=f"Номер текущего решения {self.current_solve + 1} из {len(self.all_solve)}")
        text_counter.place(x=self.size_x / 2, y=25)
        go_back = Button(self.window, text="Назад", command=partial(self.go_to_solution, self.current_solve - 1))
        go_back.place(x=0, y=self.size_y / 2 - 100, width=100, height=25)
        go_next = Button(self.window, text="Вперед", command=partial(self.go_to_solution, self.current_solve + 1))
        go_next.place(x=self.size_x - 100, y=self.size_y / 2 - 100, width=100, height=25)
        self.update_table()
        self.window.mainloop()

    def go_to_solution(self, current_solve):
        self.current_solve = current_solve
        self.create_solve_window()


def create_error_window(text):
    window_error = Tk()
    window_error.title("Error")
    window_error.geometry(f'{450}x{200}')
    error_label = Label(window_error, text=text, font=("Arial Bold", 25), fg="#ff0000")
    error_label.grid(column=5, row=5)


def create_bilder(count_entry):
    try:
        count = int(count_entry.get())
    except:
        create_error_window("Неверный ввод данных")
        return
    gui = gui_builder(count)
    gui.create_start_menu()


if __name__ == "__main__":
    window = Tk()
    window.title("Hitori")
    window.geometry(f'{300}x{150}')

    n_label = Label(window, text="Введите размер сетки")
    n_label.grid(column=3, row=5)
    n_entry = Entry(window)
    n_entry.grid(column=5, row=5)
    start = Button(window, text="Начать", command=partial(create_bilder, n_entry))
    start.grid(column=7, row=7)

    size_x = 1200
    size_y = 800

    mainloop()
