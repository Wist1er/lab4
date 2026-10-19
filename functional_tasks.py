from __future__ import annotations

import csv
import time
from collections.abc import Callable, Iterable
from functools import reduce, wraps
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def measure_time(func: Callable[..., R]) -> Callable[..., R]:
    """Среднее №8. Декоратор замера времени выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper.last_elapsed = elapsed
        print(f'Функция "{func.__name__}" выполнена за {elapsed:.6f} сек.')
        return result

    wrapper.last_elapsed = 0.0
    return wrapper


def apply_functions_with_map(
    numbers: Iterable[int],
    functions: Iterable[Callable[[int], int]],
) -> list[list[int]]:
    """Среднее №10. Применяет несколько функций к списку через map."""
    values = list(numbers)
    return [list(map(function, values)) for function in functions]


def factorial_reduce(number: int) -> int:
    """Среднее №4. Вычисляет факториал с помощью functools.reduce."""
    if number < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")

    return reduce(lambda x, y: x * y, range(1, number + 1), 1)


def compose(*functions: Callable[[T], T]) -> Callable[[T], T]:
    """Повышенное №1. Создаёт композицию функций.

    compose(f, g, h)(x) эквивалентно f(g(h(x))).
    """
    if not functions:
        return lambda value: value

    def composed(value: T) -> T:
        return reduce(lambda result, function: function(result), reversed(functions), value)

    return composed


def filter_transform_csv(
    input_file: str | Path,
    output_file: str | Path,
    filter_function: Callable[[dict[str, str]], bool],
    transform_function: Callable[[dict[str, str]], dict[str, str]],
) -> list[dict[str, str]]:
    """Повышенное №8. Фильтрует и преобразует CSV через filter и map."""
    input_path = Path(input_file)
    output_path = Path(output_file)

    with input_path.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            return []

        rows = list(reader)

    filtered_rows = filter(filter_function, rows)
    transformed_rows = list(map(transform_function, filtered_rows))

    fieldnames = list(transformed_rows[0].keys()) if transformed_rows else list(reader.fieldnames)

    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transformed_rows)

    return transformed_rows
