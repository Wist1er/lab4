import csv
import tempfile
import unittest
from pathlib import Path

from functional_tasks import (
    apply_functions_with_map,
    compose,
    factorial_reduce,
    filter_transform_csv,
    measure_time,
)


class TestLab4(unittest.TestCase):
    def test_measure_time(self):
        @measure_time
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)
        self.assertGreaterEqual(add.last_elapsed, 0.0)

    def test_apply_functions_with_map(self):
        result = apply_functions_with_map(
            [1, 2, 3],
            [lambda x: x * 2, lambda x: x ** 2],
        )
        self.assertEqual(result, [[2, 4, 6], [1, 4, 9]])

    def test_factorial_reduce(self):
        self.assertEqual(factorial_reduce(0), 1)
        self.assertEqual(factorial_reduce(5), 120)
        with self.assertRaises(ValueError):
            factorial_reduce(-1)

    def test_compose(self):
        add_one = lambda x: x + 1
        multiply_by_two = lambda x: x * 2
        square = lambda x: x ** 2

        function = compose(square, multiply_by_two, add_one)
        self.assertEqual(function(3), 64)

    def test_filter_transform_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.csv"
            target = directory / "output.csv"

            source.write_text(
                "name,age\nАнна,17\nИван,20\nМария,22\n",
                encoding="utf-8",
            )

            result = filter_transform_csv(
                source,
                target,
                lambda row: int(row["age"]) >= 18,
                lambda row: {"name": row["name"].upper(), "age": row["age"]},
            )

            self.assertEqual(
                result,
                [
                    {"name": "ИВАН", "age": "20"},
                    {"name": "МАРИЯ", "age": "22"},
                ],
            )

            with target.open("r", encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(rows, result)


if __name__ == "__main__":
    unittest.main()
