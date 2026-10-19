from pathlib import Path

from functional_tasks import (
    apply_functions_with_map,
    compose,
    factorial_reduce,
    filter_transform_csv,
    measure_time,
)


@measure_time
def calculate_sum(limit: int) -> int:
    return sum(range(limit))


def main() -> None:
    print("Лабораторная работа №4, вариант 8")

    print("\nСреднее №8 — декоратор замера времени:")
    result = calculate_sum(100_000)
    print("Результат:", result)

    print("\nСреднее №10 — несколько функций через map:")
    numbers = [1, 2, 3, 4, 5]
    functions = [
        lambda x: x ** 2,
        lambda x: x * 2,
        lambda x: x + 10,
    ]
    print("Исходный список:", numbers)
    print("Результат:", apply_functions_with_map(numbers, functions))

    print("\nСреднее №4 — факториал через reduce:")
    print("5! =", factorial_reduce(5))

    print("\nПовышенное №1 — композиция функций:")
    add_one = lambda x: x + 1
    multiply_by_two = lambda x: x * 2
    square = lambda x: x ** 2

    combined = compose(square, multiply_by_two, add_one)
    print("compose(square, multiply_by_two, add_one)(3) =", combined(3))

    print("\nПовышенное №8 — CSV через map/filter:")
    input_file = Path(__file__).with_name("data.csv")
    output_file = Path(__file__).with_name("result.csv")

    def adult(row: dict[str, str]) -> bool:
        return int(row["age"]) >= 18

    def transform(row: dict[str, str]) -> dict[str, str]:
        return {
            "name": row["name"].upper(),
            "age": row["age"],
            "city": row["city"],
        }

    rows = filter_transform_csv(input_file, output_file, adult, transform)
    print("Отфильтрованные и преобразованные строки:")
    for row in rows:
        print(row)
    print("Результат записан в result.csv")


if __name__ == "__main__":
    main()
