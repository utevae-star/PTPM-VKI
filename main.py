import logging
import os
import sys

from triangle import check_triangle


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )


def main() -> None:
    setup_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    # Здесь можно вводить через input(), но для удобства — список кейсов.
    test_cases = [
        ("3", "3", "3"),        # равносторонний
        ("5", "5", "8"),        # равнобедренный
        ("3", "4", "5"),        # разносторонний
        ("1", "2", "10"),       # не треугольник
        ("-3", "4", "5"),       # невалидные числа
        ("abc", "4", "5"),      # нечисловые данные
        ("", "", ""),           # нечисловые данные
    ]

    for a, b, c in test_cases:
        kind, coords = check_triangle(a, b, c)
        print(f"Вход: ({a!r}, {b!r}, {c!r}) -> тип={kind!r}, координаты={coords}")

    # Если хочешь ручной ввод — раскомментируй:
    # a = input("Сторона A: ")
    # b = input("Сторона B: ")
    # c = input("Сторона C: ")
    # kind, coords = check_triangle(a, b, c)
    # print("Тип:", kind)
    # print("Координаты:", coords)


if __name__ == "__main__":
    main()