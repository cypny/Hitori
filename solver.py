import asyncio
import pickle
from enum import Enum
from typing import List, Tuple, Set, Iterator, Optional, Dict, Any

import parser as pars
import paterns as pat
from field import solve_field

GameField = solve_field;


class SolverState(Enum):
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FINISHED = "finished"


class Solver:
    def __init__(self,gamefield=None):
        self.state: SolverState = SolverState.STOPPED
        self.solutions: List[GameField] = []
        self.current_field: Optional[GameField] = gamefield
        self.visited: Set[str] = set()
        self.steak: List[GameField] = []
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.last_save_count: int = 0
        self.save_interval: int = 1500

    async def solve(self, game_field: GameField) -> List[GameField]:
        """
        Основной метод для поиска решений головоломки.

        Args:
            game_field: Исходное поле для решения

        Returns:
            List[GameField]: Список найденных решений
        """
        if self.state == SolverState.PAUSED:
            self.state = SolverState.RUNNING
        else:
            self.loop = asyncio.get_event_loop()
            self.solutions = []
            self.current_field = pat.run_patterns(game_field)
            self.visited = set()
            self.steak = [self.current_field]
            self.state = SolverState.RUNNING
            self.last_save_count = 0

        try:
            if self.is_solve():
                if self.current_field not in self.solutions:
                    self.solutions.append(self.current_field)

            while self.steak and self.state != SolverState.STOPPED:
                if self.state == SolverState.PAUSED or len(self.visited) - self.last_save_count >= self.save_interval:
                    await self.save_state("solver_state.pickle")
                    self.last_save_count = len(self.visited)
                    await asyncio.sleep(0.01)
                    continue

                self.current_field = self.steak.pop()

                if self.is_solve():
                    self.solutions.append(self.current_field)
                    continue

                for x, y in self._get_all_repeats():
                    if self.state == SolverState.STOPPED:
                        break
                    if self.current_field.is_white(x, y):
                        continue
                    new_field = self.current_field.copy()
                    new_field.set_black(x, y)

                    field_str = new_field.field_to_string()
                    if field_str not in self.visited:
                        self.visited.add(field_str)
                        self.steak.append(new_field)

                await asyncio.sleep(0)

        except Exception as e:
            await self.save_state("solver_state.pickle")
            raise e
        finally:
            if self.state != SolverState.PAUSED:
                self.state = SolverState.FINISHED
            return self.solutions

    def pause(self) -> None:
        """Приостанавливает выполнение решения"""
        if self.state == SolverState.RUNNING:
            self.state = SolverState.PAUSED

    def resume(self) -> None:
        """Возобновляет выполнение решения"""
        if self.state == SolverState.PAUSED:
            self.state = SolverState.RUNNING

    def stop(self) -> None:
        """Останавливает выполнение решения"""
        self.state = SolverState.STOPPED
        if self.loop:
            self.loop.stop()

    async def save_state(self, filename: str = "solver_state.pickle") -> None:
        """
        Асинхронно сохраняет текущее состояние решателя

        Args:
            filename: Имя файла для сохранения
        """
        state = {
            'solutions': self.solutions,
            'current_field': self.current_field,
            'visited': self.visited,
            'steak': self.steak,
            'state': self.state
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._save_state_to_file, state, filename)

    def _save_state_to_file(self, state: Dict[str, Any], filename: str) -> None:
        """
        Сохраняет состояние в файл

        Args:
            state: Словарь с состоянием
            filename: Имя файла
        """
        with open(filename, 'wb') as f:
            pickle.dump(state, f)

    def load_state(self, filename: str = "solver_state.pickle") -> bool:
        """
        Загружает состояние из файла

        Args:
            filename: Имя файла для загрузки

        Returns:
            bool: Успешность загрузки
        """
        try:
            with open(filename, 'rb') as f:
                state = pickle.load(f)
                self.solutions = state['solutions']
                self.current_field = state['current_field']
                self.visited = state['visited']
                self.steak = state['steak']
                self.state = state['state']
                return True
        except Exception:
            return False

    def _get_all_repeats(self) -> Iterator[Tuple[int, int]]:
        field = self.current_field
        seen = set()
        result = []

        for x in range(field.field_len):
            line_y = self._collect_line_values(x, is_horizontal=False)
            line_x = self._collect_line_values(x, is_horizontal=True)

            for pos in self._find_duplicates(line_y):
                if pos not in seen:
                    seen.add(pos)
                    result.append(pos)

            for pos in self._find_duplicates(line_x):
                if pos not in seen:
                    seen.add(pos)
                    result.append(pos)

        yield from result

    def _collect_line_values(self, line_index: int, is_horizontal: bool) -> Dict[
        int, List[Tuple[int, int]]]:
        """
        Собирает все значения в строке или столбце и возвращает их в виде словаря:
        ключ - значение, значение - список координат (x, y), где это значение встречается.

        Args:
            field: Текущее поле
            line_index: Индекс строки/столбца
            is_horizontal: Если True - обрабатываем строку, иначе - столбец

        Returns:
           Словарь значений и их позиций
        """
        field = self.current_field
        result: Dict[int, List[Tuple[int, int]]] = {}
        for i in range(field.field_len):
            x, y = (line_index, i) if is_horizontal else (i, line_index)
            if not field.is_black(x, y):
                val = field.values[x][y]
                result.setdefault(val, []).append((x, y))
        return result

    def _find_duplicates(self, data: Dict[int, List[Tuple[int, int]]]) -> Iterator[Tuple[int, int]]:
        """
        Ищет дубликаты в переданных данных и возвращает позиции, где они встречаются.

        Args:
            data: Словарь значений и их позиций

        Yields:
            Позиции дубликатов
        """
        for positions in data.values():
            if len(positions) > 1:
                yield from positions

    def white_have_way(self) -> bool:
        """
        Проверяет, все ли белые ячейки связаны между собой через смежные белые клетки.
        Используется алгоритм DFS для поиска всех доступных белых ячеек.
        """
        field = self.current_field
        start = (0, 1) if field.is_black(0, 0) else (0, 0)
        steak = [start]
        visited = set()

        while steak:
            x, y = steak.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if field.argument_correct(new_x) and field.argument_correct(new_y):
                    if not field.is_black(new_x, new_y):
                        steak.append((new_x, new_y))

        for x in range(field.field_len):
            for y in range(field.field_len):
                if not field.is_black(x, y) and (x, y) not in visited:
                    return False
        return True

    def is_solve(self) -> bool:
        """
        Проверяет, является ли текущее поле решением.

        Решение считается найденным, если:
        - Нет повторяющихся чисел в строках/столбцах
        - Все белые клетки связаны между собой

        Returns:
            bool: текущее поле — решение
        """
        return not any(True for _ in self._get_all_repeats()) and self.white_have_way()


if __name__ == "__main__":
    field = pars.get_field_by_console()
    solver = Solver()
    fields = asyncio.run(solver.solve(field))
    print(f"\nНайдено решений: {len(fields)}")
    for i, solution in enumerate(fields, 1):
        print(f"\nРешение {i}:")
        pars.write_field(solution)
