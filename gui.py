from functools import partial
from tkinter import *

import parser as pars
import solver as sol
import asyncio
import tkinter as tk
from tkinter import ttk
from functools import partial
import threading

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

class AsyncTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        self.thread = None
        
    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        
    def run(self):
        self.thread = threading.Thread(target=self.start_async_loop, daemon=True)
        self.thread.start()
        self.mainloop()
        
    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread:
            self.thread.join()
        self.destroy()

class SolutionWindow:
    def __init__(self, game_field, n):
        self.n = n
        self.size_x = 1200
        self.size_y = 800
        self.width_cell = (self.size_x - 200) / n
        self.height_cell = (self.size_y - 200) / n
        self.current_solve = 0
        self.table_gui = []
        self.solver = sol.Solver()
        
        self.window = AsyncTk()
        self.window.geometry(f'{self.size_x}x{self.size_y}')
        self.window.title("Solve")
        
        self._init_ui()
        self.window.after(100, lambda: self._async_start_solving(game_field))
        self.window.run()
        
    def _init_ui(self):
        self._create_grid()
        self._create_control_buttons()
        self.status_label = tk.Label(self.window, text="Идёт поиск решений...")
        self.status_label.place(x=self.size_x / 2, y=25)
        
    def _create_control_buttons(self):
        self.pause_button = tk.Button(self.window, text="Пауза", command=self._toggle_pause)
        self.pause_button.place(x=self.size_x - 200, y=50, width=100, height=25)
        
        self.stop_button = tk.Button(self.window, text="Стоп", command=self._stop_solving)
        self.stop_button.place(x=self.size_x - 200, y=80, width=100, height=25)
        
    def _hide_control_buttons(self):
        self.pause_button.place_forget()
        self.stop_button.place_forget()
        
    def _async_start_solving(self, game_field):
        asyncio.run_coroutine_threadsafe(
            self._solve_and_update(game_field), 
            self.window.loop
        )
        
    async def _solve_and_update(self, game_field):
        self.solutions = await self.solver.solve(game_field)
        self.window.after(0, self._update_ui_after_solve)
        
    def _update_ui_after_solve(self):
        self._hide_control_buttons()
        if len(self.solutions) > 0:
            self._show_solution_controls()
            self.status_label.configure(text=f"Найдено решений: {len(self.solutions)}")
        else:
            self._show_no_solution()
            self.status_label.configure(text="Решений не найдено")
            
    def _toggle_pause(self):
        if self.solver.state == sol.SolverState.RUNNING:
            self.solver.pause()
            self.pause_button.configure(text="Продолжить")
            self.status_label.configure(text="Поиск на паузе")
        elif self.solver.state == sol.SolverState.PAUSED:
            self.solver.resume()
            self.pause_button.configure(text="Пауза")
            self.status_label.configure(text="Идёт поиск решений...")
            
    def _stop_solving(self):
        self.solver.stop()
        self.status_label.configure(text="Поиск остановлен")
        self._hide_control_buttons()

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
        if self.current_solve >= len(self.solutions) or self.current_solve < 0:
            return
            
        text_counter = Label(self.window, 
                           text=f"Номер текущего решения {self.current_solve + 1} из {len(self.solutions)}")
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
        field = self.solutions[self.current_solve]
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
