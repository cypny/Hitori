import asyncio
from enum import Enum
from decorators import measure_time
import field
import parser as pars
import paterns as pat

class SolverState(Enum):
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FINISHED = "finished"

class Solver:
    def __init__(self):
        self.state = SolverState.STOPPED
        self.solutions = []
        self.current_field = None
        self.visited = set()
        self.steak = []
        
    async def solve(self, game_field):
        self.solutions = []
        self.current_field = pat.run_patterns(game_field)
        self.visited = set()
        self.steak = [self.current_field]
        self.state = SolverState.RUNNING
        
        repeats = get_all_repeats(self.current_field)
        if len(repeats) == 0 and white_have_way(self.current_field):
            self.solutions.append(self.current_field)

        while self.steak and self.state != SolverState.STOPPED:
            if self.state == SolverState.PAUSED:
                await asyncio.sleep(0.1)
                continue
                
            self.current_field = self.steak.pop()
            current_repeats = get_all_repeats(self.current_field)
            
            if len(current_repeats) == 0:
                if white_have_way(self.current_field):
                    self.solutions.append(self.current_field)
                continue
                
            for x, y in current_repeats:
                if self.current_field.is_white(x, y):
                    continue
                new_field = self.current_field.copy()
                new_field.set_black(x, y)
                
                field_str = new_field.field_to_string()
                if field_str not in self.visited:
                    self.visited.add(field_str)
                    self.steak.append(new_field)
                    
            await asyncio.sleep(0)  # Даём возможность другим корутинам выполниться
            
        self.state = SolverState.FINISHED
        return self.solutions

    def pause(self):
        if self.state == SolverState.RUNNING:
            self.state = SolverState.PAUSED

    def resume(self):
        if self.state == SolverState.PAUSED:
            self.state = SolverState.RUNNING

    def stop(self):
        self.state = SolverState.STOPPED

def get_all_repeats(game_field):
    rez = set()
    for x in range(game_field.field_len):
        line_y = {}
        line_x = {}
        for y in range(game_field.field_len):
            if not game_field.is_black(x, y):
                val = game_field.values[x][y]
                if val in line_y:
                    rez.add(line_y[val])
                    rez.add((x, y))
                line_y[val] = (x, y)
            if not game_field.is_black(y, x):
                val = game_field.values[y][x]
                if val in line_x:
                    rez.add(line_x[val])
                    rez.add((y, x))
                line_x[val] = (y, x)
    return rez
def white_have_way(game_field):
    start = (0, 1) if game_field.is_black(0, 0) else (0, 0)
    steak = [start]
    visited = set()

    while steak:
        x, y = steak.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_x, new_y = x + dx, y + dy
            if (game_field.argument_correct(new_x) and 
                game_field.argument_correct(new_y) and 
                not game_field.is_black(new_x, new_y)):
                steak.append((new_x, new_y))

    for x in range(game_field.field_len):
        for y in range(game_field.field_len):
            if not game_field.is_black(x, y) and (x, y) not in visited:
                return False
    return True

def is_solve(game_field):
    return len(get_all_repeats(game_field)) == 0 and white_have_way(game_field)

def get_all_step(game_field):
    rez = []
    points = get_all_repeats(game_field)
    for x, y in points:
        if game_field.is_white(x,y):
            continue
        new_field = game_field.copy()
        new_field.set_black(x, y)
        rez.append(new_field)
    return rez

if __name__ == "__main__":
    field = pars.get_field_by_console()
    solver = Solver()
    fields = asyncio.run(solver.solve(field))
    for i in fields:
        pars.write_field(i)

